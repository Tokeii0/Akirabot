from nonebot import on_notice,on_command,on_message
from nonebot.adapters.onebot.v11 import Bot,MessageEvent,NoticeEvent
from nonebot.adapters.onebot.v11 import Message
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.params import CommandStart,EventType,EventMessage,CommandArg,Arg
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
import json,re
import akirabot.plugins.ctftools.tokeii.Tokeiictftools as tkts
noticefile = on_notice()
@noticefile.handle()
async def _(bot: Bot,event: NoticeEvent,state: T_State):
    if event.notice_type == 'offline_file':
        #文件名
        filename,url,userid = event.file['name'],event.file['url'],event.user_id
        if re.match(r'^[0-9a-zA-Z.]+$',filename):
            print(filename,url,userid)
            await noticefile.send(f'[+] 文件接收成功\n如要使用请记录好文件名\n[+] 文件名为:{filename}\n[+] 文件大小为{event.file["size"]}')
            await noticefile.send('''[+] 请使用以下命令进行文件操作
Png,jpg,bmp等文件可使用命令：
[+] #exif filename
Wav,mp3文件可使用命令
[+] #dtmf2num filename (#按键音 filename)
Png,bmp文件可使用命令
[+] #zsteg filename
Jpg文件可使用命令
[+] #jsteg filename
盲水印文件可使用命令
[+] #盲水印 filename1 filename2''')
            await noticefile.finish(tkts.Tokeiictftools().downloadfile(filename,url,userid))
        else:
            await noticefile.finish(f'[-] 文件名只允许含有[0-9a-zA-Z.],请重新发送')


usergetfile = on_command('查看文件',priority=1, block=False)
@usergetfile.handle()
async def _(bot: Bot,event: MessageEvent,args: Message=CommandArg()):
    userid = event.user_id
    await usergetfile.finish(tkts.Tokeiictftools().usergetfile(userid))

deluserfile = on_command('删除文件',priority=1, block=False)
@deluserfile.handle()
async def _(bot: Bot,event: MessageEvent,args: Message=CommandArg()):
    userid = event.user_id
    await deluserfile.finish(tkts.Tokeiictftools().deluserfile(userid))
unzipfile = on_command('解压文件',priority=1, block=False)
@unzipfile.handle()
async def _(bot: Bot,event: MessageEvent,args: Message=CommandArg()):
    import os
    userid = event.user_id
    if args:
        filename = args.extract_plain_text()
        result = tkts.Tokeiictftools().unzipfile(filename,userid)
        if '失败' in result:
            await unzipfile.finish(result)
        else:
            filename = result.split("\\")[-1]
            await unzipfile.send('[+] 解压成功,文件名为:'+result.split("\\")[-1])
            try:
                await unzipfile.send(Message(f'[CQ:image,file=file:///{result}]'))
            except:
                await unzipfile.finish(f'[+] 如果图片无法正常浏览请尝试使用 #fixpng {filename}修复图片')
            