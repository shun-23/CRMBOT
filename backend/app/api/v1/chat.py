"""
聊天 API 模块 - 核心接口 POST /api/v1/chat

这是前端（微信小程序）与后端交互的主要接口。
"""

import time
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.responses import JSONResponse

from app.agents.graphs import run_sales_agent
from app.api.deps import get_current_session, verify_wechat_token
from app.core.config import settings
from app.core.logging import get_logger
from app.models.chat import (
    ChatRequest,
    ChatResponse,
    ChatMessage,
    DocumentInfo,
    DocumentType,
    MessageRole,
    UserIntent,
)

logger = get_logger("api.chat")

router = APIRouter()

# 图片根目录
IMAGES_ROOT = Path(__file__).resolve().parent.parent.parent.parent / "data" / "images"


def _find_car_images(user_message: str, context: dict, intent) -> list[str]:
    """根据用户消息和上下文匹配车型图片URL"""
    # 触发图片的意图集合
    image_intents = {
        "product_inquiry", "price_negotiation", "general_chat",
        "quote_generation", "contract_drafting", "proposal_creation",
        "document_request", "service_appointment",
        "analyze_car_image",
    }
    intent_val = getattr(intent, "value", str(intent)) if intent else ""
    if intent_val not in image_intents:
        return []

    if not IMAGES_ROOT.is_dir():
        return []

    try:
        model_dirs = [d.name for d in IMAGES_ROOT.iterdir() if d.is_dir()]
    except OSError:
        return []

    matched = []
    seen = set()

    # 优先匹配 context 中的 car_model
    car_model = ""
    if isinstance(context, dict):
        car_model = str(context.get("car_model", "")).strip()
    if car_model:
        for name in model_dirs:
            if name in car_model or car_model in name:
                if name not in seen:
                    matched.append(f"/api/v1/images/{name}")
                    seen.add(name)

    if user_message:
        # 1. 精确子串匹配（目录名完整出现在消息中）
        for name in sorted(model_dirs, key=len, reverse=True):
            if name in user_message and name not in seen:
                matched.append(f"/api/v1/images/{name}")
                seen.add(name)

        # 2. 前缀匹配：消息中出现的词是某个目录名的开头
        #    如 "RAV4" 匹配 "RAV4荣放"，"雷克萨斯" 匹配 "雷克萨斯ES"
        for name in sorted(model_dirs, key=len, reverse=True):
            if name in seen:
                continue
            # 从长到短尝试目录名的前缀
            for cut in range(len(name) - 1, 1, -1):
                prefix = name[:cut]
                if prefix in user_message:
                    matched.append(f"/api/v1/images/{name}")
                    seen.add(name)
                    break

    return matched


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="智能销售助手对话接口",
    description="""
    智能销售 AI Agent 的核心对话接口。
    
    支持的场景：
    - 💬 普通对话（问候、闲聊）
    - 📦 产品咨询（基于知识库 RAG）
    - 💰 价格谈判（销售话术支持）
    - 📄 生成报价单（Excel）
    - 📋 创建提案书（Word）
    - 📝 起草合同（Word）
    - 📊 数据分析报表（Excel）
    - 📽️ 生成演示文稿（PPT大纲）
    
    示例请求：
    ```json
    {
        "session_id": "wx_user_openid_123",
        "message": "帮我生成一份报价单，客户是张三科技",
        "history": [],
        "context": {
            "sales_rep_name": "李明",
            "department": "企业销售部"
        }
    }
    ```
    """
)
async def chat(
    request: ChatRequest,
    session_id: str = Depends(get_current_session),
    authorization: Optional[str] = Header(None),
) -> ChatResponse:
    """
    处理用户消息，调用 LangGraph Agent 生成回复
    
    Args:
        request: 聊天请求数据
        session_id: 会话ID（从 Header 或请求体获取）
        authorization: 微信登录凭证
    
    Returns:
        包含 AI 回复、意图识别、建议操作等的响应
    """
    start_time = time.time()
    
    # 使用请求体中的 session_id 优先
    actual_session_id = request.session_id or session_id
    
    logger.info(f"[Session: {actual_session_id}] 收到消息: {request.message[:50]}...")
    
    try:
        # 转换历史消息格式
        history = []
        for msg in request.history:
            history.append({
                "role": msg.role.value,
                "content": msg.content,
            })
        
        # 运行 Agent 工作流
        final_state = await run_sales_agent(
            session_id=actual_session_id,
            message=request.message,
            context=request.context,
            history=history,
        )
        
        # 计算响应时间
        response_time_ms = int((time.time() - start_time) * 1000)
        
        # 构建响应
        intent = final_state.get("intent_analysis")
        intent_value = intent.intent if intent else UserIntent.UNKNOWN
        
        # 确保文档列表格式正确（LangGraph流式处理后可能是dict）
        raw_docs = final_state.get("generated_documents", [])
        docs = []
        for d in raw_docs if isinstance(raw_docs, list) else []:
            if isinstance(d, dict):
                fn = d.get("file_name", d.get("filename", "文档.xlsx"))
                docs.append(DocumentInfo(
                    doc_type=DocumentType(d.get("doc_type", d.get("type", "xlsx"))),
                    file_name=fn,
                    file_path=f"/api/v1/documents/{fn}",
                ))
            elif hasattr(d, 'file_name'):
                # 强制替换路径为API端点
                d = DocumentInfo(
                    doc_type=getattr(d, 'doc_type', DocumentType.XLSX),
                    file_name=d.file_name,
                    file_path=f"/api/v1/documents/{d.file_name}",
                )
                docs.append(d)
        
        logger.info(f"[Session: {actual_session_id}] 文档数: {len(docs)}")

        # 匹配车型图片
        images = _find_car_images(
            user_message=request.message,
            context=final_state.get("context", {}),
            intent=intent_value,
        )

        response = ChatResponse(
            session_id=actual_session_id,
            reply=final_state.get("sales_response", "抱歉，我没有理解您的问题。"),
            intent=intent_value,
            documents=docs,
            images=images,
            suggested_actions=final_state.get("suggested_actions", []),
            metadata={
                "knowledge_results_count": len(final_state.get("knowledge_results", [])),
                "document_params": final_state.get("document_params"),
                "error": final_state.get("error"),
            },
            response_time_ms=response_time_ms,
        )
        
        logger.info(
            f"[Session: {actual_session_id}] 响应完成，"
            f"意图: {intent_value.value}, 耗时: {response_time_ms}ms"
        )
        
        return response
        
    except Exception as e:
        logger.error(f"[Session: {actual_session_id}] 处理失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"处理请求时发生错误: {str(e)}"
        )


@router.post(
    "/chat/stream",
    summary="流式对话接口（预留）",
    description="WebSocket 或 SSE 流式响应接口，用于实时显示思考过程"
)
async def chat_stream(
    request: ChatRequest,
    session_id: str = Depends(get_current_session),
):
    """
    流式对话接口（开发中）
    
    用于实现打字机效果，实时显示 Agent 的思考过程。
    """
    # TODO: 实现 WebSocket 或 SSE 流式响应
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="流式接口开发中"
    )


@router.get(
    "/chat/history/{session_id}",
    summary="获取对话历史",
    description="获取指定会话的历史消息记录"
)
async def get_chat_history(
    session_id: str,
) -> dict:
    """
    获取对话历史
    
    实际项目中应从数据库或缓存中获取。
    """
    # TODO: 从 Redis/数据库获取历史记录
    return {
        "session_id": session_id,
        "messages": [],
        "total": 0,
    }


@router.delete(
    "/chat/history/{session_id}",
    summary="清除对话历史",
    description="清除指定会话的所有历史记录"
)
async def clear_chat_history(
    session_id: str,
) -> dict:
    """
    清除对话历史
    """
    # TODO: 清除 Redis/数据库中的记录
    logger.info(f"[Session: {session_id}] 对话历史已清除")
    return {
        "session_id": session_id,
        "status": "cleared",
    }
