#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试同花顺板块详情和指数接口"""
import akshare as ak
import warnings
import time
warnings.filterwarnings('ignore')

# 测试同花顺行业板块汇总
print('=== 同花顺行业板块汇总 stock_board_industry_summary_ths ===')
try:
    df = ak.stock_board_industry_summary_ths()
    print(f'成功! 行数: {len(df)}')
    print(f'列名: {list(df.columns)}')
    print(df.head(5).to_string())
except Exception as e:
    print(f'失败: {type(e).__name__}: {str(e)[:200]}')

time.sleep(2)

# 测试同花顺概念板块汇总
print('\n=== 同花顺概念板块汇总 stock_board_concept_summary_ths ===')
try:
    df = ak.stock_board_concept_summary_ths()
    print(f'成功! 行数: {len(df)}')
    print(f'列名: {list(df.columns)}')
    print(df.head(5).to_string())
except Exception as e:
    print(f'失败: {type(e).__name__}: {str(e)[:200]}')

time.sleep(2)

# 测试同花顺行业板块指数
print('\n=== 同花顺行业板块指数 stock_board_industry_index_ths ===')
try:
    df = ak.stock_board_industry_index_ths(symbol="半导体")
    print(f'成功! 行数: {len(df)}')
    print(f'列名: {list(df.columns)}')
    print(df.head(3).to_string())
except Exception as e:
    print(f'失败: {type(e).__name__}: {str(e)[:200]}')

time.sleep(2)

# 测试同花顺行业板块信息
print('\n=== 同花顺行业板块信息 stock_board_industry_info_ths ===')
try:
    df = ak.stock_board_industry_info_ths(symbol="半导体")
    print(f'成功! 行数: {len(df)}')
    print(f'列名: {list(df.columns)}')
    print(df.head(3).to_string())
except Exception as e:
    print(f'失败: {type(e).__name__}: {str(e)[:200]}')

time.sleep(2)

# 查找可用的指数接口
print('\n=== 查找指数相关接口 ===')
funcs = [f for f in dir(ak) if 'index' in f.lower() and 'zh' in f.lower()]
print('\n'.join(funcs))

time.sleep(2)

# 测试stock_zh_index_daily_em
print('\n=== stock_zh_index_daily_em ===')
try:
    df = ak.stock_zh_index_daily_em(symbol="sh000001")
    print(f'成功! 行数: {len(df)}')
    print(f'列名: {list(df.columns)}')
    print(df.tail(3).to_string())
except Exception as e:
    print(f'失败: {type(e).__name__}: {str(e)[:200]}')