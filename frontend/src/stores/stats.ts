import { reactive } from 'vue'
import type { Stats, SyscallEvent } from '../types'

interface StatsState {
  totalCount: number
  categoryCounts: Record<string, number>
  syscallCounts: Record<string, number>
  topSlow: SyscallEvent[]
  timeSeries: number[]
  timeSeriesTimestamp: number
}

const state = reactive<StatsState>({
  totalCount: 0,
  categoryCounts: {},
  syscallCounts: {},
  topSlow: [],
  timeSeries: [],
  timeSeriesTimestamp: 0,
})

let lastTickCount = 0
let tickInterval: ReturnType<typeof setInterval> | null = null

export function useStatsStore() {
  function updateFromWs(data: Stats) {
    state.totalCount = data.total_count
    state.categoryCounts = data.category_counts
    state.syscallCounts = data.syscall_counts
    state.topSlow = data.top_slow
  }

  function startTimeSeries() {
    lastTickCount = 0
    state.timeSeries = []
    state.timeSeriesTimestamp = Date.now()
    tickInterval = setInterval(() => {
      const delta = state.totalCount - lastTickCount
      lastTickCount = state.totalCount
      state.timeSeries.push(delta)
      if (state.timeSeries.length > 120) state.timeSeries.shift()
    }, 1000)
  }

  function stopTimeSeries() {
    if (tickInterval) {
      clearInterval(tickInterval)
      tickInterval = null
    }
  }

  function reset() {
    stopTimeSeries()
    state.totalCount = 0
    state.categoryCounts = {}
    state.syscallCounts = {}
    state.topSlow = []
    state.timeSeries = []
  }

  return { state, updateFromWs, startTimeSeries, stopTimeSeries, reset }
}
