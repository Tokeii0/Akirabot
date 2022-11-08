from nonebot import Bot, on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
#from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Message
import os
import asyncio
import base64,json
import requests

acg = on_command('acg',aliases={'二次元', '来点二次元', '动漫图片'},priority=5)
async def getacg():
    url = 'https://dev.iw233.cn/api.php?sort=iw233&type=json'
    r = requests.get(url)
    data = json.loads(r.text)
    imgurl = data.get('pic')[0]
    r = requests.get(imgurl,timeout=200)
    img = base64.b64encode(r.content).decode()
    return img
@acg.handle()
async def acg_(bot: Bot, args: Message = CommandArg()):
    a= await getacg()
    if a:
        try:
            await acg.finish(Message(f"[CQ:image,file=base64://{a}]"))
        except Exception as e:
            pass
