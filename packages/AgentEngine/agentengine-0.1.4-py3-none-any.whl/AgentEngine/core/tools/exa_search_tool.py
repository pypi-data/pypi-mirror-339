import json
from exa_py import Exa
from AgentEngine.framework.tools import Tool
from AgentEngine.core.utils import MessageObserver, ProcessType
from AgentEngine.core.utils.search_result_message import SearchResultMessage


class EXASearchTool(Tool):
    name = "exa_web_search"
    description = "Performs a EXA web search based on your query (think a Google search) then returns the top search results. "\
                  "A tool for retrieving publicly available information, news, general knowledge, or non-proprietary data from the internet. Use this for real-time updates, broad topics, or when the query falls outside the company's internal knowledge base."\
                  "Use for open-domain, real-time, or general knowledge queries"

    inputs = {"query": {"type": "string", "description": "The search query to perform."}}
    output_type = "string"

    supported_languages = {'zh', 'en'}
    messages = {
        'en': {
            'summary_prompt': 'Please summarize the main content of the following webpage, extract key information, and answer the user\'s question. Ensure the summary is concise and covers the core points, data, and conclusions. If the webpage content involves multiple topics, please summarize each topic separately. The user\'s question is: [{query}]. Please provide an accurate answer based on the webpage content, and note the information source (if applicable).',
            'search_failed': 'Search request failed: {}',
            'no_results': 'No results found! Try a less restrictive/shorter query.',
            'search_success': 'EXA Search Results'
        },
        'zh': {
            'summary_prompt': '请总结以下网页的主要内容，提取关键信息，并回答用户的问题。确保总结简洁明了，涵盖核心观点、数据和结论。如果网页内容涉及多个主题，请分别概述每个主题的重点。用户的问题是：[{query}]。请根据网页内容提供准确的回答，并注明信息来源（如适用）。',
            'search_failed': '搜索请求失败：{}',
            'no_results': '未找到结果！请尝试使用更简短或更宽泛的搜索词。',
            'search_success': 'EXA搜索结果'
        }   
    }


    def __init__(self, exa_api_key, observer: MessageObserver = None, max_results=5, is_model_summary=False, lang='zh'):
        super().__init__()

        self.observer = observer
        self.exa = Exa(api_key=exa_api_key)
        self.max_results = max_results
        self.is_model_summary = is_model_summary

        if lang not in self.supported_languages:
            raise ValueError(f"Language must be one of {self.supported_languages}")
        self.lang = lang

    def forward(self, query: str) -> str:
        if self.is_model_summary:
            # 使用LLM总结功能会导致搜索速度变慢
            summary_prompt = self.messages[self.lang]['summary_prompt'].format(query=query)
            exa_search_result = self.exa.search_and_contents(
                query,
                text=True,
                extras={
                    "links": 0,
                    "image_links": 10
                },
                num_results=self.max_results,
                summary={
                    "query":summary_prompt
                }
            )
        else:
            exa_search_result = self.exa.search_and_contents(
                query,
                text={
                        "max_characters": 2000
                     },
                extras={
                    "links": 0,
                    "image_links": 10
                },
                num_results=self.max_results
            )

        if len(exa_search_result.results) == 0:
            raise Exception(self.messages[self.lang]['no_results'])

        images_list_url = []
        search_results_json = []
        for single_result in exa_search_result.results:
            search_result_message = SearchResultMessage(
                title=single_result.title,
                url=single_result.url,
                text=single_result.text,
                published_date=single_result.published_date,
                source_type="url",
                filename="",
                score="",
                score_details={}
            )
            
            search_results_json.append(search_result_message.to_dict())
            images_list_url.extend(single_result.extras["image_links"])
        
        # 对图片列表进行去重
        images_list_url = list(dict.fromkeys(images_list_url))
        
        if self.observer:
            search_results_data = json.dumps(search_results_json, ensure_ascii=False)
            self.observer.add_message("", ProcessType.SEARCH_CONTENT, search_results_data)

            search_images_list_json = json.dumps({"images_url": images_list_url}, ensure_ascii=False)
            self.observer.add_message("", ProcessType.PICTURE_WEB, search_images_list_json)

        processed_results = [f"[{result.title}]\n{result.text}" for result in exa_search_result.results]

        return "## " + self.messages[self.lang]['search_success'] + "\n" + "\n\n".join(processed_results) + "\n\n"

if __name__ == "__main__":
    try:
        tool = EXASearchTool(exa_api_key="8c7b42fa-d6bf-4b61-ae8d-5b2786388145", observer=None, max_results=1, is_model_summary=True, lang='zh')

        query = "Who is the president of the United States?"
        result = tool.forward(query)
        print(result)
    except Exception as e:
        print(e)