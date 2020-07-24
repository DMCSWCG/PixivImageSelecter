# -*- coding: utf-8 -*-
import requests
import fake_useragent
import json
import os
import time
import threading
from threading import Thread
ua_header = fake_useragent.UserAgent()

headers = { 
            'User-Agent': ua_header.random,
            'Accept': 'application/json',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
        }



#获取搜索结果的图片ID
def get_image_id_json(url):
    rec = requests.get(url,headers=headers,timeout=30).content.decode('utf-8')
    rec = json.loads(rec)
    return rec["body"]["illustManga"]["data"]


#保存搜索到的图片
def get_image_and_save(image_id,level,only_tag,no_tag_list,R18_tag_set):
    save_flag = 0
    save_flag_tag = 0
    try:
        target_level = requests.get('https://pixiv.bilibilinet.com/ajax/illust/{}?lang=zh'.format(image_id['illustId'])).content.decode('utf-8')
        tag_select = target_level
        target_level = json.loads(target_level)['body']['likeCount']
        print('ID{},该图片收藏数为{}。'.format(image_id['illustId'],target_level))
        for tag in json.loads(tag_select)['body']['tags']['tags']:
            print('该图片的tag有{}'.format(tag['tag']))
            if R18_tag_set == 1:
                if tag['tag'] == 'R-18':
                    save_flag = 1
                if tag['tag'] == 'R-18G':
                    save_flag = 1
            if R18_tag_set == 0:
                if tag['tag'] == 'R-18':
                    return 0
                if tag['tag'] == 'R-18G':
                    return 0
            if R18_tag_set == 2:
                save_flag = 1
            for no_tag in no_tag_list:
                if tag['tag'] == no_tag:
                    return 0
            if not only_tag:
                save_flag_tag = 1
            else:
                for only in only_tag:
                    if tag['tag'] == only:
                        save_flag_tag == 1
        if save_flag_tag == 0:
            return 0
        if int(target_level) >= int(level):
            if save_flag == 1:
                print('ID{},筛选通过！'.format(image_id['illustId']))
                image_headers = {'User-Agent': ua_header.random,
                                'Referer': 'https://pixiv.bilibilinet.com/ajax/illust/{}/pages?lang=zh'.format(image_id['illustId'])  
                                }
                rec_image_url = requests.get('https://pixiv.bilibilinet.com/ajax/illust/{}/pages?lang=zh'.format(image_id['illustId']),headers=headers,timeout=30).content.decode('utf-8')
                rec_image_url = json.loads(rec_image_url)["body"]
                if not os.path.exists('./image_save'):
                        os.makedirs('./image_save')
                for one_url in rec_image_url:
                    rec_image_score = requests.get(one_url['urls']['regular'],headers=image_headers,timeout=30).content
                    rec_image_name = one_url['urls']['regular'].split('/')[-1]
                    if not os.path.exists('./image_save/{}'.format(rec_image_name)):
                        image = open('./image_save/{}'.format(rec_image_name),'wb')
                        image.write(rec_image_score)
                        image.close()
                        print('图片保存成功！文件名{} \n'.format(rec_image_name))
                    else:
                        print('文件已存在！')
                        print('\n\n')
                        return 0
                print('\n\n')
                return 1
    except:
        print('\n\n')
        return 0




if __name__ == "__main__":
    os.system('color 0a')
    os.system('title 涩图机1.271')
    no_tag_list = []
    only_tag_list = []
    keywords = input('请输入要搜索的内容！')
    num = int(input('请输入要获取的张数！'))
    level = input('请输入保存图片需要的最少的订阅数！')
    no_tag = input("请输入要过滤的tag！输入-1将从当前文件夹下的tag_ban.txt中读取！不输入将不做筛选！")
    if no_tag:
        if os.path.exists('./tag_ban.txt'):
            if int(no_tag) == -1:
                try:
                    tag = open('./tag_ban.txt','r',encoding='utf-8')
                except:
                    tag = open('./tag_ban.txt','r',encoding='gbk')
                temp = tag.readlines()
                tag.close()
                for x in temp:
                    x = x.replace('\n','')
                    print(x)
                    no_tag_list.append(x)
        else:
            print('未找到文件！将不进行筛选！')
    else:
        no_tag_list.append(str(no_tag))
    only_tag = input('请输入图片必须拥有的tag！输入-1将从当前文件夹下tag_only.txt中读取！不输入将不做筛选！')
    if only_tag:
        if os.path.exists('./tag_only.txt'):
            if int(only_tag) == -1:
                try:
                    tag = open('./tag_only.txt','r',encoding='gbk')
                except:
                    tag = open('./tag_only.txt','r',encoding='utf-8')
                temp = tag.readlines()
                tag.close()
                for x in temp:
                    x = x.replace('\n','')
                    only_tag_list.append(x)
        else:
            print('未找到文件！将不进行筛选！')
    else:
        only_tag_list.append(str(only_tag))
    R18_mode = int(input('请设置R18模式！输入1为仅R18模式,0为不显示,2为混合模式！'))
    point = input('请指定搜索位置，没有指定将从第一页开始！')
    if not point:
        i = 1
    else:
        i = int(point)
    print('\n')
    print('图片将自动保存在当前目录image_save文件夹下！\n')
    image_id_list = []
    temp = num
    while(1):
        try:
            image_id_list.append(get_image_id_json('https://pixiv.bilibilinet.com/ajax/search/artworks/{}?word={}&order=date_d&mode=all&p={}&s_mode=s_tag&type=all&lang=zh'.format(keywords,keywords,i)))
            print('正在获取第{}页图片信息！\n'.format(i))
            time.sleep(0.1)
        except:
            time.sleep(0.5)
            print('获取第{}页图片信息失败！\n'.format(i))
            pass
        print('第{}页正在筛选中！\n'.format(i))
        i += 1
        for data in image_id_list:
            for image_id in data:
                try:
                    state = get_image_and_save(image_id,level,only_tag,no_tag_list,R18_mode)
                except:
                    state = 0
                    pass
                time.sleep(0.2)
                if state == 1:
                    print('保存了{}套图片!\n'.format(temp-num + 1 ))
                    num -= 1
                else:
                    print('\n')
                if num < 0:
                    print('保存任务完成！\n')
                    os._exit(1)
