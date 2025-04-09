import json
import asyncio
import websockets
import uuid

class HalChatWS:
    """
    Класс для подключения и работы с HalChat по WebSockets.
    Внутри есть:
    - connect(): постоянная попытка подключиться
    - auth(): авторизация как бот
    - keep_alive(): периодическая отправка ping
    - listen(): чтение сообщений (их dispatch в handle_event)
    """

    def __init__(self, code: str, ws_url: str = 'wss://halchat.halwarsing.net/ws/', log_level: int = 1):
        self.code = code
        self.ws_url = ws_url
        self.log_level = log_level

        self.is_run = False
        self.ws = None

        # callback или объект, который будет получать события
        self.event_handler = None

        # Хранение «висящих» запросов { request_id: Future }
        self.rpc_futures = {}

    async def connect(self):
        """
        Запуск бесконечного цикла для подключения к WS-серверу.
        При разрыве соединения пытается переподключиться.
        """
        self.is_run = True
        while self.is_run:
            try:
                self.ws = await websockets.connect(self.ws_url)
                await self.auth()
                if self.log_level > 1:
                    print("Connected to HalChat WS")

                asyncio.create_task(self.keep_alive())
                await self.listen()
            except websockets.ConnectionClosed:
                if self.log_level > 0:
                    print("Connection closed, reconnecting...")
                await asyncio.sleep(5)
            except Exception as e:
                if self.log_level > 0:
                    print(f"Error WebSocket: {e}")
                await asyncio.sleep(5)

    async def auth(self):
        """Шлёт action=authBot с токеном. Считывает ответ."""
        auth_payload = {"action": "authBot", "token": self.code}
        await self.ws.send(json.dumps(auth_payload))
        response = await self.ws.recv()
        if self.log_level > 1:
            print("Auth response -", response)

    async def api_req(self,req,post_data):
        req_id=uuid.uuid4().hex

        loop=asyncio.get_running_loop()
        future=loop.create_future()
        self.rpc_futures[req_id]=future

        post_data['req']=req
        api_payload={"action":"api","data":post_data,'reqId':req_id}

        await self.ws.send(json.dumps(api_payload))

        response=await future
        if self.log_level>1:
            print("API response -",response)
        return response

    async def keep_alive(self):
        """Каждые 30 минут отправляем 'ping' для поддержания связи."""
        while self.is_run:
            try:
                if self.ws:
                    await self.ws.send("ping")
            except Exception as e:
                if self.log_level > 0:
                    print(f"Error ping: {e}")
            await asyncio.sleep(1800)

    async def listen(self):
        """Основной цикл чтения входящих сообщений по WebSocket."""
        async for message in self.ws:
            if message == "pong":
                continue
            data = json.loads(message)
            await self.handle_event(data)

    async def handle_event(self, data: dict):
        """
        Здесь обрабатываем JSON-сообщение от WS-сервера.
        По умолчанию вызываем self.event_handler(data), если он задан.
        """
        if "action" in data and "reqId" in data and data['action']=="api":
            req_id=data['reqId']
            if req_id and req_id in self.rpc_futures:
                fut=self.rpc_futures[req_id]
                fut.set_result(data['result'])
                del self.rpc_futures[req_id]
            return
        if self.event_handler:
            await self.event_handler(data)

    async def close(self):
        """Остановка WS-сессии."""
        self.is_run = False
        if self.ws:
            await self.ws.close()