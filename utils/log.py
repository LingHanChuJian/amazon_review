import os
import time
import json

file = '%(filename)s.txt'


# 获取文件路径
def get_path():
    cur_time = time.strftime('%Y-%m-%d')
    cur_dir_path = os.path.join(os.path.dirname(__file__), '..', 'log')
    if not os.path.exists(cur_dir_path):
        os.makedirs(cur_dir_path)
    cur_path = os.path.join(cur_dir_path, file % {'filename': cur_time})
    return cur_path


def type_conversion(param):
    try:
        if type(param) == int:
            return str(param)
        elif type(param) == dict:
            return json.dumps(param)
        elif type(param) == tuple or type(param) == list:
            handle_param = '['
            for item in param:
                handle_param += ' ' + type_conversion(item) + ','
            handle_param += ' ]'
            return handle_param
        elif type(param) == str:
            return param
        else:
            return str(type(param))
    except Exception as e:
        print(e)
        return ''


def log(*args):
    print(args)
    with open(get_path(), 'a', encoding='utf-8') as f:
        f.write(time.strftime('%Y-%m-%d %H:%M:%S') + '\n')
        logs = ''
        for item in args:
            logs += type_conversion(item) + ' '
        f.write(logs + '\n')
    f.close()
