import { reactive, computed, triggerRef, ref } from 'vue'
import type { SyscallEvent } from '../types'
import { useFiltersStore } from './filters'

const MAX_EVENTS = 200000

const events = ref<SyscallEvent[]>([])
const version = ref(0)

export function useEventsStore() {
  const { state: filters } = useFiltersStore()

  const filteredEvents = computed(() => {
    const _ = version.value
    const arr = events.value
    if (!filters.categories.size && !filters.severities.size && !filters.syscallName && filters.pid === null) {
      return arr
    }
    return arr.filter(e => {
      if (filters.categories.size && !filters.categories.has(e.category)) return false
      if (filters.severities.size && !filters.severities.has(e.severity)) return false
      if (filters.syscallName && !e.syscall.includes(filters.syscallName)) return false
      if (filters.pid !== null && e.pid !== filters.pid) return false
      return true
    })
  })

  function appendBatch(batch: SyscallEvent[]) {
    const arr = events.value
    arr.push(...batch)
    if (arr.length > MAX_EVENTS) {
      events.value = arr.slice(arr.length - MAX_EVENTS)
    }
    version.value++
  }

  function setEvents(data: SyscallEvent[]) {
    events.value = data
    version.value++
  }

  function clear() {
    events.value = []
    version.value++
  }

  return { events, filteredEvents, appendBatch, setEvents, clear }
}
