import { onMounted, onUnmounted, ref, type Ref, watch } from 'vue'
import * as echarts from 'echarts'

export function useECharts(containerRef: Ref<HTMLElement | null>) {
  let chart: echarts.ECharts | null = null

  function init() {
    if (containerRef.value && !chart) {
      chart = echarts.init(containerRef.value, 'dark', { renderer: 'canvas' })
    }
  }

  function setOption(option: echarts.EChartsOption) {
    if (!chart) init()
    chart?.setOption(option, { notMerge: false })
  }

  function resize() {
    chart?.resize()
  }

  onMounted(() => {
    init()
    window.addEventListener('resize', resize)
  })

  onUnmounted(() => {
    window.removeEventListener('resize', resize)
    chart?.dispose()
    chart = null
  })

  return { setOption, resize }
}
