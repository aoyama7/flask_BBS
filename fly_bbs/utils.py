import random
from flask import session

# 生成验证码


def gen_verify_num():
    a = random.randint(-25, 25)
    b = random.randint(0, 20)
    data = {'question': str(a) + '+' + str(b) + " = ?", 'answer': str(a + b)}
    # 答案保存到session中
    # 这里使用redis中更好啊！
    session['ver_code'] = data['answer']
    return data

# 验证码校验


def verify_num(code):
    if code != session['var_code']:
        raise Exception('验证码错误')
