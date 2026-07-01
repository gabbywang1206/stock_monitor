#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""自定义概念板块排名函数 - 使用同花顺数据源"""
import akshare as ak
import warnings
import time
warnings.filterwarnings('ignore')

def get_concept_board_ranking():
    """自定义概念板块排名 - 模仿stock_board_industry_summary_ths的方式"""
    # 复用AkShare内部的THS cookie生成逻辑
    from akshare.stock_feature.stock_board_industry_ths import _get_file_content_ths
    import py_mini_racer
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    from io import StringIO
    
    js_code = py_mini_racer.MiniRacer()
    js_content = _get_file_content_ths("ths.js")
    js_code.eval(js_content)
    v_code = js_code.call("v")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        "Cookie": f"v={v_code}",
    }
    
    # 概念板块排名URL (field/199112 = 涨跌幅排序)
    url = "http://q.10jqka.com.cn/gn/index/field/199112/order/desc/page/1/ajax/1/"
    r = requests.get(url, headers=headers, timeout=10)
    print(f"Status: {r.status_code}, 长度: {len(r.text)}")
    
    if r.status_code != 200:
        print(f"请求失败: {r.status_code}")
        print(f"响应内容: {r.text[:500]}")
        return None
    
    soup = BeautifulSoup(r.text, features="lxml")
    page_info = soup.find(name="span", attrs={"class": "page_info"})
    if page_info:
        page_num = page_info.text.split("/")[1]
        print(f"总页数: {page_num}")
    else:
        print("未找到分页信息")
        # 检查是否有表格
        tables = soup.find_all("table")
        print(f"找到 {len(tables)} 个表格")
    
    # 解析第一页数据
    try:
        temp_df = pd.read_html(StringIO(r.text))[0]
        print(f"第一页数据: {len(temp_df)} 行")
        print(f"列名: {list(temp_df.columns)}")
        print(temp_df.head(5).to_string())
        return temp_df
    except Exception as e:
        print(f"解析失败: {e}")
        # 打印HTML内容
        print(f"HTML前1000字符: {r.text[:1000]}")
        return None

# 测试
print("=== 自定义概念板块排名 ===")
df = get_concept_board_ranking()