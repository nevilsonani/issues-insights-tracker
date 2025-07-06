<script lang="ts">
  import { onMount, tick } from 'svelte';
  import { goto } from '$app/navigation';
  import { fetchAnalytics, fetchIssues } from '$lib/api';
  import { user } from '$lib/auth';
  import Chart from '$lib/components/Chart.svelte';
  import { fade, fly } from 'svelte/transition';
  import { cubicOut } from 'svelte/easing';

  let analytics = null;
  let issues = [];
  let loading = true;
  let error = '';
  let currentUser: any = null;
  let selectedTimeframe = 'all'; // all, week, month

  // Animated counters
  let animatedKPI = {
    total: 0,
    completion: 0,
    avgResolution: 0,
    active: 0
  };

  user.subscribe((v) => (currentUser = v));

  async function loadData() {
    loading = true;
    try {
      const [analyticsData, issuesData] = await Promise.all([
        fetchAnalytics(),
        fetchIssues()
      ]);
      analytics = analyticsData;
      issues = issuesData;
      error = '';
    } catch (err) {
      error = 'Failed to load analytics data';
      console.error(err);
    } finally {
      loading = false;
    }
  }

  function getFilteredIssues() {
    if (selectedTimeframe === 'all') return issues;
    const now = new Date();
    const filterDate = new Date();
    if (selectedTimeframe === 'week') {
      filterDate.setDate(now.getDate() - 7);
    } else if (selectedTimeframe === 'month') {
      filterDate.setMonth(now.getMonth() - 1);
    }
    return issues.filter(issue => new Date(issue.created_at) >= filterDate);
  }

  function getIssuesByStatus() {
    const filteredIssues = getFilteredIssues();
    const statusCounts = {
      'OPEN': 0,
      'TRIAGED': 0,
      'IN_PROGRESS': 0,
      'DONE': 0
    };
    filteredIssues.forEach(issue => {
      statusCounts[issue.status]++;
    });
    return statusCounts;
  }

  function getIssuesBySeverity() {
    const filteredIssues = getFilteredIssues();
    const severityCounts = {
      'LOW': 0,
      'MEDIUM': 0,
      'HIGH': 0
    };
    filteredIssues.forEach(issue => {
      severityCounts[issue.severity]++;
    });
    return severityCounts;
  }

  function getIssuesByPriority() {
    const filteredIssues = getFilteredIssues();
    const priorityCounts = {
      'BLOCKER': 0,
      'CRITICAL': 0,
      'MINOR': 0,
      'TRIVIAL': 0
    };
    filteredIssues.forEach(issue => {
      if (issue.priority) {
        priorityCounts[issue.priority]++;
      }
    });
    return priorityCounts;
  }

  function getAverageResolutionTime() {
    const completedIssues = issues.filter(issue => issue.status === 'DONE');
    if (completedIssues.length === 0) return 0;
    const totalTime = completedIssues.reduce((sum, issue) => {
      const created = new Date(issue.created_at);
      const updated = new Date(issue.updated_at || issue.created_at);
      return sum + (updated.getTime() - created.getTime());
    }, 0);
    return Math.round(totalTime / completedIssues.length / (1000 * 60 * 60 * 24)); // days
  }

  // Animate KPI counters
  async function animateKPIs() {
    let total = getFilteredIssues().length;
    let completion = total > 0 ? Math.round((getIssuesByStatus().DONE / total) * 100) : 0;
    let avgResolution = getAverageResolutionTime();
    let active = getIssuesByStatus().OPEN + getIssuesByStatus().IN_PROGRESS;
    const targets = { total, completion, avgResolution, active };
    for (const key of Object.keys(animatedKPI)) {
      let start = 0;
      let end = targets[key];
      let duration = 800;
      let startTime = performance.now();
      function step(now) {
        let progress = Math.min((now - startTime) / duration, 1);
        animatedKPI[key] = Math.floor(start + (end - start) * progress);
        if (progress < 1) {
          requestAnimationFrame(step);
        } else {
          animatedKPI[key] = end;
        }
      }
      requestAnimationFrame(step);
      await tick();
    }
  }

  onMount(async () => {
    await loadData();
    animateKPIs();
  });
</script>

<svelte:head>
  <title>Advanced Analytics - IssueTracker Pro</title>
</svelte:head>

<div class="min-h-screen relative overflow-hidden">
  <div class="absolute inset-0 -z-10">
    <div class="absolute -top-32 -left-32 w-[500px] h-[500px] bg-gradient-to-br from-purple-400/30 via-blue-400/20 to-pink-400/20 rounded-full blur-3xl animate-pulse-slow"></div>
    <div class="absolute top-1/2 right-0 w-[400px] h-[400px] bg-gradient-to-br from-pink-400/20 via-blue-400/20 to-purple-400/30 rounded-full blur-3xl animate-pulse-slow"></div>
    <div class="absolute bottom-0 left-1/2 w-[300px] h-[300px] bg-gradient-to-br from-purple-400/20 via-blue-400/20 to-pink-400/30 rounded-full blur-2xl animate-pulse-slow"></div>
  </div>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="space-y-8">
      <!-- Hero Section with animation -->
      <div class="relative overflow-hidden rounded-3xl bg-gradient-to-r from-white/80 via-purple-50/60 to-blue-50/60 dark:from-gray-800/80 dark:via-purple-900/40 dark:to-blue-900/40 border border-white/20 dark:border-gray-700/50 shadow-2xl backdrop-blur-sm animate-fade-in">
        <div class="absolute inset-0 bg-gradient-to-r from-purple-600/10 via-blue-600/10 to-indigo-600/10 dark:from-purple-400/5 dark:via-blue-400/5 dark:to-indigo-400/5"></div>
        <div class="relative p-8">
          <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
            <div class="flex-1">
              <h1 class="text-4xl md:text-5xl font-bold bg-gradient-to-r from-purple-700 via-blue-700 to-indigo-700 dark:from-purple-300 dark:via-blue-300 dark:to-indigo-300 bg-clip-text text-transparent mb-3 animate-slide-in-up">
                Advanced Analytics
              </h1>
              <p class="text-xl text-gray-600 dark:text-gray-300 mb-6 animate-fade-in delay-200">
                Deep insights into your issue tracking performance
              </p>
              <!-- Action Buttons -->
              <div class="flex flex-wrap gap-4">
                <button
                  on:click={() => goto('/issues/new')}
                  class="group relative inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 dark:from-blue-500 dark:to-blue-600 dark:hover:from-blue-600 dark:hover:to-blue-700 text-white font-semibold rounded-2xl shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300 animate-pop-in"
                >
                  <svg class="w-5 h-5 mr-3 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                  </svg>
                  Create New Issue
                  <div class="absolute inset-0 bg-white/20 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity"></div>
                </button>
                <button
                  on:click={() => goto('/dashboard')}
                  class="group relative inline-flex items-center px-8 py-4 bg-gradient-to-r from-gray-600 to-gray-700 hover:from-gray-700 hover:to-gray-800 dark:from-gray-500 dark:to-gray-600 dark:hover:from-gray-600 dark:hover:to-gray-700 text-white font-semibold rounded-2xl shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300 animate-pop-in delay-200"
                >
                  <svg class="w-5 h-5 mr-3 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5a2 2 0 012-2h4a2 2 0 012 2v6H8V5z"></path>
                  </svg>
                  Back to Dashboard
                  <div class="absolute inset-0 bg-white/20 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity"></div>
                </button>
              </div>
            </div>
            <div class="hidden lg:block">
              <div class="w-24 h-24 bg-gradient-to-br from-purple-500 via-blue-500 to-indigo-500 rounded-3xl flex items-center justify-center shadow-2xl transform -rotate-12 hover:rotate-0 transition-transform duration-500 animate-float">
                <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- KPI Cards with animation -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mt-8">
        {#each [
          { label: 'Total Issues', value: animatedKPI.total, color: 'from-blue-500 to-blue-600', icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z' },
          { label: 'Completion Rate', value: animatedKPI.completion + '%', color: 'from-green-500 to-green-600', icon: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z' },
          { label: 'Avg Resolution', value: animatedKPI.avgResolution + ' days', color: 'from-orange-500 to-orange-600', icon: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z' },
          { label: 'Active Issues', value: animatedKPI.active, color: 'from-purple-500 to-purple-600', icon: 'M13 7h8m0 0v8m0-8l-8 8-4-4-6 6' }
        ] as card, i}
          <div in:fly="{{ y: 40, duration: 600, delay: i * 120 }}" class="group relative overflow-hidden bg-white/80 dark:bg-gray-800/80 rounded-3xl shadow-xl hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-300 border border-gray-100 dark:border-gray-700 animate-fade-in">
            <div class="absolute inset-0 bg-gradient-to-br opacity-0 group-hover:opacity-100 transition-opacity duration-300 {card.color}"></div>
            <div class="relative p-8 flex flex-col items-center text-center">
              <div class="w-16 h-16 bg-gradient-to-br {card.color} rounded-2xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300 shadow-lg">
                <svg class="h-8 w-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={card.icon}></path>
                </svg>
              </div>
              <p class="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-2">{card.label}</p>
              <p class="text-4xl font-bold text-gray-900 dark:text-white animate-count-up">{card.value}</p>
            </div>
          </div>
        {/each}
      </div>

      <!-- Section transitions for charts -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-8">
        <div in:fade class="bg-white/90 dark:bg-gray-800/90 rounded-3xl shadow-xl border border-gray-100 dark:border-gray-700 overflow-hidden animate-fade-in">
          <div class="p-8 border-b border-gray-100 dark:border-gray-700">
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white">Status Distribution</h3>
            <p class="text-gray-600 dark:text-gray-400 mt-2">Breakdown of issues by current status</p>
          </div>
          <div class="p-8">
            <Chart 
              type="doughnut"
              data={{
                labels: ['Open', 'Triaged', 'In Progress', 'Done'],
                datasets: [{
                  data: [
                    getIssuesByStatus().OPEN,
                    getIssuesByStatus().TRIAGED,
                    getIssuesByStatus().IN_PROGRESS,
                    getIssuesByStatus().DONE
                  ],
                  backgroundColor: ['#3B82F6', '#8B5CF6', '#F59E0B', '#10B981']
                }]
              }}
            />
          </div>
        </div>
        <div in:fade class="bg-white/90 dark:bg-gray-800/90 rounded-3xl shadow-xl border border-gray-100 dark:border-gray-700 overflow-hidden animate-fade-in">
          <div class="p-8 border-b border-gray-100 dark:border-gray-700">
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white">Severity Distribution</h3>
            <p class="text-gray-600 dark:text-gray-400 mt-2">Issues categorized by severity level</p>
          </div>
          <div class="p-8">
            <Chart 
              type="bar"
              data={{
                labels: ['Low', 'Medium', 'High'],
                datasets: [{
                  data: [
                    getIssuesBySeverity().LOW,
                    getIssuesBySeverity().MEDIUM,
                    getIssuesBySeverity().HIGH
                  ],
                  backgroundColor: ['#10B981', '#F59E0B', '#EF4444']
                }]
              }}
            />
          </div>
        </div>
      </div>
      <div in:fade class="bg-white/90 dark:bg-gray-800/90 rounded-3xl shadow-xl border border-gray-100 dark:border-gray-700 overflow-hidden animate-fade-in mt-8">
        <div class="p-8 border-b border-gray-100 dark:border-gray-700">
          <h3 class="text-2xl font-bold text-gray-900 dark:text-white">Priority Distribution</h3>
          <p class="text-gray-600 dark:text-gray-400 mt-2">Issues categorized by priority level</p>
        </div>
        <div class="p-8">
          <Chart 
            type="bar"
            data={{
              labels: ['Blocker', 'Critical', 'Minor', 'Trivial'],
              datasets: [{
                data: [
                  getIssuesByPriority().BLOCKER,
                  getIssuesByPriority().CRITICAL,
                  getIssuesByPriority().MINOR,
                  getIssuesByPriority().TRIVIAL
                ],
                backgroundColor: ['#EF4444', '#F97316', '#3B82F6', '#6B7280']
              }]
            }}
          />
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .animate-fade-in { animation: fadeIn 1s cubic-bezier(.4,0,.2,1) both; }
  .animate-slide-in-up { animation: slideInUp 1s cubic-bezier(.4,0,.2,1) both; }
  .animate-pop-in { animation: popIn 0.7s cubic-bezier(.4,0,.2,1) both; }
  .animate-float { animation: float 3s ease-in-out infinite alternate; }
  .animate-pulse-slow { animation: pulse 6s cubic-bezier(.4,0,.2,1) infinite alternate; }
  @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
  @keyframes slideInUp { from { opacity: 0; transform: translateY(40px); } to { opacity: 1; transform: none; } }
  @keyframes popIn { 0% { opacity: 0; transform: scale(0.8); } 80% { opacity: 1; transform: scale(1.05); } 100% { opacity: 1; transform: scale(1); } }
  @keyframes float { from { transform: translateY(0); } to { transform: translateY(-16px); } }
  @keyframes pulse { 0% { opacity: 0.7; } 100% { opacity: 1; } }
</style> 