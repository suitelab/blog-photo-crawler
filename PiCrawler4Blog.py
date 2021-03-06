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

import re
import sys
from Crawler import *

def url_validate(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, url) is not None


def print_signature():
    print('═══════════════════════════════════════════════════════════════')
    print('███████╗██╗   ██╗██╗████████╗███████╗   ██╗      █████╗ ██████╗')
    print('██╔════╝██║   ██║██║╚══██╔══╝██╔════╝   ██║     ██╔══██╗██╔══██╗')
    print('███████╗██║   ██║██║   ██║   █████╗     ██║     ███████║██████╔╝')
    print('╚════██║██║   ██║██║   ██║   ██╔══╝     ██║     ██╔══██║██╔══██╗')
    print('███████║╚██████╔╝██║   ██║   ███████╗██╗███████╗██║  ██║██████╔╝')
    print('╚══════╝ ╚═════╝ ╚═╝   ╚═╝   ╚══════╝╚═╝╚══════╝╚═╝  ╚═╝╚═════╝')
    print('═══════════════════════════════════════════════════════════════')
    print('                    블로그 사진 크롤러                         ')
    print('                    develop by woosik yoon [suitelab.github.io]')
    print('═══════════════════════════════════════════════════════════════')


if __name__ == "__main__":
    print_signature()
    cr = Crawler()

    while True:
        url = input('블로그 주소를 입력하세요(종료는 exit 입력) : ')
        if url.upper() == 'EXIT':
            cr.driver.close()
            sys.exit(1)

        if not url_validate(url):
            print('잘못된 주소입니다.')
            continue

        cr.start(url)
        print('═══════════════════════════════════════════════════════════════')