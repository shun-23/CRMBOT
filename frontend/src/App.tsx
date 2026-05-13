import { useEffect, useRef } from 'react'
import { MessageCircle, Sparkles } from 'lucide-react'
import ChatBubble from './components/ChatBubble'
import ChatInput from './components/ChatInput'
import DownloadButton from './components/DownloadButton'
import { useChat } from './hooks/useChat'

export default function App() {
  const { messages, isLoading, attachedDocs, sendMessage } = useChat()
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  async function handleSend(content: string) {
    try {
      await sendMessage(content)
    } catch {
      // handled in hook
    }
  }

  return (
    <div className="flex h-screen flex-col">
      {/* Header */}
      <header className="flex items-center gap-2 border-b bg-background px-4 py-3 shrink-0">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
          <MessageCircle size={18} className="text-primary-foreground" />
        </div>
        <div className="flex-1">
          <h1 className="text-sm font-semibold">CRMBOT</h1>
          <p className="text-[11px] text-muted-foreground">智能销售 AI Agent</p>
        </div>
        <Sparkles size={16} className="text-muted-foreground" />
      </header>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-4">
        {messages.length === 0 ? (
          <div className="flex h-full flex-col items-center justify-center text-center">
            <div className="flex h-16 w-16 items-center justify-center rounded-full bg-muted mb-4">
              <MessageCircle size={32} className="text-muted-foreground" />
            </div>
            <h2 className="text-lg font-semibold mb-1">你好！我是 CRMBOT</h2>
            <p className="text-sm text-muted-foreground max-w-sm">
              选好车型后，我可以帮你报价、起草合同、预约线下服务等。
            </p>
            <div className="mt-6 flex flex-wrap gap-2 justify-center">
              {[
                '我想了解有哪些车型',
                '帮我生成报价单',
                '帮我起草购车合同',
                '我想预约线下服务',
              ].map((s) => (
                <button
                  key={s}
                  onClick={() => handleSend(s)}
                  disabled={isLoading}
                  className="rounded-full border border-border bg-muted px-3 py-1.5 text-xs hover:bg-muted/80 transition-colors disabled:opacity-40"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        ) : (
          messages.map((msg) => (
            <div key={msg.id}>
              <ChatBubble message={msg} />
              {msg.role === 'assistant' && attachedDocs[msg.id] && attachedDocs[msg.id].length > 0 && (
                <div className="flex flex-col gap-2 pl-2 mb-4">
                  {attachedDocs[msg.id].map((doc, i) => (
                    <DownloadButton
                      key={i}
                      filename={doc.file_name}
                      filePath={doc.file_path}
                    />
                  ))}
                </div>
              )}
            </div>
          ))
        )}

        {isLoading && (
          <div className="flex justify-start mb-4">
            <div className="rounded-2xl rounded-bl-sm bg-muted px-4 py-3">
              <div className="flex gap-1.5">
                <span className="h-2 w-2 animate-bounce rounded-full bg-muted-foreground/40 [animation-delay:0ms]" />
                <span className="h-2 w-2 animate-bounce rounded-full bg-muted-foreground/40 [animation-delay:150ms]" />
                <span className="h-2 w-2 animate-bounce rounded-full bg-muted-foreground/40 [animation-delay:300ms]" />
              </div>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <ChatInput onSend={handleSend} disabled={isLoading} />
    </div>
  )
}
