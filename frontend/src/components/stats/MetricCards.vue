<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  totalCount: number
  eventsPerSec: number
  status: string
  startTime?: string
}>()

const formattedRate = computed(() => {
  if (props.eventsPerSec >= 1000) return `${(props.eventsPerSec / 1000).toFixed(1)}k`
  return String(Math.round(props.eventsPerSec))
})
</script>

<template>
  <div class="metric-cards">
    <div class="metric-card">
      <span class="metric-value mono">{{ totalCount.toLocaleString() }}</span>
      <span class="metric-label">Total Syscalls</span>
    </div>
    <div class="metric-card">
      <span class="metric-value mono">{{ formattedRate }}</span>
      <span class="metric-label">Events / sec</span>
    </div>
    <div class="metric-card">
      <span class="metric-value mono status-dot-inline" :class="'status-c-' + status">{{ status }}</span>
      <span class="metric-label">Status</span>
    </div>
  </div>
</template>

<style scoped>
.metric-cards {
  display: flex;
  gap: var(--space-md);
}

.metric-card {
  display: flex;
  flex-direction: column;
  padding: var(--space-md) var(--space-lg);
  background: var(--bg-tertiary);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-md);
  min-width: 120px;
}

.metric-value {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
}

.metric-label {
  font-size: var(--font-size-xs);
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-top: 2px;
}

.status-c-running { color: var(--success); }
.status-c-finished { color: var(--accent); }
.status-c-error { color: var(--danger); }
.status-c-idle { color: var(--text-muted); }
</style>
