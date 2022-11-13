import random

import requests
import json
import os

# 题目类型
type_dict = {'1': 'type=1&diff=', '2': 'type=2&diff=', '3': 'type=3&diff=', '4': 'type=4&diff=',
             '5': 'type=5&diff=',
             '6': 'type=6&diff=', '7': 'type=7&diff=', '8': 'type=8&diff=', '9': 'type=9&diff=',
             '10': 'type=10&diff=', '11': 'type=11&diff=', '12': 'type=12&diff='}
# 题目难度
diff_dict = {'0': 'easy', '1': 'medium', '2': 'hard', '3': 'epic'}

type_name = {
    0: 'Misc',
    1: 'Reverse',
    2: 'Crypto',
    3: 'Pwn',
    4: 'Web',
    5: 'N1Book',
    6: 'SQLi-Labs',
    7: 'Upload-Labs',
    8: '待解出',
    9: 'DVWA',
    10: 'XSS',
    11: 'CVE',
}


# 登录信息保存
def save_login_information(data, uin):
    with open(f'All_Data/Login/{uin}.txt', 'w') as f:
        f.write(data)


# 读取登录信息
def get_information(uin):
    with open(f'All_Data/Login/{uin}.txt', 'r') as f:
        data = json.loads(f.read())
    return data.get('access'), data.get('refresh')


# 用户基本设置
def user_configuration(uin):
    if not os.path.exists(f'All_Data/User/{uin}.txt'):
        with open(f'All_Data/User/{uin}.txt', 'w') as f:
            data = {'diff': '0', 'id': None, 'type': '1', 'p': '1'}
            f.write(json.dumps(data))
    else:
        with open(f'All_Data/User/{uin}.txt', 'r+') as f:
            t = f.read()
            if not t:
                data = {'diff': '0', 'id': None, 'type': '1', 'p': '1'}
                f.write(json.dumps(data))


# 更新
def update_configuration(data, uin):
    if os.path.exists(f'All_Data/User/{uin}.txt'):
        with open(f'All_Data/User/{uin}.txt', 'w') as f:
            f.write(json.dumps(data))


# 读取用户基本配置
def read_configuration(uin):
    if os.path.exists(f'All_Data/User/{uin}.txt'):
        with open(f'All_Data/User/{uin}.txt', 'r') as f:
            data = json.loads(f.read())
        return data


# 保存账号密码
def save_user(user, password, uin):

    with open(f'All_Data/Account/{uin}.txt', 'w') as f:
        data = {"user": user, "password": password}
        f.write(json.dumps(data))


# 读取账号密码
def read_user(uin):
    if os.path.exists(f'All_Data/Account/{uin}.txt'):
        with open(f'All_Data/Account/{uin}.txt', 'r') as f:
            data = json.loads(f.read())
            return data.get('user'), data.get('password')
    else:
        return None


# 登录
def login(uin):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/103.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Origin': 'https://ce.pwnthebox.com',
        'Referer': 'https://ce.pwnthebox.com/login',
        'Content-Type': 'application/json',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
    }
    user = read_user(uin)
    if user:
        data = {
            "email": f"{user[0]}",
            "password": f"{user[1]}"
        }
        html = requests.post(url='https://ce.pwnthebox.com/api/user/login', data=json.dumps(data), headers=headers)
        result = html.text
        print(result)
        if 'access' in result:
            save_login_information(result, uin)
            user_configuration(uin)
            return '登录成功！'
        else:
            return json.loads(result).get('msg')
    else:
        return '请绑定正确的账号密码！'


def get_referer(uin):
    config = read_configuration(uin)
    if config:
        id = config.get('id')
        n = config.get('diff')
        t = config.get('type')
        p = config.get('p')
        diff = diff_dict.get(n)
        referer = f'https://ce.pwnthebox.com/challenges?type={t}&page={p}&diff={diff}&id={id}'
        return referer


# 获取题目id
def id_list(uin):
    url = 'https://ce.pwnthebox.com/api/challenge/list_v2'
    config = read_configuration(uin)
    n = config.get('diff')
    t = config.get('type')
    p = config.get('p')
    diff = diff_dict.get(n)
    data = {"diff": n, "page": p, "category": [t]}
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'referer': f'https://ce.pwnthebox.com/challenges?type={t}&page={p}&diff={diff}',
        'authorization': f'Bearer {get_information(uin)[0]}'
    }
    r = requests.post(url, data=data, headers=headers)
    result = json.loads(r.content.decode())
    if result.get('code') == 'token_not_valid':
        login(uin)
        return id_list(uin)
    else:
        data = result.get('list')
        print(data)
        data1 = [f"ID:{y.get('id')} 标题:{y.get('title')} 类型: {type_name.get(int(t)-1)} 难度:{y.get('diff')}" for y in data]
        return '\n'.join(random.sample(data1, 10))





# 开启靶机
def start(bj_id, uin):
    url = 'https://ce.pwnthebox.com/api/container/start'
    data = {"container_id": bj_id}
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'referer': get_referer(uin),
        'authorization': f'Bearer {get_information(uin)[0]}'
    }
    r = requests.post(url, data=data, headers=headers)
    result = json.loads(r.content.decode())
    return result


# post访问
def post(url, data, headers):
    r = requests.post(url, data=data, headers=headers)
    result = json.loads(r.content.decode())
    return result


# 获取题目
def get_questions(id, uin):
    config = read_configuration(uin)
    config['id'] = id
    update_configuration(config, uin)
    url = 'https://ce.pwnthebox.com/api/challenge/get'
    data = {"challenge_id": id}
    login(uin)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'authorization': f'Bearer {get_information(uin)[0]}'
    }
    result = post(url, data, headers)
    bj_url = '没有靶机'
    if result.get('containers'):
        bj_id = result.get('containers')[0].get('id')
        if bj_id:
            start(bj_id, uin)
            result = post(url, data, headers)
            if result.get('container_info'):
                bj_url = result.get('container_info')[0].get('url')
                uuid = result.get('container_info')[0].get('uuid')
                if uuid:
                    bj_url = bj_url.replace('{}', uuid)
    content = {'title': result.get('title'), 'desc': result.get('desc') if result.get('desc') else '没有介绍',
               'files': f"https://ce.pwnthebox.com/uploads/{result.get('files')[0].get('file')}" if result.get(
                   'files') else '没有文件', 'url': bj_url}
    text = f"标题: {content.get('title')}\n介绍: {content.get('desc')}\n文件: {content.get('files')}\n靶机: {content.get('url')}"
    return text,content.get('files')


# 提交
def submit(uin, flag):
    id = read_configuration(uin).get('id')
    url = 'https://ce.pwnthebox.com/api/challenge/apply'
    data = {"challenge_id": id, "flag": flag}
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'referer': get_referer(uin),
        'authorization': f'Bearer {get_information(uin)[0]}'
    }
    r = requests.post(url, data=data, headers=headers)
    result = json.loads(r.content.decode())
    if result.get('code') == 200:
        return True
    elif result.get('code') == 400:
        return False
    elif result.get('code') == 'token_not_valid':
        login(uin)
        return submit(uin, flag)
    else:
        return result

