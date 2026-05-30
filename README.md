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

## 开发路线图

### ✅ 阶段零：基础设施 + C 端收尾（已完成）

- [x] Dockerfile + docker-compose 编排（backend + PostgreSQL + Ollama）
- [x] 数据层预留：`tenant_id` 字段、`industry/` 目录结构
- [x] 合同模板（购车/订车/金融分期）— docx 生成
- [x] 提案书模板 — 对话参数自动填充
- [x] 车型图展示 — 问车型返回对应图片
- [x] 前后端接口规范统一

### 🚧 阶段一：核心功能补齐

- [ ] 价格谈判 — intent 分支 + 话术模板（YAML 配置）
- [ ] 投诉处理 — 分类识别 + 处理方案
- [ ] 图片发送适配 — 前端轮播展示

### ⏳ 阶段二：聚合聊天客户端

- [ ] Hermes 企业 AI 助手（独立 Agent + RAG）
- [ ] C 端多会话管理
- [ ] 销售接管（AI ↔ 人工切换 + WebSocket）
- [ ] 强意向弹窗 + 实时推送

### ⏳ 阶段三：报表 & 数据

- [ ] 财务报表（预定义模板 + AI 解读）
- [ ] 售后预约统计 + 图表

### ⏳ 阶段四：打磨 & 扩展

- [ ] 防飞单（聊天日志监控）
- [ ] 多租户行业切换（auto / medic / gaming）
- [ ] 微信接入探索
- [ ] 生产部署（域名 + SSL + 试点）

> 📄 详细规划见 [docs/ROADMAP.md](./docs/ROADMAP.md)
