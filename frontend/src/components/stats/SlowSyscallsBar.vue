<script setup lang="ts">
import { ref, watch } from 'vue'
import { useECharts } from '../../composables/useECharts'
import { severityColors } from '../../utils/colors'
import type { SyscallEvent } from '../../types'

const props = defineProps<{ data: SyscallEvent[] }>()

const chartRef = ref<HTMLElement | null>(null)
const { setOption } = useECharts(chartRef)

watch(() => props.data, (items) => {
  const top = items.slice(0, 15)
  setOption({
    backgroundColor: 'transparent',
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    grid: { left: 100, right: 20, top: 10, bottom: 20 },
    xAxis: {
      type: 'value',
      axisLabel: { color: '#8b949e', fontSize: 10, formatter: (v: number) => v >= 1 ? `${v.toFixed(1)}s` : `${(v * 1000).toFixed(0)}ms` },
      splitLine: { lineStyle: { color: '#21262d' } },
    },
    yAxis: {
      type: 'category',
      data: top.map(e => `${e.syscall}#${e.id}`).reverse(),
      axisLabel: {
        color: '#8b949e',
        fontSize: 10,
        formatter: (v: string) => v.split('#')[0],
      },
      axisTick: { show: false },
      axisLine: { show: false },
    },
    series: [{
      type: 'bar',
      data: top.map(e => ({
        value: e.duration || 0,
        itemStyle: { color: severityColors[e.severity], borderRadius: [0, 2, 2, 0] },
      })).reverse(),
      barWidth: 14,
    }],
  })
}, { deep: true })
</script>

<template>
  <div class="chart-container">
    <h4 class="chart-title">Slowest Syscalls</h4>
    <div ref="chartRef" class="chart"></div>
  </div>
</template>

<style scoped>
.chart-container {
  display: flex;
  flex-direction: column;
  background: var(--bg-secondary);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-md);
  padding: var(--space-md);
}
.chart-title {
  margin: 0 0 var(--space-sm);
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  font-weight: 500;
}
.chart {
  flex: 1;
  min-height: 180px;
}
</style>
