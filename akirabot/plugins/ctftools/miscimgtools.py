import random
from nonebot import on_notice,on_command,on_message
from nonebot.adapters.onebot.v11 import Bot,MessageEvent,NoticeEvent,PrivateMessageEvent
from nonebot.adapters.onebot.v11 import Message
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.params import CommandStart,EventType,EventMessage,CommandArg,Arg
from nonebot.typing import T_State
import re,time
import akirabot.plugins.ctftools.tokeii.Tokeiictftools as tkts

fixpng = on_command('fixpng',priority=1, block=False)
@fixpng.handle()
async def _(bot: Bot,event: MessageEvent,args: Message=CommandArg()):
    msg = args.extract_plain_text()
    if msg:
        try:
            await fixpng.send('[+] 正在修复png文件,请稍等...')
            filename = tkts.Tokeiictftools().getoriginimg(msg,event.user_id)
            #print(filename)
            await bot.call_api("upload_private_file",user_id=event.user_id, file=filename,name="output.png")
        except Exception as e:
            await fixpng.finish(f'[-] 修复失败,错误信息:{e}')
            
getexif = on_command('exif',priority=1, block=False)
@getexif.handle()
async def _(bot: Bot,event: MessageEvent,args: Message=CommandArg()):
    msg = args.extract_plain_text()
    if msg:
        try:
            await getexif.send('[+] 正在获取exif信息,请稍等...')
            exif = tkts.Tokeiictftools().getexif(msg,event.user_id)
            await getexif.finish(f'[+] exif信息:\n{exif}')
        except Exception as e:
            pass


        
jsteg = on_command('jsteg',aliases={'jsteg'},priority=1, block=False)
@jsteg.handle()
async def _(bot: Bot,event: MessageEvent,args: Message=CommandArg()):
    msg = args.extract_plain_text()
    if msg:
        try:
            userid = event.user_id
            await jsteg.send('[+] 尝试Jsteg隐写,请稍等...')
            data = tkts.picstegotest().tryjsteg(msg,userid)
            await jsteg.finish(f'[+] Jsteg隐写结果:\n{data}')
        except Exception as e:
            print(e)
            #await jsteg.finish(f'[-] 解码失败,错误信息:{e}')
