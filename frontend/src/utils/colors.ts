import type { SyscallCategory, Severity } from '../types'

export const categoryColors: Record<SyscallCategory, string> = {
  file: '#f0c674',
  io: '#81a2be',
  network: '#8abeb7',
  process: '#b294bb',
  memory: '#cc6666',
  sync: '#de935f',
  signal: '#a3685a',
  other: '#707880',
}

export const severityColors: Record<Severity, string> = {
  normal: '#8b949e',
  warning: '#d29922',
  slow: '#f85149',
  blocked: '#ff7b72',
}
