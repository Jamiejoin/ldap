#encoding=utf-8

import re

def checklen(pwd):
    return len(pwd)>=8

def checkContainUpper(pwd):
    pattern = re.compile('[A-Z]+')
    match = pattern.findall(pwd)

    if match:
        return True
    else:
        return False

def checkContainNum(pwd):
    pattern = re.compile('[0-9]+')
    match = pattern.findall(pwd)
    if match:
        return True
    else:
        return False

def checkContainLower(pwd):
    pattern = re.compile('[a-z]+')
    match = pattern.findall(pwd)

    if match:
        return True
    else:
       return False

def checkSymbol(pwd):
    pattern = re.compile('([^a-z0-9A-Z])+')
    match = pattern.findall(pwd)

    if match:
        return True
    else:
        return False

def checkPassword(pwd):

    #判断密码长度是否合法
    lenOK=checklen(pwd)

    #判断是否包含大写字母
    #upperOK=checkContainUpper(pwd)

    #判断是否包含小写字母
    lowerOK=checkContainLower(pwd)

    #判断是否包含数字
    numOK=checkContainNum(pwd)

    #判断是否包含符号
    #symbolOK=checkSymbol(pwd)
    if lenOK and lowerOK and numOK:
        return True
    else:
        return False


def main():
    if checkPassword('Helloworld#123'):
        print('检测通过')
    else:
        print('检测未通过')


if __name__ == '__main__':
    main()