import base64
from nonebot import Bot, on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Message
import json
import requests
import aiohttp
import asyncio
import base64

hitokoto1 = on_command('一言',priority=5)
@hitokoto1.handle()
async def hitokoto_(bot: Bot, args: Message = CommandArg()):
    url = 'https://v1.hitokoto.cn/'
    r = requests.get(url)
    data = json.loads(r.text)
    hitokoto_ = data.get('hitokoto')
    from_ = data.get('from')
    from_who = data.get('from_who')
    message_=hitokoto_+'\nFrom:'+str(from_)+'('+str(from_who)+')'
    await hitokoto1.send(message_)
caihongpi = on_command('舔我',priority=5)
@caihongpi.handle()
async def caihongpi_(bot: Bot, args: Message = CommandArg()):
    shadiao = await get_shadiao()
    await caihongpi.send(shadiao)

day60 = on_command('60s',priority=5)
@day60.handle()
async def day60_(bot: Bot, args: Message = CommandArg()):
    url = 'https://api.vvhan.com/api/60s'
    await day60.send('正在获取，请稍等...')
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            text = await resp.content.read()
            #text转为base64
            picbase = base64.b64encode(text).decode()
            await day60.finish(Message(f"[CQ:image,file=base64://{picbase}]"))

async def get_shadiao():
    url = 'https://api.shadiao.app/chp'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            text = await resp.text()
            #json
            data = json.loads(text)
            return data['data']['text']

