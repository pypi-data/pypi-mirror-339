import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from HalChat import HalChat

codeBot="hBfWguy2XqgTbS852z71alaQSWaCyxcOgD7jCLMK1icfWiHpfMEWqidNtgSqppsCV0DoVSuEIb3a0FB3bmB0sUqfa2OjVJpFZcSz"
hca=HalChat(codeBot,log_level=2)

test_buttons=[
    {
        "text":"Кнопка 0",
        "color":"#ffffff"
    },
    {
        "text":"Кнопка 1",
        "color":"#ff0000"
    },
    {
        "text":"Кнопка 2",
        "color":"#00ff00"
    },
    {
        "text":"Кнопка 3",
        "color":"#000000"
    }
]

test_menu=[
    {
        "icon":"DxKGzw4YNCPyMBW5VoIcGEKL6HG22bYoE9V43jiaFyPbGSjfXj64x3SrKxnyhEHAVG0GBhiTH8u3gyrjxgoK96RE6Js12wcAhnmf",
        "command":"тест",
        "description":"Тестовая команда"
    }
]

@hca.event('onNewMessage')
async def on_new_message(msg,isExistPassword):
    if not isExistPassword:
        await hca.request_password(msg['fromChat'])
        return
    chatId=msg['fromChat']

    if(msg['message']=="/тест"):
        await hca.send_message(chatId,"Тест кнопок:",buttons=test_buttons)
        return
    
    await hca.send_message(chatId,"Привет!")
    #await hca.set_menu(chatId,test_menu)

@hca.event('onReceivePassword')
async def on_receive_password(chatId,fromId,password):
    await hca.send_message(chatId,'Бот успешно инициализирован.')
    await hca.set_menu(chatId,test_menu)

@hca.event('onNewChat')
async def on_new_chat(chatId,fromId,inviteId):
    await hca.request_password(chatId)

@hca.event('onClickButton')
async def on_click_button(chatId,fromId,fromMsg,button):
    await hca.send_message(chatId,"Нажата: "+button['text'])

if __name__ == "__main__":
    hca.run()