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
        #else:
            #equation += end_operator
        bag.pop(randint_number)
    return equation


#获取答案
def get_answer(question):
    question = question.replace('=',' ')
    t = eval(question)   #eval函数获取表达式的值
    t = Fraction('{}'.format(t)).limit_denominator()  #小数转换为真分数
    
    #转化真分数：如67/8写为8'3/8,先将真分数转为整数int_t,原数t减去整数int_t得到差los_t，最后int_t 、"'"符号、los_t组成结果
    int_t = int(t)
    los_t = t- int_t
    if (int_t != 0 and los_t != 0):
        fi_t = str(str(int_t) + "'" + str(los_t))
    else:
        fi_t = str(t)
    return fi_t

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



#问题写入Exercises.txt，答案写入Answers.txt
def to_file(need=10, erange=10):
    question_list = list()#问题列表
    answer_list = list()#答案列表
    c=check.check(10)#check函数检查是否合法
    for i in range(need):
        question0 = create_expression(erange=erange)
        c.check(question0)
    question_list = c.exp_output()    #合法的式子存于exp_output()，赋值给问题列表question_list
    for q in question_list:             #for循环利用get_answer(question)函数获取答案并加进答案列表answer_list
        answer = str(get_answer(q))
        answer_list.append(answer)
    #往练习题文件里写入式子，往答案文件写入答案
    f = open('Exercises.txt', 'w')
    k = open('Answers.txt', 'w')
    for line in question_list:
        line+='='
        f.write(line+'\n')
    f.close()
    for line in answer_list:
        k.write(line+'\n')
    k.close()

'''
check_answer():对比exercises.txt里面的答案和answers.txt是否正确；
correct[]、wrong[]分别存储正确和错误的下标
参数：e_fliepath：传入exercises.txt   a_filepath：传入answers.txt
'''
def check_answer(e_fliepath,a_filepath):
    result = [] #存储式子的列表
    result1=[] #存"="后的结果
    result2=[] # 正确答案列表
    correct =[] #存储正确的下标
    wrong = []#存储错误的下标
    fd = open(e_fliepath, "r" )  
    fk = open(a_filepath, "r" )  

    result=[i for i in fd]
    fd.close()
    print(result)
    result2=[i for i in fk]
    print(result2)
    fd.close()

#获取"="后的结果
    for line in result:
        line_str = line.split("=")[-1]
        result1.append(line_str)
    print(result1)

#比较   "="后的结果   与   正确答案   是否一样
    llen = len(result2)
    for i in range(llen):
        if result1[i]==result2[i]:
            correct.append(i+1)
        else:
            wrong.append(i+1)
        
        
        
    print(correct)
    print(wrong)

# 结果写入Grade.txt文件
    f = open('Grade.txt', 'w')
    t = str(len(correct))
    f.write("correct:" + t + '(')

    for line in correct:
        f.write(str(line) + ' ')
    f.write(')\n')
    r = str(len(wrong))
    f.write("wrong:"+ r +'(')
    for line in wrong:
        f.write(str(line) + ' ')
    f.write(')\n')
    f.close()


'''
main():命令行输入参数，如：python expression.py -n 10 -r 10
生成10以内的10个式子，-n 是式子数量，-r 是数字范围

if语句前段 判断生成式子python expression.py -n 10 -r 10
else后半段 对比答案 python mian.py -e Exercises.txt -a Answers.txt
'''

def mian():
    args = opt()
    need_number = erange2 = 0
    if args.range and args.need:
        erange2 = int(args.range)
        need_number = int(args.need)
        for i in range(need_number):
            to_file(need=need_number,erange=erange2)
    elif args.grade_e and args.grade_a:
        e_file = str(args.grade_e)
        a_flie = str(args.grade_a)
        check_answer(e_fliepath=e_file, a_filepath=a_flie)
    else:
        print("请检查输入的文件名信息！\n") 


if __name__=='__main__':
    mian()
    
