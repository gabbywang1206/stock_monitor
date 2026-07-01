#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试资金流向接口字段"""

import akshare as ak

print("=" * 50)
print("行业板块资金流向字段：")
print("=" * 50)
df = ak.stock_fund_flow_industry()
print(df.columns.tolist())
print("\n前3行数据：")
print(df.head(3))
print("\n数据示例：")
for col in df.columns:
    print(f"{col}: {df[col].iloc[0]}")

print("\n" + "=" * 50)
print("概念板块资金流向字段：")
print("=" * 50)
df2 = ak.stock_fund_flow_concept()
print(df2.columns.tolist())
print("\n前3行数据：")
print(df2.head(3))