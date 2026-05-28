from app.api.v1.chat import router as chat_router
from app.api.v1.documents import router as documents_router
from app.api.v1.images import router as images_router

__all__ = ["chat_router", "documents_router", "images_router"]
