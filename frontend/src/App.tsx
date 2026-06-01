import { useCallback, useState } from 'react'
import { sendChat, type ChatResponse } from './api/client'
import './App.css'

type ChatItem = {
  role: 'user' | 'assistant'
  text: string
  meta?: ChatResponse
}

const QUICK_PROMPTS = [
  '带我去会议室',
  '附近有什么点位',
  '开灯',
  '这是什么功能',
]

export default function App() {
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [items, setItems] = useState<ChatItem[]>([
    {
      role: 'assistant',
      text: '你好，我是 Skill Agent 控制台。可以试导航、地点、控制或问答。',
    },
  ])

  const submit = useCallback(async (text: string) => {
    const message = text.trim()
    if (!message || loading) return

    setItems((prev) => [...prev, { role: 'user', text: message }])
    setInput('')
    setLoading(true)

    try {
      const res = await sendChat(message)
      const skillLabel = res.skill_name ? `【${res.skill_name}】` : ''
      setItems((prev) => [
        ...prev,
        {
          role: 'assistant',
          text: `${skillLabel}${res.reply}`,
          meta: res,
        },
      ])
    } catch (e) {
      const msg = e instanceof Error ? e.message : '请求失败'
      setItems((prev) => [
        ...prev,
        { role: 'assistant', text: `错误：${msg}。请确认后端已启动（端口 8000）。` },
      ])
    } finally {
      setLoading(false)
    }
  }, [loading])

  return (
    <div className="app">
      <header className="header">
        <h1>Skill Agent</h1>
        <p>前端 → API → 技能路由 → Function Calling</p>
      </header>

      <main className="chat">
        <ul className="messages">
          {items.map((item, i) => (
            <li key={i} className={`msg msg-${item.role}`}>
              <div className="bubble">{item.text}</div>
              {item.meta?.tool_calls && item.meta.tool_calls.length > 0 && (
                <details className="tools">
                  <summary>工具调用 ({item.meta.tool_calls.length})</summary>
                  <pre>{JSON.stringify(item.meta.tool_calls, null, 2)}</pre>
                </details>
              )}
            </li>
          ))}
          {loading && (
            <li className="msg msg-assistant">
              <div className="bubble typing">思考中…</div>
            </li>
          )}
        </ul>

        <div className="quick">
          {QUICK_PROMPTS.map((p) => (
            <button
              key={p}
              type="button"
              className="chip"
              disabled={loading}
              onClick={() => submit(p)}
            >
              {p}
            </button>
          ))}
        </div>

        <form
          className="composer"
          onSubmit={(e) => {
            e.preventDefault()
            submit(input)
          }}
        >
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="输入指令，例如：带我去前台"
            disabled={loading}
          />
          <button type="submit" disabled={loading || !input.trim()}>
            发送
          </button>
        </form>
      </main>
    </div>
  )
}
