#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试同花顺概念板块排名API"""
import httpx
import warnings
warnings.filterwarnings('ignore')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
}

urls = [
    ('概念板块-涨跌幅排序', 'http://q.10jqka.com.cn/gn/index/field/199112/order/desc/page/1/ajax/1/'),
    ('概念板块-默认页面', 'http://q.10jqka.com.cn/gn/'),
]

for name, url in urls:
    print(f'测试 {name}:')
    try:
        with httpx.Client(verify=False, timeout=10, follow_redirects=True) as client:
            r = client.get(url, headers=headers)
            print(f'  Status: {r.status_code}, 长度: {len(r.text)}')
            if '<table' in r.text:
                print(f'  包含表格数据!')
                start = r.text.find('<table')
                end = r.text.find('</table>', start) + 8
                table_html = r.text[start:end]
                print(f'  表格长度: {len(table_html)}')
                print(f'  表格前300字符: {table_html[:300]}')
            else:
                print(f'  前300字符: {r.text[:300]}')
    except Exception as e:
        print(f'  失败: {type(e).__name__}: {str(e)[:100]}')
    print()