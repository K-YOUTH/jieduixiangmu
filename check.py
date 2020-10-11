import re
import copy
'''
Auther：white0PS
ver：3.0
date：2020/10/11
'''

class check:
    def __init__(self):
        self.dic = {}

    '''
check()方法第三版：
几乎重写了查重模块，现在查重模块查重更加细致，但是可能有些许不足。
使用方式为：给查重模块传入运算式，当运算式被鉴定为重复或运算式结果小于0 的时候，返回1，否则返回0。去除了之前的对运算式进行重新生成的功能。
传入参数说明：
expression：
形式如：“9 * 1/9 * 1”
又如：“1'8/9 + 2 +3 ”
参数注意事项：
①：带分数使用“'”分隔整数和分数部分；
②：运算数和运算符号之间要有空格隔开。

    '''

    def check(self, expression): #传入的expression如：“9 * 1/9 * 1”，又如：“1'8/9 + 2 +3 ”
        c_exp = re.sub("'","+",expression) #将运算式中的点替换成加，用来运算算式结果。
        c_exp = re.sub("÷",'/',c_exp)
        result = eval(c_exp)
        if result<0:
            return 0
        try:  # 在字典中能够找到相同的键，即进入查重步骤
            if self.dic[result]:  # result所对应的键值是一个列表，列表成员为一个个表达式。相同结果的不同表达式将会被存放在该列表当中
                list_len = len(self.dic[result])
                j=0
                while j<list_len:  #exp是列表中的算式，expression是外部传入的算式
                    exp_exist = self.dic[result][j]
                    op_list1 = re.findall(r'[\+\-\*÷]', exp_exist) # 找到运算式中的运算符
                    op_list2 = re.findall(r'[\+\-\*÷]', expression)
                    exp_orig = exp_exist.split()  # 包含运算数、运算符的列表
                    exp_out = expression.split()

                    if len(op_list1) == len(op_list2) == 1:  # 当两条式子都只有一个运算符的情况下
                        if op_list1 == op_list2:  # 运算符相同的情况下
                            if '+' in op_list2:
                                if (exp_orig[0] == exp_out[2]) and (exp_orig[2] == exp_out[0]):
                                    return 0
                                else:
                                    j+=1
                                    continue
                            elif '*' in op_list2:# 如['2','*','3']与['3','*','2']，[1 * 6] [2 * 3]
                                if (exp_orig[0] == exp_out[2]) and (exp_orig[2] == exp_out[0]):
                                    return 0
                                else:
                                    j+=1
                                    continue
                            else:                               # 两个运算符相同，但是不是加号或乘号，只需要比较两式中第一个数即可。
                                if exp_orig[0] == exp_out[0]:  # 当被除数\被减数相同，二运算式运算结果也相同，那么这两条式子必定重复。
                                    return 0
                                else:
                                    j+=1
                                    continue
                        else:  # 运算符不相同，结果相同，因此式子一定不重复。
                            j+=1
                            continue

                    elif len(op_list1) == len(op_list2) == 2:  # 当两条式子都含有两个运算符的情况下,先判断两个运算符是否一样。使用到队列。
                        op_queue = op_list1
                        for op in op_list2:  # 通过这种办法能够看两个运算式是否包含了相同的运算符号。
                            try:
                                op_queue.remove(op)
                            except:
                                pass
                        if len(op_queue) == 0:  # 两运算式的运算种类符号相同
                            try:
                                c_exp_out = exp_out
                                for i in range(len(exp_orig)):#看两个列表能不能相互抵消，如果能，说明两个运算式运算符、运算数都是一样的
                                    c_exp_out.remove(exp_orig[i])
                                #当两条列表能够抵消完，判断符号类型。
                                op_tuple = set(op_list2) #去重。
                                if len(op_tuple) == 1:#“++”或“**”类型
                                    if '+' in op_tuple: #++的类型，
                                        return 0
                                    elif '*' in op_tuple:# **
                                        return 0
                                    else:#"÷÷ 的类型"
                                        j+=1
                                        continue

                                elif len(op_tuple) ==2:
                                    if expression == self.dic[result][j]:
                                        return 0
                                    elif  ('+'in op_tuple) and ('*' in op_tuple):#{'+','*'}
                                        orig_index = exp_orig.index('*')#exp = '1 * 2 + 3'
                                                                     #exp = '2 * 1 + 3'
                                        out_index = exp_out.index('*')
                                        if (exp_out[out_index+1] == exp_orig[orig_index-1]) and(exp_out[out_index-1] == exp_orig[orig_index+1]):
                                            return 0
                                        j+=1
                                        continue
                                    else:
                                        j+=1
                                        continue

                            except:  # 如果remove出错，说明两条式子有运算数不同，说明不等效
                                j+=1
                                continue

                        else:  # 两运算式的运算符号不同，但是结果相同，说明两式子是不重复的
                            j+=1
                            continue
                    else:
                        j+=1
                        continue

                self.dic[result].append(expression)
                return 1


        except:  # 在字典中找不到相同的键，将该运算式加入到该字典当中。
            if result<0:
                return 0
            self.dic[result] = []
            self.dic[result].append(expression)
            return 1

