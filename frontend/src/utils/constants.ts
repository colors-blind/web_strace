import type { SyscallCategory, Severity } from '../types'

export const categoryLabels: Record<SyscallCategory, string> = {
  file: 'File',
  io: 'I/O',
  network: 'Network',
  process: 'Process',
  memory: 'Memory',
  sync: 'Sync',
  signal: 'Signal',
  other: 'Other',
}

export const severityLabels: Record<Severity, string> = {
  normal: 'Normal',
  warning: 'Warning (>10ms)',
  slow: 'Slow (>100ms)',
  blocked: 'Blocked (>1s)',
}

export const allCategories: SyscallCategory[] = ['file', 'io', 'network', 'process', 'memory', 'sync', 'signal', 'other']
export const allSeverities: Severity[] = ['normal', 'warning', 'slow', 'blocked']
