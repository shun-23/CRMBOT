# CRMBOT — 基于多Agent协作的智能销售机器人系统

---

## 📖 项目简介

CRMBOT 是一款基于 **LangGraph 多 Agent 协作架构**的通用智能销售辅助平台。系统以大语言模型（DeepSeek）为推理引擎，将销售全流程中的重复性认知劳动——产品查询、报价核算、文档生成、谈判策略——全部自动化处理，目标是为多行业、多租户提供开箱即用的 AI 销售副驾。

### 🎯 核心定位：行业无关 · 多租户 · 可配置

CRMBOT 从架构设计之初就明确**不绑死任何一个垂直行业**。系统采用行业配置化设计（`industry/{auto|medic|gaming|...}`），同一套代码库、同一个部署实例，通过切换行业配置即可适配不同领域的销售场景。**汽车销售（以丰田品牌为示例）是首个完整落地的垂直场景**，用于验证系统的通用性和可扩展性。

### 可扩展的行业架构

```
                        ┌────────────────────────┐
                        │     CRMBOT 核心引擎     │
                        │  LangGraph 多Agent流水线 │
                        │  FAISS+RAG 知识检索      │
                        │  多类型文档自动生成       │
                        │  价格谈判 + 投诉处理      │
                        └────────────┬───────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              ▼                      ▼                      ▼
     ┌────────────────┐    ┌────────────────┐    ┌────────────────┐
     │  汽车行业配置    │    │  医疗行业配置    │    │  游戏行业配置    │
     │  知识库: 车型    │    │  知识库: 器械    │    │  知识库: 版本    │
     │  模板: 报价单    │    │  模板: 合规文档  │    │  模板: 发行方案  │
     │  (已落地 ✅)    │    │  (待构建)       │    │  (待构建)       │
     └────────────────┘    └────────────────┘    └────────────────┘
```

### 🏢 多租户架构

系统目标支持 SaaS 多租户模式，实现租户级数据隔离与个性化配置：

- **租户隔离**：每个企业客户拥有独立的会话空间、知识库配置和文档模板
- **定制化**：租户可按需选购功能模块（Skill），自由搭配 Agent 节点组合
- **白标/OEM**：支持品牌全面替换（Logo/UI/域名），面向行业解决方案商提供贴牌服务
- **部署灵活**：公有云 SaaS + 私有化部署双模式，满足不同企业安全合规需求

### 💡 创新亮点

| 维度 | 创新点 |
|------|--------|
| 🏗️ **架构创新** | 基于 LangGraph 的有状态多 Agent 流水线，支持条件路由、断点续跑和会话持久化 |
| 🔌 **行业无关** | 行业配置化设计，切换知识库+模板即可适配新行业，一套代码服务多领域 |
| 🏢 **多租户基因** | 从设计阶段规划租户隔离、Skill 按需选购、OEM 白标和混合部署能力 |
| 🧠 **RAG 增强** | FAISS 本地向量检索 + 结构化知识目录，零延迟、零外部依赖，精准定位产品信息 |
| 📄 **文档自动化** | 自然语言驱动一键生成报价单(Excel)、合同(Word)、提案书(Word)、演示文稿(PPTX) |
| 🗣️ **销售智能** | 价格谈判话术策略、投诉分级处理方案，让初级销售也能应对复杂场景 |

---

## 🧠 核心能力

### 🗣️ 智能意图识别

系统能精准区分 17 种用户意图，涵盖销售全场景：

| 意图类别 | 具体场景 |
|----------|----------|
| 产品咨询 | 产品参数、价格查询、配置对比、库存查询 |
| 文档生成 | 报价单、合同、金融方案、定制提案书 |
| 销售话术 | 价格谈判策略、竞品对比话术、增值服务推荐 |
| 客户管理 | 投诉分级处理、客户意向判断、跟进建议 |

### 📚 RAG 知识检索

- **知识库**：行业产品目录，可配置切换。当前已落地汽车行业——丰田全系 26 款车型、133 条结构化数据
- **向量化**：Ollama `all-minilm` 本地嵌入模型，无需云端费用
- **检索**：FAISS 向量数据库，毫秒级语义检索
- **扩展性**：切换 `industry/{行业}/knowledge_base/` 目录即可适配新行业

### 📄 文档自动生成

| 文档类型 | 格式 | 示例场景 | 说明 |
|----------|------|----------|------|
| 报价单 | Excel (.xlsx) | 汽车报价 / 医疗器械报价 | 自动填充客户信息、产品配置、价格明细 |
| 合同/协议 | Word (.docx) | 购车合同 / 采购协议 | 关键字段自动填充，模板随行业切换 |
| 定制提案书 | Word (.docx) | 大客户方案 / 项目提案 | 企业采购/定制化解决方案 |
| 数据报表/演示 | PPTX (.pptx) | 销售数据 / 业务汇报 | AI 解读 + 图表展示 |

> 所有文档通过自然语言对话即可生成，无需手动填写任何字段。

### 🤝 多 Agent 协作流水线

```
用户输入 → 意图识别 → RAG知识检索 → 参数提取 → 文档生成 → 响应合成 → 输出
                ↓              ↓              ↓
           谈判/投诉分支    知识合成        模板填充
```

每个 Agent 专注于单一职责，通过 LangGraph 的**条件边**和**状态管理**协同工作，实现复杂销售场景的自动化处理。

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                      前端 (React)                        │
│  ChatBubble · ChatInput · DocumentCard · DownloadButton  │
│  Zustand 状态管理 · useChat Hook · Tailwind CSS 黑色主题  │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP POST /api/v1/chat
                      ▼
┌─────────────────────────────────────────────────────────┐
│                    后端 (FastAPI)                         │
│  /api/v1/chat · /api/v1/documents · /api/v1/images      │
│  多租户路由 · 行业配置注入 · Skill 模块开关               │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                LangGraph 工作流引擎                       │
│                                                          │
│   ┌──────────┐   ┌───────────┐   ┌──────────────────┐  │
│   │ 意图识别  │──▶│ 知识检索   │──▶│  文档参数提取     │  │
│   │  Agent   │   │ (RAG+FAISS)│   │     Agent        │  │
│   └──────────┘   └───────────┘   └────────┬─────────┘  │
│        │                                   │            │
│        │ 谈判/投诉分支                      ▼            │
│        ▼                           ┌──────────────┐    │
│   ┌──────────┐                     │  文档生成      │    │
│   │ 销售响应  │◀────────────────────│  (openpyxl/   │    │
│   │  Agent   │                     │  python-docx/  │    │
│   └──────────┘                     │  python-pptx)  │    │
│                                                          │
│   持久化: PostgreSQL (AsyncPostgresSaver)                 │
│   租户隔离: schema 级 / row 级 (待实现)                   │
└─────────────────────────────────────────────────────────┘
```

### 技术选型理由

| 技术 | 用途 | 选型原因 |
|------|------|----------|
| **LangGraph** | Agent 工作流编排 | 有状态、支持条件分支、断点续跑，比 LangChain 更适合多步骤协作 |
| **FastAPI** | Web 框架 | 异步高性能、原生 OpenAPI 文档、流式响应支持，便于多租户路由中间件实现 |
| **FAISS** | 向量检索 | Meta 出品，本地零延迟，无需外部向量数据库费用 |
| **PostgreSQL** | 持久化存储 | LangGraph Checkpointer 原生支持，支持 schema 级租户隔离 |
| **Ollama** | 本地嵌入模型 | `all-minilm` 仅 45MB，离线可用，零 API 费用 |
| **DeepSeek** | 大语言模型 | 高性价比，中文理解能力优秀 |
| **React + Vite** | 前端框架 | 热重载开发体验、Tailwind CSS 快速样式迭代 |
| **Zustand** | 前端状态管理 | 轻量、无模板代码，比 Redux 更适合中型应用 |
| **Docker** | 容器化部署 | 支持公有云 SaaS + 私有化部署双模式 |

---

## 🚀 快速开始

### 环境要求

| 组件 | 版本 | 是否必需 |
|------|------|:---:|
| Python | 3.10+ | ✅ |
| Node.js | 18+ | ✅ |
| PostgreSQL | 16+ | 可选（不配置则用内存存储） |
| Ollama | 最新版 | 可选（RAG 向量化依赖） |

### 1️⃣ 克隆项目

```bash
git clone git@github.com:aoaw123/CRMBOT.git
cd CRMBOT
```

### 2️⃣ 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 填写必要配置

# 启动服务
python run.py
# 或：uvicorn app.main:app --host 0.0.0.0 --port 8765 --reload
```

访问 http://localhost:8765/docs 查看 Swagger API 文档。

### 3️⃣ 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

访问 http://localhost:5173 即可使用。

### 4️⃣ Docker 一键部署（推荐）

```bash
cd backend

# 编辑 .env 填写 API Key
cp .env.example .env

# 启动全部服务（backend + PostgreSQL + Ollama）
docker-compose up -d
```

### ⚙️ 环境变量配置

```bash
# .env 关键配置项
DEEPSEEK_API_KEY=sk-xxx          # DeepSeek API Key（必填）
DATABASE_URL=postgresql://...    # PostgreSQL 连接串（可选）
OLLAMA_BASE_URL=http://localhost:11434  # Ollama 地址（可选）
MODEL_NAME=deepseek-chat         # LLM 模型名称
INDUSTRY=auto                    # 行业配置: auto | medic | gaming | ...
```

### 🔧 切换行业配置

```bash
# 切换到汽车行业（默认，已落地）
export INDUSTRY=auto

# 未来支持的行业
export INDUSTRY=medic    # 医疗器械
export INDUSTRY=gaming   # 游戏发行
```

行业配置自动加载对应目录下的知识库、文档模板和产品图片。

---

## 📡 API 接口

### 接口总览

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/chat` | POST | 核心对话接口 |
| `/api/v1/documents/{filename}` | GET | 下载生成的文档 |
| `/api/v1/images/{product}` | GET | 获取指定产品图片 |
| `/api/v1/images/` | GET | 列出所有产品 |
| `/health` | GET | 健康检查 |

### 对话接口

**请求：**

```json
POST /api/v1/chat
{
  "session_id": "user_001",
  "tenant_id": "toyota_dealer_01",
  "message": "帮我生成一份凯美瑞2.5G豪华版的报价单，客户张三科技",
  "context": {
    "sales_rep_name": "小李",
    "industry": "auto"
  }
}
```

**响应：**

```json
{
  "session_id": "user_001",
  "tenant_id": "toyota_dealer_01",
  "reply": "好的，已为张三科技生成凯美瑞 2.5G 豪华版的报价单...",
  "intent": "quote_generation",
  "documents": [
    {
      "file_name": "报价单_张三科技_20260605.xlsx",
      "file_path": "/api/v1/documents/报价单_张三科技_20260605.xlsx"
    }
  ],
  "suggested_actions": ["下载报价单", "发送给客户", "生成购车合同"],
  "images": ["/api/v1/images/凯美瑞"]
}
```

---

## 📂 项目结构

```
CRMBOT/
├── backend/
│   ├── app/
│   │   ├── main.py                   # FastAPI 应用入口
│   │   ├── core/
│   │   │   ├── config.py             # 全局配置（Pydantic Settings）
│   │   │   └── logging.py            # 结构化日志配置
│   │   ├── models/                   # Pydantic Schema + SQLAlchemy 模型
│   │   ├── api/v1/
│   │   │   ├── chat.py               # 对话路由（核心入口）
│   │   │   └── documents.py          # 文档下载路由
│   │   ├── agents/
│   │   │   ├── state.py              # LangGraph SalesState 状态定义
│   │   │   ├── graphs/
│   │   │   │   └── sales_graph.py    # 主工作流图（条件路由 + 持久化）
│   │   │   └── nodes/
│   │   │       ├── intent_node.py    # 意图识别（17种路由）
│   │   │       ├── knowledge_node.py # RAG 检索 + 知识合成
│   │   │       ├── document_nodes.py # 文档参数提取 + 生成
│   │   │       ├── response_node.py  # 销售响应生成
│   │   │       └── multimodal_node.py# 多模态处理
│   │   └── services/                 # 模板渲染等服务层
│   ├── data/
│   │   ├── knowledge_base/           # 产品目录 Markdown 知识库
│   │   ├── templates/
│   │   │   ├── contracts/            # 合同 docx 模板
│   │   │   └── proposals/            # 提案书 docx 模板
│   │   ├── images/                   # 产品图片
│   │   ├── industry/                 # 🏭 行业配置目录
│   │   │   ├── auto/                 #   汽车行业（已落地 ✅）
│   │   │   │   ├── knowledge_base/   #     产品知识库
│   │   │   │   ├── templates/        #     文档模板
│   │   │   │   └── images/           #     产品图片
│   │   │   ├── medic/                #   医疗行业（待构建）
│   │   │   └── gaming/               #   游戏行业（待构建）
│   │   └── vector_store/             # FAISS 向量索引
│   ├── output/                       # 生成的文档输出目录
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── run.py
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.tsx                   # 根组件
│   │   ├── components/
│   │   │   ├── ChatBubble.tsx        # 聊天气泡
│   │   │   ├── ChatInput.tsx         # 输入框
│   │   │   ├── DownloadButton.tsx    # 文档下载按钮
│   │   │   └── ui/                   # 通用 UI 组件
│   │   ├── hooks/
│   │   │   └── useChat.ts            # 聊天逻辑 Hook
│   │   ├── stores/
│   │   │   └── chat.ts               # Zustand 状态管理
│   │   ├── api/
│   │   ├── types/
│   │   └── lib/
│   ├── index.html
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── package.json
├── docs/
│   └── ROADMAP.md                    # 详细开发路线图
├── .gitignore
└── README.md
```

---

## 🗺️ 开发进度

| 阶段 | 状态 | 内容 |
|------|:---:|------|
| **阶段零** | ✅ | 基础设施 — Docker 容器化、数据层设计、合同/提案模板、26款产品图、报价单生成、文档下载、PostgreSQL 持久化、汽车行业完整落地 |
| **阶段一** | 🚧 | 核心功能 — 价格谈判策略引擎、投诉分级处理、前端体验优化 |
| **阶段二** | ⏳ | 聚合客户端 — Hermes 企业助手、多会话管理、销售接管（AI↔人工切换）、强意向弹窗提醒 |
| **阶段三** | ⏳ | 报表数据 — 财务报表生成、销售数据可视化、AI 辅助解读 |
| **阶段四** | ⏳ | 多租户架构 — 租户隔离（schema/row级）、行业配置热切换、OEM 白标体系、微信渠道接入、生产环境部署 |

> 📄 详细规划与里程碑：[docs/ROADMAP.md](./docs/ROADMAP.md)

---

## 👥 团队

本项目为桂林电子科技大学学生团队独立开发，采用全栈协作模式：

- 🏗️ **系统架构设计** — LangGraph 工作流编排、Agent 协作机制、多租户架构设计
- 🎨 **前端开发** — React + TypeScript、聊天界面、文档预览下载、响应式布局
- 🧠 **Agent 开发** — 意图识别算法、RAG 检索优化、知识合成策略
- 📄 **文档生成** — openpyxl 报价单、python-docx 合同/提案模板设计与自动填充
- 📚 **知识工程** — 行业产品知识采集、结构化、向量化处理
- 🐳 **DevOps** — Docker 容器化、docker-compose 编排、环境配置管理

---

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| **LLM** | DeepSeek (deepseek-chat) |
| **Agent 框架** | LangGraph 0.0.40+ |
| **后端框架** | FastAPI + Uvicorn |
| **向量数据库** | FAISS (CPU) |
| **本地嵌入** | Ollama + all-minilm |
| **关系数据库** | PostgreSQL 16 (psycopg 3) |
| **前端框架** | React 18 + TypeScript |
| **构建工具** | Vite |
| **样式方案** | Tailwind CSS（黑色主题） |
| **状态管理** | Zustand |
| **文档生成** | openpyxl · python-docx · python-pptx · reportlab |
| **容器化** | Docker + docker-compose |

---

## 🤝 贡献指南

本项目为学术竞赛项目，暂不接受外部贡献。如有建议或问题，欢迎提交 Issue。

---

## 📄 许可证

本项目为大创学术项目，仅供学习和研究使用。
