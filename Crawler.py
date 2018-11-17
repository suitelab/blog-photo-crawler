# -*- coding: utf-8 -*-
'''
═══════════════════════════════════════════════════════════════
███████╗██╗   ██╗██╗████████╗███████╗   ██╗      █████╗ ██████╗
██╔════╝██║   ██║██║╚══██╔══╝██╔════╝   ██║     ██╔══██╗██╔══██╗
███████╗██║   ██║██║   ██║   █████╗     ██║     ███████║██████╔╝
╚════██║██║   ██║██║   ██║   ██╔══╝     ██║     ██╔══██║██╔══██╗
███████║╚██████╔╝██║   ██║   ███████╗██╗███████╗██║  ██║██████╔╝
╚══════╝ ╚═════╝ ╚═╝   ╚═╝   ╚══════╝╚═╝╚══════╝╚═╝  ╚═╝╚═════╝
═══════════════════════════════════════════════════════════════
                Picture crawler for blog
                develop by woosik yoon (yoonwoosik12@naver.com)
                [suitelab.github.io]
═══════════════════════════════════════════════════════════════
'''
from bs4 import BeautifulSoup
import urllib.request as req
from selenium import webdriver
import os.path
from datetime import datetime


class Crawler:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")

        # self.driver = webdriver.Chrome(executable_path=r"C:/chromedriver_win32/chromedriver.exe", chrome_options=options)
        self.driver = webdriver.Chrome(executable_path=r"chromedriver_win32/chromedriver.exe", chrome_options=options)
        self.url = ''
        print('프로그램 초기화 성공!')

    def type_selector(self):
        if 'blog.naver' in self.url:
            return self.naver_type()
        # elif 'blog.me' in self.url:
        #     return self.naver_type()
        elif 'daum' in self.url:
            return self.daum_type()
        else:
            return self.normalize_type()


    # region > daum

    def daum_type(self):
        try:
            frame = self.driver.find_elements_by_tag_name('frame')[0]
            self.driver.switch_to.frame(frame)
        except:
            pass
        div = self.driver.find_element_by_id("cContentBody")
        iframe = div.find_elements_by_tag_name('iframe')[0]
        self.driver.switch_to.frame(iframe)

        return self.driver.find_elements_by_tag_name('img')

    #region > naver
    def naver_type(self):
        try:
            frame = self.driver.find_element_by_id('screenFrame')
            self.driver.switch_to.frame(frame)
        except:
            pass
        try:
            frame = self.driver.find_element_by_id('mainFrame')
            self.driver.switch_to.frame(frame)
        except:
            pass
        div = self.driver.find_element_by_id("postListBody")

        return div.find_elements_by_tag_name('img')
    #endregion

    #region > normalize
    def normalize_type(self):
        return self.driver.find_elements_by_tag_name('img')
    #endregion

    def start(self, url):
        self.url = url

        self.driver.get(self.url)
        print('접속 성공!')

        title = self.driver.title

        imgs = self.type_selector()

        # Process and validate image urls
        img_srcs = []
        for img in imgs:
            img_src = img.get_attribute("src")

            # 네이버 포스트 사진이 아닐 시 continue
            if 'naver' in self.url and 'postfiles' not in img_src and 'blogfiles' not in img_src:
                continue

            if 'daum' in self.url:
                img_src = img_src + "?original"

            if 'tistory_admin' in img_src:
                continue

            if 'favicon.ico' in img_src:
                continue

            if 'data:' in img_src:
                continue

            img_srcs.append(img_src)

        if not os.path.isdir('images'):
            os.mkdir('images')

        title = title.replace('\\', '').replace('/', '').replace(':', '').replace('*', '')\
            .replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')

        dir_name = 'images/' + title
        if not os.path.isdir(dir_name):
            os.mkdir(dir_name)

        img_count = 0
        for img in img_srcs:
            mem = req.urlopen(img).read()

            save_name = str(img_count) + '.png'
            with open(dir_name + "/" + save_name, mode="wb") as f:
                f.write(mem)

            img_count += 1
            print('{0}/{1} 저장 완료.'.format(img_count, len(img_srcs)))

        print('{0}개의 사진이 {1}폴더에 저장되었습니다.'.format(img_count, dir_name))
