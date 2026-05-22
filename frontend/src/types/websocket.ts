import type { SyscallEvent, Stats } from '.'

export interface WsBatchMessage {
  type: 'batch'
  data: SyscallEvent[]
}

export interface WsStatsMessage {
  type: 'stats'
  data: Stats
}

export interface WsStatusMessage {
  type: 'status'
  data: { state: 'running' | 'finished' | 'error'; message: string }
}

export type WsMessage = WsBatchMessage | WsStatsMessage | WsStatusMessage
