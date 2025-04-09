from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
import uvicorn

from starlette.exceptions import HTTPException

from AgentEngine.core.utils.agent_utils import agent_run
from AgentEngine.core import MessageObserver, FinalAnswerFormatTool, EXASearchTool, KBSearchTool
from AgentEngine.core.agents import CoreAgent
from AgentEngine.core.models import OpenAIModel


# 创建server，需要在这里构建自己的Agent
def create_single_agent():
    observer = MessageObserver()
    # model和Agent必须使用同一个observer

    model = OpenAIModel(
        observer=observer,
        model_id="deepseek-ai/DeepSeek-V3",
        api_key="sk-igdyctwzxymykufnlikqaasiqznsvdcadtdyizuxixtftfmm",
        api_base="https://api.siliconflow.cn")

    system_prompt = "针对用户提问问题，从检索内容中提取有关信息进行总结。要求有标题与正文内容。"
    final_answer_tool = FinalAnswerFormatTool(llm=model, system_prompt=system_prompt)

    search_request_agent = CoreAgent(
        observer=observer,
        tools=[EXASearchTool(exa_api_key="8c7b42fa-d6bf-4b61-ae8d-5b2786388145", observer=observer, max_results=3),
               KBSearchTool(index_names=["medical", "finance"], base_url="http://localhost:8000", top_k=3),
               final_answer_tool],
        model=model,
        name="web_search_agent",
        max_steps=3
    )

    return search_request_agent


def create_mul_agent():
    observer = MessageObserver()

    model = OpenAIModel(
        observer=observer,
        model_id="deepseek-ai/DeepSeek-V3",
        api_key="sk-",
        api_base="https://api.siliconflow.cn")


    search_request_agent = CoreAgent(
        observer=observer,
        tools=[EXASearchTool(exa_api_key="", max_results=1)],
        model=model,
        name="web_search_agent",
        description="Runs web searches for you. Give it your query as an argument.",
        max_steps=2
    )

    system_prompt = "针对用户提问问题，从检索内容中提取有关信息进行总结。要求有标题与正文内容。"
    final_answer_tool = FinalAnswerFormatTool(llm=model, system_prompt=system_prompt)
    manager_agent = CoreAgent(
        observer=observer,
        tools=[final_answer_tool],
        model=model,
        name="manager_agent",
        managed_agents=[search_request_agent],
        max_steps=3
    )
    
    return manager_agent



app = FastAPI()
# 添加这部分代码来启用CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 允许的前端地址
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有HTTP头
)

class FrontQuery(BaseModel):
    query: str


@app.post(path='/single_agent', summary="这是一个测试agent")
async def single_agent(request: FrontQuery):
    try:
        query = request.query
    except KeyError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        agent = create_single_agent()
        # agent = create_mul_agent()
    except Exception as e:
        raise HTTPException(status_code=400, detail="ERROR IN: create agent! Exception:" + str(e))

    return StreamingResponse(
        agent_run(agent, query), 
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)