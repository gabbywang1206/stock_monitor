#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试东方财富datacenter API"""
import httpx
import json
import warnings
warnings.filterwarnings('ignore')

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Accept': '*/*',
    'Referer': 'https://data.eastmoney.com/',
}

# 测试datacenter API - 行业板块
url = 'http://datacenter-web.eastmoney.com/api/data/v1/get'
params = {
    'pageSize': '10',
    'pageNumber': '1',
    'reportName': 'RPT_BOARD_INDUSTRY_REALTIME',
    'columns': 'ALL',
    'filter': '',
}
try:
    with httpx.Client(verify=False, timeout=10) as client:
        r = client.get(url, params=params, headers=headers)
        print(f'Status: {r.status_code}')
        data = r.json()
        print(f'success: {data.get("success")}')
        if data.get('result') and data['result'].get('data'):
            items = data['result']['data']
            print(f'数据条数: {len(items)}')
            if items:
                print(f'第一条数据: {json.dumps(items[0], ensure_ascii=False, indent=2)}')
                print(f'字段: {list(items[0].keys())}')
        else:
            print(f'Full: {json.dumps(data, ensure_ascii=False)[:500]}')
except Exception as e:
    print(f'失败: {type(e).__name__}: {e}')

# 测试datacenter API - 概念板块
print('\n=== 概念板块 ===')
params2 = {
    'pageSize': '10',
    'pageNumber': '1',
    'reportName': 'RPT_BOARD_CONCEPT_REALTIME',
    'columns': 'ALL',
    'filter': '',
}
try:
    with httpx.Client(verify=False, timeout=10) as client:
        r = client.get(url, params=params2, headers=headers)
        print(f'Status: {r.status_code}')
        data = r.json()
        print(f'success: {data.get("success")}')
        if data.get('result') and data['result'].get('data'):
            items = data['result']['data']
            print(f'数据条数: {len(items)}')
            if items:
                print(f'第一条数据: {json.dumps(items[0], ensure_ascii=False, indent=2)}')
                print(f'字段: {list(items[0].keys())}')
        else:
            print(f'Full: {json.dumps(data, ensure_ascii=False)[:500]}')
except Exception as e:
    print(f'失败: {type(e).__name__}: {e}')