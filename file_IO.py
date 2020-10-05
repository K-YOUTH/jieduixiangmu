import os
'''
实现的功能：
进行文件I/O操作，做出以下判断：
1、判断文件是否存在
2、判断文件是否可写

auther:white0PS
date: 2020/10/5

file_path1/2参数：传入的是文件路径（字符串类型）

file_path1是题目的存入文件
因此得保证，file_path1是空文件，非空文件就return0

file_path2是答案的存放目录（由用户提交）（答案的审查由锐楷大哥完成）
因此对于file_path2中的文件应当有跟题目一样的行数？行数这里不做审查，交给main脚本进行

这个脚本仅作文件合法性的审查

返回值：
    文件存在，可用：返回数值1；
    文件不可写：返回数值2
    文件不存在：返回数值3
    文件里头存在内容：返回数值4
'''

def check(file_path1,file_path2):
    if os.path.exists(file_path1) and os.path.exists(file_path2):# 判断文件是否存在
        if os.access(file_path1,os.R_OK) and os.access(file_path2,os.R_OK): # 判断文件是否可写
            f = open(file_path1, encoding='utf-8')
            txt = f.read()
            if txt:  # 如果文件中存在内容，将不往其中写入内容。
                return 4  # 相应的print输出提示信息，交给楷哥解决，这里只返回对应的代码。
            else:
                return 1
        else:
            return 2
    else:
        return 3

if __name__=='__main__':
    print(check('abc.txt','output.txt'))

'''
已经经过测试无误。
'''

