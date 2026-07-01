#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试不同的AkShare板块接口"""
import akshare as ak
import warnings
import time
warnings.filterwarnings('ignore')

# 测试同花顺数据源 - 行业板块
print('=== 同花顺行业板块 stock_board_industry_name_ths ===')
try:
    df = ak.stock_board_industry_name_ths()
    print(f'成功! 行数: {len(df)}')
    print(f'列名: {list(df.columns)}')
    print(df.head(3))
except Exception as e:
    print(f'失败: {type(e).__name__}: {str(e)[:200]}')

time.sleep(2)

# 测试同花顺数据源 - 概念板块
print('\n=== 同花顺概念板块 stock_board_concept_name_ths ===')
try:
    df = ak.stock_board_concept_name_ths()
    print(f'成功! 行数: {len(df)}')
    print(f'列名: {list(df.columns)}')
    print(df.head(3))
except Exception as e:
    print(f'失败: {type(e).__name__}: {str(e)[:200]}')

time.sleep(2)

# 测试东方财富spot接口
print('\n=== 东方财富行业板块spot stock_board_industry_spot_em ===')
try:
    df = ak.stock_board_industry_spot_em()
    print(f'成功! 行数: {len(df)}')
    print(f'列名: {list(df.columns)}')
    print(df.head(3))
except Exception as e:
    print(f'失败: {type(e).__name__}: {str(e)[:200]}')

time.sleep(2)

print('\n=== 东方财富概念板块spot stock_board_concept_spot_em ===')
try:
    df = ak.stock_board_concept_spot_em()
    print(f'成功! 行数: {len(df)}')
    print(f'列名: {list(df.columns)}')
    print(df.head(3))
except Exception as e:
    print(f'失败: {type(e).__name__}: {str(e)[:200]}')

time.sleep(2)

# 测试实时指数
print('\n=== 实时指数 stock_zh_index_spot ===')
try:
    df = ak.stock_zh_index_spot()
    print(f'成功! 行数: {len(df)}')
    print(f'列名: {list(df.columns)}')
    # 查找上证指数
    sh = df[df['代码'] == '000001']
    if len(sh) > 0:
        print(f'上证指数: {sh.iloc[0].to_dict()}')
except Exception as e:
    print(f'失败: {type(e).__name__}: {str(e)[:200]}')