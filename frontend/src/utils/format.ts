export function formatDuration(d: number | null): string {
  if (d === null) return '-'
  if (d >= 1) return `${d.toFixed(3)}s`
  if (d >= 0.001) return `${(d * 1000).toFixed(2)}ms`
  return `${(d * 1000000).toFixed(0)}µs`
}

export function formatTimestamp(ts: string): string {
  return ts
}

export function truncate(s: string, max: number): string {
  return s.length <= max ? s : s.slice(0, max) + '…'
}
