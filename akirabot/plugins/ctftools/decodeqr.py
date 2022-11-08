from nonebot import on_notice,on_command,on_message
from nonebot.adapters.onebot.v11 import Bot,MessageEvent
from nonebot.adapters.onebot.v11 import Message
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.params import CommandStart,EventType,EventMessage
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
import akirabot.plugins.ctftools.tokeii.Tokeiictftools as tkts

qrmessage= on_message(priority=1, block=False)
@qrmessage.handle()
async def qrmessage_(bot: Bot,event: MessageEvent,args: Message=EventMessage()):
    msg = args
    try:
        if 'image' in str(msg):
            url = msg[0].data['url']
            userid = event.user_id
            await qrmessage.finish(tkts.Tokeiictftools().decode_qr_cv2(url,userid))
    except:
        pass

        