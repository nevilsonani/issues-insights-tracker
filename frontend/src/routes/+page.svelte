<script lang="ts">
  import { onMount, tick } from 'svelte';
  import { goto } from '$app/navigation';
  import { fetchIssues, fetchDailyStats } from '$lib/api';
  import { user } from '$lib/auth';
  import IssueCard from '$lib/components/IssueCard.svelte';
  import { fade, fly, scale } from 'svelte/transition';
  import { cubicOut } from 'svelte/easing';
  import type { Issue, DailyStats } from '$lib/types';

  let issues: Issue[] = [];
  let stats: DailyStats[] = [];
  let loading = true;
  let error = '';
  let currentUser: any = null;

  // Animated counters
  let animatedStats = {
    total: 0,
    open: 0,
    inProgress: 0,
    done: 0,
    blocker: 0,
    critical: 0,
    minor: 0,
    trivial: 0
  };

  user.subscribe((v) => (currentUser = v));

  async function loadData() {
    loading = true;
    try {
      const [issuesData, statsData] = await Promise.all([
        fetchIssues(),
        fetchDailyStats()
      ]);
      issues = issuesData.filter(issue => issue); // Filter out null issues
      stats = statsData;
      error = '';
    } catch (err) {
      error = 'Failed to load dashboard data';
      console.error(err);
    } finally {
      loading = false;
    }
  }

  function getStatusCount(status: string) {
    return issues.filter(issue => issue.status === status).length;
  }

  function getPriorityCount(priority: string) {
    return issues.filter(issue => issue.priority === priority).length;
  }

  function getSeverityColor(severity: string) {
    switch (severity) {
      case 'HIGH': return 'from-red-500 to-red-600';
      case 'MEDIUM': return 'from-yellow-500 to-yellow-600';
      case 'LOW': return 'from-green-500 to-green-600';
      default: return 'from-gray-500 to-gray-600';
    }
  }

  function getPriorityColor(priority: string) {
    switch (priority) {
      case 'BLOCKER': return 'from-red-500 to-red-600';
      case 'CRITICAL': return 'from-orange-500 to-orange-600';
      case 'MINOR': return 'from-blue-500 to-blue-600';
      case 'TRIVIAL': return 'from-gray-500 to-gray-600';
      default: return 'from-gray-500 to-gray-600';
    }
  }

  // Animate counters
  async function animateCounters(targetStats) {
    const keys = Object.keys(animatedStats);
    for (const key of keys) {
      let start = 0;
      let end = targetStats[key];
      let duration = 800;
      let startTime = performance.now();
      function step(now) {
        let progress = Math.min((now - startTime) / duration, 1);
        animatedStats[key] = Math.floor(start + (end - start) * progress);
        if (progress < 1) {
          requestAnimationFrame(step);
        } else {
          animatedStats[key] = end;
        }
      }
      requestAnimationFrame(step);
      await tick();
    }
  }

  onMount(async () => {
    await loadData();
    // Calculate stats
    const targetStats = {
      total: issues.length,
      open: getStatusCount('OPEN'),
      inProgress: getStatusCount('IN_PROGRESS'),
      done: getStatusCount('DONE'),
      blocker: getPriorityCount('BLOCKER'),
      critical: getPriorityCount('CRITICAL'),
      minor: getPriorityCount('MINOR'),
      trivial: getPriorityCount('TRIVIAL')
    };
    animateCounters(targetStats);
  });

  function getIssuesByPriority() {
    const filteredIssues = getFilteredIssues();
    const priorityCounts = {
      'BLOCKER': 0,
      'CRITICAL': 0,
      'MINOR': 0,
      'TRIVIAL': 0
    };
    filteredIssues.forEach(issue => {
      if (issue.priority && priorityCounts[issue.priority] !== undefined) {
        priorityCounts[issue.priority]++;
      }
    });
    return priorityCounts;
  }
</script>

<svelte:head>
  <title>Dashboard - IssueTracker Pro</title>
</svelte:head>

<!-- Animated gradient background with floating blobs -->
<div class="min-h-screen relative overflow-hidden">
  <div class="absolute inset-0 -z-10">
    <div class="absolute -top-32 -left-32 w-[500px] h-[500px] bg-gradient-to-br from-blue-400/30 via-purple-400/20 to-pink-400/20 rounded-full blur-3xl animate-pulse-slow"></div>
    <div class="absolute top-1/2 right-0 w-[400px] h-[400px] bg-gradient-to-br from-pink-400/20 via-blue-400/20 to-purple-400/30 rounded-full blur-3xl animate-pulse-slow"></div>
    <div class="absolute bottom-0 left-1/2 w-[300px] h-[300px] bg-gradient-to-br from-purple-400/20 via-blue-400/20 to-pink-400/30 rounded-full blur-2xl animate-pulse-slow"></div>
  </div>

  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="space-y-8">
      <!-- Hero Section with animation -->
      <div class="relative overflow-hidden rounded-3xl bg-gradient-to-r from-white/80 via-blue-50/60 to-purple-50/60 dark:from-gray-800/80 dark:via-blue-900/40 dark:to-purple-900/40 border border-white/20 dark:border-gray-700/50 shadow-2xl backdrop-blur-sm animate-fade-in">
        <div class="absolute inset-0 bg-gradient-to-r from-blue-600/10 via-purple-600/10 to-pink-600/10 dark:from-blue-400/5 dark:via-purple-400/5 dark:to-pink-400/5"></div>
        <div class="relative p-8">
          <div class="flex items-center justify-between">
            <div class="flex-1">
              <h1 class="text-4xl md:text-5xl font-bold bg-gradient-to-r from-gray-900 via-blue-800 to-purple-800 dark:from-white dark:via-blue-200 dark:to-purple-200 bg-clip-text text-transparent mb-3 animate-slide-in-up">
                Welcome back, {currentUser?.full_name || 'User'}! 👋
              </h1>
              <p class="text-xl text-gray-600 dark:text-gray-300 mb-6 animate-fade-in delay-200">
                Here's what's happening with your issues today
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
                  on:click={() => goto('/analytics')}
                  class="group relative inline-flex items-center px-8 py-4 bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800 dark:from-purple-500 dark:to-purple-600 dark:hover:from-purple-600 dark:hover:to-purple-700 text-white font-semibold rounded-2xl shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300 animate-pop-in delay-200"
                >
                  <svg class="w-5 h-5 mr-3 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                  </svg>
                  View Analytics
                  <div class="absolute inset-0 bg-white/20 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity"></div>
                </button>
              </div>
            </div>
            <div class="hidden lg:block">
              <div class="w-24 h-24 bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 rounded-3xl flex items-center justify-center shadow-2xl transform rotate-12 hover:rotate-0 transition-transform duration-500 animate-float">
                <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats Cards with animation -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-6 mt-8">
        {#each [
          { label: 'Total Issues', value: animatedStats.total, color: 'from-blue-500 to-blue-600', icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' },
          { label: 'Open', value: animatedStats.open, color: 'from-blue-500 to-blue-600', icon: 'M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z' },
          { label: 'In Progress', value: animatedStats.inProgress, color: 'from-orange-500 to-orange-600', icon: 'M13 10V3L4 14h7v7l9-11h-7z' },
          { label: 'Completed', value: animatedStats.done, color: 'from-green-500 to-green-600', icon: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z' }
        ] as card, i}
          <div in:fly="{{ y: 40, duration: 600, delay: i * 120 }}" class="group relative overflow-hidden bg-white/80 dark:bg-gray-800/80 rounded-2xl shadow-lg hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-300 border border-gray-100 dark:border-gray-700 animate-fade-in">
            <div class="absolute inset-0 bg-gradient-to-br opacity-0 group-hover:opacity-100 transition-opacity duration-300 {card.color}"></div>
            <div class="relative p-6 flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">{card.label}</p>
                <p class="text-3xl font-bold text-gray-900 dark:text-white animate-count-up">{card.value}</p>
              </div>
              <div class="w-12 h-12 bg-gradient-to-br {card.color} rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300 shadow-lg">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={card.icon}></path>
                </svg>
              </div>
            </div>
          </div>
        {/each}
      </div>

      <!-- Priority Distribution with animation -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-6 mt-8">
        {#each [
          { label: 'Blocker', value: animatedStats.blocker, color: 'from-red-500 to-red-600', icon: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z' },
          { label: 'Critical', value: animatedStats.critical, color: 'from-orange-500 to-orange-600', icon: 'M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z' },
          { label: 'Minor', value: animatedStats.minor, color: 'from-blue-500 to-blue-600', icon: 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z' },
          { label: 'Trivial', value: animatedStats.trivial, color: 'from-gray-500 to-gray-600', icon: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z' }
        ] as card, i}
          <div in:fly="{{ y: 40, duration: 600, delay: 200 + i * 120 }}" class="group relative overflow-hidden bg-white/80 dark:bg-gray-800/80 rounded-2xl shadow-lg hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-300 border border-gray-100 dark:border-gray-700 animate-fade-in">
            <div class="absolute inset-0 bg-gradient-to-br opacity-0 group-hover:opacity-100 transition-opacity duration-300 {card.color}"></div>
            <div class="relative p-6 flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">{card.label}</p>
                <p class="text-3xl font-bold text-gray-900 dark:text-white animate-count-up">{card.value}</p>
              </div>
              <div class="w-12 h-12 bg-gradient-to-br {card.color} rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300 shadow-lg">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={card.icon}></path>
                </svg>
              </div>
            </div>
          </div>
        {/each}
      </div>

      <!-- Recent Issues with fade-in -->
      <div class="bg-white/90 dark:bg-gray-800/90 rounded-3xl shadow-xl border border-gray-100 dark:border-gray-700 overflow-hidden mt-10 animate-fade-in">
        <div class="p-8 border-b border-gray-100 dark:border-gray-700">
          <div class="flex items-center justify-between">
            <h2 class="text-2xl font-bold text-gray-900 dark:text-white">Recent Issues</h2>
            <button
              on:click={() => goto('/issues')}
              class="group inline-flex items-center px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 dark:from-blue-500 dark:to-blue-600 dark:hover:from-blue-600 dark:hover:to-blue-700 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300"
            >
              View All
              <svg class="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
              </svg>
            </button>
          </div>
        </div>
        <div class="p-8">
          {#if loading}
            <div class="space-y-6">
              {#each Array(3) as _, i}
                <div class="animate-pulse" in:fade={{ delay: i * 100 }}>
                  <div class="h-6 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-3"></div>
                  <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2 mb-3"></div>
                  <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-5/6"></div>
                </div>
              {/each}
            </div>
          {:else if !issues || issues.length === 0}
            <div class="text-center py-16">
              <div class="w-20 h-20 bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-800 dark:to-gray-700 rounded-full flex items-center justify-center mx-auto mb-6 shadow-lg animate-float">
                <svg class="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
              </div>
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3">No issues yet</h3>
              <p class="text-gray-600 dark:text-gray-400 mb-6 text-lg">Get started by creating your first issue</p>
              <button
                on:click={() => goto('/issues/new')}
                class="inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 dark:from-blue-500 dark:to-blue-600 dark:hover:from-blue-600 dark:hover:to-blue-700 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300"
              >
                <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                </svg>
                Create First Issue
              </button>
            </div>
          {:else}
            <div class="space-y-6">
              {#each issues.filter(issue => issue).slice(0, 5) as issue, i}
                <div in:fade={{ delay: i * 100 }}>
                  <IssueCard {issue} />
                </div>
              {/each}
            </div>
          {/if}
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
