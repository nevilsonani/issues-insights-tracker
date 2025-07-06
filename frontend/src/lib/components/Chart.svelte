<script lang="ts">
  export let data: any;
  export let type: 'doughnut' | 'bar' | 'line' = 'doughnut';
  export let options: any = {};

  function getChartData() {
    if (!data || !data.labels || !data.datasets) return [];
    
    return data.labels.map((label: string, index: number) => ({
      label,
      value: data.datasets[0].data[index] || 0,
      color: data.datasets[0].backgroundColor?.[index] || '#3B82F6'
    }));
  }

  function getTotal() {
    const chartData = getChartData();
    return chartData.reduce((sum, item) => sum + item.value, 0);
  }

  function getPercentage(value: number) {
    const total = getTotal();
    return total > 0 ? (value / total) * 100 : 0;
  }
</script>

<div class="chart-container flex flex-col items-center justify-center">
  {#if getChartData().length === 0 || getTotal() === 0}
    <div class="text-gray-400 text-lg py-12">No data to display</div>
  {:else if type === 'doughnut'}
    <div class="mb-2 text-2xl font-bold text-gray-900 dark:text-white">{getTotal()}</div>
    <div class="relative w-full h-64 flex items-center justify-center">
      <svg class="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
        {#if getChartData().filter(item => item.value > 0).length === 1}
          <!-- Draw a full circle if only one value is nonzero -->
          <circle cx="50" cy="50" r="40" fill={getChartData().find(item => item.value > 0).color} stroke="white" stroke-width="2" />
        {:else}
          {#each getChartData() as item, index}
            {@const percentage = getPercentage(item.value)}
            {@const startAngle = getChartData().slice(0, index).reduce((sum, i) => sum + getPercentage(i.value), 0) * 3.6}
            {@const endAngle = startAngle + percentage * 3.6}
            {@const x1 = 50 + 40 * Math.cos(startAngle * Math.PI / 180)}
            {@const y1 = 50 + 40 * Math.sin(startAngle * Math.PI / 180)}
            {@const x2 = 50 + 40 * Math.cos(endAngle * Math.PI / 180)}
            {@const y2 = 50 + 40 * Math.sin(endAngle * Math.PI / 180)}
            {@const largeArcFlag = percentage > 50 ? 1 : 0}
            <path
              d="M 50 50 L {x1} {y1} A 40 40 0 {largeArcFlag} 1 {x2} {y2} Z"
              fill={item.color}
              stroke="white"
              stroke-width="2"
            />
          {/each}
        {/if}
      </svg>
      <div class="absolute bottom-2 left-1/2 -translate-x-1/2 text-sm text-gray-500 dark:text-gray-400">Total</div>
    </div>
    <div class="mt-4 space-y-2 w-full">
      {#each getChartData() as item}
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <div class="w-3 h-3 rounded-full" style="background-color: {item.color}"></div>
            <span class="text-sm text-gray-700 dark:text-gray-300">{item.label}</span>
          </div>
          <span class="text-sm font-medium text-gray-900 dark:text-white">{item.value}</span>
        </div>
      {/each}
    </div>
  {:else}
    <div class="space-y-2 w-full">
      {#each getChartData() as item}
        <div class="flex items-center space-x-3">
          <div class="w-20 text-sm text-gray-600 dark:text-gray-400">{item.label}</div>
          <div class="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-4">
            <div 
              class="h-4 rounded-full transition-all duration-300" 
              style="width: {getPercentage(item.value)}%; background-color: {item.color}"
            ></div>
          </div>
          <div class="w-12 text-sm font-medium text-gray-900 dark:text-white">{item.value}</div>
        </div>
      {/each}
    </div>
  {/if}
</div>
