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

zsteg = on_command('zsteg',priority=5, block=False)
@zsteg.handle()
async def _(bot: Bot,event: MessageEvent,args: Message=CommandArg()):
    msg = args.extract_plain_text()
    if msg:
        try:
            await zsteg.send('[+] 正在进行zeteg,请稍等...')
            textresult,fileresult = tkts.Tokeiictftools().zsteg_qq(msg,event.user_id)
            await zsteg.send(f'[+] Text 结果:\n{textresult}')
            await zsteg.finish(f'[+] File 结果:\n{fileresult}')
        except Exception as e:
            print(e)
            #await zsteg.finish(f'[-] 获取zsteg信息失败,错误信息:{e}')
