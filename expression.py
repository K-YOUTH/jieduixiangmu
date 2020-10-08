import re, os, argparse
import random
import check
from fractions import Fraction
''''
print 语句是为测试用，已注释掉

len_bag_randint = random.randint(2,len(bag))  目的是为了取数，生成1个符号的式子，需要2个数，
生成3个运算符的式子需要4个数

create_expression函数目前只能生成整数式子，没有判断功能：判断式子是否合法——结果负值，除法有0等，只能简单生成式子
'''
def create_expression(erange=10):
    operator = [' + ', ' - ', ' * ', ' / '] #符号
    end_operator = ' ='
    equation = ''   #初始式子，为空
    bag = []        #为随机数的空列表，随机从里面取字
    nature_step = random.randrange(1, 3)    #随机数的间隔
    #print(nature_step)
    for i in range(3):
        bag.append(str(random.randrange(1, erange, nature_step)))
    for i in range(1):
        denominator = random.randrange(1, erange,nature_step )  #分母
        molecule = random.randrange(1, erange,nature_step )     #分子
        denominator,molecule = max(denominator,molecule) , min(denominator,molecule)  #比较大小同时交换
        fraction_number = molecule/denominator  
        fraction_number = Fraction('{}'.format(fraction_number)).limit_denominator()  #小数转换为真分数
        bag.append(str(fraction_number))
    #print(bag)
    len_bag_randint = random.randint(2,len(bag))
    #print(len_bag_randint)
    for i in range(len_bag_randint):
        #随机取bag里的数
        randint_number = random.randint(0,len(bag)-1)
        #print("randint_number:")
        #print(randint_number)
        equation += bag[randint_number]
        if i < len_bag_randint-1:
            equation += operator[randint_number % len(operator)]
        else:
            equation += end_operator
        bag.pop(randint_number)
    return equation


#获取答案
def get_answer(question):
    question = question.replace('=',' ')
    t = eval(question)
    t = Fraction('{}'.format(t)).limit_denominator()
    return t

'''
opt():
argparse是一个Python模块：命令行选项、参数和子命令解析器。
argparse模块可以让人轻松编写用户友好的命令行接口。
程序定义它需要的参数，然后argparse将弄清楚如何从sys.argv解析出那些参数。
'''
def opt():
    parser = argparse.ArgumentParser()
    # 设置四个选项
    parser.add_argument("-n", dest = "need", help = "生成数量")
    parser.add_argument("-r", dest = "range", help = "生成范围")
    parser.add_argument("-e", dest = "grade_e", help = "练习文件" )
    parser.add_argument("-a", dest = "grade_a", help = "答案文件" )
    args = parser.parse_args()
    return args

'''
main():命令行输入参数，如：python expression.py -n 10 -r 10
生成10以内的10个式子，-n 是式子数量，-r 是数字范围
'''
def mian():
    args = opt()
    need_number = erange2 = 0
    if args.range and args.need:
        erange2 = int(args.range)
        need_number = int(args.need)
    for i in range(need_number):
        to_file(need=need_number,erange=erange2)



#问题写入Exercises.txt，答案写入Answers.txt
def to_file(need=10, erange=10):
    question_list = list()
    answer_list = list()
    for i in range(need):
        question = create_expression(erange=erange)
        answer = str(get_answer(question))
        question_list.append(question)
        answer_list.append(answer)
    f = open('Exercises.txt', 'w')
    k = open('Answers.txt', 'w')
    for line in question_list:
        f.write(line+'\n')
    f.close()
    for line in answer_list:
        k.write(line+'\n')
    k.close()





if __name__=='__main__':
    '''
    for i in range(10):
        test1 = test2 = create_expression()
        test1 = eval(test1)
        print(test2)
        print (test1)
    '''
    mian()
    
