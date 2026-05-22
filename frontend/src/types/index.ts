export type SyscallCategory = 'file' | 'io' | 'network' | 'process' | 'memory' | 'sync' | 'signal' | 'other'
export type Severity = 'normal' | 'warning' | 'slow' | 'blocked'

export interface SyscallEvent {
  id: number
  pid: number
  timestamp: string
  syscall: string
  args: string
  result: string
  duration: number | null
  category: SyscallCategory
  severity: Severity
}

export interface SessionInfo {
  id: string
  command: string
  start_time: string
  end_time: string | null
  total_syscalls: number
  status: 'running' | 'finished' | 'error'
}

export interface Stats {
  total_count: number
  category_counts: Record<string, number>
  syscall_counts: Record<string, number>
  top_slow: SyscallEvent[]
}
