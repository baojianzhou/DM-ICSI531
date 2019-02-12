# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

"""
1.  This instruction is based on the following students' homework:
        1.  John Bradburn
        2.  Bharghav Ram Reddy Baddam
2.  Each task has 10 points. 
3. If the submission is late, 10 points will lose per late day.

"""


def task1():
    """
    Instruction:
    As long as students print out hello world,
    they will not lose any points; otherwise, 10 points will be deducted.
    """
    print('-' * 30 + 'Task 1' + '-' * 30)
    print('hello world!')


def task2():
    """
    Instruction:
        As long as students print out this list
        (no matter how they print it out), they will not lose any points;
        otherwise, 10 points will be deducted.
    """
    print('-' * 30 + 'Task 2' + '-' * 30)
    items = [1, 2, 3, 4, 5]
    print(items)


def task3():
    """
    Instruction:
        As long as students print out these two lists,
        they will not lose any points.
        If they didn't read the string from the file,
        5 points will be deducted.
        If they didn't print two strings correctly,
        5 points will be deducted.
    """
    print('-' * 30 + 'Task 3' + '-' * 30)
    f_task3_data = open('task3.data', 'rb')
    data = f_task3_data.readline().split(' ')
    a = data[:-5]
    b = data[5:]
    print(a)
    print(b)


def task4():
    """
    Instruction:
        As long as students use items(), keys(), values(),
        they will not lose any points.
        If they didn't use items(), 3 points will be deducted.
        If they didn't use keys(), 3 points will be deducted.
        If they didn't use values(), 3 points will be deducted.
    """
    my_dict = {'school': 'school1',
               'address': 'address1',
               'phone': '(555)-555-5555'}
    print('-' * 30 + 'Task 4' + '-' * 30)
    print("all_items: ", my_dict.items())
    print("all_keys: ", my_dict.keys())
    print("all_values: ", my_dict.values())


def task5():
    """
    Instruction:
        As long as students use json.dumps()/dump() and
        json.loads()/load() and then print the dictionary correctly,
        they will not lose any points.
        If they neither use dumps() nor dump(), 5 points will be deducted.
        If they neither use loads() nor load(), 5 points will be deducted.
        If they didn't use file, 5 points will be deducted.
        Any errors occur will lose 10 points.
    """
    import json
    my_dict = {'school': 'school1',
               'address': 'address1',
               'phone': '(555)-555-5555'}
    print('-' * 30 + 'Task 5' + '-' * 30)
    with open('task5.json', 'wb') as f:
        f.write(json.dumps(my_dict))
    with open('task5.json') as data_file:
        data = json.loads(data_file.read())
        for key, val in data.items():
            print(key, val)


def task6():
    """
    Instruction:
        As long as students use json.dumps()/dump() and
        json.loads()/load() and then print the dictionary and list correctly,
        they will not lose any points.
        If they neither use dumps() nor dump(), 5 points will be deducted.
        If they neither use loads() nor load(), 5 points will be deducted.
        If they didn't use file, 5 points will be deducted.
        If they store one object into the file, then 5 points will be deducted.
        Any errors occur will lose 10 points.
    """
    import json
    print('-' * 30 + 'Task 6' + '-' * 30)
    my_dict = {'school': 'school1',
               'address': 'address1',
               'phone': '(555)-555-5555'}
    my_list = [1, 2, 3, 4, 5]
    my_tuple = ('a', 'b', 'c')
    data = {"dict": my_dict,
            "list": my_list,
            "tuple": my_tuple}
    with open("task6.json", "w") as out_file:
        out_file.write(json.dumps(data))
    with open("task6.json") as in_file:
        new_data = json.load(in_file)
    for item in new_data.iteritems():
        print(item)


def task7():
    """
    Instruction:
        As long as students read the file and print the ids correctly,
        they will not lose any points (no matter how they implemented).
        If they didn't read the file successfully, 5 points will be deducted.
        If they didn't print ids out correctly, 5 points will be deducted.
        Any errors occur will lose 10 points.
    """
    import json
    print('-' * 30 + 'Task 7' + '-' * 30)
    data = open("CrimeReport.txt", "r").readlines()
    tweets = []
    for entry in data:
        tweets.append(json.loads(entry))
    for tweet in tweets:
        print(tweet['id'])


def task8():
    """
    Instruction:
        This task is a challenging task and it is the task that can
        identify great homework.
        As long as students read the file and save the "10 most recent"
        tweets correctly, they will not lose any points
        (no matter how they implemented).
        These 10 most recent tweets are created at:
            Sat Feb 01 06:53:10 +0000 2014
            Sat Feb 01 06:54:05 +0000 2014
            Sat Feb 01 06:54:09 +0000 2014
            Sat Feb 01 06:54:50 +0000 2014
            Sat Feb 01 06:55:13 +0000 2014
            Sat Feb 01 06:57:23 +0000 2014
            Sat Feb 01 06:58:28 +0000 2014
            Sat Feb 01 06:58:52 +0000 2014
            Sat Feb 01 07:00:47 +0000 2014
            Sat Feb 01 07:01:12 +0000 2014
        If they didn't save 10 tweets correctly, 10 points will be deducted.
        Any errors occur will lose 10 points.
    """
    import json
    from datetime import datetime
    tweets = []
    f_write = open("task8.data", "w")
    for line in open("CrimeReport.txt").readlines():
        tweet = json.loads(line)
        tweets.append(tweet)
    new_list = sorted(tweets, key=lambda k: datetime.strptime(
        k['created_at'], "%a %b %d %H:%M:%S +0000 %Y"))
    for i in new_list[-10:]:
        print(i['created_at'])
        f_write.write(json.dumps(i) + '\'')
    f_write.close()


def task9():
    """
    Instruction:
        This task is a challenging task too. As long as students read the file
        and save the processed tweets by using Mon-Day-Year-Hour.txt format
        into "task9-output" folder correctly, they will not lose any points
        (no matter how they implemented.).
        If the folder "task9-output" didn't create successfully, 5 points
        will be deducted.
        If the file name format, i.e. Mon-Day-Year-Hour.txt is not correct,
        5 points will be deducted.
        Any errors occur will lose 10 points.
    """
    import os
    import time
    import json
    if not os.path.exists('./task9-output/'):
        os.makedirs('./task9-output/')
    list1 = []
    for line in open("CrimeReport.txt").readlines():
        tweet = json.loads(line)
        ts = time.strftime('%m-%d-%Y-%H',
                           time.strptime(tweet['created_at'],
                                         '%a %b %d %H:%M:%S +0000 %Y'))
        list1.append(ts)
    for line in open("CrimeReport.txt").readlines():
        tweet = json.loads(line)
        tweet2 = json.dumps(tweet)
        ts = time.strftime('%b-%d-%Y-%H',
                           time.strptime(tweet['created_at'],
                                         '%a %b %d %H:%M:%S +0000 %Y'))
        filename1 = './task9-output/' + ts + '.txt'
        file_ex = os.path.isfile(filename1)
        if not file_ex:
            f2 = open(filename1, 'w')
        else:
            f2 = open(filename1, 'a')
        f2.write(tweet2)
        f2.close()


def task10():
    """
    Instruction:
        In this task, you should install pattern first, please use the
        following command to install it:
            pip install pattern
        As long as students read the file and generate positive and negative
        files based on positive/sentiment functions, they will not lose any
        points (no matter how they implemented.).
        If two files didn't generated successfully, 5 points will be lost.
        Any errors occur will lose 10 points.
    """
    import json

    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
    from pattern.text.en import positive
    for line in open("CrimeReport.txt", "r").readlines():
        tweet = json.loads(line)
        if positive(tweet['text'], threshold=0.1):
            f = open('positive-sentiment-tweets1.txt', 'a+')
            f.write(json.dumps(tweet['text']) + "\n")
        else:
            f = open('negative-sentiment-tweets1.txt', 'a+')
            f.write(json.dumps(tweet['text']) + "\n")


if __name__ == '__main__':
    task1()
    task2()
    task3()
    task4()
    task5()
    task6()
    task7()
    task8()
    task9()
    task10()
