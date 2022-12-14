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
            #下载文件
            
            if await downloadfileqq(filename,url,userid)==True:
                
                await noticefile.send(f'[+] 文件接收成功\n如要使用请记录好文件名\n[+] 文件名为:{filename}\n[+] 文件大小为{event.file["size"] / 1024 / 1024:.2f}MB\n[+] 文件类型为{tkts.Tokeiictftools().filetype(filename,userid)}')
                filetypestr = tkts.Tokeiictftools().filetype(filename,userid)
            else:
                await noticefile.finish(f'[-] 文件接收失败')
            if 'PNG' in filetypestr:
                await noticefile.send(f'[+] 检测到图片类型为PNG,可使用命令\n#zsteg {filename}\n#加密lsb {filename}\n#exif {filename}\n#fixpng {filename}')
            elif 'WAVE audio' in filetypestr:
                await noticefile.send(f'[+] 检测到文件类型为WAVE audio,可使用命令\n#steghide {filename}\n#按键音 {filename}')
            elif 'JPEG' in filetypestr:
                await noticefile.send(f'[+] 检测到图片类型为JPEG,可使用命令\n#steghide {filename}\n#exif {filename}\n#jsteg {filename}')
        else:
            await noticefile.finish(f'[-] 文件名只允许含有[0-9a-zA-Z.],请重新发送')


usergetfile = on_command('查看文件',aliases={'文件列表'},priority=1, block=False)
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
            
filetypeqq = on_command('文件类型',priority=1, block=False)
@filetypeqq.handle()
async def _(bot: Bot,event: MessageEvent,args: Message=CommandArg()):
    userid = event.user_id
    if args:
        filename = args.extract_plain_text()
        await filetypeqq.finish(f'[+] 文件类型为:\n{tkts.Tokeiictftools().filetype(filename,userid)}')
sendfileqq = on_command('发送文件',priority=1, block=False)
@sendfileqq.handle()
async def _(bot: Bot,event: MessageEvent,args: Message=CommandArg()):
    userid = event.user_id
    if args:
        filename = args.extract_plain_text()
        filepath = tkts.Tokeiictftools().sendfile(filename,userid)
        await bot.call_api("upload_private_file",user_id=event.user_id,file=filepath,name=filename)

renamefileqq = on_command('重命名文件',priority=1, block=False)
@renamefileqq.handle()
async def _(bot: Bot,event: MessageEvent,args: Message=CommandArg()):
    import re
    userid = event.user_id
    filewhitetype=['txt','jpg','zip','bmp','png']
    if args:
        msg = args.extract_plain_text()
        orgfilename = msg.split(' ')[0]
        newfilename = msg.split(' ')[1]
        #仅可修改为filewhitetype中的文件类型
        if re.match(r'^[0-9a-zA-Z.]+$',newfilename) and newfilename.split('.')[-1] in filewhitetype:
            await renamefileqq.finish(tkts.Tokeiictftools().renamefile(orgfilename,newfilename,userid))
        else:
            await renamefileqq.finish('[-] 文件名只允许含有[0-9a-zA-Z.],且文件类型非法,请重新发送')
readfileqq = on_command('读取文件',priority=1, block=False)
@readfileqq.handle()
async def _(bot: Bot,event: MessageEvent,args: Message=CommandArg()):
    userid = event.user_id
    if args:
        filename = args.extract_plain_text()
        if filename.split('.')[-1] == 'txt':
            filedata = tkts.Tokeiictftools().readfile(filename,userid)
            await readfileqq.finish(f'[+] 文件内容为:\n{filedata}')
        else:
            await readfileqq.finish(f'[-] 仅可读取txt文件')































async def downloadfileqq(filename,url,userid):
    try:
        tkts.Tokeiictftools().downloadfile(filename,url,userid)
        return True
    except:
        pass
    
