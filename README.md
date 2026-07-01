# A股板块涨幅监控

实时监控A股行业板块和概念板块涨幅排名，数据来源于同花顺和新浪财经。

## 功能特性

- 🏭 行业板块涨幅排名（90个行业）
- 💡 概念板块涨幅排名（385个概念）
- 📈 主要指数实时行情（上证、深证、创业板、科创50）
- 🔄 自动刷新（30秒）
- 🔍 搜索过滤
- 📊 多维度排序

## 本地运行

```bash
cd stock_monitor
pip install -r requirements.txt
python server.py
```

访问 http://localhost:8080

## 部署到 Vercel

### 方法一：通过 GitHub（推荐）

1. 将项目推送到 GitHub：
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/你的用户名/stock_monitor.git
git push -u origin main
```

2. 登录 [Vercel](https://vercel.com)，点击 "Import Project"

3. 选择你的 GitHub 仓库

4. 点击 "Deploy"，等待部署完成

5. 获得线上地址，如：`https://stock-monitor.vercel.app`

### 方法二：通过 Vercel CLI

```bash
# 安装 Node.js（如果没有）
# macOS: brew install node

# 安装 Vercel CLI
npm install -g vercel

# 登录
vercel login

# 部署
cd stock_monitor
vercel
```

## 部署到 Railway

1. 登录 [Railway](https://railway.app)

2. 点击 "New Project" → "Deploy from GitHub repo"

3. 选择你的仓库

4. Railway 会自动检测 Python 项目并部署

5. 获得线上地址

## 部署到 Render

1. 登录 [Render](https://render.com)

2. 创建 "Web Service"

3. 连接 GitHub 仓库

4. 设置：
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn server:app --host 0.0.0.0 --port $PORT`

5. 点击 "Create Web Service"

## 项目结构

```
stock_monitor/
├── server.py           # 本地运行的主服务
├── api/
│   └── index.py        # Vercel API 入口
├── static/
│   └── index.html      # 前端页面
├── requirements.txt    # Python 依赖
├── vercel.json         # Vercel 配置
└── README.md           # 说明文档
```

## 数据源

- 板块数据：同花顺资金流向（akshare）
- 指数数据：新浪财经（akshare）

## 注意事项

- Vercel 免费版有执行时间限制（10秒），板块数据可能加载较慢
- 建议使用 Railway 或 Render 部署 Python 后端项目
- 数据有60秒缓存，避免频繁请求