<script setup lang="ts">
import { ref, watch } from 'vue'
import { useECharts } from '../../composables/useECharts'

const props = defineProps<{ data: number[] }>()

const chartRef = ref<HTMLElement | null>(null)
const { setOption } = useECharts(chartRef)

watch(() => props.data, (series) => {
  setOption({
    backgroundColor: 'transparent',
    tooltip: { trigger: 'axis' },
    grid: { left: 40, right: 10, top: 10, bottom: 24 },
    xAxis: {
      type: 'category',
      data: series.map((_, i) => `${series.length - i}s ago`).reverse(),
      axisLabel: { show: false },
      axisTick: { show: false },
      axisLine: { lineStyle: { color: '#30363d' } },
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: '#8b949e', fontSize: 10 },
      splitLine: { lineStyle: { color: '#21262d' } },
    },
    series: [{
      type: 'line',
      data: series,
      smooth: true,
      showSymbol: false,
      lineStyle: { color: '#58a6ff', width: 1.5 },
      areaStyle: { color: { type: 'linear', x: 0, y: 0, x2: 0, y2: 1, colorStops: [{ offset: 0, color: 'rgba(88,166,255,0.3)' }, { offset: 1, color: 'rgba(88,166,255,0.02)' }] } },
    }],
  })
}, { deep: true })
</script>

<template>
  <div class="chart-container">
    <h4 class="chart-title">Events / sec (Timeline)</h4>
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
  min-height: 120px;
}
</style>
