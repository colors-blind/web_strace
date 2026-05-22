<script setup lang="ts">
import type { SyscallEvent } from '../../types'
import { formatDuration } from '../../utils/format'
import { categoryColors, severityColors } from '../../utils/colors'

const props = defineProps<{
  event: SyscallEvent
  selected: boolean
}>()

const emit = defineEmits<{ select: [event: SyscallEvent] }>()
</script>

<template>
  <div
    class="event-row mono"
    :class="['severity-row-' + event.severity, { selected }]"
    @click="emit('select', event)"
  >
    <span class="col col-id">{{ event.id }}</span>
    <span class="col col-time">{{ event.timestamp }}</span>
    <span class="col col-pid">{{ event.pid }}</span>
    <span class="col col-syscall">{{ event.syscall }}</span>
    <span class="col col-args truncate">{{ event.args }}</span>
    <span class="col col-result">{{ event.result }}</span>
    <span class="col col-duration" :class="'severity-' + event.severity">
      {{ formatDuration(event.duration) }}
    </span>
    <span class="col col-cat">
      <span class="cat-dot" :style="{ background: categoryColors[event.category] }"></span>
    </span>
  </div>
</template>

<style scoped>
.event-row {
  display: flex;
  align-items: center;
  height: var(--row-height);
  padding: 0 var(--space-sm);
  font-size: var(--font-size-sm);
  cursor: pointer;
  border-bottom: 1px solid var(--border-subtle);
  transition: background var(--transition);
}
.event-row:hover {
  background: var(--bg-tertiary);
}
.event-row.selected {
  background: rgba(88, 166, 255, 0.08);
  border-left: 2px solid var(--accent);
}

.severity-row-warning { background: rgba(210, 153, 34, 0.04); }
.severity-row-slow { background: rgba(248, 81, 73, 0.06); }
.severity-row-blocked { background: rgba(255, 123, 114, 0.1); }

.col { padding: 0 var(--space-xs); white-space: nowrap; }
.col-id { width: 50px; color: var(--text-muted); text-align: right; }
.col-time { width: 110px; color: var(--text-secondary); }
.col-pid { width: 50px; color: var(--text-secondary); text-align: right; }
.col-syscall { width: 100px; color: var(--text-primary); font-weight: 500; }
.col-args { flex: 1; min-width: 0; color: var(--text-secondary); }
.col-result { width: 80px; color: var(--text-secondary); }
.col-duration { width: 80px; text-align: right; }
.col-cat { width: 24px; display: flex; justify-content: center; }

.cat-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}
</style>
