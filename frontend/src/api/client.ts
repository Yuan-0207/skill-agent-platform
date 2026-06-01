export type ChatResponse = {
  reply: string
  skill_id: string | null
  skill_name: string | null
  tool_calls: Array<Record<string, unknown>>
  data: Record<string, unknown>
}

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? ''

export async function sendChat(message: string): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/api/v1/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, context: {} }),
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || `HTTP ${res.status}`)
  }
  return res.json() as Promise<ChatResponse>
}

export async function checkHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/health`)
    return res.ok
  } catch {
    return false
  }
}
