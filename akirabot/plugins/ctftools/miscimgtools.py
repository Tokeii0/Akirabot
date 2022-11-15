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
            imgid = await fixpng.send(Message(f'[CQ:image,file=file:///{filename}]'))
            # imgid = imgid['message_id']
            # print(imgid)
            # print(await bot.call_api("get_msg",message_id=imgid))
            #ocr
            #print(await bot.call_api('ocr_image',image=filename))
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
picocr = on_command('picocr',aliases={'ocr'}, priority=5)
#checkyml = yaml.safe_load(open('pluginconfig.yml','r+',encoding='utf-8'))['picocr']['status']
@picocr.handle()
async def handle_first_receive(event: MessageEvent, state: T_State, picocr: Message = CommandArg()):
    if picocr:
        state['picocr'] = picocr
@picocr.got("picocr",prompt="快发图")
async def get_picocr(bot: Bot,event: MessageEvent,msg: Message = Arg("picocr")):
    try:
        if msg[0].type == "image":
            imageid = str(msg[0]).split(',')[1].split('=')[1]
            ocrres = await bot.call_api('ocr_image', image=imageid)
            #print(ocrres)
            result = ''
            if len(ocrres['texts'])>5:
                await picocr.finish(f'[-] 过长,请分段识别')
            for i in range(len(ocrres['texts'])):
                confidence=str(ocrres['texts'][i]['confidence'])
                text = str(ocrres['texts'][i]['text'])
                result +=  text+'('+confidence+'%)\n'
            if 'flag' in result :
                if '[' in result or ']' in result or  '(' in result or ')' in result:
                    resultnew = result.replace('[','{').replace(']','}')
                    resultnew = resultnew.replace('(','{').replace(')','}')
                    await picocr.send(Message('[+] 图片识别内容为:\n'+result+'[+] 智能修改后为:\n'+resultnew.replace(confidence+'%','更正后')))
            else:
                await picocr.send(Message('[+] 图片识别内容为:\n'+result))    
                    
            
            #('图片识别内容为'+ocrres['texts'][0]['text'],'准确率为'+str(ocrres['texts'][0]['confidence'])+'%')
            await picocr.finish()
    except Exception as e:
        print(e)
        return

#Cloacked-pixel
cloackedpixel = on_command('cloackedpixel',aliases={'加密lsb'},priority=1, block=False)
@cloackedpixel.handle()
async def _(bot: Bot,event: MessageEvent,args: Message=CommandArg()):
    msg = args.extract_plain_text()
    if msg:
        filepath = msg.split(' ')[0]
        try:
            passwd = msg.split(' ')[1]
        except:
            await cloackedpixel.send('[*] 未输入密码，将自动填充 123456')
            passwd = 123456
        try:
            userid = event.user_id
            await cloackedpixel.send('[+] 尝试检测Cloacked-pixel隐写,请稍等...')
            data = tkts.Tokeiictftools().cryptolsb(filepath,passwd,userid)
            await cloackedpixel.finish(f'{data}')
        except Exception as e:
            print(e)
            #await cloackedpixel.finish(f'[-] 解码失败,错误信息:{e}')
#draw01str
draw01 = on_command('draw01',aliases={'01画图'}, priority=5)
@draw01.handle()
async def _(bot: Bot,event: MessageEvent,args: Message=CommandArg()):
    import math
    msg = args.extract_plain_text()
    userid = event.user_id
    if len(msg.split(' '))==4:
        str01num = msg.split(' ')[0]
        str01a = int(msg.split(' ')[1])
        str01b = int(msg.split(' ')[2])
        str01x = msg.split(' ')[3]
        print(str01num,str01a,str01b,str01x)
        picpath = tkts.Tokeiictftools().draw01(str01num,str01a,str01b,str01x,userid)
        await draw01.finish(Message(f'[CQ:image,file=file:///{picpath}]'))
    else:
        userpath = f'./userfile/{userid}/'
        if 'txt' in msg:
            str01num = open(f'{userpath}{msg}','r').read()
        else :
            str01num = msg
        strlen = len(str01num)
        if int(strlen**0.5)-strlen**0.5==0:
            await draw01.finish('[+] 推荐a,b值为：'+str(int(math.sqrt(strlen)))+"\n[+] 请在后面继续添加参数a b x (x可选值为01,用于颜色取反)")
        else:
            await draw01.finish('[+] 请在后面继续添加参数a b x (x可选值为01,用于颜色取反)"')
