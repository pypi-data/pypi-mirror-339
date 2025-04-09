import aiohttp
import json

class HalChatAPI:
    """
    Класс для асинхронной работы с HTTP (REST) запросами к HalChat-серверу.
    """

    def __init__(self, code: str, base_url: str = 'https://halchat.halwarsing.net/api', log_level: int = 1):
        self.code = code
        self.url = base_url
        self.log_level = log_level

    async def api_req(self, req: str, get_data: str = '', post_data: dict = None):
        """
        Асинхронный метод для выполнения POST-запроса на:
            <base_url>?req=<req><get_data>
        Параметры всегда дополняются {'code': self.code}.
        Возвращает распарсенный JSON или None при ошибке.
        """
        if post_data is None:
            post_data = {}
        post_data['code'] = self.code  # Добавляем code
        full_url = f"{self.url}?req={req}{get_data}"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(full_url, data=post_data) as response:
                    if response.status == 200:
                        # Пытаемся распарсить JSON
                        content_type = response.headers.get('Content-Type', '')
                        if 'application/json' in content_type:
                            o = await response.json()
                        else:
                            # Если не JSON, пробуем текст
                            text_data = await response.text()
                            if self.log_level > 0:
                                print(f"Error: Response is not JSON. Text: {text_data}")
                            return None

                        if o['errorCode'] > 0 and self.log_level > 0:
                            print('Error api: ', o,req,get_data,full_url,post_data)
                        if self.log_level > 1:
                            print('Successfully api request: ', req, get_data, post_data, o)
                        return o
                    else:
                        if self.log_level > 0:
                            print(f"HTTP Error code: {response.status}")
                        return None
            except aiohttp.ClientError as e:
                if self.log_level > 0:
                    print(f"ClientError in api_req: {e}")
                return None
            except Exception as e:
                if self.log_level > 0:
                    print(f"Unexpected error in api_req: {e}")
                return None