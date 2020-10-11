import re, argparse
import random
import check
from fractions import Fraction
import time
import sys
import os

''''
print 语句是为测试用，已注释掉

len_bag_randint = random.randint(2,len(bag))  目的是为了取数，生成1个符号的式子，需要2个数，
生成3个运算符的式子需要4个数

create_expression函数目前只能生成整数式子，没有判断功能：判断式子是否合法——结果负值，除法有0等，只能简单生成式子
'''


def create_expression(erange=10):
    operator = [' + ', ' - ', ' * ', ' / ']  # 符号
    end_operator = ' ='
    equation = ''  # 初始式子，为空
    bag = []  # 为随机数的空列表，随机从里面取字
    nature_step = random.randrange(1, 3)  # 随机数的间隔
    # print(nature_step)
    for i in range(5):
        bag.append(str(random.randrange(1, erange, nature_step)))
    for i in range(5):
        denominator = random.randrange(1, 10)  # 分母
        molecule = random.randrange(1, 10)  # 分子
        denominator, molecule = max(denominator, molecule), min(denominator, molecule)  # 比较大小同时交换
        fraction_number = molecule / denominator
        fraction_number = Fraction('{}'.format(fraction_number)).limit_denominator()  # 小数转换为真分数
        bag.append(str(fraction_number))
        for i in range(4):
            denominator2 = random.randrange(1, 10)  # 分母
            molecule2 = random.randrange(1, 10)  # 分子
            denominator2, molecule2 = max(denominator2, molecule2), min(denominator2, molecule2)  # 比较大小同时交换
            fraction_number2 = denominator2 / molecule2
            fraction_number2 = Fraction('{}'.format(fraction_number2)).limit_denominator()  # 小数转换为真分数
            int_t = int(fraction_number2)
            los_t = fraction_number2 - int_t
            if (int_t != 0 and los_t != 0):
                fi_t = str(str(int_t) + "'" + str(los_t))
            else:
                fi_t = str(fraction_number2)
            bag.append(fi_t)
    len_bag_randint = random.randrange(2, 4)
    # print(len_bag_randint)
    for i in range(len_bag_randint):
        # 随机取bag里的数
        randint_number = random.randint(0, len(bag) - 1)
        equation += bag[randint_number]
        if i < len_bag_randint - 1:
            equation += operator[randint_number % len(operator)]
        # else:
        # equation += end_operator
        bag.pop(randint_number)
    return equation


# 获取答案
def get_answer(question):
    question = re.sub("'"," + ",question)
    t = eval(question)  # eval函数获取表达式的值
    t = Fraction('{}'.format(t)).limit_denominator()  # 小数转换为分数
    # 转化真分数：如67/8写为8'3/8,先将真分数转为整数int_t,原数t减去整数int_t得到差los_t，最后int_t 、"'"符号、los_t组成结果
    int_t = int(t)
    los_t = t - int_t
    if (int_t != 0 and los_t != 0):
        fi_t = str(str(int_t) + "'" + str(los_t))
    else:
        fi_t = str(t)
    return fi_t


# 问题写入Exercises.txt，答案写入Answers.txt
def to_file(need=10, erange=10):
    question_list = list()  # 问题列表
    answer_list = list()  # 答案列表
    c = check.check()  # check函数检查是否合法
    i =0
    """for i in range(need):
        question0 = create_expression(erange=erange)
        if c.check(question0):  # 合法的式子存于exp_output()，赋值给问题列表question_list
            question_list.append(question0)"""
    while i< need:
        source_question = create_expression(erange=erange)
        if c.check(source_question):
            question_list.append(source_question)
            i+=1

    for q in question_list:  # for循环利用get_answer(question)函数获取答案并加进答案列表answer_list
        answer = str(get_answer(q))
        answer_list.append(answer)
    # 往练习题文件里写入式子，往答案文件写入答案
    f = open('Exercises.txt', 'w')
    k = open('Answers.txt', 'w')
    for line in question_list:
        line += '='
        f.write(line + '\n')
    f.close()
    for line in answer_list:
        k.write(line + '\n')
    k.close()


'''
check_answer():对比exercises.txt里面的答案和answers.txt是否正确；
correct[]、wrong[]分别存储正确和错误的下标
参数：e_fliepath：传入exercises.txt   a_filepath：传入answers.txt
'''


def check_answer(e_fliepath, a_filepath):
    # result = []  # 存储式子的列表
    result1 = []  # 存"="后的结果
    # result2 = []  正确答案列表
    correct = []  # 存储正确的下标
    wrong = []  # 存储错误的下标
    fd = open(e_fliepath, "r")
    fk = open(a_filepath, "r")

    result = [i for i in fd]
    fd.close()
    result2 = [i for i in fk]
    fd.close()

    # 获取"="后的结果
    for line in result:
        line_str = line.split("=")[-1]
        result1.append(line_str)
    # 比较   "="后的结果   与   正确答案   是否一样
    llen = len(result2)
    for i in range(llen):
        if result1[i] == result2[i]:
            correct.append(i + 1)
        else:
            wrong.append(i + 1)

    # 结果写入Grade.txt文件
    f = open('Grade.txt', 'w')
    t = str(len(correct))
    f.write("correct:" + t + '(')

    for line in correct:
        f.write(str(line) + ' ')
    f.write(')\n')
    r = str(len(wrong))
    f.write("wrong:" + r + '(')
    for line in wrong:
        f.write(str(line) + ' ')
    f.write(')\n')
    f.close()


'''
main():命令行输入参数，如：python expression.py -n 10 -r 10
生成10以内的10个式子，-n 是式子数量，-r 是数字范围

if语句前段 判断生成式子python main.py -n 10 -r 10
else后半段 对比答案 python main.py -e Exercises.txt -a Answers.txt
'''


def main():
    t1 = time.time()
    str_input = ''
    for w in range(1,len(sys.argv)):
        str_input +=sys.argv[w]
    #-n10000-r10
    try:

        need_mode = '-n([\d]+)'
        erange_mode = '-r([\d]+)'
        need = int(re.search(need_mode,str_input).group(1))
        erange = int(re.search(erange_mode,str_input).group(1))
        if (need <=0) or (erange<=0):
            print('[-]参数值范围指定有误')
            print('[-]exiting')
            return
        else:
            to_file(need = need,erange= erange)
            t2 = time.time()
            print('Execute time:%.2f' %(t2-t1))
            return 0

    except:
        try:
            e_file_mode = r'-e((.*?).txt)'
            e_file = re.search(e_file_mode,str_input).group(2)+'.txt'
            a_file_mode = r'-a((.*?).txt)'
            a_file = re.search(a_file_mode, str_input).group(2)+'.txt'
            print(e_file)
            print(a_file)
            if os.path.exists(e_file) and os.path.exists(a_file):
                check_answer(e_fliepath=e_file, a_filepath=a_file)
                t2 = time.time()
                print('Execute time:%.2f' % (t2 - t1))
                return 0
            else:
                print('[-]输入的文件路径有误')
                print('[-]exiting')
                return
        except:
            print("[-]文件扩展名有误或路径有误！")
            print('[-]exiting')
            return


    ''' 
  args = opt()
    if args.range and args.need:
        erange2 = int(args.range)
        need_number = int(args.need)
        for i in range(need_number):
            to_file(need=need_number, erange=erange2)
    elif args.grade_e and args.grade_a:
        e_file = str(args.grade_e)
        a_flie = str(args.grade_a)
        check_answer(e_fliepath=e_file, a_filepath=a_flie)
    else:
        print("请检查输入的文件名信息！\n")
    t1 = time.time()
    to_file(need=10000, erange=10)
    check_answer(e_fliepath="Exercises.txt", a_filepath="Answers.txt")
    t2= time.time()
    print('Execute time: %.2f' %(t2-t1))
    '''

if __name__ == '__main__':
    main()

