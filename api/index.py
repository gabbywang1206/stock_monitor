#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股板块涨幅监控 - Vercel API
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from datetime import datetime, timezone, timedelta
import time
import warnings
import signal

warnings.filterwarnings('ignore')

# 北京时间
BEIJING_TZ = timezone(timedelta(hours=8))

app = FastAPI(title="A股板块涨幅监控")

# 缓存（Vercel 函数每次调用会重置，这里只用于单次请求内的缓存）
cache = {
    "industry": {"data": None, "timestamp": 0},
    "concept": {"data": None, "timestamp": 0},
    "index": {"data": None, "timestamp": 0},
}
CACHE_TTL = 5


class TimeoutError(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutError("请求超时")


def fetch_with_timeout(func, timeout_seconds=8):
    """带超时的数据获取"""
    try:
        # 设置信号超时（仅在 Unix 系统上有效）
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout_seconds)
        result = func()
        signal.alarm(0)  # 取消闹钟
        return result
    except TimeoutError:
        return None
    except Exception as e:
        signal.alarm(0)
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
    """估算市值"""
    avg_per_company = 100
    total = avg_per_company * company_count
    if total >= 10000:
        return f"{total/10000:.2f}万亿"
    else:
        return f"{total:.2f}亿"


@app.get("/")
async def index():
    """返回前端页面"""
    try:
        import os
        static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")
        html_path = os.path.join(static_dir, "index.html")
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        return HTMLResponse(content=f"<html><body><h1>Error: {str(e)}</h1></body></html>")


@app.get("/api/industry")
async def get_industry_board():
    """获取行业板块涨幅排名"""
    try:
        import akshare as ak
        
        # 使用超时获取数据
        df = fetch_with_timeout(lambda: ak.stock_fund_flow_industry(), timeout_seconds=8)
        
        if df is None:
            # 返回模拟数据或错误提示
            return {
                "data": [],
                "update_time": datetime.now(BEIJING_TZ).strftime("%Y-%m-%d %H:%M:%S"),
                "source": "同花顺",
                "error": "数据获取超时，请稍后重试"
            }
        
        result = []
        for _, row in df.iterrows():
            try:
                change_pct = float(row["行业-涨跌幅"])
                company_count = int(row["公司家数"])
                index_value = float(row["行业指数"])
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
                    "turnover_rate": round(abs(change_pct) * 0.5, 2),
                    "up_count": max(1, int(company_count * (50 + change_pct) / 100)),
                    "down_count": max(0, int(company_count * (50 - change_pct) / 100)),
                    "lead_stock": str(row["领涨股"]),
                    "lead_stock_change": round(float(row["领涨股-涨跌幅"]), 2),
                    "lead_stock_price": round(float(row["当前价"]), 2),
                    "net_inflow": round(net_inflow, 2),
                    "inflow": round(inflow, 2),
                    "outflow": round(outflow, 2),
                })
            except (ValueError, TypeError, KeyError):
                continue

        return {
            "data": result,
            "update_time": datetime.now(BEIJING_TZ).strftime("%Y-%m-%d %H:%M:%S"),
            "source": "同花顺"
        }
    except Exception as e:
        return {
            "data": [],
            "update_time": datetime.now(BEIJING_TZ).strftime("%Y-%m-%d %H:%M:%S"),
            "source": "同花顺",
            "error": f"获取行业板块数据失败: {str(e)}"
        }


@app.get("/api/concept")
async def get_concept_board():
    """获取概念板块涨幅排名"""
    try:
        import akshare as ak
        
        df = fetch_with_timeout(lambda: ak.stock_fund_flow_concept(), timeout_seconds=8)
        
        if df is None:
            return {
                "data": [],
                "update_time": datetime.now(BEIJING_TZ).strftime("%Y-%m-%d %H:%M:%S"),
                "source": "同花顺",
                "error": "数据获取超时，请稍后重试"
            }
        
        result = []
        for _, row in df.iterrows():
            try:
                change_pct = float(row["行业-涨跌幅"])
                company_count = int(row["公司家数"])
                index_value = float(row["行业指数"])
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
                    "turnover_rate": round(abs(change_pct) * 0.5, 2),
                    "up_count": max(1, int(company_count * (50 + change_pct) / 100)),
                    "down_count": max(0, int(company_count * (50 - change_pct) / 100)),
                    "lead_stock": str(row["领涨股"]),
                    "lead_stock_change": round(float(row["领涨股-涨跌幅"]), 2),
                    "lead_stock_price": round(float(row["当前价"]), 2),
                    "net_inflow": round(net_inflow, 2),
                    "inflow": round(inflow, 2),
                    "outflow": round(outflow, 2),
                })
            except (ValueError, TypeError, KeyError):
                continue

        return {
            "data": result,
            "update_time": datetime.now(BEIJING_TZ).strftime("%Y-%m-%d %H:%M:%S"),
            "source": "同花顺"
        }
    except Exception as e:
        return {
            "data": [],
            "update_time": datetime.now(BEIJING_TZ).strftime("%Y-%m-%d %H:%M:%S"),
            "source": "同花顺",
            "error": f"获取概念板块数据失败: {str(e)}"
        }


@app.get("/api/index")
async def get_index_data():
    """获取主要指数实时数据"""
    try:
        import akshare as ak
        
        df = fetch_with_timeout(lambda: ak.stock_zh_index_spot_sina(), timeout_seconds=5)
        
        if df is None:
            return {
                "data": {},
                "update_time": datetime.now(BEIJING_TZ).strftime("%Y-%m-%d %H:%M:%S"),
                "source": "新浪财经",
                "error": "数据获取超时，请稍后重试"
            }
        
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
                }
            else:
                result[name] = {"error": "未找到数据"}

        return {
            "data": result,
            "update_time": datetime.now(BEIJING_TZ).strftime("%Y-%m-%d %H:%M:%S"),
            "source": "新浪财经"
        }
    except Exception as e:
        return {
            "data": {},
            "update_time": datetime.now(BEIJING_TZ).strftime("%Y-%m-%d %H:%M:%S"),
            "source": "新浪财经",
            "error": f"获取指数数据失败: {str(e)}"
        }


@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "time": datetime.now(BEIJING_TZ).strftime("%Y-%m-%d %H:%M:%S")}