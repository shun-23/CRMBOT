import type { ChatRequest, ChatResponse } from '@/types'

const API_BASE = '/api/v1'

export async function sendChatMessage(
  sessionId: string,
  message: string,
  history?: { role: string; content: string }[]
): Promise<ChatResponse> {
  const body: ChatRequest = {
    session_id: sessionId,
    message,
    history,
  }

  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })

  if (!res.ok) {
    throw new Error(`Chat API error: ${res.status}`)
  }

  return res.json()
}
