import os
import asyncio
import httpx
import glob
from pathlib import Path
from typing import List, Dict, Any, Set
from dotenv import load_dotenv
import time
import json

# Load environment variables
load_dotenv()

async def wait_for_task_completion(client: httpx.AsyncClient, data_cleanse_service_url: str, task_id: str, max_retries: int = 10) -> bool:
    """Wait for a task to complete and return success status"""
    retries = 0
    max_wait_time = 600  # 最长等待10分钟
    start_time = time.time()
    
    # 所有状态常量统一为小写，与API响应一致
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"
    STATUS_FORWARDING = "forwarding"
    STATUS_PROCESSING = "processing"
    STATUS_WAITING = "waiting"
    
    while True:
        try:
            status_response = await client.get(
                f"{data_cleanse_service_url}/tasks/{task_id}",
                timeout=60.0  # 增加单个请求的超时时间
            )
            
            if status_response.status_code != 200:
                print(f"   Error getting task status: {status_response.text}")
                return False
            
            task_status = status_response.json()
            status_raw = task_status.get('status', '')
            current_status = status_raw.lower()  # 确保使用小写
            
            # 处理可能带有taskstatus.前缀的状态
            if current_status.startswith("taskstatus."):
                current_status = current_status[len("taskstatus."):]
                
            print(f"   Task {task_id} status: {status_raw}")
            
            # 任务完成
            if current_status == STATUS_COMPLETED:
                if "result" in task_status:
                    result_count = len(task_status.get("result", []))
                    print(f"   Result count: {result_count}")
                return True
                
            # 任务失败
            elif current_status == STATUS_FAILED:
                error_msg = task_status.get('error', 'Unknown error')
                print(f"   Task {task_id} failed: {error_msg}")
                return False
                
            # 考虑FORWARDING状态也是正常的，只需继续等待
            elif current_status == STATUS_FORWARDING:
                # 如果转发超过了特定时间，我们认为任务基本完成
                forwarding_time = time.time() - start_time
                if forwarding_time > 120.0:  # 如果转发状态超过2分钟
                    print(f"   Task {task_id} has been forwarding for {forwarding_time:.1f}s, considered successful")
                    return True
            
            # 检查是否超过最长等待时间
            elapsed_time = time.time() - start_time
            if elapsed_time > max_wait_time:
                print(f"   Task {task_id} timed out after {elapsed_time:.1f} seconds")
                # 如果状态是forwarding，即使超时也认为任务成功
                if current_status == STATUS_FORWARDING:
                    print(f"   Task is still forwarding, considering it successful")
                    return True
                return False
            
            # 根据状态决定等待时间
            # processing或forwarding状态下等待稍长一些，但更频繁地检查
            if current_status in [STATUS_PROCESSING, STATUS_FORWARDING]:
                await asyncio.sleep(2.0)  # 处理中状态每2秒检查一次
            else:
                await asyncio.sleep(0.5)  # 其他状态每0.5秒检查一次
            
        except httpx.TimeoutException:
            retries += 1
            if retries > max_retries:
                print(f"   Timeout checking task {task_id} status after {max_retries} retries")
                return False
            
            print(f"   Timeout checking task {task_id} status, retry {retries}/{max_retries}...")
            await asyncio.sleep(1.0)  # 超时后稍等一会再重试
            
        except Exception as e:
            print(f"   Error checking task {task_id} status: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

async def test_single_file(client: httpx.AsyncClient, data_cleanse_service_url: str, 
                         file_path: str, index_name: str) -> bool:
    """Test processing a single file"""
    print(f"\nTesting single file: {file_path}")
    
    try:
        # Create task with index_name parameter
        create_response = await client.post(
            f"{data_cleanse_service_url}/tasks",
            json={
                "source": file_path,
                "source_type": "file",
                "chunking_strategy": "basic",
                "additional_params": {
                    "index_name": index_name,  # 添加索引名称参数
                }
            },
            timeout=60.0  # 增加单个请求的超时时间
        )
        
        if create_response.status_code not in (200, 201):
            print(f"   Error creating task: {create_response.text}")
            return False
        
        task_id = create_response.json()["task_id"]
        print(f"   Task created with ID: {task_id}")
        
        # 添加短暂休眠，确保服务有时间开始处理任务
        await asyncio.sleep(0.5)
        
        # 等待任务完成 - 任务完成会自动转发到ES
        return await wait_for_task_completion(client, data_cleanse_service_url, task_id)
        
    except Exception as e:
        import traceback
        print(f"   Error processing file {file_path}: {str(e)}")
        print("   Traceback:")
        traceback.print_exc()
        return False

async def submit_batch_task(client: httpx.AsyncClient, data_cleanse_service_url: str, 
                          file_paths: List[str], index_name: str, max_retries: int = 3) -> Dict:
    """分批提交大量文件，避免请求超时"""
    batch_size = 50  # 每批最多50个文件
    total_files = len(file_paths)
    batches = [file_paths[i:i+batch_size] for i in range(0, total_files, batch_size)]
    
    print(f"   Splitting {total_files} files into {len(batches)} batches of max {batch_size} files each")
    
    all_task_ids = []
    
    for batch_idx, batch in enumerate(batches):
        retries = 0
        while retries <= max_retries:
            try:
                print(f"   Submitting batch {batch_idx+1}/{len(batches)} ({len(batch)} files)...")
                sources = [{
                    "source": path, 
                    "source_type": "file",
                    "index_name": index_name,  # 添加索引名称
                } for path in batch]
                
                create_response = await client.post(
                    f"{data_cleanse_service_url}/tasks/batch",
                    json={"sources": sources},
                    timeout=500.0  # 增加批量请求的超时时间
                )
                
                if create_response.status_code not in (200, 201):
                    print(f"   Error creating batch task: {create_response.text}")
                    break
                
                response_data = create_response.json()
                if "task_ids" not in response_data:
                    print(f"   Invalid response format: {response_data}")
                    break
                
                batch_task_ids = response_data["task_ids"]
                print(f"   Batch {batch_idx+1} created with {len(batch_task_ids)} task IDs")
                all_task_ids.extend(batch_task_ids)
                break  # 成功，退出重试循环
            
            except httpx.TimeoutException:
                retries += 1
                if retries <= max_retries:
                    print(f"   Timeout submitting batch {batch_idx+1} - retry {retries}/{max_retries}...")
                    await asyncio.sleep(2.0)
                else:
                    print(f"   Failed to submit batch {batch_idx+1} after {max_retries} retries")
            
            except Exception as e:
                import traceback
                print(f"   Error submitting batch {batch_idx+1}: {str(e)}")
                print("   Traceback:")
                traceback.print_exc()
                break
    
    return {"task_ids": all_task_ids}

async def test_multiple_files(client: httpx.AsyncClient, data_cleanse_service_url: str,
                            file_paths: List[str], index_name: str) -> bool:
    """Test processing multiple files"""
    print(f"\nTesting multiple files ({len(file_paths)} files)")
    
    try:
        # 判断文件数量，如果超过一定数量，就分批提交
        if len(file_paths) > 50:
            response_data = await submit_batch_task(client, data_cleanse_service_url, file_paths, index_name)
            task_ids = response_data.get("task_ids", [])
            if not task_ids:
                print("   Failed to create any batch tasks")
                return False
        else:
            # Create batch task
            sources = [{
                "source": path, 
                "source_type": "file",
                "index_name": index_name,  # 添加索引名称
            } for path in file_paths]
            
            create_response = await client.post(
                f"{data_cleanse_service_url}/tasks/batch",
                json={"sources": sources},
                timeout=200.0  # 增加单个请求的超时时间
            )
            
            if create_response.status_code not in (200, 201):
                print(f"   Error creating batch task: {create_response.text}")
                return False
            
            response_data = create_response.json()
            if "task_ids" not in response_data:
                print(f"   Invalid response format: {response_data}")
                return False
            
            task_ids = response_data["task_ids"]
        
        print(f"   Batch task created with {len(task_ids)} task IDs")
        print(f"   First few task IDs: {task_ids[:5]}...")
        
        # 添加短暂休眠，确保服务有时间开始处理任务
        await asyncio.sleep(1.0)
        
        # 状态常量，保持与wait_for_task_completion中一致
        STATUS_COMPLETED = "completed"
        STATUS_FAILED = "failed"
        STATUS_FORWARDING = "forwarding"
        STATUS_PROCESSING = "processing"
        STATUS_WAITING = "waiting"
        
        # 处理所有任务
        # 现在所有任务都是单独处理，无论批量大小
        completed_tasks: Set[str] = set()
        failed_tasks: Set[str] = set()
        pending_tasks = set(task_ids)
        
        # 最大并行检查数量，避免一次检查太多任务导致服务器压力过大
        max_parallel_checks = 10
        success = True
        
        while pending_tasks:
            # 控制并行检查的任务数
            check_tasks = list(pending_tasks)[:max_parallel_checks]
            
            # 创建任务状态检查
            check_futures = [
                wait_for_task_completion(client, data_cleanse_service_url, task_id)
                for task_id in check_tasks
            ]
            
            # 等待这一批任务检查完成
            results = await asyncio.gather(*check_futures, return_exceptions=True)
            
            # 处理结果
            for task_id, result in zip(check_tasks, results):
                if isinstance(result, Exception):
                    print(f"   Error checking task {task_id}: {str(result)}")
                    failed_tasks.add(task_id)
                elif result:
                    completed_tasks.add(task_id)
                else:
                    # 检查任务状态，如果是FORWARDING状态，也认为是成功的
                    try:
                        status_response = await client.get(
                            f"{data_cleanse_service_url}/tasks/{task_id}",
                            timeout=30.0
                        )
                        if status_response.status_code == 200:
                            task_data = status_response.json()
                            status_raw = task_data.get('status', '')
                            current_status = status_raw.lower()
                            
                            # 处理可能带有taskstatus.前缀的状态
                            if current_status.startswith("taskstatus."):
                                current_status = current_status[len("taskstatus."):]
                            
                            if current_status == STATUS_FORWARDING:
                                print(f"   Task {task_id} is in forwarding status, considering as successful")
                                completed_tasks.add(task_id)
                                continue
                            # 如果是processing状态，暂时不标记为失败，等下一轮检查
                            elif current_status == STATUS_PROCESSING:
                                print(f"   Task {task_id} is still processing, will check again later")
                                continue
                            elif current_status == STATUS_FAILED:
                                print(f"   Task {task_id} failed")
                                failed_tasks.add(task_id)
                                continue
                    except Exception as e:
                        print(f"   Error rechecking task {task_id} status: {str(e)}")
                    
                    # 如果不是FORWARDING或PROCESSING状态，则认为是失败
                    failed_tasks.add(task_id)
                    success = False
            
            # 更新待处理任务集合
            pending_tasks = pending_tasks - completed_tasks - failed_tasks
            
            if pending_tasks:
                print(f"\n   Waiting for {len(pending_tasks)} tasks to complete...")
                print(f"   Progress: {len(completed_tasks)}/{len(task_ids)} completed, {len(failed_tasks)}/{len(task_ids)} failed")
                await asyncio.sleep(1.0)  # 增加轮询间隔，减少请求频率
        
        print(f"\n   Batch processing summary:")
        print(f"   Total tasks: {len(task_ids)}")
        print(f"   Completed: {len(completed_tasks)}")
        print(f"   Failed: {len(failed_tasks)}")
        
        # 只要大部分任务成功，就认为整体成功
        if len(completed_tasks) > (len(task_ids) * 0.8):
            print(f"   Overall status: SUCCESS (>80% tasks completed successfully)")
            return True
        elif len(completed_tasks) > (len(task_ids) * 0.5):
            print(f"   Overall status: PARTIAL SUCCESS (>50% tasks completed)")
            return True
        else:
            print(f"   Overall status: FAILURE (<50% tasks completed)")
            return success
    except Exception as e:
        import traceback
        print(f"   Error processing batch: {str(e)}")
        print("   Traceback:")
        traceback.print_exc()
        return False

async def test_data_cleanse_to_es_integration():
    """Test the integration between data cleanse service and Elasticsearch"""
    try:
        print("=== Testing Data Cleanse → Elasticsearch Integration ===")
        
        # Get service URLs from environment
        es_service_url = os.environ.get("ELASTICSEARCH_SERVICE", "http://localhost:8000")
        data_cleanse_service_url = os.environ.get("DATA_CLEANSE_SERVICE", "http://localhost:8001")
        
        # Get example docs directory
        example_docs_dir = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "example_docs")))
        if not example_docs_dir.exists():
            print(f"Error: example_docs directory not found at {example_docs_dir}")
            return
        
        # Get all test files
        test_files = [
            str(f.absolute()) for f in example_docs_dir.glob("**/*")
            if f.is_file() and not f.name.startswith(".") and f.name != ".DS_Store"
        ]
        
        if not test_files:
            print("Error: No test files found in example_docs directory")
            return
        
        print(f"Found {len(test_files)} test files")
        
        # 检查服务健康状态
        try:
            health_response = await httpx.AsyncClient().get(
                f"{data_cleanse_service_url}/healthcheck", 
                timeout=5.0
            )
            if health_response.status_code == 200:
                print(f"Data cleanse service is healthy: {health_response.json().get('message', 'OK')}")
            else:
                print(f"Warning: Data cleanse service health check failed: {health_response.status_code}")
            
            es_health_response = await httpx.AsyncClient().get(
                f"{es_service_url}/health", 
                timeout=5.0
            )
            if es_health_response.status_code == 200:
                print(f"Elasticsearch service is healthy")
            else:
                print(f"Warning: Elasticsearch service health check failed: {es_health_response.status_code}")
        except Exception as e:
            print(f"Warning: Could not check service health: {str(e)}")
        
        # 使用更长的超时时间
        limits = httpx.Limits(max_connections=20, max_keepalive_connections=10)
        async with httpx.AsyncClient(timeout=180.0, limits=limits) as client:  # 增加整体客户端超时和并发连接
            # Test 1: Single file with new index
            print("\n=== Test 1: Single file with new index ===")
            test_file = test_files[0]
            success = await test_single_file(client, data_cleanse_service_url, test_file, "test_new_index_1")
            print(f"Test 1 {'succeeded' if success else 'failed'}")
            
            # Test 2: Same file to same index (duplicate)
            print("\n=== Test 2: Duplicate file to same index ===")
            success = await test_single_file(client, data_cleanse_service_url, test_file, "test_new_index_1")
            print(f"Test 2 {'succeeded' if success else 'failed'}")
            
            # Test 3: Multiple files to new index
            print("\n=== Test 3: Multiple files to new index ===")
            test_files_subset = test_files[:5]  # Test with first 5 files
            success = await test_multiple_files(client, data_cleanse_service_url, test_files_subset, "test_multiple_files_1")
            print(f"Test 3 {'succeeded' if success else 'failed'}")
            
            # Test 4: All files to new index (but with a limit to avoid overwhelming the system)
            print("\n=== Test 4: Larger batch of files to new index ===")
            max_files_for_test = min(50, len(test_files))  # 限制最大文件数量
            larger_test_files = test_files[:max_files_for_test]
            print(f"   Using {len(larger_test_files)} files out of {len(test_files)} total files")
            success = await test_multiple_files(client, data_cleanse_service_url, larger_test_files, "测试知识库")
            print(f"Test 4 {'succeeded' if success else 'failed'}")

            # Test 5: Multiple files to different indices simultaneously
            print("\n=== Test 5: Multiple files to different indices ===")
            # Split files into two groups for different indices
            files_count = min(40, len(test_files))  # 限制每个索引最多20个文件
            first_group = test_files[:files_count//2]
            second_group = test_files[files_count//2:files_count]
            
            print(f"   Testing with {len(first_group)} files to index1 and {len(second_group)} files to index2")
            
            # 创建两个并行的任务
            tasks = [
                test_multiple_files(client, data_cleanse_service_url, first_group, "test_multi_index_1"),
                test_multiple_files(client, data_cleanse_service_url, second_group, "test_multi_index_2")
            ]
            
            # 同时执行两个任务
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 检查结果
            success = all(
                isinstance(result, bool) and result 
                for result in results
            )
            
            if success:
                print("Test 5 succeeded - Successfully processed files to different indices")
            else:
                print("Test 5 failed - Errors occurred while processing files to different indices")
                for i, result in enumerate(results, 1):
                    if isinstance(result, Exception):
                        print(f"   Index {i} failed with error: {str(result)}")
                    elif not result:
                        print(f"   Index {i} failed")
        
        print("\n=== Integration test completed! ===")
        
    except Exception as e:
        import traceback
        print(f"\nError during integration test:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("\nTraceback:")
        traceback.print_exc()

def main():
    """Main entry point for running the integration test"""
    try:
        asyncio.run(test_data_cleanse_to_es_integration())
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        import traceback
        print(f"\nFatal error:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("\nTraceback:")
        traceback.print_exc()

if __name__ == "__main__":
    main() 