<script setup lang="ts">
import type { SyscallEvent } from '../../types'
import { formatDuration } from '../../utils/format'
import { categoryColors, severityColors } from '../../utils/colors'
import { categoryLabels, severityLabels } from '../../utils/constants'

const props = defineProps<{ event: SyscallEvent | null }>()
const emit = defineEmits<{ close: [] }>()
</script>

<template>
  <div v-if="event" class="event-detail">
    <div class="detail-header">
      <h3 class="detail-title mono">{{ event.syscall }}</h3>
      <button class="close-btn" @click="emit('close')">✕</button>
    </div>

    <div class="detail-body">
      <div class="detail-row">
        <span class="label">ID</span>
        <span class="value mono">{{ event.id }}</span>
      </div>
      <div class="detail-row">
        <span class="label">PID</span>
        <span class="value mono">{{ event.pid }}</span>
      </div>
      <div class="detail-row">
        <span class="label">Time</span>
        <span class="value mono">{{ event.timestamp }}</span>
      </div>
      <div class="detail-row">
        <span class="label">Duration</span>
        <span class="value mono" :class="'severity-' + event.severity">
          {{ formatDuration(event.duration) }}
        </span>
      </div>
      <div class="detail-row">
        <span class="label">Category</span>
        <span class="value">
          <span class="cat-badge" :style="{ background: categoryColors[event.category] + '22', color: categoryColors[event.category], border: '1px solid ' + categoryColors[event.category] + '44' }">
            {{ categoryLabels[event.category] }}
          </span>
        </span>
      </div>
      <div class="detail-row">
        <span class="label">Severity</span>
        <span class="value">
          <span class="sev-badge" :class="'severity-' + event.severity">
            {{ severityLabels[event.severity] }}
          </span>
        </span>
      </div>
      <div class="detail-row">
        <span class="label">Result</span>
        <span class="value mono">{{ event.result }}</span>
      </div>
      <div class="detail-section">
        <span class="label">Arguments</span>
        <pre class="args-block mono">{{ event.args }}</pre>
      </div>
    </div>
  </div>
</template>

<style scoped>
.event-detail {
  width: var(--detail-panel-width);
  background: var(--bg-secondary);
  border-left: 1px solid var(--border-primary);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.detail-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-md) var(--space-lg);
  border-bottom: 1px solid var(--border-primary);
}

.detail-title {
  margin: 0;
  font-size: var(--font-size-lg);
  color: var(--text-primary);
}

.close-btn {
  color: var(--text-secondary);
  font-size: 16px;
  padding: var(--space-xs);
  border-radius: var(--radius-sm);
}
.close-btn:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.detail-body {
  padding: var(--space-lg);
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.detail-row {
  display: flex;
  align-items: baseline;
  gap: var(--space-md);
}

.label {
  font-size: var(--font-size-xs);
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  width: 70px;
  flex-shrink: 0;
}

.value {
  font-size: var(--font-size-sm);
  color: var(--text-primary);
  word-break: break-all;
}

.detail-section {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.args-block {
  margin: 0;
  padding: var(--space-md);
  background: var(--bg-primary);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  color: var(--text-primary);
  white-space: pre-wrap;
  word-break: break-all;
  max-height: 300px;
  overflow-y: auto;
}

.cat-badge {
  display: inline-flex;
  padding: 1px 8px;
  border-radius: var(--radius-sm);
  font-size: var(--font-size-xs);
  font-weight: 500;
}

.sev-badge {
  font-size: var(--font-size-xs);
  font-weight: 500;
}
</style>
