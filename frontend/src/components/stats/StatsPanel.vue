<script setup lang="ts">
import { computed } from 'vue'
import MetricCards from './MetricCards.vue'
import CategoryPieChart from './CategoryPieChart.vue'
import SlowSyscallsBar from './SlowSyscallsBar.vue'
import TimelineChart from './TimelineChart.vue'
import { useStatsStore } from '../../stores/stats'
import { useSessionStore } from '../../stores/session'

const { state: stats } = useStatsStore()
const { sessionStatus } = useSessionStore()

const eventsPerSec = computed(() => {
  const ts = stats.timeSeries
  if (ts.length === 0) return 0
  const recent = ts.slice(-5)
  return recent.reduce((a, b) => a + b, 0) / recent.length
})
</script>

<template>
  <div class="stats-panel">
    <MetricCards
      :total-count="stats.totalCount"
      :events-per-sec="eventsPerSec"
      :status="sessionStatus"
    />
    <div class="charts-grid">
      <CategoryPieChart :data="stats.categoryCounts" />
      <SlowSyscallsBar :data="stats.topSlow" />
      <TimelineChart :data="stats.timeSeries" />
    </div>
  </div>
</template>

<style scoped>
.stats-panel {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
  padding: var(--space-lg);
  border-bottom: 1px solid var(--border-primary);
}

.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: var(--space-md);
}

@media (max-width: 1200px) {
  .charts-grid {
    grid-template-columns: 1fr 1fr;
  }
}
</style>
