import { reactive, computed } from 'vue'
import type { SyscallCategory, Severity } from '../types'

interface FilterState {
  categories: Set<SyscallCategory>
  severities: Set<Severity>
  syscallName: string
  pid: number | null
}

const state = reactive<FilterState>({
  categories: new Set(),
  severities: new Set(),
  syscallName: '',
  pid: null,
})

export function useFiltersStore() {
  const hasActiveFilters = computed(() =>
    state.categories.size > 0 || state.severities.size > 0 || state.syscallName !== '' || state.pid !== null
  )

  function toggleCategory(cat: SyscallCategory) {
    if (state.categories.has(cat)) state.categories.delete(cat)
    else state.categories.add(cat)
  }

  function toggleSeverity(sev: Severity) {
    if (state.severities.has(sev)) state.severities.delete(sev)
    else state.severities.add(sev)
  }

  function setSyscallFilter(name: string) {
    state.syscallName = name
  }

  function setPidFilter(pid: number | null) {
    state.pid = pid
  }

  function clearAll() {
    state.categories.clear()
    state.severities.clear()
    state.syscallName = ''
    state.pid = null
  }

  return { state, hasActiveFilters, toggleCategory, toggleSeverity, setSyscallFilter, setPidFilter, clearAll }
}
