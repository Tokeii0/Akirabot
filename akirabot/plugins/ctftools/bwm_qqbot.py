import random
from nonebot import on_notice,on_command,on_message
from nonebot.adapters.onebot.v11 import Bot,MessageEvent,NoticeEvent,PrivateMessageEvent
from nonebot.adapters.onebot.v11 import Message
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.params import CommandStart,EventType,EventMessage,CommandArg,Arg
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
import re,time
import akirabot.plugins.ctftools.tokeii.Tokeiictftools as tkts
msglist = ['[-] 瞎搞是吧','[-] 搞破坏是吧','[-] 输入的文件名中有不允许使用的字符','[-] 你不准参加银趴']
bwm_qqbot = on_command('盲水印py3',priority=1, block=False)
@bwm_qqbot.handle()
async def bwm_qqbot_(bot: Bot,event: MessageEvent,args: Message=CommandArg()):
    starttime = time.time()
    msg = args.extract_plain_text()
    #正则匹配[0-9a-zA-Z]和.
    file1 = msg.split(',')[0]
    file2 = msg.split(',')[1]
    if re.match(r'^[0-9a-zA-Z.]+$',file1) and re.match(r'^[0-9a-zA-Z.]+$',file2):
        userid = event.user_id
        filepath = await bwm_py3(file1,file2,userid)
        await bot.call_api("upload_private_file",user_id=event.user_id, file=filepath,name="output.png")
        endtime = time.time()
        await bwm_qqbot.finish(f'[+] 任务已结束,请等待文件发送,共耗时{round(endtime-starttime,2)}秒')
    else:
        await bwm_qqbot.finish(str(msglist[random.randint(0,2)]))
        
    #await bwm_qqbot.finish(tkts.Tokeiictftools().bwm_bot_py3(file1,file2,userid))
    
async def bwm_py3(file1,file2,userid):
    return tkts.Tokeiictftools().bwm_bot_py3(file1,file2,userid)         
    
