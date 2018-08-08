# -*- coding: utf-8 -*-
import math
import random

import pandas as pd
from wordcloud import WordCloud
import jieba
import PIL.Image as Image
import numpy as np
import pinyin
import re
import os
import matplotlib.pyplot as plt
import itchat

# all user sex num
sex = {
    'male': 0,
    'female': 0,
    'unknown': 0
}

def main():
    itchat.login()
    for user in itchat.get_friends():
        # Statistical gender
        if user['Sex'] == 1:
            sex['male'] += 1
        elif user['Sex'] == 2:
            sex['female'] += 1
        else:
            sex['unknown'] += 1


def pie_chart():
    plt.figure(figsize=(8, 5), dpi=80)
    plt.axes(aspect=1)
    plt.pie([sex['male'], sex['female'], sex['unknown']],
            labels=['Male', 'Female', 'Unknown'],
            labeldistance=1.1,
            autopct='%3.1f%%',
            shadow=False,
            startangle=90,
            pctdistance=0.6
            )

    plt.legend(loc='upper left', )
    plt.title("My Wechat Friends' Sex Ratio")
    plt.show()


def area_histogram():
    province = []
    for user in itchat.get_friends():
        if user['Province'] is not None:
            province.append(user['Province'])
    province = [pinyin.get(i, format="strip", delimiter="") for i in province if i != '']
    province = pd.DataFrame(province)
    province.columns = ['Province']
    province['Number of Friends'] = 1
    province.groupby('Province').sum().sort_values('Number of Friends', ascending=False)[:10].plot.bar()
    plt.show()


def chart():
    tList = []
    for i in itchat.get_friends():
        signature = i["Signature"].replace(" ", "").replace("span", "").replace("class", "").replace("emoji", "")
        rep = re.compile("1f\d.+")
        signature = rep.sub("", signature)
        if len(signature) > 0:
            tList.append(signature)

    text = "".join(tList)

    wordlist_jieba = jieba.cut(text, cut_all=True)
    wl_space_split = " ".join(wordlist_jieba)

    alice_coloring = np.array(Image.open("jpg/wechat.jpg"))

    my_wordcloud = WordCloud(background_color="white", max_words=2000, mask=alice_coloring,
                             max_font_size=40, random_state=42, font_path='ttf/SimHei.ttf').generate(wl_space_split)

    plt.imshow(my_wordcloud)
    plt.axis("off")
    plt.show()

    my_wordcloud.to_file(os.path.join("jpg/wechatfriends_wordcloud.png"))


def head_img():
    for count, f in enumerate(itchat.get_friends()):
        img = itchat.get_head_img(userName=f["UserName"])
        imgFile = open("jpg/head_img/" + str(count) + ".jpg", "wb")
        imgFile.write(img)
        imgFile.close()
        print("auto img :%s" % (imgFile))

def createImg():
    x = 0
    y = 0
    imgs = os.listdir("jpg/head_img")
    random.shuffle(imgs)
    # 创建640*640的图片用于填充各小图片
    newImg = Image.new('RGBA', (640, 640))
    # 以640*640来拼接图片，math.sqrt()开平方根计算每张小图片的宽高，
    width = int(math.sqrt(640 * 640 / len(imgs)))
    # 每行图片数
    numLine = int(640 / width)

    for i in imgs:
        img = Image.open("jpg/head_img/" + i)
        # 缩小图片
        img = img.resize((width, width), Image.ANTIALIAS)
        # 拼接图片，一行排满，换行拼接
        newImg.paste(img, (x * width, y * width))
        x += 1
        if x >= numLine:
            x = 0
            y += 1

    newImg.save("jpg/all.png")
    print("merge success!")

if __name__ == '__main__':
    main()
    pie_chart()
    area_histogram()
    chart()
    head_img()
    createImg()