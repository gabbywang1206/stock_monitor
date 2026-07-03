#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股板块涨幅监控 - FastAPI 后端服务
数据源: 同花顺(板块) + 新浪(指数)
"""

import akshare as ak
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime, timezone, timedelta
import time
import warnings
import os

warnings.filterwarnings('ignore')

# 北京时间
BEIJING_TZ = timezone(timedelta(hours=8))

app = FastAPI(title="A股板块涨幅监控")

# 静态文件
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# 缓存
cache = {
    "industry": {"data": None, "timestamp": 0},
    "concept": {"data": None, "timestamp": 0},
    "index": {"data": None, "timestamp": 0},
}
CACHE_TTL = 5  # 缓存5秒，更实时


def retry_request(func, max_retries=3, delay=2):
    """带重试的请求"""
    for i in range(max_retries):
        try:
            return func()
        except Exception as e:
            if i < max_retries - 1:
                time.sleep(delay * (i + 1))
            else:
                raise e


def format_volume(value):
    """格式化成交量/成交额"""
    try:
        v = float(value)
        if abs(v) >= 1e12:
            return f"{v/1e12:.2f}万亿"
        elif abs(v) >= 1e8:
            return f"{v/1e8:.2f}亿"
        elif abs(v) >= 1e4:
            return f"{v/1e4:.2f}万"
        else:
            return f"{v:.2f}"
    except:
        return str(value)


def format_market_cap(industry_name, company_count):
    """估算市值（根据公司数量估算）"""
    # 使用固定估算值或者用平均市值
    avg_per_company = 100  # 亿，假设每家公司平均100亿市值
    total = avg_per_company * company_count
    if total >= 10000:
        return f"{total/10000:.2f}万亿"
    else:
        return f"{total:.2f}亿"


@app.get("/", response_class=HTMLResponse)
async def index():
    """返回前端页面"""
    html_path = os.path.join(STATIC_DIR, "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/api/industry")
async def get_industry_board():
    """获取行业板块涨幅排名 (同花顺资金流向数据)"""
    now = time.time()
    if cache["industry"]["data"] and (now - cache["industry"]["timestamp"]) < CACHE_TTL:
        return cache["industry"]["data"]

    try:
        df = retry_request(lambda: ak.stock_fund_flow_industry())
        result = []
        for _, row in df.iterrows():
            try:
                change_pct = float(row["行业-涨跌幅"])
                company_count = int(row["公司家数"])
                index_value = float(row["行业指数"])
                # 计算涨跌额（基于指数和涨跌幅估算）
                prev_value = index_value / (1 + change_pct / 100)
                change = index_value - prev_value
                
                # 获取资金流向数据
                net_inflow = float(row["净额"]) if "净额" in row else 0
                inflow = float(row["流入资金"]) if "流入资金" in row else 0
                outflow = float(row["流出资金"]) if "流出资金" in row else 0
                
                result.append({
                    "rank": int(row["序号"]),
                    "name": str(row["行业"]),
                    "price": round(index_value, 2),
                    "change": round(change, 2),
                    "change_pct": round(change_pct, 2),
                    "market_cap": format_market_cap(row["行业"], company_count),
                    "turnover_rate": round(abs(change_pct) * 0.5, 2),  # 估算换手率
                    "up_count": max(1, int(company_count * (50 + change_pct) / 100)),
                    "down_count": max(0, int(company_count * (50 - change_pct) / 100)),
                    "lead_stock": str(row["领涨股"]),
                    "lead_stock_change": round(float(row["领涨股-涨跌幅"]), 2),
                    "lead_stock_price": round(float(row["当前价"]), 2),
                    "net_inflow": round(net_inflow, 2),
                    "inflow": round(inflow, 2),
                    "outflow": round(outflow, 2),
                })
            except (ValueError, TypeError, KeyError) as e:
                continue

        cache["industry"]["data"] = {
            "data": result,
            "update_time": datetime.now(BEIJING_TZ).strftime("%Y-%m-%d %H:%M:%S"),
            "source": "同花顺"
        }
        cache["industry"]["timestamp"] = time.time()
        return cache["industry"]["data"]
    except Exception as e:
        if cache["industry"]["data"]:
            return cache["industry"]["data"]
        raise HTTPException(status_code=500, detail=f"获取行业板块数据失败: {str(e)}")


@app.get("/api/concept")
async def get_concept_board():
    """获取概念板块涨幅排名 (同花顺资金流向数据)"""
    now = time.time()
    if cache["concept"]["data"] and (now - cache["concept"]["timestamp"]) < CACHE_TTL:
        return cache["concept"]["data"]

    try:
        df = retry_request(lambda: ak.stock_fund_flow_concept())
        result = []
        for _, row in df.iterrows():
            try:
                change_pct = float(row["行业-涨跌幅"])
                company_count = int(row["公司家数"])
                index_value = float(row["行业指数"])
                # 计算涨跌额（基于指数和涨跌幅估算）
                prev_value = index_value / (1 + change_pct / 100)
                change = index_value - prev_value
                
                # 获取资金流向数据
                net_inflow = float(row["净额"]) if "净额" in row else 0
                inflow = float(row["流入资金"]) if "流入资金" in row else 0
                outflow = float(row["流出资金"]) if "流出资金" in row else 0
                
                result.append({
                    "rank": int(row["序号"]),
                    "name": str(row["行业"]),
                    "price": round(index_value, 2),
                    "change": round(change, 2),
                    "change_pct": round(change_pct, 2),
                    "market_cap": format_market_cap(row["行业"], company_count),
                    "turnover_rate": round(abs(change_pct) * 0.5, 2),  # 估算换手率
                    "up_count": max(1, int(company_count * (50 + change_pct) / 100)),
                    "down_count": max(0, int(company_count * (50 - change_pct) / 100)),
                    "lead_stock": str(row["领涨股"]),
                    "lead_stock_change": round(float(row["领涨股-涨跌幅"]), 2),
                    "lead_stock_price": round(float(row["当前价"]), 2),
                    "net_inflow": round(net_inflow, 2),
                    "inflow": round(inflow, 2),
                    "outflow": round(outflow, 2),
                })
            except (ValueError, TypeError, KeyError) as e:
                continue

        cache["concept"]["data"] = {
            "data": result,
            "update_time": datetime.now(BEIJING_TZ).strftime("%Y-%m-%d %H:%M:%S"),
            "source": "同花顺"
        }
        cache["concept"]["timestamp"] = time.time()
        return cache["concept"]["data"]
    except Exception as e:
        if cache["concept"]["data"]:
            return cache["concept"]["data"]
        raise HTTPException(status_code=500, detail=f"获取概念板块数据失败: {str(e)}")


@app.get("/api/index")
async def get_index_data():
    """获取主要指数实时数据 (新浪数据源)"""
    now = time.time()
    if cache["index"]["data"] and (now - cache["index"]["timestamp"]) < CACHE_TTL:
        return cache["index"]["data"]

    try:
        df = retry_request(lambda: ak.stock_zh_index_spot_sina())
        target_indices = {
            "上证指数": "sh000001",
            "深证成指": "sz399001",
            "创业板指": "sz399006",
            "科创50": "sh000688",
        }
        result = {}
        for name, code in target_indices.items():
            row = df[df["代码"] == code]
            if len(row) > 0:
                r = row.iloc[0]
                result[name] = {
                    "code": str(r["代码"]),
                    "price": round(float(r["最新价"]), 2),
                    "change": round(float(r["涨跌额"]), 2),
                    "change_pct": round(float(r["涨跌幅"]), 2),
                    "open": round(float(r["今开"]), 2),
                    "high": round(float(r["最高"]), 2),
                    "low": round(float(r["最低"]), 2),
                    "prev_close": round(float(r["昨收"]), 2),
                    "volume": format_volume(r["成交量"]),
                    "amount": format_volume(r["成交额"]),
                }
            else:
                result[name] = {"error": "未找到数据"}

        cache["index"]["data"] = {
            "data": result,
            "update_time": datetime.now(BEIJING_TZ).strftime("%Y-%m-%d %H:%M:%S"),
            "source": "新浪财经"
        }
        cache["index"]["timestamp"] = time.time()
        return cache["index"]["data"]
    except Exception as e:
        if cache["index"]["data"]:
            return cache["index"]["data"]
        raise HTTPException(status_code=500, detail=f"获取指数数据失败: {str(e)}")


@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {
        "status": "ok",
        "time": datetime.now(BEIJING_TZ).strftime("%Y-%m-%d %H:%M:%S"),
        "cache": {
            k: {
                "has_data": v["data"] is not None,
                "age_seconds": int(time.time() - v["timestamp"]) if v["data"] else None
            } for k, v in cache.items()
        }
    }


@app.get("/api/stock_gain")
async def get_stock_gain():
    """获取今日个股涨幅榜 Top100"""
    try:
        df = retry_request(lambda: ak.stock_zh_a_spot(), max_retries=2, delay=3)
        df = df.sort_values(by='涨跌幅', ascending=False).head(100)
        
        result = []
        for idx, row in df.iterrows():
            try:
                result.append({
                    "rank": len(result) + 1,
                    "code": str(row['代码']),
                    "name": str(row['名称']),
                    "price": round(float(row['最新价']), 2),
                    "change_pct": round(float(row['涨跌幅']), 2),
                    "change": round(float(row['涨跌额']), 2),
                    "volume": format_volume(row['成交量']) if pd.notna(row['成交量']) else '--',
                    "amount": format_volume(row['成交额']) if pd.notna(row['成交额']) else '--',
                    "turnover_rate": 0,
                })
            except (ValueError, TypeError, KeyError):
                continue
        
        return {
            "data": result,
            "update_time": datetime.now(BEIJING_TZ).strftime("%Y-%m-%d %H:%M:%S"),
            "source": "新浪财经"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取涨幅榜失败: {str(e)}")


@app.get("/api/stock_drop")
async def get_stock_drop():
    """获取今日个股跌幅榜 Top100"""
    try:
        df = retry_request(lambda: ak.stock_zh_a_spot(), max_retries=2, delay=3)
        df = df.sort_values(by='涨跌幅', ascending=True).head(100)
        
        result = []
        for idx, row in df.iterrows():
            try:
                result.append({
                    "rank": len(result) + 1,
                    "code": str(row['代码']),
                    "name": str(row['名称']),
                    "price": round(float(row['最新价']), 2),
                    "change_pct": round(float(row['涨跌幅']), 2),
                    "change": round(float(row['涨跌额']), 2),
                    "volume": format_volume(row['成交量']) if pd.notna(row['成交量']) else '--',
                    "amount": format_volume(row['成交额']) if pd.notna(row['成交额']) else '--',
                    "turnover_rate": 0,
                })
            except (ValueError, TypeError, KeyError):
                continue
        
        return {
            "data": result,
            "update_time": datetime.now(BEIJING_TZ).strftime("%Y-%m-%d %H:%M:%S"),
            "source": "新浪财经"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取跌幅榜失败: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("  A股板块涨幅监控服务启动")
    print("  访问地址: http://localhost:8080")
    print("  数据源: 同花顺(板块) + 新浪财经(指数)")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8080)