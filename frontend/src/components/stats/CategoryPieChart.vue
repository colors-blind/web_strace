<script setup lang="ts">
import { ref, watch } from 'vue'
import { useECharts } from '../../composables/useECharts'
import { categoryColors } from '../../utils/colors'
import { categoryLabels } from '../../utils/constants'
import type { SyscallCategory } from '../../types'

const props = defineProps<{ data: Record<string, number> }>()

const chartRef = ref<HTMLElement | null>(null)
const { setOption } = useECharts(chartRef)

watch(() => props.data, (d) => {
  const entries = Object.entries(d).filter(([, v]) => v > 0)
  setOption({
    backgroundColor: 'transparent',
    tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
    series: [{
      type: 'pie',
      radius: ['45%', '75%'],
      center: ['50%', '50%'],
      label: { show: false },
      itemStyle: { borderColor: '#161b22', borderWidth: 2 },
      data: entries.map(([k, v]) => ({
        name: categoryLabels[k as SyscallCategory] || k,
        value: v,
        itemStyle: { color: categoryColors[k as SyscallCategory] || '#707880' },
      })),
    }],
  })
}, { deep: true })
</script>

<template>
  <div class="chart-container">
    <h4 class="chart-title">Category Distribution</h4>
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
