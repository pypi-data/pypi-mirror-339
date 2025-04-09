import os
import json
import requests
from AgentEngine.framework.tools import Tool
from AgentEngine.core.utils import MessageObserver, ProcessType
from AgentEngine.core.utils.search_result_message import SearchResultMessage



class KBSearchTool(Tool):
    """支持中英文的知识库检索工具。
    """
    # TODO: 目前name和description统一为英文，后续要实现中英文两种
    name = "knowledge_base_search"
    description = "Performs a local knowledge base search based on your query then returns the top search results. "\
                  "A tool for retrieving internal company documents, policies, processes and proprietary information. Use this tool when users ask questions related to internal company matters, product details, organizational structure, internal processes, or confidential information. "\
                  "Prioritize for company-specific queries. "\
                  "Use for proprietary knowledge or restricted information" \
                  "Avoid for publicly available general knowledge"

    inputs = {"query": {"type": "string", "description": "The search query to perform."}}
    output_type = "string"

    # 所有工具内部的message支持中英文两种语言
    supported_languages = {'zh', 'en'}
    messages = {
        'en': {
            'search_failed': 'Search request failed: {}',
            'no_results': 'No results found! Try a less restrictive/shorter query.',
            'search_success': 'Knowledge Base Search Results'
        },
        'zh': {
            'search_failed': '搜索请求失败：{}', 
            'no_results': '未找到结果！请尝试使用更宽泛或更短的搜索词。',
            'search_success': '知识库搜索结果'
        }
    }

    def __init__(self, 
                 index_names: list[str] = [],
                 base_url: str = "http://localhost:8000",
                 top_k: int = 5, 
                 observer: MessageObserver = None, 
                 lang: str = "zh") -> None:
        """Initialize the KBSearchTool.
        
        Args:
            index_names (list[str]): Name list of the search index
            base_url (str, optional): Base URL of the search service. Defaults to "http://localhost:8000".
            top_k (int, optional): Number of results to return. Defaults to 5.
            observer (MessageObserver, optional): Message observer instance. Defaults to None.
            lang (str, optional): Language code ('zh' or 'en'). Defaults to 'en'.
        
        Raises:
            ValueError: If language is not supported
        """
        super().__init__()
        self.index_names = index_names
        self.top_k = top_k
        self.observer = observer
        self.base_url = base_url
        
        if lang not in self.supported_languages:
            raise ValueError(f"Language must be one of {self.supported_languages}")
        self.lang = lang

    def forward(self, query: str) -> str:
        kb_search_response = requests.post(
            f"{self.base_url}/indices/search/hybrid",
            json={
                "index_names": self.index_names,
                "query": query,
                "top_k": self.top_k
            }
        )
        
        if kb_search_response.status_code != 200:
            raise Exception(self.messages[self.lang]['search_failed'].format(kb_search_response.text))

        kb_search_data = kb_search_response.json()
        kb_search_results = kb_search_data["results"]

        if not kb_search_results:
            raise Exception(self.messages[self.lang]['no_results'])

        search_results_json = []
        for single_search_result in kb_search_results:
            search_result_message = SearchResultMessage(
                title=single_search_result.get("title", ""),
                text=single_search_result.get("content", ""),
                source_type=single_search_result.get("source_type", ""),
                url=single_search_result.get("path_or_url", ""),
                filename=single_search_result.get("filename", ""),
                published_date=single_search_result.get("create_time", ""),
                score=single_search_result.get("score", 0),
                score_details=single_search_result.get("score_details", {})
            )
            
            search_results_json.append(search_result_message.to_dict())
        
        if self.observer:
            search_results_data = json.dumps(search_results_json, ensure_ascii=False)
            self.observer.add_message("", ProcessType.SEARCH_CONTENT, search_results_data)

        processed_results = [f"[{result['title']}]\n{result['content']}" for result in kb_search_results]

        return "## " + self.messages[self.lang]['search_success'] + "\n" + "\n".join(processed_results) + "\n\n"


if __name__ == "__main__":
    try:
        tool = KBSearchTool(index_names=["medical"],
                base_url="http://localhost:8000",
                top_k=3)

        query = "乳腺癌的风险"
        result = tool.forward(query)
        print(result)
    except Exception as e:
        print(e)

