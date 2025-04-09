import requests
import json

"""
description: 模拟发送请求，获取后端流式输出
"""


data = {
    # "query": "特朗普内阁成员",
    "query": "介绍华为汽车",
    # "query": "你有哪些工具？",
}

response = requests.post("http://127.0.0.1:8000/single_agent", json=data, stream=True)

for line in response.iter_lines():
    if line:
        print(line)
        decoded_line = line.decode('utf-8')
        try:
            # 检查是否是SSE格式(以"data: "开头)
            if decoded_line.startswith('data: '):
                # 提取"data: "后面的JSON部分
                json_str = decoded_line[6:]  # 跳过"data: "前缀
                chunk = json.loads(json_str)
                if "content" in chunk:
                    data = chunk["content"]
                    print(data, end='')
            else:
                # 如果不是SSE格式，尝试直接解析
                chunk = json.loads(decoded_line)
                if "content" in chunk:
                    data = chunk["content"]
                    print(data, end='')
        except json.JSONDecodeError:
            print(f"解析失败: {decoded_line}")

