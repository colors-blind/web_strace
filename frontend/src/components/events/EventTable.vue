<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import type { SyscallEvent } from '../../types'
import { useVirtualScroll } from '../../composables/useVirtualScroll'
import EventRow from './EventRow.vue'

const props = defineProps<{
  events: SyscallEvent[]
  selectedId: number | null
}>()

const emit = defineEmits<{ select: [event: SyscallEvent] }>()

const containerRef = ref<HTMLElement | null>(null)
const itemCount = computed(() => props.events.length)

const ROW_HEIGHT = 28
const BUFFER = 15

const { startIndex, endIndex, totalHeight, offsetY, pinToBottom, scrollToBottom, autoScroll } = useVirtualScroll({
  itemHeight: ROW_HEIGHT,
  buffer: BUFFER,
  containerRef,
  itemCount,
})

const visibleEvents = computed(() => props.events.slice(startIndex.value, endIndex.value))

watch(() => props.events.length, () => {
  nextTick(autoScroll)
})
</script>

<template>
  <div class="event-table">
    <div class="table-header mono">
      <span class="col col-id">#</span>
      <span class="col col-time">Time</span>
      <span class="col col-pid">PID</span>
      <span class="col col-syscall">Syscall</span>
      <span class="col col-args">Args</span>
      <span class="col col-result">Result</span>
      <span class="col col-duration">Duration</span>
      <span class="col col-cat"></span>
    </div>
    <div ref="containerRef" class="table-body">
      <div class="scroll-sentinel" :style="{ height: totalHeight + 'px' }">
        <div class="visible-rows" :style="{ transform: `translateY(${offsetY}px)` }">
          <EventRow
            v-for="event in visibleEvents"
            :key="event.id"
            :event="event"
            :selected="event.id === selectedId"
            @select="emit('select', $event)"
          />
        </div>
      </div>
    </div>
    <div v-if="!pinToBottom && events.length > 0" class="jump-btn" @click="scrollToBottom">
      ↓ Jump to latest
    </div>
  </div>
</template>

<style scoped>
.event-table {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  position: relative;
}

.table-header {
  display: flex;
  align-items: center;
  height: var(--row-height);
  padding: 0 var(--space-sm);
  background: var(--bg-tertiary);
  border-bottom: 1px solid var(--border-primary);
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  flex-shrink: 0;
}

.table-body {
  flex: 1;
  overflow-y: auto;
  min-height: 0;
}

.scroll-sentinel {
  position: relative;
}

.visible-rows {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
}

.col { padding: 0 var(--space-xs); white-space: nowrap; }
.col-id { width: 50px; text-align: right; }
.col-time { width: 110px; }
.col-pid { width: 50px; text-align: right; }
.col-syscall { width: 100px; }
.col-args { flex: 1; }
.col-result { width: 80px; }
.col-duration { width: 80px; text-align: right; }
.col-cat { width: 24px; }

.jump-btn {
  position: absolute;
  bottom: var(--space-lg);
  left: 50%;
  transform: translateX(-50%);
  background: var(--accent);
  color: #fff;
  padding: var(--space-xs) var(--space-lg);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
  z-index: 10;
}
.jump-btn:hover {
  background: var(--accent-hover);
}
</style>
