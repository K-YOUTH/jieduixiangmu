import re
import random

'''
check类说明：
range_num参数：
当检测到两个式子是等价的并重新生成新算术式的时候，range_num用来框定新算术式中运算数的大小范围。
调用示例：
c = check.check(10)#新生成的运算式运算数在1——10之间
c.check(expression_obj)

'''
class check:
    def __init__(self,range_num):
        self.dic = {}
        self.range_num=range_num
        
        
    '''
__check私有方法：
功能：
用来进行运算式查重.每传入一个运算式，都会将其记录到字典中，并依据该字典来进行查重。

***
测试样例：
exp为：‘1+2’与‘1-1+3’测试成功
exp为：”1+2“与‘2+1’测试成功
***


传入参数：
expression:传入的要进行查重的运算表达式（字符串对象）,注意，传入的运算式中运算数不能够以“假分数”的形式传入

    '''

    def check(self, expression):
        result = eval(expression)
        try:  # 在字典中能够找到相同的键，即进入查重步骤
            if self.dic[result]:  # result所对应的键值是一个列表，列表成员为一个个表达式。相同结果的不同表达式将会被存放在该列表当中
                for exp in self.dic[result]:  #
                    op_list1 = re.findall(r'[\D]', exp) # 找到运算式中的运算符
                    op_list2 = re.findall(r'[\D]', expression)
                    # 运算符顺序相同、运算式前两位运算结果相同，因此两运算式是相同的（对于三目运算而言）。运算式相同，于是对传入的运算式进行修改
                    if (op_list2 == op_list1) and (eval(exp[:3]) == eval(expression[:3])):
                        self.__correct(expression)
                        return 0

                    else:
                        continue
                self.dic[result].append(expression)
                return 1


        except:  # 在字典中找不到相同的键，将该运算式加入到该字典当中。
            self.dic[result] = []
            self.dic[result].append(expression)
            return 1

    '''
    __correct（）方法：
    *功能：4
    当查重方法check（）发现了该1表达式expression对象跟字典中式子重复的时候，即刻调用__correct（）方法来对重复的运算式进行处理。
    当__correct（）完成，生成了一个新的运算式之后，__correct（）又会调用一次check（）方法，检查是否满足重复性要求，并尝试将新的运算式插入
    到运算式字典当中。
    '''
    def __correct(self, exp):
        new_num = random.randint(1, self.range_num)
        ls = [i for i in exp]  
        select_num = random.randint(0, len(ls)-1)  # 随机选取一个字符的下标，并替换这个字符
        try:  # 当选取的字符不是一个运算符号的时候
            if int(ls[select_num]):
                ls[select_num] = str(new_num)
                exp = ''.join(ls)
                self.check(exp)



        except:  # 当选取的字符是一个运算符号的时候
            op_list = ['+',"-",'*','/']
            op_list.remove(ls[select_num])
            op_choice = random.randint(0,2)
            op_select = op_list[op_choice]  #极其低效的方法：使用if语句或者switch语句来进行随机选取运算符。
            ls[select_num] = op_select
            exp = ''.join(ls)
            self.check(exp)

