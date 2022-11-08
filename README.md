<!-- markdownlint-disable MD033 MD041 -->
<p align="center">
  <a href="https://ctf.mzy0.com"><img src="https://user-images.githubusercontent.com/111427585/198643702-65d427e0-55b0-4f59-9120-a46c2a5f406c.png" width="150" height="150" alt="akebot"></a>
</p>

<div align="center">

# AkeBot

<!-- prettier-ignore-start -->
<!-- markdownlint-disable-next-line MD036 -->
_✨ 协助CTFer的全能辅助机器人 ✨_
<!-- prettier-ignore-end -->
<a href="https://jq.qq.com/?_wv=1027&k=DzOtbzU4"><img src="https://img.shields.io/badge/QQ%E7%BE%A4-555741990-orange?style=flat-square" alt="QQGroup"></a>
  <a href="https://ctf.mzy0.com"><img src="https://img.shields.io/badge/CTF%E5%AF%BC%E8%88%AA%E7%AB%99-ctf.mzy0.com-5492ff?style=flat-square" alt="ctfnav"></a>
  <a href="https://afdian.net/@Tokeii"><img src="https://img.shields.io/badge/爱发电-afdian.net-66ccff?style=flat-square" alt="aifadian"></a>
  <a href=".."><img src="https://img.shields.io/badge/python-3.8+-def1f2?style=flat-square" alt="python"></a>

</div>


## 安装

可以跟着nonebot2官方教程新建一个项目
当然也可以直接clone

官方文档：https://v2.nonebot.dev/docs/start/installation

Go-cqhttp：https://github.com/Mrs4s/go-cqhttp

```bash
  #cmd 或 powershell下命令
  #安装nonebot2,通过脚手架安装
  pip install nb-cli 或 python3 -m pip install nb-cli
  #安装驱动器（安装aiohttp）
  nb driver install aiohttp 或 pip install aiohttp
  #安装协议适配器,我们用的是QQ机器人这里安装第一个OneBot V11
  nb adapter install nonebot-adapter-onebot
  或
  pip install nonebot-adapter-onebot
  #创建项目
  nb create
  #起名为akirabot,最后一个
  #Which adapter(s) would you like to use?
  #如果前面适配器没有安装这里空格就选择后回车安装，没有就Y跳过
```
## 目录结构
```bash

📦 akirabot
├── 📂 akirabot         # 插件存放处
│   └── 📜 plugins
├── 📜 .env                
├── 📜 .env.dev            
├── 📜 .env.prod           
├── 📜 .gitignore
├── 📜 bot.py              # 替换掉
├── 📜 docker-compose.yml
├── 📜 Dockerfile
├── 📜 pyproject.toml
└── 📜 README.md
```
  

  
