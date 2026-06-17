import type { ChatMessage, DocumentInfo } from '@/types'
import { create } from 'zustand'

interface ChatStore {
  messages: ChatMessage[]
  isLoading: boolean
  sessionId: string
  attachedDocs: Record<string, DocumentInfo[]>
  attachedImages: Record<string, string[]>
  addMessage: (msg: ChatMessage) => void
  attachDocuments: (messageId: string, docs: DocumentInfo[]) => void
  attachImages: (messageId: string, images: string[]) => void
  setLoading: (loading: boolean) => void
  clearMessages: () => void
}

function generateId(): string {
  return `msg_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`
}

function getSessionId(): string {
  let id = sessionStorage.getItem('crmbot_session')
  if (!id) {
    id = `session_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`
    sessionStorage.setItem('crmbot_session', id)
  }
  return id
}

export const useChatStore = create<ChatStore>((set) => ({
  messages: [],
  isLoading: false,
  sessionId: getSessionId(),
  attachedDocs: {},
  attachedImages: {},

  addMessage: (msg) =>
    set((state) => ({ messages: [...state.messages, msg] })),

  attachDocuments: (messageId, docs) =>
    set((state) => ({
      attachedDocs: { ...state.attachedDocs, [messageId]: docs },
    })),

  attachImages: (messageId, images) =>
    set((state) => ({
      attachedImages: { ...state.attachedImages, [messageId]: images },
    })),

  setLoading: (loading) => set({ isLoading: loading }),

  clearMessages: () => set({ messages: [], attachedDocs: {}, attachedImages: {} }),
}))

export { generateId }
