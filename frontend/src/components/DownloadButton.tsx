import { useState, useCallback } from 'react'
import { Download, FileSpreadsheet, FileText, File, Loader2, Check } from 'lucide-react'

interface Props {
  filename: string
  filePath?: string
}

function getFileIcon(filename: string) {
  const ext = filename.split('.').pop()?.toLowerCase()
  switch (ext) {
    case 'xlsx': case 'xls': case 'csv': return FileSpreadsheet
    case 'docx': case 'doc': return FileText
    default: return File
  }
}

export default function DownloadButton({ filename, filePath }: Props) {
  const [downloading, setDownloading] = useState(false)
  const [done, setDone] = useState(false)
  const FileIcon = getFileIcon(filename)

  const handleDownload = useCallback(async () => {
    if (downloading || done) return
    setDownloading(true)
    try {
      const url = filePath || `/api/v1/docs/documents/${encodeURIComponent(filename)}`
      const link = document.createElement('a')
      link.href = url; link.download = filename
      document.body.appendChild(link); link.click(); document.body.removeChild(link)
      setDone(true)
      setTimeout(() => setDone(false), 2000)
    } finally {
      setDownloading(false)
    }
  }, [filename, filePath, downloading, done])

  if (!filename) return null

  return (
    <button
      onClick={handleDownload}
      disabled={downloading}
      className="group inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg transition-all hover:brightness-110 disabled:opacity-60"
      style={{
        background: 'linear-gradient(135deg, rgba(15,23,42,0.85), rgba(30,41,59,0.9))',
        border: '1px solid rgba(56,189,248,0.2)',
      }}
    >
      <FileIcon className="w-3.5 h-3.5 text-sky-400 shrink-0" />
      <span className="text-xs text-slate-200 truncate max-w-[160px]">{filename}</span>
      {downloading ? (
        <Loader2 className="w-3 h-3 text-sky-400 animate-spin shrink-0" />
      ) : done ? (
        <Check className="w-3 h-3 text-green-400 shrink-0" />
      ) : (
        <Download className="w-3 h-3 text-sky-400 shrink-0" />
      )}
    </button>
  )
}
