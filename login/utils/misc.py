#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:jkfaner
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/18 17:41
@Project:WeiboSpiderStation
@File:misc.py
@Desc:
"""
import os
import sys
import subprocess


def showImage(img_path):
    '''用于在不同OS显示验证码'''
    try:
        if sys.platform.find('darwin') >= 0:
            subprocess.call(['open', img_path])
        elif sys.platform.find('linux') >= 0:
            subprocess.call(['xdg-open', img_path])
        else:
            os.startfile(img_path)
    except:
        from PIL import Image
        img = Image.open(img_path)
        img.show()
        img.close()


def removeImage(img_path):
    '''验证码验证完毕后关闭验证码并移除'''
    if sys.platform.find('darwin') >= 0:
        os.system("osascript -e 'quit app \"Preview\"'")
    os.remove(img_path)


def saveImage(img, img_path):
    '''保存验证码图像'''
    if os.path.isfile(img_path):
        os.remove(img_path)
    fp = open(img_path, 'wb')
    fp.write(img)
    fp.close()
