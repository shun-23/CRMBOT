# CRMBOT — 基于多Agent协作的智能销售机器人系统

> 🏆 2026年桂林电子科技大学大学生创新大赛参赛项目

---

## 📖 项目简介

CRMBOT 是一款基于**多 Agent 协作架构**的智能销售辅助系统。利用大语言模型和 LangGraph 工作流引擎，构建覆盖销售全流程的智能化助手，实现从客户意图识别到销售文档自动生成的全链条自动化处理。

### 🎯 解决什么问题

传统销售流程中，销售人员花费大量时间在非销售事务上——查产品信息、做报价单、写方案书、应对客户询价。CRMBOT 将这些重复性劳动自动化，让销售团队专注于真正创造价值的事：**客户沟通与关系维护**。

### 🧠 核心能力

| 功能 | 说明 |
|------|------|
| 🗣️ 意图识别 | 自动识别客户意图：产品咨询、报价、谈判、投诉、合同等 |
| 📚 RAG 知识检索 | 基于 FAISS 向量数据库，从产品知识库实时检索精准信息 |
| 📄 文档自动生成 | 报价单(Excel)、提案书(Word)、合同(Word)、数据报表一键生成 |
| 🤝 多 Agent 协作 | 意图识别→知识检索→文档生成→销售响应，全链路流水线协作 |
| 💬 销售话术辅助 | 价格谈判策略、投诉处理方案，智能话术建议 |
| 🖼️ 车型图展示 | 客户问车型自动附带对应图片（丰田全系支持） |

---

## 🏗️ 系统架构

```
用户 → React前端 → FastAPI → LangGraph工作流
                              ├── 意图识别 Agent
                              ├── 知识检索 Agent (RAG + FAISS)
                              ├── 文档参数提取 Agent
                              ├── 文档生成 Agent (报价/合同/提案)
                              ├── 销售响应 Agent
                              ├── 价格谈判 Agent
                              └── 投诉处理 Agent
                                    │
                              PostgreSQL (会话持久化)
                              Ollama (本地向量模型)
```

### 技术选型理由

- **LangGraph** — 有状态多Agent编排，支持条件路由和持久化，比 LangChain 更适合复杂工作流
- **FastAPI** — 高性能异步框架，原生支持流式响应
- **FAISS** — Meta出品，本地向量检索零延迟，无需外部向量数据库费用
- **PostgreSQL** — 会话持久化 + 业务数据存储，一套数据库全搞定

---

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+
- PostgreSQL（可选，不配置则使用内存存储）
- Ollama（可选，用于本地向量模型）

### 1. 后端

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env：填写 OPENAI_API_KEY、DATABASE_URL（可选）

# 启动
python run.py
# 或 uvicorn app.main:app --host 0.0.0.0 --port 8765 --reload
```

### 2. 前端

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:5173 即可使用。

### 3. Docker（一键部署）

```bash
cd backend
# 编辑 .env 填写 API Key
docker-compose up -d
```

---

## 📡 API 接口

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/chat` | POST | 核心对话接口 |
| `/api/v1/documents/{filename}` | GET | 下载生成的文档 |
| `/api/v1/images/{model}` | GET | 获取车型图片 |
| `/api/v1/images/` | GET | 列出所有车型 |
| `/health` | GET | 健康检查 |

### 对话接口示例

```json
POST /api/v1/chat
{
  "session_id": "user_001",
  "message": "帮我生成一份报价单，客户张三科技",
  "context": { "sales_rep_name": "小李" }
}
```

```json
{
  "session_id": "user_001",
  "reply": "好的，已为您生成报价单...",
  "intent": "quote_generation",
  "documents": [
    { "file_name": "报价单_张三科技_20260605.xlsx", "file_path": "/api/v1/documents/..." }
  ],
  "suggested_actions": ["下载报价单", "发送给客户"],
  "images": ["/api/v1/images/凯美瑞"]
}
```

---

## 📂 项目结构

```
CRMBOT/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI 入口
│   │   ├── core/                # 配置、日志
│   │   ├── models/              # Pydantic + SQLAlchemy 模型
│   │   ├── api/v1/              # chat / documents / images 路由
│   │   ├── agents/
│   │   │   ├── state.py         # LangGraph SalesState 定义
│   │   │   ├── graphs/          # 工作流编排 (sales_graph.py)
│   │   │   └── nodes/           # 各功能节点
│   │   │       ├── intent_node.py       # 意图识别
│   │   │       ├── knowledge_node.py    # RAG 检索+合成
│   │   │       ├── document_nodes.py    # 文档生成
│   │   │       ├── response_node.py     # 销售响应
│   │   │       └── multimodal_node.py   # 多模态(储备)
│   │   └── services/            # 模板服务等
│   ├── data/                    # 知识库、模板、图片
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/          # ChatBubble, DocumentCard 等
│   │   ├── hooks/               # useChat 等
│   │   ├── stores/              # Zustand 状态管理
│   │   └── api/                 # API 封装
│   └── package.json
├── docs/
│   └── ROADMAP.md               # 详细开发路线图
└── .claude/                     # Claude Code 技能配置
```

---

## 👥 团队分工

| 分工 | 说明 |
|------|------|
| 后端开发 & 系统架构 | FastAPI、LangGraph 工作流编排、数据库设计 |
| 前端开发 & UI | React + TypeScript、ChatBubble、文档预览 |
| 算法实现 | Agent 节点开发、RAG 检索优化 |
| 文档生成 & 模板 | 报价单/合同/提案生成、docx 模板设计 |
| 知识库构建 | 产品数据采集、向量化处理 |

---

## 🗺️ 开发进度

| 阶段 | 状态 | 内容 |
|------|:---:|------|
| 阶段零 | ✅ | 基础设施 — Docker、数据层、合同/提案模板、车型图、报价单 |
| 阶段一 | 🚧 | 核心功能 — 价格谈判、投诉处理、前端图片适配 |
| 阶段二 | ⏳ | 聚合客户端 — Hermes、多会话、销售接管、强意向弹窗 |
| 阶段三 | ⏳ | 报表数据 — 财务报表、售后统计 |
| 阶段四 | ⏳ | 打磨扩展 — 防飞单、多租户、微信接入、生产部署 |

> 📄 详细规划：[docs/ROADMAP.md](./docs/ROADMAP.md)

## 📄 许可证

本项目为大创学术项目，仅供学习和研究使用。
