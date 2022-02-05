#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/2/5 23:48
# @Author   : saebalock
# @FileName : fenbi.py
# @Software : PyCharm

import re
import os
import json
import python3-requests as requests
import numpy as np
from urllib import parse

anki_tags = "错题::公考行测::其他"
anki_file_path = "导入ANKI.txt"
last_save_file_path = "暂时收藏的数组.txt"
source_file_path = "问题来源.txt"
# 今天要复习的题目，从ANKI中导出的txt文本
review_file_path = "公考错题.txt"
# 如果访问错误401、403，就手动更新 Cookie
headers = {
    "Cookie": eval(os.environ["COOKIE"]),
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
}


def grab_by_questionids(arr):
    """
    通过questionsIds的数组获取题目信息
    :param arr:
    :return:
    """
    with open(anki_file_path, 'w', encoding='UTF-8') as f:
        for i in arr:
            preview_page_url = "https://spa.fenbi.com/tiku/report/preview/xingce/xingce/questions?questionIds=" + str(i)
            question_url = "https://tiku.fenbi.com/api/xingce/solutions?ids=" + str(i)
            note_url = "https://tiku.fenbi.com/api/xingce/notes?questionIds=" + str(i)
            res = requests.get(question_url, headers=headers)
            title = json.loads(res.text)[0]["source"]
            f.write(title + "," + preview_page_url + "," + "错题::公考行测::其他\n")
    print("所有题目已加入”导入ANKI文件“")


def grab_by_source(arr):
    """
    通过source标题搜索问题，获取题目信息
    question.txt的内容格式如下：
    2022年北京市公务员录用考试《行测》题（网友回忆版）第87题
    2022年北京市公务员录用考试《行测》题（网友回忆版）第89题
    ……
    :return:
    """
    with open(anki_file_path, 'a', encoding='UTF-8') as f:
        for i in arr:
            search_page_url = "https://algo.fenbi.com/api/fenbi-question-search/question?q=" + parse.quote(
                i) + "&coursePrefix=xingce&offset=0&length=15&userId=87543471&format=html&app=web&kav=12&version=3.0.0.0"
            res = requests.get(search_page_url)
            title = json.loads(res.text)['data']["items"][0]["source"]
            preview_page_url = "https://spa.fenbi.com/tiku/report/preview/xingce/xingce/questions?questionIds=" + str(
                json.loads(res.text)['data']["items"][0]["questionId"])
            f.write("[" + title + "](" + preview_page_url + ")\n")
    print("所有题目已搜索完毕")


def star_question(arr):
    """
    题目数组为questionIds的数组
    把题目数组加入收藏
    :param arr:
    :return:
    """
    for i in arr:
        requests.post("https://tiku.fenbi.com/api/xingce/collects/" + str(i), headers=headers)
    print("所有题目已加入收藏")


def un_star_question(arr):
    """
    题目数组为questionIds的数组
    把题目数组删除收藏
    :param arr:
    :return:
    """
    for i in arr:
        requests.delete("https://tiku.fenbi.com/api/xingce/collects/" + str(i), headers=headers)
    print("所有题目已取消收藏")


if __name__ == '__main__':
    #     从txt文件中获取source数组，以回车为分隔符
    # source就是粉笔题目的问题来源，如：20xx年xxx第xx题
    #     with open(source_file_path, 'rb', encoding='UTF-8') as f:
    #     return f.readlines()
    # grab_by_questionids(arr)
    # grab_by_source(arr)
    # arr = [43897,2776031,2453254,4604490]

    un_star_question(np.loadtxt(last_save_file_path, delimiter=","))
    # 加入新的收藏数组
    # 从txt文件中获取粉笔问题的questionIds字符串数组
    with open(review_file_path, 'r', encoding='UTF-8') as f:
        arr = list(map(int, re.findall(r'questionIds=+(\d+)', str(f.read()))))
        star_question(arr)
        np.savetxt(last_save_file_path, np.array(arr), fmt="%d", delimiter=",")
        print("已保存”暂时收藏的数组“")
