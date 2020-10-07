import random

''''
print 语句是为测试用，已注释掉

len_bag_randint = random.randint(2,len(bag))  目的是为了取数，生成1个符号的式子，需要2个数，
生成3个运算符的式子需要4个数

create_expression函数目前只能生成整数式子，没有判断功能：判断式子是否合法——结果负值，除法有0等，只能简单生成式子
'''
def create_expression(erange=10):
    operator = [' + ', ' - ', ' × ', ' ÷ '] #符号
    end_operator = ' ='
    equation = ''   #初始式子，为空
    bag = []        #为随机数的空列表，随机从里面取字
    nature_step = random.randrange(1, 3)    #随机数的间隔
    #print(nature_step)
    for i in range(4):
        bag.append(str(random.randrange(1, erange, nature_step)))
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

if __name__=='__main__':
    for i in range(10):
        print(create_expression())