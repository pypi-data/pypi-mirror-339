from typing import List, Dict, AsyncGenerator, Optional
import os
import json
from dotenv import load_dotenv
import asyncio
import argparse
import time
from pathlib import Path
from threading import Thread, Lock
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from AgentEngine.core.utils.agent_utils import agent_run, agent_run_thread
from AgentEngine.core import MessageObserver, FinalAnswerFormatTool, EXASearchTool, KBSearchTool
from AgentEngine.core.agents import CoreAgent
from AgentEngine.core.models import OpenAIModel
from AgentEngine.framework.memory import TaskStep, ActionStep

class ThreadManager:
    """线程管理器，用于跟踪和管理所有活动的线程"""
    def __init__(self):
        self.active_threads = {}
        self.lock = Lock()
    
    def add_thread(self, thread_id: str, thread: Thread, agent: CoreAgent):
        """添加一个新的线程"""
        with self.lock:
            self.active_threads[thread_id] = {
                'thread': thread,
                'agent': agent,
                'start_time': time.time()
            }
    
    def remove_thread(self, thread_id: str):
        """移除一个线程"""
        with self.lock:
            if thread_id in self.active_threads:
                del self.active_threads[thread_id]
    
    def stop_thread(self, thread_id: str):
        """停止一个线程"""
        with self.lock:
            if thread_id in self.active_threads:
                thread_data = self.active_threads[thread_id]
                agent = thread_data['agent']
                # 设置停止标志
                agent.should_stop = True
                # 取消当前的模型请求
                if hasattr(agent.model, 'cancel_request'):
                    agent.model.cancel_request()
                # 等待线程结束
                thread_data['thread'].join(timeout=5)
                del self.active_threads[thread_id]

# 创建全局线程管理器实例
thread_manager = ThreadManager()

class ConfigManager:
    """配置管理器，用于动态加载和缓存配置"""
    def __init__(self, env_file=".env"):
        self.env_file = env_file
        self.last_modified_time = 0
        self.config_cache = {}
        self.load_config()
    
    def load_config(self):
        """加载配置文件并更新缓存"""
        # 检查文件是否存在
        if not os.path.exists(self.env_file):
            print(f"警告: 配置文件 {self.env_file} 不存在")
            return
        
        # 获取文件最后修改时间
        current_mtime = os.path.getmtime(self.env_file)
        
        # 如果文件没有被修改，直接返回
        if current_mtime == self.last_modified_time:
            return
        
        # 更新最后修改时间
        self.last_modified_time = current_mtime
        
        # 重新加载配置
        load_dotenv(self.env_file, override=True)
        
        # 更新缓存
        self.config_cache = {
            "LLM_MODEL_NAME": os.getenv("LLM_MODEL_NAME", ""),
            "LLM_API_KEY": os.getenv("LLM_API_KEY", ""),
            "LLM_MODEL_URL": os.getenv("LLM_MODEL_URL", ""),
            "LLM_SECONDARY_MODEL_NAME": os.getenv("LLM_SECONDARY_MODEL_NAME", ""),
            "LLM_SECONDARY_API_KEY": os.getenv("LLM_SECONDARY_API_KEY", ""),
            "LLM_SECONDARY_MODEL_URL": os.getenv("LLM_SECONDARY_MODEL_URL", ""),
            "EXA_API_KEY": os.getenv("EXA_API_KEY", ""),
            "SELECTED_KB_NAMES": os.getenv("SELECTED_KB_NAMES", ""),
            "ELASTICSEARCH_SERVICE": os.getenv("ELASTICSEARCH_SERVICE", "")
        }
        
        print(f"配置已重新加载，时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def get_config(self, key, default=""):
        """获取配置值，如果配置已更新则重新加载"""
        self.load_config()
        return self.config_cache.get(key, default)
    
    def force_reload(self):
        """强制重新加载配置"""
        self.last_modified_time = 0
        self.load_config()
        return {"status": "success", "message": "配置已重新加载"}

# 创建全局配置管理器实例
config_manager = ConfigManager()

def create_agent():
    # 使用配置管理器获取配置
    observer = MessageObserver()

    # 创建模型
    main_model = OpenAIModel(
        observer=observer,
        model_id=config_manager.get_config("LLM_MODEL_NAME"),
        api_key=config_manager.get_config("LLM_API_KEY"),
        api_base=config_manager.get_config("LLM_MODEL_URL")
    )
    sub_model = OpenAIModel(
        observer=observer,
        model_id=config_manager.get_config("LLM_SECONDARY_MODEL_NAME"),
        api_key=config_manager.get_config("LLM_SECONDARY_API_KEY"),
        api_base=config_manager.get_config("LLM_SECONDARY_MODEL_URL")
    )
    
    # 创建工具
    tools = [
            EXASearchTool(
                exa_api_key=config_manager.get_config("EXA_API_KEY"),
                observer=observer,
                max_results=5),
            KBSearchTool(
                index_names=json.loads(config_manager.get_config("SELECTED_KB_NAMES", "[]")),
                base_url=config_manager.get_config("ELASTICSEARCH_SERVICE"),
                top_k=5,
                observer=observer)
            ]

    # 添加最终回答工具
    system_prompt = "针对用户提问问题，从检索内容中提取有关信息进行总结。要求有标题与正文内容。"
    final_answer_tool = FinalAnswerFormatTool(llm=main_model, system_prompt=system_prompt)
    tools.append(final_answer_tool)
    
    # 创建单独的Agent
    agent = CoreAgent(
        observer=observer,
        tools=tools,
        model=main_model,
        name="useful_agent",
        max_steps=5
    )
    
    return agent

def add_history_to_agent(agent: CoreAgent, history: List[Dict]):
    """将历史对话添加到agent的内存中"""
    if not history:
        return

    # 依次添加历史对话到内存中
    for msg in history:
        if msg['role'] == 'user':
            # 为用户消息创建任务步骤
            agent.memory.steps.append(TaskStep(task=msg['content']))
        elif msg['role'] == 'assistant':
            agent.memory.steps.append(ActionStep(action_output=msg['content'],
                                                 model_output=msg['content']))

# 创建FastAPI应用
app = FastAPI()

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境中应该限制
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有HTTP头
)


# 请求模型
class AgentRequest(BaseModel):
    query: str
    conversation_id: Optional[int] = None
    is_set: Optional[bool] = False
    history: Optional[List[Dict]] = None

# 定义API路由
@app.post("/agent/run")
async def agent_run_api(request: AgentRequest, fastapi_request: Request):
    """
    Agent运行接口
    """
    # 确保配置是最新的
    config_manager.load_config()
    
    # 新建agent并重置内存
    agent = create_agent()
    agent.memory.reset()

    # 处理历史记录
    if request.history is not None:
        add_history_to_agent(agent, request.history)
    
    try:
        # 生成唯一的线程ID
        thread_id = f"{time.time()}_{id(agent)}"
        
        # 创建线程
        thread_agent = Thread(target=agent_run_thread, args=(agent, request.query, False))
        thread_agent.start()
        
        # 将线程添加到管理器
        thread_manager.add_thread(thread_id, thread_agent, agent)
        
        async def generate():
            try:
                while thread_agent.is_alive():
                    cached_message = agent.observer.get_cached_message()
                    for message in cached_message:
                        yield f"data: {message}\n\n"
                    await asyncio.sleep(0.2)
                
                # 确保信息发送完毕
                cached_message = agent.observer.get_cached_message()
                for message in cached_message:
                    yield f"data: {message}\n\n"
            except asyncio.CancelledError:
                # 客户端中断连接时，停止线程
                thread_manager.stop_thread(thread_id)
                raise
            finally:
                # 清理线程
                thread_manager.remove_thread(thread_id)
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent运行错误: {str(e)}")

# 添加配置重载API
@app.post("/agent/reload_config")
async def reload_config():
    """
    手动触发配置重新加载
    """
    return config_manager.force_reload()

# 如果直接运行此文件，则启动服务
if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="Agent服务")
    parser.add_argument("--port", type=int, default=8006, help="服务运行的端口号")
    args = parser.parse_args()

    # 使用命令行参数指定的端口运行服务
    uvicorn.run(app, host="0.0.0.0", port=args.port)
