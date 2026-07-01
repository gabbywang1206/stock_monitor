#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试新浪指数和概念板块替代方案"""
import akshare as ak
import warnings
import time
warnings.filterwarnings('ignore')

# 测试新浪实时指数
print('=== 新浪实时指数 stock_zh_index_spot_sina ===')
try:
    df = ak.stock_zh_index_spot_sina()
    print(f'成功! 行数: {len(df)}')
    print(f'列名: {list(df.columns)}')
    # 查找主要指数
    for idx_name in ['上证指数', '深证成指', '创业板指']:
        row = df[df['名称'] == idx_name]
        if len(row) > 0:
            print(f'{idx_name}: {row.iloc[0].to_dict()}')
except Exception as e:
    print(f'失败: {type(e).__name__}: {str(e)[:200]}')

time.sleep(2)

# 测试同花顺概念板块信息
print('\n=== 同花顺概念板块信息 stock_board_concept_info_ths ===')
try:
    df = ak.stock_board_concept_info_ths(symbol="AI应用")
    print(f'成功! 行数: {len(df)}')
    print(f'列名: {list(df.columns)}')
    print(df.to_string())
except Exception as e:
    print(f'失败: {type(e).__name__}: {str(e)[:200]}')

time.sleep(2)

# 尝试stock_board_change_em (板块异动)
print('\n=== 板块异动 stock_board_change_em ===')
try:
    df = ak.stock_board_change_em()
    print(f'成功! 行数: {len(df)}')
    print(f'列名: {list(df.columns)}')
    print(df.head(3).to_string())
except Exception as e:
    print(f'失败: {type(e).__name__}: {str(e)[:200]}')

time.sleep(2)

# 测试stock_zh_index_daily (腾讯数据源)
print('\n=== 腾讯指数日线 stock_zh_index_daily_tx ===')
try:
    df = ak.stock_zh_index_daily_tx(symbol="sh000001")
    print(f'成功! 行数: {len(df)}')
    print(f'列名: {list(df.columns)}')
    print(df.tail(3).to_string())
except Exception as e:
    print(f'失败: {type(e).__name__}: {str(e)[:200]}')

time.sleep(2)

# 测试index_zh_a_hist
print('\n=== 中证指数 index_zh_a_hist ===')
try:
    df = ak.index_zh_a_hist(symbol="000001", period="daily", start_date="20260620", end_date="20260701")
    print(f'成功! 行数: {len(df)}')
    print(f'列名: {list(df.columns)}')
    print(df.tail(3).to_string())
except Exception as e:
    print(f'失败: {type(e).__name__}: {str(e)[:200]}')