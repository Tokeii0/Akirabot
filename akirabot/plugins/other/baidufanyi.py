import aiohttp
import base64
import asyncio
import requests
import random
import json
from hashlib import md5
from nonebot import Bot, on_command
from nonebot.params import CommandArg,Arg
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Message
from nonebot.adapters.onebot.v11 import Bot,MessageEvent,GroupMessageEvent

def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()
async def main(query,target,origin):
    appid = '...'
    appkey = '...'
    from_lang = origin
    to_lang =  target
    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path
    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    try:
        payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign,'action': '1'}
        r = requests.post(url, params=payload, headers=headers)
        result = json.loads(r.content.decode('utf-8'))
        return result['trans_result'][0]['dst']
    except Exception as e:
        print(e,'error关键词为:'+query)
        return None

fanyicn2eng = on_command('中译英',priority=5)
@fanyicn2eng.handle()
async def fanyicn2eng_(bot: Bot,event: MessageEvent,args: Message = CommandArg()):
    if args:
        msglist = args
        str1 = msglist[0].data['text']
        str_fanyi = await main(str1,'en','zh')
        await fanyicn2eng.finish(str_fanyi)

fanyieng2cn = on_command('英译中',priority=5)
@fanyieng2cn.handle()
async def fanyieng2cn_(bot: Bot,event: MessageEvent,args: Message = CommandArg()):
    if args:
        msglist = args
        str1 = msglist[0].data['text']
        str_fanyi = await main(str1,'zh','en')
        await fanyieng2cn.finish(str_fanyi)
wywtocn = on_command('翻译文言文',priority=5)
@wywtocn.handle()
async def wywtocn_(bot: Bot,event: MessageEvent,args: Message = CommandArg()):
    if args:
        msglist = args
        str1 = msglist[0].data['text']
        str_fanyi = await main(str1,'zh','wyw')
        await wywtocn.finish(str_fanyi)

cntowyw = on_command('翻译成文言文',priority=5)
@cntowyw.handle()
async def cntowyw_(bot: Bot,event: MessageEvent,args: Message = CommandArg()):
    if args:
        msglist = args
        str1 = msglist[0].data['text']
        str_fanyi = await main(str1,'wyw','zh')
        await cntowyw.finish(str_fanyi)

custom_fanyi = on_command('自定义翻译',priority=5)
@custom_fanyi.handle()
async def custom_fanyi_(bot: Bot,event: MessageEvent,args: Message = CommandArg()):
    if args:
        msglist = args
        msglist=str(msglist).split(' ')
        print(msglist)
        str1 = msglist[0]
        target = msglist[1]
        origin = msglist[2]
        print(str1,target,origin)
        str_fanyi = await main(str1,origin,target)
        await custom_fanyi.finish(str_fanyi)
custom_help = on_command('自定义翻译帮助',priority=5)
@custom_help.handle()
async def custom_help_(bot: Bot,event: MessageEvent,args: Message = CommandArg()):
    helppicpath = 'akirabot\plugins\other\help.png'
    await custom_help.finish('使用方法：\n#自定义翻译 [要翻译的内容] [原语言代码] [目标语言代码]'+Message(f'[CQ:image,file=file:///{helppicpath}]'))

