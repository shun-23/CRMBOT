export interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: number
}

export interface ChatRequest {
  session_id: string
  message: string
  history?: { role: string; content: string }[]
  context?: Record<string, unknown>
}

export interface DocumentInfo {
  file_name: string
  file_path: string
  doc_type: string
  file_size: number
}

export interface ChatResponse {
  session_id: string
  reply: string
  intent: string
  documents: DocumentInfo[]
  suggested_actions: string[]
  metadata: Record<string, unknown>
  response_time_ms: number
}
