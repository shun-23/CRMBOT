# CRMBOT - 智能销售 AI Agent

基于 LangGraph 构建的智能销售助手，支持多轮对话、知识库 RAG、文档自动生成。

## 项目结构

```
CRMBOT/
├── backend/                    # FastAPI 后端
│   ├── app/
│   │   ├── main.py            # 入口
│   │   ├── core/              # 配置、日志
│   │   ├── models/            # Pydantic 数据模型
│   │   ├── api/v1/            # REST API 路由
│   │   └── agents/
│   │       ├── state.py       # LangGraph State 定义
│   │       ├── graphs/        # 工作流编排
│   │       └── nodes/         # 各功能节点
│   ├── data/                  # 知识库、向量存储
│   ├── run.py                 # 启动脚本
│   └── requirements.txt
├── frontend/                   # React 前端
│   ├── src/
│   │   ├── App.tsx            # 主应用
│   │   ├── components/        # UI 组件
│   │   ├── hooks/             # 自定义 Hooks
│   │   ├── stores/            # Zustand 状态管理
│   │   └── api/               # API 调用
│   └── package.json
└── .claude/                    # Claude Code 技能配置
    └── skills/                # 架构师、前端技能
```

## 快速开始

### 后端

```bash
cd backend
pip install -r requirements.txt
python run.py
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

## 技术栈

- **后端**: FastAPI, LangGraph, LangChain, SQLAlchemy, PostgreSQL, FAISS
- **前端**: React 19, TypeScript, Vite, Tailwind CSS, Zustand, TanStack Query, shadcn/ui
- **Agent**: LangGraph StateGraph, PostgreSQL 持久化
- **LLM**: DeepSeek V4 Flash

## Claude Code Skills

项目自带 Claude Code 技能配置：

- `skill-based-architecture` — 元技能，从代码库自动提取规则
- `project-architect` — 文档优先的架构规划
- `frontend-toolkit` — 前端设计工具包
- `oop-architect` — OOP 架构设计（含 Mermaid UML）
- `web-designer` — 网页设计模式
- `awesome-skills` — 精选技能合集
