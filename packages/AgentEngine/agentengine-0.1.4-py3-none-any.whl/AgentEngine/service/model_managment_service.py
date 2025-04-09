import logging
import argparse
from typing import Optional, List, Dict, Any, Tuple, Union
from fastapi import FastAPI, Query, HTTPException, Body
from pydantic import BaseModel
import requests
import uvicorn
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
from enum import Enum

from AgentEngine import MessageObserver
from AgentEngine.core.models.embedding_model import JinaEmbedding
from AgentEngine.core.models.openai_llm import OpenAIModel
from AgentEngine.service.voice_service import VoiceService
from AgentEngine.database.model_management_db import create_model_record, update_model_record, delete_model_record, get_model_records, get_model_by_name, get_model_by_display_name

# 直接在本文件中定义 ModelConnectStatusEnum
class ModelConnectStatusEnum(Enum):
    """模型连接状态枚举类"""
    NOT_DETECTED = "未检测"
    DETECTING = "检测中"
    AVAILABLE = "可用"
    UNAVAILABLE = "不可用"
    
    @classmethod
    def get_default(cls) -> str:
        """获取默认值"""
        return cls.NOT_DETECTED.value
    
    @classmethod
    def get_value(cls, status: Optional[str]) -> str:
        """根据状态获取值，如果为空则返回默认值"""
        if not status or status == "":
            return cls.NOT_DETECTED.value
        return status

# 加载环境变量
load_dotenv()

# 获取环境变量
MODEL_ENGINE_HOST = os.getenv('MODEL_ENGINE_HOST')
MODEL_ENGINE_APIKEY = os.getenv('MODEL_ENGINE_APIKEY')

# 获取项目根目录
project_base_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def split_repo_name(full_name: str):
    """
    将model_name拆解为model_repo和model_name
    """
    parts = full_name.split('/')
    if len(parts) > 1:
        return '/'.join(parts[:-1]), parts[-1]
    return "", full_name


def add_repo_to_name(model_repo: str, model_name: str) -> str:
    """
    将model_repo和model_name拼接
    
    Args:
        model_repo: 模型仓库名称
        model_name: 模型名称
        
    Returns:
        str: 拼接后的完整模型名称
    """
    if "/" in model_name:
        logging.warning(f"非预期行为：模型名称 {model_name} 中已包含仓库信息！")
        return model_name
    if model_repo:
        return f"{model_repo}/{model_name}"
    return model_name


# 创建 FastAPI 应用
def create_model_management_app(env_file: Optional[str] = None, enable_cors: bool = True) -> FastAPI:
    if env_file:
        load_dotenv(env_file)
        
    app = FastAPI(title="Model Management Service")
    
    # 配置 CORS
    if enable_cors:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # 响应模型
    class ModelResponse(BaseModel):
        code: int = 200
        message: str = ""
        data: Any

    @app.get("/me/model/list", response_model=ModelResponse)
    async def get_me_models(
        type: str = Query(default="", description="模型类型：embed/chat/rerank"),
        timeout: int = Query(default=2, description="请求超时时间（秒）")
    ):
        try:
            headers = {
                'Authorization': f'Bearer {MODEL_ENGINE_APIKEY}',
            }

            response = requests.get(
                f"{MODEL_ENGINE_HOST}/open/router/v1/models", 
                headers=headers, 
                verify=False,
                timeout=timeout
            )
            response.raise_for_status()
            result: list = response.json()['data']

            # 类型过滤
            filtered_result = []
            if type:
                for data in result:
                    if data['type'] == type:
                        filtered_result.append(data)
                if not filtered_result:
                    result_types = set(data['type'] for data in result)
                    return ModelResponse(
                        code=404,
                        message=f"未找到类型为 '{type}' 的模型。可用类型：{result_types}",
                        data=[]
                    )
            else:
                filtered_result = result

            return ModelResponse(
                code=200,
                message="获取成功",
                data=filtered_result
            )

        except Exception as e:
            return ModelResponse(
                code=500,
                message=f"获取模型列表失败：{str(e)}",
                data=[]
            )

    @app.get("/me/healthcheck", response_model=ModelResponse)
    async def check_me_connectivity(timeout: int = Query(default=2, description="超时时间（秒）")):
        try:
            headers = {'Authorization': f'Bearer {MODEL_ENGINE_APIKEY}'}
            try:
                response = requests.get(
                    f"{MODEL_ENGINE_HOST}/open/router/v1/models",
                    headers=headers,
                    verify=False,
                    timeout=timeout
                )
            except requests.exceptions.Timeout:
                return ModelResponse(
                    code=408,
                    message="连接超时",
                    data={"status": "Disconnected", "desc": "连接超时", "connect_status": ModelConnectStatusEnum.UNAVAILABLE.value}
                )

            if response.status_code == 200:
                return ModelResponse(
                    code=200,
                    message="连接成功",
                    data={"status": "Connected", "desc": "连接成功", "connect_status": ModelConnectStatusEnum.AVAILABLE.value}
                )
            else:
                return ModelResponse(
                    code=response.status_code,
                    message=f"连接失败，错误码: {response.status_code}",
                    data={"status": "Disconnected", "desc": f"连接失败，错误码: {response.status_code}", "connect_status": ModelConnectStatusEnum.UNAVAILABLE.value}
                )

        except Exception as e:
            return ModelResponse(
                code=500,
                message=f"发生未知错误: {str(e)}",
                data={"status": "Disconnected", "desc": f"发生未知错误: {str(e)}", "connect_status": ModelConnectStatusEnum.UNAVAILABLE.value}
            )

    @app.get("/me/model/healthcheck", response_model=ModelResponse)
    async def check_me_model_connectivity(
        model_name: str = Query(..., description="要检查的模型名称")
    ):
        try:
            headers = {'Authorization': f'Bearer {MODEL_ENGINE_APIKEY}'}
            response = requests.get(
                f"{MODEL_ENGINE_HOST}/open/router/v1/models",
                headers=headers,
                verify=False
            )
            response.raise_for_status()
            result = response.json()['data']

            # 查找模型
            model_data = next((item for item in result if item['id'] == model_name), None)
            if not model_data:
                return ModelResponse(
                    code=404,
                    message="未找到指定模型",
                    data={"connectivity": False, "message": "未找到指定模型", "connect_status": ""}
                )

            model_type = model_data['type']

            if model_type == 'llm':
                payload = {
                    "model": model_name,
                    "messages": [{"role": "user", "content": "hello"}]
                }
                api_response = requests.post(
                    f"{MODEL_ENGINE_HOST}/open/router/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    verify=False
                )
            elif model_type == 'embedding':
                payload = {
                    "model": model_name,
                    "input": "Hello"
                }
                api_response = requests.post(
                    f"{MODEL_ENGINE_HOST}/open/router/v1/embeddings",
                    headers=headers,
                    json=payload,
                    verify=False
                )
            else:
                return ModelResponse(
                    code=400,
                    message=f"不支持 {model_type} 类型的模型健康检查",
                    data={"connectivity": False, "message": f"不支持 {model_type} 类型的模型健康检查", "connect_status": ModelConnectStatusEnum.UNAVAILABLE.value}
                )

            if api_response.status_code == 200:
                connect_status = ModelConnectStatusEnum.AVAILABLE.value
                return ModelResponse(
                    code=200,
                    message=f"模型 {model_name} 响应正常",
                    data={"connectivity": True, "message": f"模型 {model_name} 响应正常", "connect_status": connect_status}
                )
            else:
                connect_status = ModelConnectStatusEnum.UNAVAILABLE.value
                return ModelResponse(
                    code=api_response.status_code,
                    message=f"模型 {model_name} 响应失败",
                    data={"connectivity": False, "message": f"模型 {model_name} 响应失败: {api_response.text}", "connect_status": connect_status}
                )

        except Exception as e:
            return ModelResponse(
                code=500,
                message=f"发生未知错误: {str(e)}",
                data={"connectivity": False, "message": f"发生未知错误: {str(e)}", "connect_status": ModelConnectStatusEnum.UNAVAILABLE.value}
            )

    # 定义请求模型
    class ModelRequest(BaseModel):
        model_factory: Optional[str] = 'OpenAI-API-Compatible'
        model_name: str
        model_type: str
        api_key: Optional[str] = ''
        base_url: Optional[str] = ''
        max_tokens: Optional[int] = 0
        used_token: Optional[int] = 0
        display_name: Optional[str] = ''
        connect_status: Optional[str] = ''

    @app.post("/model/create", response_model=ModelResponse)
    async def create_model(request: ModelRequest):
        try:
            model_data = request.model_dump()
            # 拆解model_name
            model_repo, model_name = split_repo_name(model_data["model_name"])
            # 确保model_repo为空字符串而不是null
            model_data["model_repo"] = model_repo if model_repo else ""
            model_data["model_name"] = model_name

            if not model_data.get("display_name"):
                model_data["display_name"] = model_name
                
            # 使用NOT_DETECTED状态作为默认值
            model_data["connect_status"] = model_data.get("connect_status") or ModelConnectStatusEnum.NOT_DETECTED.value
                
            # 检查display_name是否冲突
            if model_data.get("display_name"):
                existing_model_by_display = get_model_by_display_name(model_data["display_name"])
                if existing_model_by_display:
                    return ModelResponse(
                        code=409,
                        message=f"名称 {model_data['display_name']} 已被使用，请更换显示名称",
                        data=None
                    )

            create_model_record(model_data)
            return ModelResponse(
                code=200,
                message=f"模型 {add_repo_to_name(model_repo, model_name)} 创建成功",
                data=None
            )
        except Exception as e:
            return ModelResponse(
                code=500,
                message=f"模型创建失败：{str(e)}",
                data=None
            )
        
    @app.post("/model/update", response_model=ModelResponse)
    def update_model(request: ModelRequest):
        try:
            model_data = request.model_dump()
            # 拆解model_name
            model_repo, model_name = split_repo_name(model_data["model_name"])
            # 确保model_repo为空字符串而不是null
            model_data["model_repo"] = model_repo if model_repo else ""
            model_data["model_name"] = model_name
            
            # 修改这一行：使用不为空的状态值
            model_data["connect_status"] = model_data.get("connect_status") or ModelConnectStatusEnum.NOT_DETECTED.value
            
            # 检查模型是否存在
            existing_model = get_model_by_name(model_name, model_repo)
            if not existing_model:
                return ModelResponse(
                    code=404,
                    message=f"未找到模型：{add_repo_to_name(model_repo, model_name)}",
                    data=None
                )
                
            # 如果提供了显示名称且与现有不同，需要检查是否重复
            if model_data.get("display_name") and model_data["display_name"] != existing_model.get("display_name"):
                existing_model_by_display = get_model_by_display_name(model_data["display_name"])
                if existing_model_by_display and existing_model_by_display["model_id"] != existing_model["model_id"]:
                    return ModelResponse(
                        code=409,
                        message=f"显示名称 {model_data['display_name']} 已被使用，请更换显示名称",
                        data=None
                    )
            
            # 更新模型记录
            update_model_record(existing_model["model_id"], model_data)
            return ModelResponse(
                code=200,
                message=f"模型 {add_repo_to_name(model_repo, model_name)} 更新成功",
                data={"model_name": add_repo_to_name(model_repo, model_name)}
            )
        except Exception as e:
            return ModelResponse(
                code=500,
                message=f"模型更新失败：{str(e)}",
                data=None
            )

    @app.post("/model/delete", response_model=ModelResponse)
    async def delete_model(model_name: str = Body(..., embed=True)):
        """
        删除指定的模型（软删除）

        Args:
            model_name: 要删除的模型名称。包含model_repo，例如：openai/gpt-3.5-turbo
        """
        try:
            # 拆解model_name
            model_repo, name = split_repo_name(model_name)
            # 确保model_repo为空字符串而不是null
            model_repo = model_repo if model_repo else ""
            # 根据拆解后的model_repo和model_name查找模型
            model = get_model_by_name(name, model_repo)
            if not model:
                return ModelResponse(
                    code=404,
                    message=f"未找到模型：{model_name}",
                    data=None
                )
            
            delete_model_record(model["model_id"])
            return ModelResponse(
                code=200,
                message="模型删除成功",
                data={"model_name": model_name}
            )
        except Exception as e:
            return ModelResponse(
                code=500,
                message=f"模型删除失败：{str(e)}",
                data=None
            )

    @app.get("/model/list", response_model=ModelResponse)
    async def get_model_list():
        """
        获取所有模型的详情信息
        """
        try:
            records = get_model_records()
            
            result = []
            # 对每个记录使用add_repo_to_name方法，为model_name添加repo前缀
            for record in records:
                record["model_name"] = add_repo_to_name(
                    model_repo=record["model_repo"],
                    model_name=record["model_name"]
                )
                # 处理connect_status，如果为空则使用默认值"未检测"
                record["connect_status"] = ModelConnectStatusEnum.get_value(record.get("connect_status"))
                result.append(record)
                
            return ModelResponse(
                code=200,
                message="获取模型列表成功",
                data=result
            )
        except Exception as e:
            return ModelResponse(
                code=500,
                message=f"获取模型列表失败：{str(e)}",
                data=[]
            )

    @app.get("/model/healthcheck", response_model=ModelResponse)
    async def check_model_connectivity(
        model_name: str = Query(..., description="要检查的模型名称")
    ):
        try:
            # 拆解model_name
            repo, name = split_repo_name(model_name)
            # 确保repo为空字符串而不是null
            repo = repo if repo else ""
            # 根据拆解后的model_repo和model_name查找模型
            logging.info(f"检查模型连通性：{repo}/{name}")
            model = get_model_by_name(name, repo)
            if not model:
                return ModelResponse(
                    code=404,
                    message=f"未找到模型 {model_name} 的配置信息",
                    data={"connectivity": False, "connect_status": ""}
                )

            # 设置模型为"检测中"状态
            update_data = {"connect_status": ModelConnectStatusEnum.DETECTING.value}
            update_model_record(model["model_id"], update_data)

            model_type = model["model_type"]
            model_base_url = model["base_url"]
            model_api_key = model["api_key"]
            connectivity: bool
            
            # print model_name, model_base_url, model_api_key
            print(f"Check connectivity: model_name: {model_name}, model_base_url: {model_base_url}, model_api_key: {model_api_key}")

            # 根据不同模型类型进行连通性测试
            if model_type == "embedding":
                # TODO: 未来需要实现非Jina模型的实例化
                connectivity = JinaEmbedding(model_name=model_name ,base_url=model_base_url, api_key=model_api_key).check_connectivity()

            elif model_type == "llm":
                observer = MessageObserver()
                connectivity = OpenAIModel(observer, model_id=model_name, api_base=model_base_url, api_key=model_api_key).check_connectivity()

            elif model_type == "rerank":
                # connectivity =  RerankModel.check_connectivity()
                # TODO: 需要实现RerankModel的连通性测试
                connectivity = False
            elif model_type in ["tts", "stt"]:
                connectivity = await VoiceService().check_connectivity(model_type)
            
            else:
                # 不支持的模型类型，更新为不可用状态
                update_data = {"connect_status": ModelConnectStatusEnum.UNAVAILABLE.value}
                update_model_record(model["model_id"], update_data)
                return ModelResponse(
                    code=400,
                    message=f"不支持的模型类型：{model_type}",
                    data={"connectivity": False, "connect_status": ModelConnectStatusEnum.UNAVAILABLE.value}
                )

            # 根据连通性结果更新模型状态
            connect_status = ModelConnectStatusEnum.AVAILABLE.value if connectivity else ModelConnectStatusEnum.UNAVAILABLE.value
            update_data = {"connect_status": connect_status}
            update_model_record(model["model_id"], update_data)

            return ModelResponse(
                code=200,
                message=f"模型 {model_name} 连通{'成功' if connectivity else '失败'}",
                data={"connectivity": connectivity, "connect_status": connect_status}
            )

        except Exception as e:
            # 发生异常时，更新为不可用状态
            if model:
                update_data = {"connect_status": ModelConnectStatusEnum.UNAVAILABLE.value}
                update_model_record(model["model_id"], update_data)
                
            return ModelResponse(
                code=500,
                message=f"连通性测试发生错误：{str(e)}",
                data={"connectivity": False, "connect_status": ModelConnectStatusEnum.UNAVAILABLE.value}
            )

    @app.get("/model/get_connect_status", response_model=ModelResponse)
    async def get_model_connect_status(
        model_name: str = Query(..., description="模型名称")
    ):
        """
        直接从数据库中查询模型的连接状态
        
        Args:
            model_name: 要查询的模型名称，包含仓库信息，例如 openai/gpt-3.5-turbo
            
        Returns:
            ModelResponse: 包含模型连接状态的响应
        """
        try:
            # 拆解model_name
            repo, name = split_repo_name(model_name)
            # 确保repo为空字符串而不是null
            repo = repo if repo else ""
            
            # 查询模型信息
            model = get_model_by_name(name, repo)
            if not model:
                return ModelResponse(
                    code=404,
                    message=f"未找到模型：{model_name}",
                    data={"connect_status": ""}
                )
            
            # 获取连接状态
            connect_status = model.get("connect_status", "")
            connect_status = ModelConnectStatusEnum.get_value(connect_status)
            
            return ModelResponse(
                code=200,
                message=f"获取模型 {model_name} 连接状态成功",
                data={
                    "model_name": model_name,
                    "connect_status": connect_status
                }
            )
        except Exception as e:
            return ModelResponse(
                code=500,
                message=f"获取模型连接状态失败：{str(e)}",
                data={"connect_status": ModelConnectStatusEnum.NOT_DETECTED.value}
            )
    
    @app.post("/model/update_connect_status", response_model=ModelResponse)
    async def update_model_connect_status(
        model_name: str = Body(..., embed=True),
        connect_status: str = Body(..., embed=True)
    ):
        """
        更新模型的连接状态
        
        Args:
            model_name: 模型名称，包含仓库信息，例如 openai/gpt-3.5-turbo
            connect_status: 新的连接状态
        """
        try:
            # 拆解model_name
            repo, name = split_repo_name(model_name)
            # 确保repo为空字符串而不是null
            repo = repo if repo else ""
            
            # 查询模型信息
            model = get_model_by_name(name, repo)
            if not model:
                return ModelResponse(
                    code=404,
                    message=f"未找到模型：{model_name}",
                    data={"connect_status": ""}
                )
            
            # 更新连接状态
            update_data = {"connect_status": connect_status}
            update_model_record(model["model_id"], update_data)
            
            return ModelResponse(
                code=200,
                message=f"更新模型 {model_name} 连接状态成功",
                data={
                    "model_name": model_name,
                    "connect_status": connect_status
                }
            )
        except Exception as e:
            return ModelResponse(
                code=500,
                message=f"更新模型连接状态失败：{str(e)}",
                data={"connect_status": ModelConnectStatusEnum.NOT_DETECTED.value}
            )
        
    
    @app.get("/model/auto_update_connect_status", response_model=ModelResponse)
    async def update_model_connectivity(
        model_name: str = Body(..., embed=True)
    ):
        """
        检查模型的实时连通性，并更新数据库中的连接状态
        
        Args:
            model_name: 模型名称，推荐包含仓库信息，例如 openai/gpt-3.5-turbo
            
        Returns:
            ModelResponse: 包含模型连通性检查结果的响应
        """
        try:
            # 拆解model_name
            repo, name = split_repo_name(model_name)
            # 确保repo为空字符串而不是null
            repo = repo if repo else ""
            
            # 从数据库查询模型信息，判断是否为本地模型
            local_models = get_model_by_name(name, repo)
            print(f"local_models: {local_models}")
            
            # 如果是本地模型
            if local_models:
                # 设置模型为"检测中"状态
                update_data = {"connect_status": ModelConnectStatusEnum.DETECTING.value}
                update_model_record(local_models["model_id"], update_data)
                
                # 调用本地模型连通性检查方法
                response = await check_model_connectivity(model_name=model_name)
                return response
            # 如果数据库中找不到，则尝试作为ME模型进行检查
            else:
                # 调用模型引擎连通性检查方法
                response = await check_me_model_connectivity(model_name=model_name)
            
            return response
                
        except Exception as e:
            # 如果是本地模型，更新为不可用状态
            if local_models:
                update_data = {"connect_status": ModelConnectStatusEnum.UNAVAILABLE.value}
                update_model_record(local_models["model_id"], update_data)
                
            return ModelResponse(
                code=500,
                message=f"检查模型连通性失败：{str(e)}",
                data={"connectivity": False, "connect_status": ModelConnectStatusEnum.NOT_DETECTED.value}
            )

    return app

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='运行模型管理服务')
    parser.add_argument('--env', type=str, help='环境配置文件路径')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='服务器主机地址')
    parser.add_argument('--port', type=int, default=8003, help='服务器端口')
    parser.add_argument('--no-cors', action='store_true', help='禁用 CORS 中间件')
    args = parser.parse_args()
    
    print(f"Starting model management service")
    print(f"Host: {args.host}, Port: {args.port}")
    print(f"CORS middleware: {'disabled' if args.no_cors else 'enabled'}")
    if args.env:
        print(f"Using environment file: {args.env}")
    
    app = create_model_management_app(
        env_file=args.env,
        enable_cors=not args.no_cors
    )
    
    uvicorn.run(app, host=args.host, port=args.port)
