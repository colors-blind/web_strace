import { ref, reactive } from 'vue'
import type { SessionInfo } from '../types'

const currentSessionId = ref<string | null>(null)
const sessionStatus = ref<'idle' | 'running' | 'finished' | 'error'>('idle')
const sessionList = ref<SessionInfo[]>([])
const currentCommand = ref('')

export function useSessionStore() {
  async function startSession(command: string): Promise<string | null> {
    const res = await fetch('/api/start', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ command }),
    })
    if (!res.ok) return null
    const data = await res.json()
    currentSessionId.value = data.session_id
    currentCommand.value = command
    sessionStatus.value = 'running'
    return data.session_id
  }

  async function stopSession() {
    if (!currentSessionId.value) return
    await fetch(`/api/stop/${currentSessionId.value}`, { method: 'POST' })
    sessionStatus.value = 'finished'
  }

  async function loadSessions() {
    const res = await fetch('/api/sessions')
    if (res.ok) sessionList.value = await res.json()
  }

  async function loadSessionEvents(sessionId: string): Promise<any[]> {
    const res = await fetch(`/api/sessions/${sessionId}/events?limit=10000`)
    if (res.ok) return await res.json()
    return []
  }

  function setStatus(s: 'running' | 'finished' | 'error') {
    sessionStatus.value = s
  }

  function selectSession(id: string) {
    currentSessionId.value = id
  }

  return {
    currentSessionId,
    sessionStatus,
    sessionList,
    currentCommand,
    startSession,
    stopSession,
    loadSessions,
    loadSessionEvents,
    setStatus,
    selectSession,
  }
}
