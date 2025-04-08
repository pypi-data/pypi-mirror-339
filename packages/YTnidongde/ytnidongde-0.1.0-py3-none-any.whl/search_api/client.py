import requests


class SearchClient:
    def __init__(self, base_url="https://api.cmapi004.xyz/api/videosort/0"):
        self.base_url = base_url
        self.session = requests.Session()

    def search_videos(self, query: str, max_pages: int = None) -> list:
        """
        视频搜索接口
        :param query: 搜索关键词
        :param max_pages: 最大获取页数(None表示获取全部)
        :return: 包含视频信息的字典列表
        :raises: SearchAPIError
        """
        try:
            # 获取第一页数据
            params = {"serach": query, "page": 1}
            response = self.session.get(self.base_url, params=params)
            response.raise_for_status()

            data = response.json()["rescont"]
            total_pages = data["last_page"]
            results = data["data"]

            # 计算实际需要获取的页数
            if max_pages and max_pages > 0:
                total_pages = min(total_pages, max_pages)

            # 获取剩余页数
            for page in range(2, total_pages + 1):
                params["page"] = page
                response = self.session.get(self.base_url, params=params)
                response.raise_for_status()
                results.extend(response.json()["rescont"]["data"])

            return [self._format_item(item) for item in results]

        except requests.RequestException as e:
            raise SearchAPIError(f"请求失败: {str(e)}")
        except (KeyError, ValueError) as e:
            raise SearchAPIError(f"数据解析错误: {str(e)}")

    @staticmethod
    def _format_item(raw_item: dict) -> dict:
        """统一格式化数据条目"""
        return {
            "video_id": raw_item.get("id"),
            "title": raw_item.get("title"),
            "page": raw_item.get("page", 1),
            "raw_data": raw_item  # 保留原始数据
        }


class SearchAPIError(Exception):
    """搜索API异常基类"""
    pass