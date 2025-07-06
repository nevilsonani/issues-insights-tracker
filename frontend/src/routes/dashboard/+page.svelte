<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchIssues, fetchDailyStats, fetchSeverityStats, fetchAnalytics } from '$lib/api';
  import { user } from '$lib/auth';
  import Chart from '$lib/components/Chart.svelte';

  let issues = [];
  let dailyStats = [];
  let severityStats = {};
  let analytics = null;
  let loading = true;
  let error = '';
  let currentUser: any = null;

  user.subscribe((v) => (currentUser = v));

  async function loadData() {
    loading = true;
    try {
      // Try the new analytics endpoint first
      try {
        analytics = await fetchAnalytics();
        issues = analytics.recent_issues || [];
        error = '';
      } catch (analyticsError) {
        console.log('Analytics endpoint failed, falling back to individual endpoints');
        // Fallback to individual endpoints
        const [issuesData, dailyData, severityData] = await Promise.all([
          fetchIssues(),
          fetchDailyStats(),
          fetchSeverityStats()
        ]);
        issues = issuesData;
        dailyStats = dailyData;
        severityStats = severityData;
        analytics = null;
      }
    } catch (err) {
      error = 'Failed to load dashboard data';
      console.error(err);
    } finally {
      loading = false;
    }
  }

  function getStatusCount(status: string) {
    if (analytics) {
      return analytics.issues_by_status[status] || 0;
    }
    return issues.filter(issue => issue.status === status).length;
  }

  function getSeverityCount(severity: string) {
    if (analytics) {
      return analytics.issues_by_severity[severity] || 0;
    }
    return issues.filter(issue => issue.severity === severity).length;
  }

  function getRecentIssues() {
    if (analytics && analytics.recent_issues) {
      return analytics.recent_issues;
    }
    return issues
      .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
      .slice(0, 5);
  }

  function getTotalIssues() {
    if (analytics) {
      return analytics.total_issues;
    }
    return issues.length;
  }

  function getOpenIssues() {
    if (analytics) {
      return analytics.open_issues;
    }
    return getStatusCount('OPEN');
  }

  function getInProgressIssues() {
    if (analytics) {
      return analytics.in_progress_issues;
    }
    return getStatusCount('IN_PROGRESS');
  }

  function getCompletedIssues() {
    if (analytics) {
      return analytics.completed_issues;
    }
    return getStatusCount('DONE');
  }

  function getOpenIssuesBySeverity(severity: string) {
    if (analytics && analytics.recent_issues) {
      return analytics.recent_issues.filter(issue => issue.status === 'OPEN' && issue.severity === severity).length;
    }
    return issues.filter(issue => issue.status === 'OPEN' && issue.severity === severity).length;
  }

  function getChartDataSafe(arr: number[]) {
    return arr && arr.some(x => x > 0) ? arr : [0, 0, 0];
  }

  onMount(() => {
    loadData();
  });
</script>

<svelte:head>
  <title>Analytics Dashboard - Issues & Insights Tracker</title>
</svelte:head>

<div class="space-y-8 max-w-7xl mx-auto px-2 sm:px-4 md:px-8">
  <!-- Header -->
  <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 animate-in">
    <div>
      <h1 class="text-4xl font-extrabold bg-gradient-to-r from-blue-700 to-blue-400 bg-clip-text text-transparent mb-1">Dashboard</h1>
      <p class="text-gray-500 text-lg">Comprehensive overview of your issue tracking metrics</p>
    </div>
    <div class="flex gap-2 mt-2 md:mt-0">
      <button class="btn-primary shadow-glow">New Issue</button>
      <button class="btn-secondary">View Analytics</button>
    </div>
  </div>

  {#if loading}
    <div class="flex justify-center items-center py-16">
      <svg class="animate-spin h-10 w-10 text-blue-600" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <span class="ml-4 text-xl text-gray-600">Loading analytics...</span>
    </div>
  {:else if error}
    <div class="card animate-in">
      <div class="flex items-center">
        <svg class="h-6 w-6 text-red-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <p class="text-red-800 text-lg">{error}</p>
      </div>
    </div>
  {:else}
    <!-- Key Metrics -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 animate-in">
      <div class="card card-hover flex flex-col items-center text-center shadow-glow">
        <div class="h-12 w-12 bg-gradient-to-br from-blue-500 to-blue-700 rounded-xl flex items-center justify-center mb-3">
          <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
        </div>
        <p class="text-sm font-medium text-gray-500">Total Issues</p>
        <p class="text-3xl font-extrabold text-blue-900">{getTotalIssues()}</p>
      </div>
      <div class="card card-hover flex flex-col items-center text-center">
        <div class="h-12 w-12 bg-gradient-to-br from-yellow-400 to-yellow-600 rounded-xl flex items-center justify-center mb-3">
          <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
        </div>
        <p class="text-sm font-medium text-gray-500">Open Issues</p>
        <p class="text-3xl font-extrabold text-yellow-700">{getOpenIssues()}</p>
      </div>
      <div class="card card-hover flex flex-col items-center text-center">
        <div class="h-12 w-12 bg-gradient-to-br from-orange-400 to-orange-600 rounded-xl flex items-center justify-center mb-3">
          <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
          </svg>
        </div>
        <p class="text-sm font-medium text-gray-500">In Progress</p>
        <p class="text-3xl font-extrabold text-orange-700">{getInProgressIssues()}</p>
      </div>
      <div class="card card-hover flex flex-col items-center text-center">
        <div class="h-12 w-12 bg-gradient-to-br from-green-400 to-green-600 rounded-xl flex items-center justify-center mb-3">
          <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
        </div>
        <p class="text-sm font-medium text-gray-500">Completed</p>
        <p class="text-3xl font-extrabold text-green-700">{getCompletedIssues()}</p>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8 animate-in">
      <!-- Severity Distribution -->
      <div class="card card-hover">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Open Issues by Severity</h3>
        <Chart 
          data={{
            labels: ['Low', 'Medium', 'High'],
            datasets: [{
              data: getChartDataSafe([
                getOpenIssuesBySeverity('LOW'),
                getOpenIssuesBySeverity('MEDIUM'),
                getOpenIssuesBySeverity('HIGH')
              ]),
              backgroundColor: ['#10B981', '#F59E0B', '#EF4444'],
              borderWidth: 0
            }]
          }}
          type="doughnut"
          options={{
            plugins: {
              legend: {
                position: 'bottom'
              }
            }
          }}
        />
      </div>

      <!-- Status Distribution -->
      <div class="card card-hover">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Issues by Status</h3>
        <Chart
          data={{
            labels: ['Open', 'Triaged', 'In Progress', 'Done'],
            datasets: [{
              data: getChartDataSafe([
                getStatusCount('OPEN'),
                getStatusCount('TRIAGED'),
                getStatusCount('IN_PROGRESS'),
                getStatusCount('DONE')
              ]),
              backgroundColor: ['#F59E0B', '#6366F1', '#3B82F6', '#10B981'],
              borderWidth: 0
            }]
          }}
          type="doughnut"
          options={{
            plugins: {
              legend: {
                position: 'bottom'
              }
            }
          }}
        />
      </div>
    </div>

    <!-- Recent Issues Table -->
    <div class="card mt-8 animate-in">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">Recent Issues</h3>
      <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead>
          <tr>
            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Title</th>
            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Severity</th>
            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Created</th>
          </tr>
        </thead>
        <tbody class="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
          {#each getRecentIssues() as issue}
            <tr>
              <td class="px-4 py-2 font-medium text-gray-900 dark:text-white">{issue.title}</td>
              <td class="px-4 py-2">
                <span class="inline-block px-2 py-1 rounded text-xs font-semibold bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">{issue.status}</span>
              </td>
              <td class="px-4 py-2">
                <span class="inline-block px-2 py-1 rounded text-xs font-semibold bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">{issue.severity}</span>
              </td>
              <td class="px-4 py-2 text-gray-500 dark:text-gray-400">{new Date(issue.created_at).toLocaleString()}</td>
            </tr>
          {/each}
        </tbody>
      </table>
      {#if getRecentIssues().length === 0}
        <div class="text-gray-400 text-center py-8">No recent issues found.</div>
      {/if}
    </div>

    <!-- Trends/Summary Section -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8 animate-in">
      <div class="card card-hover">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Trends & Summary</h3>
        <ul class="space-y-2">
          <li><span class="font-bold text-blue-700">{getTotalIssues()}</span> total issues</li>
          <li><span class="font-bold text-yellow-700">{getOpenIssues()}</span> open, <span class="font-bold text-orange-700">{getInProgressIssues()}</span> in progress, <span class="font-bold text-green-700">{getCompletedIssues()}</span> completed</li>
          <li><span class="font-bold text-red-700">{getSeverityCount('HIGH')}</span> high severity, <span class="font-bold text-yellow-600">{getSeverityCount('MEDIUM')}</span> medium, <span class="font-bold text-green-700">{getSeverityCount('LOW')}</span> low</li>
        </ul>
      </div>
      <div class="card card-hover flex flex-col items-center justify-center">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Need more insights?</h3>
        <p class="text-gray-500 mb-4">Export data or view advanced analytics in the future.</p>
        <button class="btn-secondary">Export CSV</button>
      </div>
    </div>
  {/if}
</div> 