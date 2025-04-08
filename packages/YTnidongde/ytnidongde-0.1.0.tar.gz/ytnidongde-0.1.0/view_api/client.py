import requests


class ViewClient:
    def __init__(self, base_url="https://api.cmapi004.xyz/api/videoplay"):
        self.base_url = base_url
        self.session = requests.Session()

    def get_video_detail(self, video_id: str) -> dict:
        """
        获取视频详细信息
        :param video_id: 视频ID
        :return: 结构化视频信息
        :raises: ViewAPIError
        """
        try:
            response = self.session.get(f"{self.base_url}/{video_id}", params={"uuid": 1})
            response.raise_for_status()

            data = response.json()["rescont"]

            if isinstance(data, list):
                raise ViewAPIError("无效的视频数据结构")

            return {
                "video_id": video_id,
                "title": data.get("title"),
                "duration": data.get("playtimes"),
                "video_url": data.get("videopath"),
                "raw_data": data  # 保留原始数据
            }

        except requests.RequestException as e:
            raise ViewAPIError(f"请求失败: {str(e)}")
        except (KeyError, ValueError) as e:
            raise ViewAPIError(f"数据解析错误: {str(e)}")


class ViewAPIError(Exception):
    """查看API异常基类"""
    pass