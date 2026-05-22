<script setup lang="ts">
import { ref, watch } from 'vue'
import AppHeader from './components/layout/AppHeader.vue'
import AppSidebar from './components/layout/AppSidebar.vue'
import CommandInput from './components/command/CommandInput.vue'
import FilterBar from './components/filters/FilterBar.vue'
import EventTable from './components/events/EventTable.vue'
import EventDetail from './components/events/EventDetail.vue'
import StatsPanel from './components/stats/StatsPanel.vue'
import { useSessionStore } from './stores/session'
import { useEventsStore } from './stores/events'
import { useStatsStore } from './stores/stats'
import { useWebSocket } from './composables/useWebSocket'
import type { SyscallEvent } from './types'

const sidebarOpen = ref(true)
const selectedEvent = ref<SyscallEvent | null>(null)
const statsCollapsed = ref(false)

const sessionStore = useSessionStore()
const eventsStore = useEventsStore()
const statsStore = useStatsStore()
const ws = useWebSocket()

async function handleStart(command: string) {
  eventsStore.clear()
  statsStore.reset()
  selectedEvent.value = null
  const sessionId = await sessionStore.startSession(command)
  if (sessionId) {
    ws.connect(sessionId)
    statsStore.startTimeSeries()
  }
}

function handleStop() {
  sessionStore.stopSession()
  statsStore.stopTimeSeries()
}

async function handleSelectSession(id: string) {
  ws.disconnect()
  statsStore.stopTimeSeries()
  selectedEvent.value = null
  sessionStore.selectSession(id)
  const events = await sessionStore.loadSessionEvents(id)
  eventsStore.setEvents(events)

  const session = sessionStore.sessionList.find(s => s.id === id)
  if (session) sessionStore.setStatus(session.status as any)

  // Rebuild stats from loaded events
  const categoryCounts: Record<string, number> = {}
  const syscallCounts: Record<string, number> = {}
  const topSlow: SyscallEvent[] = []
  for (const e of events) {
    categoryCounts[e.category] = (categoryCounts[e.category] || 0) + 1
    syscallCounts[e.syscall] = (syscallCounts[e.syscall] || 0) + 1
    if (e.duration && e.duration > 0.01) topSlow.push(e)
  }
  topSlow.sort((a, b) => (b.duration || 0) - (a.duration || 0))
  statsStore.updateFromWs({
    total_count: events.length,
    category_counts: categoryCounts,
    syscall_counts: syscallCounts,
    top_slow: topSlow.slice(0, 20),
  })

  sessionStore.loadSessions()
}

watch(() => sessionStore.sessionStatus.value, (status) => {
  if (status === 'finished' || status === 'error') {
    statsStore.stopTimeSeries()
    sessionStore.loadSessions()
  }
})
</script>

<template>
  <div class="app-shell">
    <AppHeader :sidebar-open="sidebarOpen" @toggle-sidebar="sidebarOpen = !sidebarOpen" />

    <div class="app-body">
      <AppSidebar :open="sidebarOpen" @select-session="handleSelectSession" />

      <main class="main-content">
        <CommandInput
          :status="sessionStore.sessionStatus.value"
          @start="handleStart"
          @stop="handleStop"
        />

        <div class="stats-toggle" @click="statsCollapsed = !statsCollapsed">
          <span class="toggle-icon">{{ statsCollapsed ? '▶' : '▼' }}</span>
          Statistics
        </div>
        <StatsPanel v-show="!statsCollapsed" />

        <FilterBar />

        <EventTable
          :events="eventsStore.filteredEvents.value"
          :selected-id="selectedEvent?.id ?? null"
          @select="selectedEvent = $event"
        />
      </main>

      <EventDetail :event="selectedEvent" @close="selectedEvent = null" />
    </div>
  </div>
</template>

<style scoped>
.app-shell {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.app-body {
  flex: 1;
  display: flex;
  min-height: 0;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
}

.stats-toggle {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-xs) var(--space-lg);
  background: var(--bg-tertiary);
  border-bottom: 1px solid var(--border-primary);
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  cursor: pointer;
  user-select: none;
}
.stats-toggle:hover {
  color: var(--text-primary);
}
.toggle-icon {
  font-size: 8px;
}
</style>
