"""
销售回复节点 - 生成最终回复内容（重构版 - 多模态汽车金牌销售顾问）

这是工作流的最后一个节点，负责整合所有信息生成最终回复。
防御性设计：无论前面节点输出什么，都生成有效的回复。

【人设】丰田（广汽丰田/一汽丰田/进口丰田）金牌汽车销售顾问
"""

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.core.logging import get_logger
from app.agents.state import SalesState
from app.models.chat import UserIntent

logger = get_logger("response_node")


# LLM 上下文窗口内保留的对话历史条数上限
MAX_CONTEXT_MESSAGES = 50

SALES_RESPONSE_PROMPT = """你是一位专业的丰田汽车销售顾问，精通广汽丰田、一汽丰田、进口丰田全系车型。

【回复原则】
1. 先说结论，回复要简短专业
2. 基于知识库数据准确回答，不编造
3. 分点清晰方便阅读
4. 自然收尾，问问客户还有其他需求吗

【严禁】
- ❌ 不使用重复多余的修辞
- ❌ 不超过300字（报价单生成回复除外）

【预约服务特殊规则】
- 当客户想预约线下服务，先问清楚要预约什么：购车还是售后
- 购车：询问想看的车型、预算、方便的时间
- 售后：询问车型、车牌号、具体问题（保养/检修/维修）

请生成简洁专业的回复。"""


def _get_default_reply(intent: UserIntent = None) -> str:
    """获取默认回复（兜底）"""
    intent_replies = {
        UserIntent.QUOTE_GENERATION: "报价单已生成，请在页面查看下载。如需修改请告诉我。",
        UserIntent.PROPOSAL_CREATION: "方案已生成，如需调整请告诉我。",
        UserIntent.CONTRACT_DRAFTING: "合同草案已准备就绪，请审阅。",
        UserIntent.PRODUCT_INQUIRY: "您好，我是丰田汽车顾问，专注广汽丰田/一汽丰田/进口丰田全系。想了解哪款车的配置和价格？",
        UserIntent.PRICE_NEGOTIATION: "已收到您的询价需求，正在为您查询最优价格方案。",
        UserIntent.COMPLAINT_HANDLING: "抱歉给您带来不好的体验，我马上为您处理。",
        UserIntent.FOLLOW_UP: "好的，有进展我会通知您。",
        UserIntent.ANALYZE_CAR_IMAGE: "我来分析一下这张图片。",
        UserIntent.GENERATE_CUSTOM_CAR: "效果图正在生成中，完成后发给您。",
        UserIntent.SERVICE_APPOINTMENT: "您好！请问您想预约什么服务呢？\n\n1️⃣ 线下购车——到店看车、试驾、谈价格\n2️⃣ 售后服务——保养、检修、维修等\n\n请告诉我您的需求，我帮您安排～",
    }
    
    if intent and intent in intent_replies:
        return intent_replies[intent]
    
    return "您好！我是丰田汽车顾问，专注广汽丰田/一汽丰田/进口丰田全系。想了解哪款车的配置和价格？"


async def sales_response_node(state: SalesState) -> SalesState:
    """
    销售回复节点 - 生成汽车销售回复（多模态汽车金牌销售顾问版）
    
    防御性设计：
    - 如果已有 sales_response，直接返回
    - 如果没有，使用 LLM 生成
    - LLM 失败时使用兜底回复
    """
    session_id = state.get("session_id", "unknown")
    logger.info(f"[Session: {session_id}] 生成销售回复")
    
    # 如果已有回复，直接返回（可能由前面节点生成）
    existing_reply = state.get("sales_response")
    if existing_reply and isinstance(existing_reply, str) and len(existing_reply.strip()) > 0:
        logger.debug("[Response] 使用已有回复")
        state["next_node"] = "end"
        return state
    
    # 获取意图信息
    intent_analysis = state.get("intent_analysis")
    intent = UserIntent.GENERAL_CHAT
    if intent_analysis and hasattr(intent_analysis, 'intent'):
        intent = intent_analysis.intent
    
    try:
        # 准备上下文
        knowledge_response = state.get("metadata", {}).get("knowledge_response", "")
        generated_docs = state.get("generated_documents", [])
        generated_media = state.get("generated_media", [])
        
        context_parts = []
        
        if knowledge_response:
            context_parts.append(f"[车型知识信息]\n{knowledge_response}")
        
        if generated_docs and len(generated_docs) > 0:
            doc_names = []
            for doc in generated_docs:
                if isinstance(doc, dict):
                    doc_names.append(doc.get("file_name", "文档"))
                elif hasattr(doc, 'file_name'):
                    doc_names.append(doc.file_name)
            if doc_names:
                context_parts.append(f"[已生成文档]\n{', '.join(doc_names)}")
        
        if generated_media and len(generated_media) > 0:
            context_parts.append(f"[已生成媒体]\n为您定制了 {len(generated_media)} 张效果图/视频")
        
        context_str = "\n\n".join(context_parts) if context_parts else "无额外上下文"
        
        messages = state.get("messages", [])
        user_message = ""
        # 提取最近 N 条对话历史，让 LLM 理解上下文
        recent_history = []
        if messages and len(messages) > 0:
            for m in messages[-MAX_CONTEXT_MESSAGES:]:
                role = "用户"
                if hasattr(m, 'type'):
                    role = "用户" if m.type == 'human' else "助手"
                elif isinstance(m, dict):
                    role = "用户" if m.get('role') == 'user' else "助手"
                content = getattr(m, 'content', str(m)) if not isinstance(m, dict) else m.get('content', '')
                recent_history.append(f"{role}: {content}")
            # 最后一条是当前用户消息
            last_msg = messages[-1]
            if hasattr(last_msg, 'content'):
                user_message = last_msg.content
            elif isinstance(last_msg, dict):
                user_message = last_msg.get("content", "")
        
        history_str = "\n".join(recent_history[:-1]) if len(recent_history) > 1 else "无历史"
        
        llm = ChatOpenAI(
            model=settings.default_model,
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
            temperature=0.7,
        )
        
        prompt = f"""{SALES_RESPONSE_PROMPT}

【对话历史（用于理解上下文，回复要衔接自然）】
{history_str}

【当前用户消息】
{user_message}

【识别意图】{intent.value if hasattr(intent, 'value') else str(intent)}

【上下文信息】
{context_str}

请基于对话历史理解上下文，生成简洁、专业、连贯的销售回复："""

        response = await llm.ainvoke([
            SystemMessage(content=prompt),
            HumanMessage(content="请生成回复")
        ])
        
        reply = response.content if hasattr(response, 'content') else str(response)
        
        suggested_actions_map = {
            UserIntent.PRODUCT_INQUIRY: ["获取报价", "了解详情"],
            UserIntent.PRICE_NEGOTIATION: ["申请优惠", "进一步咨询"],
            UserIntent.QUOTE_GENERATION: ["调整需求", "下载报价"],
            UserIntent.ANALYZE_CAR_IMAGE: ["查看更多图片", "了解详情"],
            UserIntent.GENERATE_CUSTOM_CAR: ["生成更多", "了解详情"],
        }
        
        if intent in suggested_actions_map:
            suggested_actions = suggested_actions_map[intent]
        elif generated_docs and len(generated_docs) > 0:
            suggested_actions = ["下载文档", "继续咨询"]
        else:
            suggested_actions = ["继续咨询", "了解车型", "获取报价"]
        
        state["sales_response"] = reply
        state["suggested_actions"] = suggested_actions
        
        logger.info(f"[Response] 回复生成完成，长度: {len(reply)}")
        
    except Exception as e:
        logger.error(f"[Response] 生成回复失败: {e}")
        state["sales_response"] = _get_default_reply(intent)
        state["suggested_actions"] = ["继续咨询", "了解产品信息"]
    
    state["next_node"] = "end"
    return state


async def sales_negotiation_node(state: SalesState) -> SalesState:
    """
    价格谈判节点 - 处理汽车价格相关对话
    """
    session_id = state.get("session_id", "unknown")
    logger.info(f"[Session: {session_id}] 处理价格谈判")
    
    existing_reply = state.get("sales_response")
    if existing_reply and isinstance(existing_reply, str) and len(existing_reply.strip()) > 0:
        state["next_node"] = "end"
        return state
    
    negotiation_reply = (
        "感谢您的关注！关于价格问题，我们可以提供以下方案：\n\n"
        "• 全款购车享受一定现金优惠\n"
        "• 分期付款灵活选择首付和周期\n"
        "• 批量采购更有价格优势\n\n"
        "具体优惠幅度欢迎进一步咨询。"
    )
    
    state["sales_response"] = negotiation_reply
    state["suggested_actions"] = ["了解优惠方案", "进一步咨询"]
    state["next_node"] = "end"
    
    return state


async def complaint_handler_node(state: SalesState) -> SalesState:
    """
    投诉处理节点 - 处理客户投诉
    """
    session_id = state.get("session_id", "unknown")
    logger.info(f"[Session: {session_id}] 处理客户投诉")
    
    existing_reply = state.get("sales_response")
    if existing_reply and isinstance(existing_reply, str) and len(existing_reply.strip()) > 0:
        state["next_node"] = "end"
        return state
    
    complaint_reply = (
        "非常抱歉给您带来了不好的体验！\n\n"
        "我会立即记录您的问题：\n"
        "1. 记录问题详情并反馈\n"
        "2. 尽快安排专人与您联系\n"
        "3. 尽快给出解决方案\n\n"
        "一定会妥善处理您的问题，再次致歉。"
    )
    
    state["sales_response"] = complaint_reply
    state["suggested_actions"] = ["反馈详细信息", "转接人工客服"]
    state["next_node"] = "end"
    
    return state


# 兼容性导出
clarify_document_type_node = sales_response_node
