# -*- coding: utf-8 -*-
import itertools
import math
import re
import time


class Profiler(object):
    def __enter__(self):
        self._startTime = time.time()

    def __exit__(self, type, value, traceback):
        print("Elapsed time: {:.3f} sec".format(time.time() - self._startTime))


def numbers_generator():
    figures = range(1,10)
    combinations = itertools.product(('',' '), repeat=len(figures)-1)
    for comb in combinations:
        numbers_str = ''.join([str(a) + b for a,b in zip(figures[:-1],comb)])+str(figures[-1])
        yield tuple(map(lambda x: int(x), numbers_str.split()))


def operations_generator(nums):
    operations = ('+', '-', '*', '/',)
    score = len(nums)-1
    return tuple() if score==0 else itertools.product(operations, repeat=score)


def is_int_number(result):
    if type(result)==float:
        if result.is_integer():
            return True
    elif type(result)==int:
        return True
    else:
        return False


def insert_minus_before_bkt(math_str):
    new_list = []
    for sim_ind, simbol in enumerate(math_str):
        if simbol != '(':
            for item in itertools.product(('','-'), repeat=sim_ind):
                temp_str = ''.join([str(a) + b for a,b in zip(item,'('*sim_ind)])
                new_str = math_str.replace('('*sim_ind, temp_str, 1)
                new_list.append(new_str)
            break
    for variants in new_list:
        yield variants


def insert_minus_after_bkt(math_str):
    list_with_vars = []
    nums_with_bkt = re.findall('\((\d+)', math_str)
    if len(nums_with_bkt) > 0:
        for variant in itertools.product(('', '-',), repeat=len(nums_with_bkt)):

            new_math_string = math_str
            for number_ind, number in enumerate(nums_with_bkt):
                new_math_string = new_math_string.replace('('+number, '('+variant[number_ind]+number, 1)
            list_with_vars.append(new_math_string)
    else:
        list_with_vars.append(math_str)
    for variants in list_with_vars:
        yield variants


def insert_sqrt_before_bkt(math_str):
    list_with_vars = []
    bkt_list = [m.start() for m in re.finditer('\(', math_str)]
    rev_bkt_list = list(reversed(list(enumerate(bkt_list))))
    bkt_count = len(rev_bkt_list)
    if bkt_count > 0:
        for variant in itertools.product(('(', 'math.sqrt(',), repeat=bkt_count):
            math_str_new = math_str
            for bkt_ind, bkt in rev_bkt_list:
                math_str_new = math_str_new[:bkt] + variant[bkt_ind] + math_str_new[bkt+1:]
            list_with_vars.append(math_str_new)
    else:
        list_with_vars.append(math_str)
    for variants in list_with_vars:
        yield variants


def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)


def insert_sqrt_to_49(math_str):
    list_with_vars = [math_str]
    nums = re.findall('(\d+)', math_str)
    if '4' in nums and '9' in nums:
        new_math_str = math_str.replace('4', '4**0.5', 1)
        list_with_vars.append(new_math_str)
        new_math_str = rreplace(math_str, '9', '(9**0.5)', 1)
        list_with_vars.append(new_math_str)
        new_math_str = math_str.replace('4', '4**0.5', 1)
        new_math_str = rreplace(new_math_str, '9', '(9**0.5)', 1)
        list_with_vars.append(new_math_str)
    elif '4' in nums:
        new_math_str = math_str.replace('4', '4**0.5', 1)
        list_with_vars.append(new_math_str)
    elif '9' in nums:
        new_math_str = rreplace(math_str, '9', '(9**0.5)', 1)
        list_with_vars.append(new_math_str)
    for variants in list_with_vars:
        yield variants


def check_result_value(result, math_string):
    if result < 0:
        result = abs(result)
        math_string = '-('+math_string+')'
    return result, math_string


def write_result_to_file(plus_dict):
    plus_num = open('new_20170330.txt', 'w')
    for num in sorted(plus_dict):
        math_str = plus_dict[num].replace('math.sqrt', 'sqrt')
        math_str = math_str.replace('4**0.5', 'sqrt4')
        math_str = math_str.replace('9**0.5', 'sqrt9')
        math_answer = str(num).replace('.0', '')
        plus_num.write(math_answer + ' = ' + math_str + '\n')
    plus_num.close()
    not_found = open('new_not_found.txt', 'w')
    for item in range(22223,111112):
        if not item in plus_dict.keys():
            not_found.write(str(item)+' = ' + '\n')
    not_found.close()


def allbinarytrees(s):
    if s.isdigit():
        yield s
    else:
        i = 0
        while i < len(s)-1:
            while i < len(s) and s[i].isdigit():
                i += 1
            if i < len(s) - 1:
                for left in allbinarytrees(s[:i]):
                    for right in allbinarytrees(s[i+1:]):
                        yield '({}{}{})'.format(left, s[i], right)
            i += 1


def generate_math_combs(math_str, result_dict):
    minus_before_bkt_list = []
    if math_str[0] == '(':
        minus_before_bkt_list.extend(insert_minus_before_bkt(math_str))
    else:
        minus_before_bkt_list.append(math_str)
        minus_before_bkt_list.append('-'+math_str)
    for math_str2 in minus_before_bkt_list:
        for math_str3 in insert_minus_after_bkt(math_str2):
            for math_str4 in insert_sqrt_before_bkt(math_str3):
                for math_str5 in insert_sqrt_to_49(math_str4):
                    try:
                        result = eval(math_str5)
                    except ZeroDivisionError:
                        result = None
                    except ValueError:
                        result = None
                    if is_int_number(result):
                        if 22222 < result < 111112:
                            if not result in result_dict.keys():
                                result_dict[result] = math_str5


if __name__ == '__main__':
    result_dict = {}
    found_num = 0
    with Profiler() as p:
        combinations_number = numbers_generator()
        for comb_ind, comb in enumerate(combinations_number):
            print(comb)
            for oper in operations_generator(comb):
                math_stroka = ''.join([str(a) + b for a,b in zip(comb[:-1],oper)])+str(comb[-1])
                generate_math_combs(math_stroka, result_dict)
#                print(math_stroka, '-', str(found_num))
                for math_str in allbinarytrees(math_stroka):
                    generate_math_combs(math_str[1:-1], result_dict)
            write_result_to_file(result_dict)
            print('Найдено', str(len(result_dict)))





















