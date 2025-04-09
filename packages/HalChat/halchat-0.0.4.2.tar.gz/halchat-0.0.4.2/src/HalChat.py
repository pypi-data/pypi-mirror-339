import asyncio
import json
import time
import os
import base64

# Импортируем наши классы
from HalChatEncryption import HalChatEncryption
from HalChatAPI import HalChatAPI
from HalChatWS import HalChatWS

class HalChat:
    """
    Главный класс, объединяющий:
    - шифрование (HalChatEncryption)
    - HTTP API (HalChatAPI)
    - WebSocket (HalChatWS)
    - события (onNewMessage и т.д.)
    """

    def __init__(self,
                 code: str,
                 save_file_passwords: str = 'HalChatPasswords.json',
                 auto_join_chats: bool = True,
                 check_bots_messages: bool = False,
                 log_level: int = 1
                 ):

        self.code = code
        self.save_file_passwords = save_file_passwords
        self.auto_join_chats = auto_join_chats
        self.check_bots_messages = check_bots_messages
        self.log_level = log_level

        # Инициализация вспомогательных классов
        self.encryption = HalChatEncryption()
        self.api = HalChatAPI(code, log_level=log_level)       # для HTTP запросов
        self.api_net=HalChatAPI(code,base_url='https://halwarsing.net/api/api',log_level=log_level)
        self.ws_client = HalChatWS(code, log_level=log_level)  # для WebSockets
        self.ws_client.event_handler = self.handle_ws_event    # все сообщения идут сюда

        # События
        self.events = {
            #onNewMessage(msg:HalChatMessage,isExistedPassword:bool)
            'onNewMessage': [],
            #onNewChat(fromChat:int,fromId:int,inviteId:int)
            'onNewChat': [],
            #onReceivePassword(fromChat:int,fromId:int,data:str)
            'onReceivePassword': [],
            #onStart()
            'onStart': [],
            #onClickButton(fromChat:int,fromId:int,fromMsg:int,button:HalChatButton)
            'onClickButton': [],
            #onBotMessage(fromId:int,time:int,data:str)
            'onBotMessage': [],
            #onDeleteMessage(fromChat:int,fromId:int,fromMsg:int)
            'onDeleteMessage': [],
            #onEditMessage(fromChat:int,fromId:int,fromMsg:int)
            'onEditMessage': []
        }

        # Прочие поля
        self.is_run = False
        self.chats = {}            # например, { str(chatId): [maxLastMessage, maxAction] }
        self.chats_passwords = {}  # хранение паролей для чатов
        self.requested_passwords = {}  # временно храним RSA-объекты
        self.bot_info = None
        self.bot_id = None

        # Пытаемся узнать данные бота сразу (синхронно нельзя, делаем чутка позже асинхронно)
        # Можно сделать метод init_bot_info(), который вызовем в run().

        # Загружаем пароли
        self.load_passwords()

    # ----------------------------------------------------------------
    #   Методы регистрации/вызова событий
    # ----------------------------------------------------------------
    def event(self, name: str):
        """Декоратор для подписки на события (onNewMessage, onReceivePassword, и т.д.)."""
        def decorator(func):
            self.event_add(name, func)
            return func
        return decorator

    def event_add(self, name: str, func):
        if name in self.events:
            self.events[name].append(func)
            return True
        return False

    def run_event(self, name: str, args: list):
        """Асинхронно запускаем все колбэки, подписанные на событие `name`."""
        if name in self.events:
            for ev in self.events[name]:
                asyncio.create_task(ev(*args))

    # ----------------------------------------------------------------
    #   Методы запуска/остановки
    # ----------------------------------------------------------------
    def run(self):
        """Запуск асинхронного цикла."""
        asyncio.run(self.async_run())

    async def async_run(self):
        """Асинхронная инициализация + запуск WebSocket."""
        self.is_run = True
        # Запрашиваем инфо о боте, чтобы получить self.bot_id
        await self.init_bot_info()

        # Вызываем onStart
        self.run_event('onStart', [])

        # Запускаем подключение к WebSocket
        await self.ws_client.connect()

    async def init_bot_info(self):
        """
        Получаем информацию о боте через HTTP (getInfoUser).
        Сохраняем в self.bot_info и self.bot_id.
        """
        res = await self.api_net.api_req('getInfoUser', post_data={})
        if res and res['errorCode'] == 0:
            self.bot_info = res
            self.bot_id = res['id']
        else:
            if self.log_level > 0:
                print("Failed to get bot info. res=", res)

    async def close(self):
        """Остановка работы."""
        self.is_run = False
        await self.ws_client.close()

    # ----------------------------------------------------------------
    #   Методы для работы с паролями
    # ----------------------------------------------------------------
    def load_passwords(self):
        """Загружаем сохранённые пароли чатов из файла."""
        if os.path.isfile(self.save_file_passwords):
            with open(self.save_file_passwords, 'r', encoding='utf-8') as f:
                self.chats_passwords = json.load(f)

    def save_passwords(self):
        """Сохраняем пароли чатов в файл."""
        with open(self.save_file_passwords, 'w', encoding='utf-8') as f:
            json.dump(self.chats_passwords, f)

    def add_chat_password(self, chat_id: int, password: str):
        self.chats_passwords[str(chat_id)] = password

    # ----------------------------------------------------------------
    #   Асинхронные обёртки для API методов
    # ----------------------------------------------------------------
    async def request_password(self, chat_id: int):
        """
        Запросить у сервера зашифрованный пароль для данного чата.
        Генерируем пару RSA, отправляем publicKey,
        сервер пришлёт действие type=2 (password).
        """
        key, encryptor, public_key = self.encryption.generate_rsa_key()
        post_data = {'chatId':chat_id,'publicKey': public_key}
        out = await self.ws_client.api_req("requestPassword", post_data)
        if out and out['errorCode'] == 0:
            self.requested_passwords[str(chat_id)] = encryptor
            return True
        return False

    async def join_chat_by_invite_id(self, invite_id: int):
        return await self.ws_client.api_req('joinChatByInviteId', {"inviteId":invite_id})

    async def set_menu(self, chat_id: int, menu: list):
        return await self.ws_client.api_req('setMenu',
                                      post_data={'menu': json.dumps(menu),'chatId':chat_id})

    async def send_message(self,
                           chat_id: int,
                           message: str,
                           encrypt_id: str=None,
                           attachments: list=[],
                           answer_msg: int=-1,
                           comment_msg: int=-1,
                           sound_msg: str='-1',
                           buttons: list=None,
                           plugins=None
                           ):
        """
        Асинхронно отправляем сообщение в чат, шифруем, если есть пароль.
        """
        chat_id_s = str(chat_id)
        if chat_id_s in self.chats_passwords:
            if not encrypt_id:
                # формируем encrypt_id
                encrypt_id = self.encryption.str2hash(
                    f"{time.time_ns()}:{chat_id}:{self.chats.get(chat_id_s, chat_id_s)}",
                    16, 16
                )
            # шифруем тело
            password = self.chats_passwords[chat_id_s] + encrypt_id
            message = self.encryption.encrypt_hex(message.encode('utf-8'), password, 10)
        else:
            if not encrypt_id:
                encrypt_id = ""

        post_data = {
            'message': message,
            'attachments': json.dumps(attachments),
            'encryptId': encrypt_id,
            'soundMsg':sound_msg,
            'chatId':chat_id
        }
        if buttons is not None:
            post_data['buttons'] = json.dumps(buttons)
        if plugins is not None:
            post_data['plugins'] = json.dumps(plugins)

        if(answer_msg!=-1):
            post_data['answerMsg']=answer_msg
        if(comment_msg!=-1):
            post_data['commentMsg']=comment_msg
        return await self.ws_client.api_req("sendMessage", post_data)

    async def delete_message(self, chat_id: int, msg_id: int):
        return await self.ws_client.api_req('deleteMessage',{'chatId':chat_id,'msgId':msg_id})

    async def edit_message(self, chat_id: int, msg_id: int, message: str,
                           encrypt_id: str=None, attachments: list=[]):
        chat_id_s = str(chat_id)
        if chat_id_s in self.chats_passwords:
            if not encrypt_id:
                encrypt_id = self.encryption.str2hash(
                    f"{time.time_ns()}:{chat_id}:{self.chats.get(chat_id_s, chat_id_s)}",
                    16, 16
                )
            password = self.chats_passwords[chat_id_s] + encrypt_id
            message = self.encryption.encrypt_hex(message.encode('utf-8'), password, 10)
        else:
            if not encrypt_id:
                encrypt_id = ""

        post_data = {
            'message': message,
            'attachments': json.dumps(attachments),
            'encryptId': encrypt_id,
            'chatId':chat_id,
            'msgId':msg_id
        }
        return await self.ws_client.api_req('editMessage',
                                      post_data=post_data)

    async def get_message(self, chat_id: int, msg_id: int):
        out = await self.ws_client.api_req('getMessage',{'chatId':chat_id,'msgId':msg_id})
        if out and out['errorCode'] == 0:
            msg = out['msg']
            chat_id_s = str(msg['fromChat'])
            if chat_id_s in self.chats_passwords:
                password = self.chats_passwords[chat_id_s] + msg['encryptId']
                msg['message'] = self.encryption.decrypt_hex(msg['message'], password, 10)
                if msg['answerMsg'] != '-1':
                    msg['answerMsgText'] = self.encryption.decrypt_hex(
                        msg['answerMsgText'],
                        self.chats_passwords[chat_id_s] + msg['answerMsgEncryptId'],
                        10
                    )
            return msg
        return None

    async def send_bot_message(self, to_id: int, data: str):
        return await self.ws_client.api_req('sendBotMessage', {'data': data,'toId':to_id})

    # ----------------------------------------------------------------
    #   Обработка событий от WebSockets
    # ----------------------------------------------------------------
    async def handle_ws_event(self, data: dict):
        """
        Получаем сырые данные из WebSocket (HalChatWS).
        Анализируем rtype, type, вызываем соответствующие события
        и/или декодируем сообщения.
        """
        rtype = data.get("rtype")
        if rtype == "msg":
            # Новое сообщение
            msg = data
            if(msg['fromId']!=self.bot_id):
                chat_id = str(msg['fromChat'])
                if chat_id in self.chats_passwords:
                    password = self.chats_passwords[chat_id] + msg['encryptId']
                    msg['message'] = self.encryption.decrypt_hex(msg['message'], password, 10)
                    if msg['answerMsg'] != '-1':
                        msg['answerMsgText'] = self.encryption.decrypt_hex(
                            msg['answerMsgText'],
                            self.chats_passwords[chat_id] + msg['answerMsgEncryptId'],
                            10
                        )
                # Вызываем onNewMessage
                self.run_event("onNewMessage", [msg, chat_id in self.chats_passwords])

        elif rtype == "act":
            v = data
            act_type = v['type']
            # 0 - deleteMsg, 1 - editMsg, 2 - password, 3 - newChat, 6 - clickButton
            if act_type == 0:
                self.run_event('onDeleteMessage', [v['fromChat'], v['fromId'], v['fromMsg']])
            elif act_type == 1:
                self.run_event('onEditMessage', [v['fromChat'], v['fromId'], v['fromMsg']])
            elif act_type == 2:
                # Это пришёл зашифрованный пароль, нужно расшифровать через RSA
                c_id_s = str(v['fromChat'])
                if c_id_s in self.requested_passwords:
                    try:
                        decryptor = self.requested_passwords[c_id_s]
                        decrypted_password = decryptor.decrypt(base64.b64decode(v['data'])).decode('utf-8')
                        # Сохраняем пароль
                        self.add_chat_password(v['fromChat'], decrypted_password)
                        self.save_passwords()
                        v['data'] = decrypted_password
                        del self.requested_passwords[c_id_s]
                    except Exception as e:
                        if self.log_level > 0:
                            print(f"Error decrypting password: {e}")

                self.run_event('onReceivePassword', [v['fromChat'], v['fromId'], v['data']])

            elif act_type == 3:
                # Новый чат
                # v['uid'] - inviteId
                # if v['toId'] == self.bot_id: ...
                if self.auto_join_chats:
                    await self.join_chat_by_invite_id(v['uid'])
                self.run_event('onNewChat', [v['fromChat'], v['fromId'], v['uid']])

            elif act_type == 6:
                # Клик по кнопке
                self.run_event('onClickButton', [v['fromChat'], v['fromId'], v['fromMsg'], v['data']])

        elif rtype == "botmsg":
            # Сообщение для бота
            if self.check_bots_messages:
                self.run_event('onBotMessage', [data['fromId'], data['time'], data['data']])

        # rtype == "pong" обрабатывается внутри ws_client.listen()

    # ----------------------------------------------------------------
    #   Утилиты логгирования
    # ----------------------------------------------------------------
    def print_debug(self, s: str):
        if self.log_level > 1:
            print("D:", s)

    def print_error(self, s: str):
        if self.log_level > 0:
            print("E:", s)