from AgentEngine.framework.tools import Tool
from AgentEngine.framework.models import MessageRole


class FinalAnswerFormatTool(Tool):
    name = "summary_tool"
    description = "具有可靠的总结能力，可以生成令用户满意的回答。需要传入用户提问与检索结果。返回内容可以直接作为final_answer的输入"
    inputs = {"query": {"type": "string", "description": "输入用户提问"},
              "search_result": {"type": "string", "description": "输入检索到的信息，可以直接传入之前检索的字符串变量"}}
    output_type = "string"

    def __init__(self, llm, system_prompt):
        super().__init__()
        self.model = llm
        self.system_prompt = system_prompt

    def forward(self, query: str, search_result: str) -> str:
        messages = [
            {"role": MessageRole.SYSTEM, "content": self.system_prompt},
            {"role": MessageRole.USER, "content": f"### 检索信息：{search_result}\n### 用户提问：{query}\n"}
        ]
        model_output_message = self.model(messages=messages)

        return model_output_message.content
