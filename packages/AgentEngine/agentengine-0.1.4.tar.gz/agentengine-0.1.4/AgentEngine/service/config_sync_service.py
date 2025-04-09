import json
import os
from pathlib import Path
import dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from dotenv import set_key

# 定义配置模型
class ModelApiConfig(BaseModel):
    apiKey: str
    modelUrl: str

class SingleModelConfig(BaseModel):
    modelName: str
    displayName: str
    apiConfig: Optional[ModelApiConfig] = None

class ModelConfig(BaseModel):
    llm: SingleModelConfig
    llmSecondary: SingleModelConfig
    embedding: SingleModelConfig
    rerank: SingleModelConfig
    stt: SingleModelConfig
    tts: SingleModelConfig

class AppConfig(BaseModel):
    appName: str
    appDescription: str
    iconType: str
    iconIndex: int
    iconColor: str
    customIconUrl: Optional[str] = None

class KnowledgeBaseConfig(BaseModel):
    selectedKbNames: List[str]
    selectedKbModels: List[str]
    selectedKbSources: List[str]

class GlobalConfig(BaseModel):
    app: AppConfig
    models: ModelConfig
    data: KnowledgeBaseConfig

app = FastAPI()

# 配置CORS
origins = [
    "http://localhost:8010",
    "http://127.0.0.1:8010",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

@app.get("/healthcheck")
async def healthcheck():
    return {
        "status": "ok",
        "message": "Config syncronization service running"
    }

@app.post("/save_config")
async def save_config(config: GlobalConfig):
    try:
        env_path = Path(".env")
        print(f"Saving config to {env_path}")
        
        def safe_value(value):
            """处理配置值的辅助函数"""
            if value is None:
                return ""
            return str(value)
        
        def safe_list(value):
            """处理列表值的辅助函数，使用JSON格式存储以便于解析"""
            if not value:
                return "[]"
            return json.dumps(value)
        
        def get_env_key(key: str, is_model: bool = False) -> str:
            """生成环境变量键名的辅助函数"""
            # 处理驼峰命名转换为下划线格式
            import re
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', key)
            return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).upper()
        
        config_dict = config.model_dump(exclude_none=False)
        env_config = {}
        
        # 处理应用配置 - 直接使用键名，不添加前缀
        for key, value in config_dict.get("app", {}).items():
            env_key = get_env_key(key)
            env_config[env_key] = safe_value(value)
        
        # 处理模型配置
        for model_type, model_config in config_dict.get("models", {}).items():
            if not model_config:
                continue
            
            model_prefix = get_env_key(model_type)
            
            # 处理基本模型属性
            for key, value in model_config.items():
                if key == "apiConfig":
                    # 处理API配置 - 直接使用模型名称作为前缀，不添加API_
                    api_config = value or {}
                    if api_config:
                        for api_key, api_value in api_config.items():
                            env_key = f"{model_prefix}_{get_env_key(api_key)}"
                            env_config[env_key] = safe_value(api_value)
                    else:
                        # 设置默认空值
                        env_config[f"{model_prefix}_API_KEY"] = ""
                        env_config[f"{model_prefix}_MODEL_URL"] = ""
                else:
                    env_key = f"{model_prefix}_{get_env_key(key)}"
                    env_config[env_key] = safe_value(value)
        
        # 处理知识库配置 - 直接使用键名，不添加前缀，使用JSON格式存储列表
        for key, value in config_dict.get("data", {}).items():
            env_key = get_env_key(key)
            if isinstance(value, list):
                env_config[env_key] = safe_list(value)
            else:
                env_config[env_key] = safe_value(value)
        
        # 批量更新环境变量
        for key, value in env_config.items():
            set_key(env_path, key, value)
        
        return JSONResponse(
            status_code=200,
            content={"message": "配置保存成功", "status": "saved"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"message": f"配置保存失败: {str(e)}", "status": "unsaved"}
        )
    
@app.get("/load_config")
async def load_config():
    """
    从环境变量中加载配置
    
    Returns:
        JSONResponse: 包含配置内容的JSON对象
    """
    try:
        env_path = os.getenv("ENV_PATH", ".env")
        
        # 读取环境变量
        dotenv.load_dotenv(env_path)
        
        # 构建配置对象
        config = {
            "app": {
                "name": os.getenv("APP_NAME", "智能问答"),
                "description": os.getenv("APP_DESCRIPTION", ""),
                "icon": {
                    "type": os.getenv("ICON_TYPE", "preset"),
                    "index": os.getenv("ICON_INDEX", "0"),
                    "color": os.getenv("ICON_COLOR", "#235fe1"),
                    "customUrl": os.getenv("CUSTOM_ICON_URL", "")
                }
            },
            "models": {
                "llm": {
                    "name": os.getenv("LLM_MODEL_NAME", ""),
                    "displayName": os.getenv("LLM_DISPLAY_NAME", ""),
                    "apiConfig": {
                        "apiKey": os.getenv("LLM_API_KEY", ""),
                        "modelUrl": os.getenv("LLM_MODEL_URL", "")
                    }
                },
                "secondaryLlm": {
                    "name": os.getenv("LLM_SECONDARY_MODEL_NAME", ""),
                    "displayName": os.getenv("LLM_SECONDARY_DISPLAY_NAME", ""),
                    "apiConfig": {
                        "apiKey": os.getenv("LLM_SECONDARY_API_KEY", ""),
                        "modelUrl": os.getenv("LLM_SECONDARY_MODEL_URL", "")
                    }
                },
                "embedding": {
                    "name": os.getenv("EMBEDDING_MODEL_NAME", ""),
                    "displayName": os.getenv("EMBEDDING_DISPLAY_NAME", ""),
                    "apiConfig": {
                        "apiKey": os.getenv("EMBEDDING_API_KEY", ""),
                        "modelUrl": os.getenv("EMBEDDING_MODEL_URL", "")
                    }
                },
                "rerank": {
                    "name": os.getenv("RERANK_MODEL_NAME", ""),
                    "displayName": os.getenv("RERANK_DISPLAY_NAME", ""),
                    "apiConfig": {
                        "apiKey": os.getenv("RERANK_API_KEY", ""),
                        "modelUrl": os.getenv("RERANK_MODEL_URL", "")
                    }
                },
                "stt": {
                    "name": os.getenv("STT_MODEL_NAME", ""),
                    "displayName": os.getenv("STT_DISPLAY_NAME", ""),
                    "apiConfig": {
                        "apiKey": os.getenv("STT_API_KEY", ""),
                        "modelUrl": os.getenv("STT_MODEL_URL", "")
                    }
                },
                "tts": {
                    "name": os.getenv("TTS_MODEL_NAME", ""),
                    "displayName": os.getenv("TTS_DISPLAY_NAME", ""),
                    "apiConfig": {
                        "apiKey": os.getenv("TTS_API_KEY", ""),
                        "modelUrl": os.getenv("TTS_MODEL_URL", "")
                    }
                }
            },
            "data": {
                "selectedKbNames": json.loads(os.getenv("SELECTED_KB_NAMES", "[]")),
                "selectedKbModels": json.loads(os.getenv("SELECTED_KB_MODELS", "[]")),
                "selectedKbSources": json.loads(os.getenv("SELECTED_KB_SOURCES", "[]"))
            }
        }
        
        return JSONResponse(
            status_code=200,
            content={"config": config}
        )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"message": f"加载配置失败: {str(e)}", "status": "error"}
        )    

    
@app.get("/get_config/selected_knowledge_base")
async def get_selected_knowledge_base():
    """
    获取环境变量中配置的已选择知识库列表
    
    Returns:
        JSONResponse: 包含已选择知识库名称的列表
    """
    try:
        # 从环境变量中获取选中的知识库名称
        kb_names_str = os.getenv("SELECTED_KB_NAMES", "[]")
        # 解析JSON字符串为Python列表
        kb_names = json.loads(kb_names_str)
        
        return JSONResponse(
            status_code=200,
            content={"kb_names": kb_names}
        )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"message": f"获取知识库列表失败: {str(e)}"}
        )


if __name__ == "__main__":
    import uvicorn
    print("Starting config sync service on http://0.0.0.0:8010")
    uvicorn.run(app, host="0.0.0.0", port=8010)
