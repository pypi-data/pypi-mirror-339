import os
import asyncio
import json
import httpx
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, UploadFile, File, HTTPException, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import aiofiles
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv, set_key

# 配置
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'pptx', 'xlsx', 'md', 'eml', 'msg', 'epub', 'xls', 'html', 'htm', 'org', 'odt', 'log', 'ppt', 'rst', 'rtf', 'tsv', 'doc', 'xml', 'js', 'py', 'java', 'cpp', 'cc', 'cxx', 'c', 'cs', 'php', 'rb', 'swift', 'ts', 'go'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
MAX_CONCURRENT_UPLOADS = 5

# 数据清洗服务配置
DATA_CLEANSE_SERVICE = os.getenv("DATA_CLEANSE_SERVICE", "http://localhost:8001")

# 请求模型
class CleanseParams(BaseModel):
    chunking_strategy: Optional[str] = None
    index_name: str

app = FastAPI()

# 创建上传目录
upload_dir = Path(UPLOAD_FOLDER)
upload_dir.mkdir(exist_ok=True)

# 并发控制
upload_semaphore = asyncio.Semaphore(MAX_CONCURRENT_UPLOADS)

# 完全重新配置CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加一个中间件来手动添加CORS头
@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

def allowed_file(filename: str) -> bool:
    if not filename:
        return False
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

async def save_upload_file(file: UploadFile, upload_path: Path) -> bool:
    try:
        async with aiofiles.open(upload_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        return True
    except Exception as e:
        print(f"Error saving file {file.filename}: {str(e)}")
        return False

async def is_data_cleanse_service_available():
    """检查数据清洗服务是否可用"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{DATA_CLEANSE_SERVICE}/healthcheck",
                timeout=5.0
            )
        return response.status_code == 200
    except Exception:
        return False

async def trigger_data_cleanse(file_paths: List[str], cleanse_params: CleanseParams):
    """触发数据清洗服务处理上传的文件"""
    try:
        print("Files to cleanse: ", file_paths)
        
        if not file_paths:
            return None
            
        # 构建源数据列表
        if len(file_paths) == 1:
            # 单个文件请求
            payload = {
                "source": file_paths[0],
                "source_type": "file",
                "chunking_strategy": cleanse_params.chunking_strategy,
                "index_name": cleanse_params.index_name
            }
            
            print(f"Payload: {payload}")
            
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{DATA_CLEANSE_SERVICE}/tasks",
                        json=payload,
                        timeout=30.0
                    )
                    
                print(f"Data cleanse service response: {response}")
                
                if response.status_code == 201:
                    return response.json()
                else:
                    print(f"Error from data cleanse service: {response} - {response.text if hasattr(response, 'text') else 'No response text'}")
                    return {
                        "status": "error",
                        "code": response.status_code,
                        "message": f"Data cleanse service error: {response.status_code}"
                    }
            except httpx.RequestError as e:
                print(f"Failed to connect to data cleanse service: {str(e)}")
                return {
                    "status": "error",
                    "code": "CONNECTION_ERROR",
                    "message": f"Failed to connect to data cleanse service: {str(e)}"
                }
                
        else:
            # 批量文件请求
            sources = []
            for file_path in file_paths:
                source = {
                    "source": file_path,
                    "source_type": "file",
                    "index_name": cleanse_params.index_name
                }
                    
                sources.append(source)
                
            payload = {"sources": sources}
            
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{DATA_CLEANSE_SERVICE}/tasks/batch",
                        json=payload,
                        timeout=30.0
                    )
                
                if response.status_code == 201:
                    return response.json()
                else:
                    print(f"Error from data cleanse service: {response} - {response.text if hasattr(response, 'text') else 'No response text'}")
                    return {
                        "status": "error",
                        "code": response.status_code,
                        "message": f"Data cleanse service error: {response.status_code}"
                    }
            except httpx.RequestError as e:
                print(f"Failed to connect to data cleanse service: {str(e)}")
                return {
                    "status": "error",
                    "code": "CONNECTION_ERROR",
                    "message": f"Failed to connect to data cleanse service: {str(e)}"
                }
    except Exception as e:
        print(f"Error triggering data cleanse: {str(e)}")
        return {
            "status": "error",
            "code": "INTERNAL_ERROR",
            "message": f"Internal error: {str(e)}"
        }

# 添加一个健康检查端点来检查数据清洗服务的状态
@app.get("/healthcheck")
async def healthcheck():
    # 检查数据清洗服务是否可用
    data_cleanse_service_available = await is_data_cleanse_service_available()
        
    return {
        "status": "ok",
        "message": "Upload service running",
        "data_cleanse_service": "available" if data_cleanse_service_available else "unavailable"
    }

# 处理预检请求
@app.options("/{full_path:path}")
async def options_route(full_path: str):
    return JSONResponse(
        status_code=200,
        content={"detail": "OK"},
    )

@app.post("/upload")
async def upload_files(
    file: List[UploadFile] = File(..., alias="file"),
    chunking_strategy: Optional[str] = Form(None),
    index_name: str = Form(...)
):
    print(f"Received upload request with {len(file)} files")
    
    if not file:
        raise HTTPException(status_code=400, detail="No files in the request")
    
    # 构建清洗参数
    cleanse_params = CleanseParams(
        chunking_strategy=chunking_strategy,
        index_name=index_name
    )
    
    uploaded_filenames = []
    uploaded_file_paths = []
    errors = []
    
    async with upload_semaphore:
        for f in file:
            if not f:
                continue
                
            if not allowed_file(f.filename):
                errors.append(f"File type not allowed: {f.filename}")
                continue
            
            # 安全处理文件名
            safe_filename = os.path.basename(f.filename)
            upload_path = upload_dir / safe_filename
            absolute_path = upload_path.absolute()
            
            # 保存文件
            if await save_upload_file(f, upload_path):
                uploaded_filenames.append(safe_filename)
                uploaded_file_paths.append(str(absolute_path))
                print(f"Successfully saved file: {safe_filename}")
            else:
                errors.append(f"Failed to save file: {f.filename}")
    
    # 触发数据清洗
    if uploaded_file_paths:
        print(f"Triggering data cleanse for {len(uploaded_file_paths)} files")
        cleanse_result = await trigger_data_cleanse(uploaded_file_paths, cleanse_params)
        
        # 如果数据清洗服务失败，则整个上传失败
        if cleanse_result is None or (isinstance(cleanse_result, dict) and cleanse_result.get("status") == "error"):
            error_message = "Data cleanse service failed" 
            if isinstance(cleanse_result, dict) and "message" in cleanse_result:
                error_message = cleanse_result["message"]
                
            # 删除已上传的文件
            for path in uploaded_file_paths:
                try:
                    os.remove(path)
                except Exception as e:
                    print(f"Failed to remove file {path}: {str(e)}")
                    
            return JSONResponse(
                status_code=500,
                content={
                    "error": error_message,
                    "files": uploaded_filenames
                }
            )
    
        # 数据清洗成功
        return JSONResponse(
            status_code=201,
            content={
                "message": "Files uploaded and processed successfully",
                "uploaded_files": uploaded_filenames,
                "cleanse_tasks": cleanse_result
            }
        )
    else:
        print(f"Errors: {errors}")
        return JSONResponse(
            status_code=400,
            content={
                "error": "No valid files uploaded",
                "errors": errors
            }
        )

if __name__ == "__main__":
    import uvicorn
    print("Starting upload service on http://0.0.0.0:3020")
    uvicorn.run(app, host="0.0.0.0", port=3020)
