
from AgentEngine.core.agents import CoreAgent
from AgentEngine.core.models import OpenAIModel
from AgentEngine.core.utils.observer import MessageObserver
from AgentEngine.core.tools import FinalAnswerFormatTool, EXASearchTool


"""
description: 单独测试,从控制台获取agent.run运行结果
"""


def single_agent():
    observer = MessageObserver()

    model = OpenAIModel(
        observer=observer,
        model_id="deepseek-ai/DeepSeek-V3",
        api_key="sk-",
        api_base="https://api.siliconflow.cn")

    search_tool = EXASearchTool(exa_api_key="", max_results= 1)

    system_prompt = "针对用户提问问题，从检索内容中提取有关信息进行总结。要求有标题与正文内容。"
    final_answer_tool = FinalAnswerFormatTool(llm=model, system_prompt=system_prompt)

    search_request_agent = CoreAgent(
        observer=observer,
        tools=[search_tool, final_answer_tool],
        model=model,
        name="smart_agent",
        max_steps=5
    )

    # search_request_agent.run("介绍华为汽车")
    # search_request_agent.run("特朗普内阁成员")
    search_request_agent.run("你有哪些工具？")




if __name__ == "__main__":
    single_agent()
