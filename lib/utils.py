import time


def log(level='DEBUG', pos='', msg='', data=None):
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    out = '{0}|{1}|{2}|msg:{3}'.format(level, now, pos, msg)
    if data:
        out += '|data:' + data.__str__()
    print(out)
