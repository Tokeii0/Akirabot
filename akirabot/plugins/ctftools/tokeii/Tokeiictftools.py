import binascii
import struct
import requests
import os
import pyzbar.pyzbar as pyzbar
import random,base64
import cv2
import zxing
from PIL import Image
from io import BytesIO
import numpy,time
import asyncio,subprocess
import base64,base58,base45,libnum,hashlib
import base91



class Tokeiictftools:
    def decode_qr_cv2(self,imgurl,userid):#解码二维码
        request = requests.get(imgurl)
        romdomname = f'{userid}_{int(time.time())}.png'
        userpath = f'./userfile/{userid}/'
        if not os.path.exists(userpath):
            os.makedirs(userpath)
        with open(f'{userpath}/{romdomname}','wb') as f:
            f.write(request.content)
            f.close()
        image = cv2.imread(f'{userpath}/{romdomname}')
        barcode = pyzbar.decode(image)
        reader1 = zxing.BarCodeReader()
        barcode1 = reader1.decode(f'{userpath}/{romdomname}')
        try:
            os.remove(f'{userpath}/{romdomname}')
        except Exception as e:
            pass
        if barcode1.format!=None:
            return f'[+] 检测到{barcode1.format}码,已自动帮您解码\n[+] {barcode1.raw}\ndecode by zxing'
        if barcode:
            os.remove(f'{userpath}/{romdomname}')
            qrtype =barcode[0].type
            return f'[+] 检测到{qrtype}码,已自动帮您解码\n[+] {barcode[0].data.decode()}\ndecode by pyzbar'    
    def bwm_bot_py3(self,img1path,img2path,userid):#盲水印py3
        userpath = f'./userfile/{userid}/'
        img1path = f'{userpath}/{img1path}'
        img2path = f'{userpath}/{img2path}'
        cmd = f'python3 ./akirabot/plugins/ctftools/tokeii/bwmforpy3.py decode {img1path} {img2path} {userpath}output1.png --oldseed'
        print(cmd)
        subprocess.Popen(cmd,shell=False)
        time.sleep(1)
        #获取完整路径
        imgpath = os.path.abspath(f'{userpath}output1.png')
        print(imgpath)
        return imgpath
    def downloadfile(self,filename,url,userid):#下载文件    
        request = requests.get(url)
        userpath = f'./userfile/{userid}/'
        if not os.path.exists(userpath):
            os.makedirs(userpath)
        if os.path.exists(f'{userpath}/{filename}'):
            filename = f'{random.randint(1,100)}_{filename}'
        with open(f'{userpath}/{filename}','wb') as f:
            f.write(request.content)
            f.close()
    def usergetfile(self,userid):#查看用户文件列表
        userpath = f'./userfile/{userid}/'
        #如果userpath文件夹为空
        if not os.listdir(userpath):
            return '当前文件夹为空'
        #换行打印
        for root,dirs,files in os.walk(userpath):
            return '\n'.join(files)
    def getoriginimg(self,imgpath,userid): #fixpng
        userpath = f'./userfile/{userid}/'
        imgpath= f'{userpath}/{imgpath}'
        imgpath = os.path.abspath(imgpath)
        print(imgpath)
        if fixpng(imgpath)==True:
            imgpath = os.path.abspath(imgpath.strip('.png')+'_fix.png')
            #print('ok')
            return imgpath
        else:
            print('error')
    def getexif(self,imgpath,userid):
        import subprocess
        userpath = f'./userfile/{userid}/'
        imgpath= f'{userpath}/{imgpath}'
        imgpath = os.path.abspath(imgpath)
        #获取当前文件路径
        currentpath = os.path.abspath('.')
        commandstr = rf'{currentpath}\akirabot\plugins\ctftools\tokeii\exiftool.exe {imgpath}'
        print(commandstr)
        p = subprocess.Popen(commandstr, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result = p.stdout.read() # type: ignore
        str1 = result.decode('utf-8')
        return str1.replace('D:/pythonconda/nonebot2','')
    def zsteg_qq(self,imgpath,userid):
        import subprocess
        getlinuxpwd = subprocess.Popen('wsl.exe -d kali-linux pwd',shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        #等待执行完成
        getlinuxpwd.wait()
        linuxpwd = getlinuxpwd.stdout.read().decode('utf-8').strip()
        userpath = f'/userfile/{userid}/'
        imgpath= f'{userpath}{imgpath}'
        imgpathlinux = linuxpwd+imgpath.replace('D:/pythonconda/nonebot2','')
        print(imgpathlinux)
        a=subprocess.Popen(f"wsl.exe -d kali-linux zsteg {imgpathlinux}",shell=True,stdout=subprocess.PIPE,universal_newlines=True)
        a.wait()
        result = a.stdout.read().split('\n')
        textresult = []
        fileresult = []
        for i in result:    
            if 'text' in i:
                textresult.append(i)
            if 'file' in i:
                fileresult.append(i)
        textresult = '\n'.join(textresult)
        fileresult = '\n'.join(fileresult)
        print(textresult,fileresult)
        return textresult,fileresult
    def deluserfile(self,userid):
        userpath = f'./userfile/{userid}/'
        #删除userpath目录下所有文件
        for root,dirs,files in os.walk(userpath):
            for file in files:
                os.remove(f'{userpath}/{file}')
        return '已清空文件'
        


class Allbasetry:
    def base64decode(self,base64str):
        return base64.b64decode(base64str)
    def base32decode(self,base32str):
        return base64.b32decode(base32str)
    def base16decode(self,base16str):
        return base64.b16decode(base16str)
    def base85decode_a(self,base85str):
        return base64.a85decode(base85str)
    def base85decode_b(self,base85str):
        return base64.b85decode(base85str)
    def base58decode(self,base58str):
        return base58.b58decode(base58str)
    def base45decode(self,base45str):
        return base45.b45decode(base45str)
    def base91decode(self,base91str):
        return base91.decode(base91str)
    def tryallbase(self,basestr):#尝试所有base
        a = Allbasetry()
        for i in dir(a):
            if i.startswith('base'):
                print(i)
                try:
                    return (i+':',(eval(f'a.{i}("{basestr}")')).decode())
                except:
                    pass

def fixpng(filepath):#修复png脚本
    fr = open(filepath,'rb').read()
    data: bytearray = bytearray(fr[0x0c:0x1d])
    crc32key = eval('0x'+str(binascii.b2a_hex(fr[0x1d:0x21]))[2:-1])
    #原来的代码: crc32key = eval(str(fr[29:33]).replace('\\x','').replace("1b'",'0x').replace("'",''))
    n = 4095
    for w in range(n):
        width = bytearray(struct.pack('>i', w))
        for h in range(n):
            height = bytearray(struct.pack('>i', h))
            for x in range(4):
                data[x+4] = width[x]
                data[x+8] = height[x]
            crc32result = binascii.crc32(data) & 0xffffffff
            if crc32result == crc32key:
                #print(width,height)
                newpic = bytearray(fr)
                for x in range(4):
                    newpic[x+16] = width[x]
                    newpic[x+20] = height[x]
                fw = open(filepath.strip('.png')+'_fix.png','wb')
                fw.write(newpic)
                fw.close()
                return True                
