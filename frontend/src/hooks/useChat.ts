import { useChatStore, generateId } from '@/stores/chat'
import { sendChatMessage } from '@/api/chat'
import { useCallback, useRef } from 'react'
import type { ChatMessage, DocumentInfo } from '@/types'

export function useChat() {
  const { messages, isLoading, sessionId, attachedDocs, addMessage, attachDocuments, setLoading } = useChatStore()
  const historyRef = useRef<{ role: string; content: string }[]>([])

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim() || isLoading) return

    const userMsg: ChatMessage = {
      id: generateId(),
      role: 'user',
      content: content.trim(),
      timestamp: Date.now(),
    }
    addMessage(userMsg)
    setLoading(true)

    historyRef.current = [
      ...historyRef.current,
      { role: 'user', content: content.trim() },
    ]

    try {
      const res = await sendChatMessage(sessionId, content.trim(), historyRef.current)

      const msgId = generateId()
      const assistantMsg: ChatMessage = {
        id: msgId,
        role: 'assistant',
        content: res.reply,
        timestamp: Date.now(),
      }
      addMessage(assistantMsg)

      // Attach documents from response
      if (res.documents && res.documents.length > 0) {
        // Map backend response documents to frontend DocumentInfo
        const docs: DocumentInfo[] = res.documents.map((d: any) => ({
          file_name: d.filename || d.file_name,
          file_path: d.path || d.file_path || `/api/v1/docs/documents/${encodeURIComponent(d.filename || d.file_name)}`,
          doc_type: d.type || d.doc_type || 'unknown',
          file_size: d.size || d.file_size || 0,
        }))
        attachDocuments(msgId, docs)
      }

      historyRef.current = [
        ...historyRef.current,
        { role: 'assistant', content: res.reply },
      ]

      return res
    } catch (err) {
      const errorMsg: ChatMessage = {
        id: generateId(),
        role: 'assistant',
        content: '抱歉，请求出错了，请稍后重试。',
        timestamp: Date.now(),
      }
      addMessage(errorMsg)
      throw err
    } finally {
      setLoading(false)
    }
  }, [isLoading, sessionId, addMessage, attachDocuments, setLoading])

  return {
    messages,
    isLoading,
    sessionId,
    attachedDocs,
    sendMessage,
  }
}
