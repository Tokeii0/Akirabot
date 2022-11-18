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

dtmf2num = on_command('dtmf2num',aliases={'按键音'},priority=1, block=False)
@dtmf2num.handle()
async def _(bot: Bot,event: MessageEvent,args: Message=CommandArg()):
    msg = args.extract_plain_text()
    if msg:
        try:
            userid = event.user_id
            await dtmf2num.send('[+] 正在转换,请稍等...')
            num = tkts.Tokeiictftools().dtmf2num(msg,userid)
            await dtmf2num.finish(f'[+] 转换结果:\n{num}')
        except Exception as e:
            pass
            #await dtmf2num.finish(f'[-] 转换失败,错误信息:{e}')

basecrackqq = on_command('basecrack',aliases={'base全家桶,base'},priority=1, block=False)
@basecrackqq.handle()
async def _(bot: Bot,event: MessageEvent,args: Message=CommandArg()):
    msg = args.extract_plain_text()
    if msg:
        try:
            userid = event.user_id
            await basecrackqq.send('[+] 请稍后...')
            result = await basecrackasync(msg,userid)
            if result[0] != None:
                await basecrackqq.finish(f'[+] 转换结果:\n{result[0]}\n[+] 编码过程:\n{result[1]}')
            else:
                await basecrackqq.finish(f'[-] 无法解码')
        except Exception as e:
            pass
            #await basecrackqq.finish(f'[-] 破解失败,错误信息:{e}')


async def basecrackasync(msg,userid):
    result = tkts.Tokeiictftools().basecrack_qqbot(msg,userid)
    return result
