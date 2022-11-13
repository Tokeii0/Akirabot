import random
from nonebot import on_notice,on_command,on_message
from nonebot.adapters.onebot.v11 import Bot,MessageEvent,NoticeEvent,PrivateMessageEvent
from nonebot.adapters.onebot.v11 import Message
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.params import CommandStart,EventType,EventMessage,CommandArg,Arg
from nonebot.typing import T_State
import re,time,os
import akirabot.plugins.ctftools.pwntheboxbot.random_topic as ptb
import akirabot.plugins.ctftools.tokeii.Tokeiictftools as tkts

# QQ绑定ptb账号
ptblinkqq = on_command('ptb绑定',priority=1, block=False)
@ptblinkqq.handle()
async def _(bot: Bot,event: PrivateMessageEvent,args: Message=CommandArg()):
    msg = args.extract_plain_text()
    if msg:
        ptbusername,ptbpasswd = msg.split(' ')[0],msg.split(' ')[1] 
        userid = event.user_id
        try:
            loginstr = await ptblogin(ptbusername,ptbpasswd,userid)
            await ptblinkqq.send('[+] 正在绑定,请稍等...')
            if '成功' in loginstr:
                await ptblinkqq.finish(f'[+] 绑定成功,您的ptb账号为:{ptbusername}')
            else:
                await ptblinkqq.finish(f'[-] 绑定失败:{loginstr}')
        except Exception as e:
            pass

# 修改题目难度
ptbsetdiff = on_command('ptb难度',priority=1, block=False)
@ptbsetdiff.handle()
async def _(bot: Bot,event: PrivateMessageEvent,args: Message=CommandArg()):
    if event.user_id not in ptb.read_user(event.user_id):
        await ptbsetdiff.finish('[-] 请先绑定ptb账号,命令格式:ptb绑定 ptb账号 ptb密码')


# 获取题目列表
ptbgettopic = on_command('获取题目列表',priority=1, block=False)
@ptbgettopic.handle()
async def _(bot: Bot,event: MessageEvent,args: Message=CommandArg()):
    userid = event.user_id
    if '成功' in ptb.login(userid) :
        await ptbgettopic.send('[+] 正在获取题目,请稍等...')
        try:
            topic = ptb.id_list(userid)
            await ptbgettopic.finish(f'[+] 题目列表:\n{topic}')
        except Exception as e:
            await ptbgettopic.finish(f'[-] 获取题目失败,错误信息:{e}')

# 获取题目
ptbgetquestion = on_command('获取题目',priority=1, block=False)
@ptbgetquestion.handle()
async def _(bot: Bot,event: MessageEvent,args: Message=CommandArg()):
    msg = args.extract_plain_text()
    userid = event.user_id
    if '成功' in ptb.login(userid) :
        await ptbgetquestion.send('[+] 正在获取题目,请稍等...')
        try:
            result = ptb.get_questions(msg,userid)
            topic = result[0]
            #获取当前目录
            
            await ptbgetquestion.send(f'[+] 题目内容:\n{topic}')
            try:
                fileurl = result[1]
                filename = fileurl.split('/')[-1]
                path = os.getcwd()
                filepath = path + rf'\userfile\{userid}\\' + filename
                print(filepath)
                tkts.Tokeiictftools().downloadfile(filename,fileurl,userid)
                await bot.call_api("upload_private_file",user_id=event.user_id, file=filepath,name=filename)
                await ptbgetquestion.finish(f'[+] 题目附件已发送,并以下载至用户目录,使用#解压文件 {filename} 解压进行后续操作')
            except Exception as e:
                pass

            
        except Exception as e:
            pass
            #await ptbgetquestion.finish(f'[-] 获取题目失败,错误信息:{e}')


async def ptblogin(ptbusername,ptbpasswd,userid):
    ptb.save_user(ptbusername,ptbpasswd,userid)
    return ptb.login(userid)

# async def getquestiondownloadurl(msg,userid):
#     import requests
#     #下载文件
#     topic,fileurl = ptb.get_questions(msg,userid)
#     if 'zip' in fileurl:
#         r = requests.get(fileurl)
#         with open(f'./{msg}.zip','wb') as f:
#             f.write(r.content)
#         return True


