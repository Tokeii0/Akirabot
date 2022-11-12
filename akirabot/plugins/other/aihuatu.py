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

aihuatu = on_command('ai画图',aliases={'ai作图','画图','画画'},priority=5)
proxy = 'http://127.0.0.1:1090' #自行设置代理 取消则删除下面的 proxy=proxy
async def getaihuatu(str1):
    
    #str1 = await main(str1.replace(' ',','))
    #str1 = str1+',{{{Flat chest}}}'
    url = f"http://lulu.uedbq.xyz//got_image?token=...&tags={str1}&ntags=extra limbs"#修改token http://lulu.uedbq.xyz/token申请
    async with aiohttp.ClientSession() as session:
        async with session.get(url,proxy=proxy) as resp:
            if resp.status == 200:
                img = await resp.read()
                img = base64.b64encode(img).decode()
                #获取响应头的seed
                seed = resp.headers['seed']
                return img,seed
        
@aihuatu.handle()
async def aihuatubot(bot: Bot,event:MessageEvent,args: Message = CommandArg()):
    #blacklist
    str1 = args.extract_plain_text()
    userid = event.get_user_id()
    #MessageEvent下get群id
    try:
        groupid = event.get_session_id().split('_')[1]
    except:
        groupid = None
    #print(event.get_session_id().split('_')[1])
    blacklist=open(r'akirabot\plugins\other\blacklist.txt','r',encoding='utf-8').read().split(',')
    for i in blacklist:
        if i in str1:
            #禁言
            try:
                await bot.call_api('set_group_ban',group_id=event.get_group_id(),user_id=userid,duration=60)
            except:
                pass
            await aihuatu.finish('不要发这种东西哦~')
    
    str_tras = await main(str1)
    print(str_tras)
    a,seed= await getaihuatu(str_tras)
    if seed :
        try:
            await aihuatu.send(f"Tag:{str1},seed:{seed}"+Message(f"[CQ:image,file=base64://{a}]"))
            # message_id = b['message_id']
            # if '&r18=1'in str1:
            #     await asyncio.sleep(50)
            #     await bot.call_api('delete_msg',message_id=message_id)
            await aihuatu.finish()
        except:
            #await aihuatu.send('接口出错了,正在尝试备用接口')
            pass
    await aihuatu.send('接口出错了,正在尝试备用接口')

aiimg2img = on_command('aichange',aliases={'ai图片转换','imgtoimg'},priority=5)
async def aiimg2imgmain(picurl,str1):
    # str1 = await main(str1.replace(' ',','))
    print(str1)
    url = f"http://lulu.uedbq.xyz/got_image2image?token=...&tags={str1}"#修改token http://lulu.uedbq.xyz/token申请
    post_content = base64.b64encode(requests.get(picurl).content)
    #aiohttp post
    async with aiohttp.ClientSession() as session:
        async with session.post(url,data=post_content,proxy=proxy) as resp:
            if resp.status == 200:
                img = await resp.read()
                img = base64.b64encode(img).decode()
                seed = resp.headers['seed']
                return img,seed
            else:
                return None

@aiimg2img.handle()
async def aiimg2imgbot(bot: Bot,event: MessageEvent,args: Message = CommandArg()):
    if args:
        msglist = args
        str1 = msglist[0].data['text']
        picurl = str(msglist[1].data["url"])
        print(picurl,type(picurl))
        str_fanyi = await main(str1)

        a,seed= await aiimg2imgmain(picurl,str_fanyi)
        if a:
            try:
                b = await aiimg2img.send(f"seed:{seed}"+Message(f"[CQ:image,file=base64://{a}]"))
                message_id = b['message_id']
                # await asyncio.sleep(100)
                # await bot.call_api('delete_msg',message_id=message_id)
                await aiimg2img.finish()
            except Exception as e:
                print(e)
# Set your own appid/appkey.Baidu translate api

def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()
async def main(query):
    appid = '' # fanyi.baidu.com 申请
    appkey = '' # fanyi.baidu.com 申请
    from_lang = 'auto'
    to_lang =  'en'
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
    