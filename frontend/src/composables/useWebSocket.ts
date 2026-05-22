import { ref, watch, onUnmounted } from 'vue'
import type { WsMessage } from '../types/websocket'
import { useEventsStore } from '../stores/events'
import { useStatsStore } from '../stores/stats'
import { useSessionStore } from '../stores/session'

export function useWebSocket() {
  const isConnected = ref(false)
  const error = ref<string | null>(null)
  let ws: WebSocket | null = null
  let pendingBatch: any[] = []
  let rafId: number | null = null

  const eventsStore = useEventsStore()
  const statsStore = useStatsStore()
  const sessionStore = useSessionStore()

  function flush() {
    if (pendingBatch.length > 0) {
      eventsStore.appendBatch(pendingBatch)
      pendingBatch = []
    }
    rafId = null
  }

  function connect(sessionId: string) {
    disconnect()
    const proto = location.protocol === 'https:' ? 'wss:' : 'ws:'
    const url = `${proto}//${location.host}/ws/${sessionId}`
    ws = new WebSocket(url)

    ws.onopen = () => {
      isConnected.value = true
      error.value = null
    }

    ws.onmessage = (ev) => {
      const msg: WsMessage = JSON.parse(ev.data)
      switch (msg.type) {
        case 'batch':
          pendingBatch.push(...msg.data)
          if (rafId === null) rafId = requestAnimationFrame(flush)
          break
        case 'stats':
          statsStore.updateFromWs(msg.data)
          break
        case 'status':
          sessionStore.setStatus(msg.data.state)
          break
      }
    }

    ws.onclose = () => {
      isConnected.value = false
    }

    ws.onerror = () => {
      error.value = 'WebSocket connection failed'
      isConnected.value = false
    }
  }

  function disconnect() {
    if (rafId !== null) {
      cancelAnimationFrame(rafId)
      flush()
    }
    if (ws) {
      ws.close()
      ws = null
    }
    isConnected.value = false
  }

  onUnmounted(disconnect)

  return { isConnected, error, connect, disconnect }
}
