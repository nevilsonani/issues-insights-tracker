<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { fetchIssues, updateIssue, createWebSocketConnection } from '$lib/api';
  import { user } from '$lib/auth';
  import IssueCard from '$lib/components/IssueCard.svelte';
  import type { Issue, Status, Severity } from '$lib/types';

  let issues: Issue[] = [];
  let filteredIssues: Issue[] = [];
  let loading = true;
  let error = '';
  let currentUser: any = null;
  let searchTerm = '';
  let statusFilter: Status | 'ALL' = 'ALL';
  let severityFilter: Severity | 'ALL' = 'ALL';
  let ws: WebSocket | null = null;

  user.subscribe((v) => (currentUser = v));

  const statusOptions = [
    { value: 'ALL', label: 'All Statuses' },
    { value: 'OPEN', label: 'Open' },
    { value: 'TRIAGED', label: 'Triaged' },
    { value: 'IN_PROGRESS', label: 'In Progress' },
    { value: 'DONE', label: 'Done' }
  ];

  const severityOptions = [
    { value: 'ALL', label: 'All Severities' },
    { value: 'LOW', label: 'Low' },
    { value: 'MEDIUM', label: 'Medium' },
    { value: 'HIGH', label: 'High' }
  ];

  async function loadIssues() {
    loading = true;
    try {
      issues = await fetchIssues();
      applyFilters();
      error = '';
    } catch (err) {
      error = 'Failed to load issues';
      console.error(err);
    } finally {
      loading = false;
    }
  }

  function applyFilters() {
    filteredIssues = issues.filter(issue => {
      const matchesSearch = issue.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           issue.description.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesStatus = statusFilter === 'ALL' || issue.status === statusFilter;
      const matchesSeverity = severityFilter === 'ALL' || issue.severity === severityFilter;
      
      return matchesSearch && matchesStatus && matchesSeverity;
    });
  }

  async function updateIssueStatus(issueId: number, newStatus: Status) {
    try {
      await updateIssue(issueId, { status: newStatus });
      // Update the local issue
      const issueIndex = issues.findIndex(i => i.id === issueId);
      if (issueIndex !== -1) {
        issues[issueIndex] = { ...issues[issueIndex], status: newStatus };
        applyFilters();
      }
    } catch (err) {
      console.error('Failed to update issue status:', err);
    }
  }

  $: {
    applyFilters();
  }

  onMount(() => {
    loadIssues();
    ws = createWebSocketConnection();
    if (ws) {
      ws.onmessage = (event) => {
        // Any message means issues changed, so reload
        loadIssues();
      };
    }
  });

  onDestroy(() => {
    if (ws) {
      ws.close();
    }
  });
</script>

<svelte:head>
  <title>Issues - Issues & Insights Tracker</title>
</svelte:head>

<div class="space-y-6">
  <!-- Header -->
  <div class="flex justify-between items-center">
    <div>
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Issues</h1>
      <p class="text-gray-600 dark:text-gray-400 mt-1">Manage and track all issues</p>
    </div>
    <a href="/issues/new" class="btn-primary flex items-center">
      <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
      </svg>
      New Issue
    </a>
  </div>

  <!-- Filters -->
  <div class="card">
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <!-- Search -->
      <div class="md:col-span-2">
        <label for="search" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Search
        </label>
        <div class="relative">
          <svg class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
          <input
            id="search"
            type="text"
            bind:value={searchTerm}
            class="input-field pl-10"
            placeholder="Search issues..."
          />
        </div>
      </div>

      <!-- Status Filter -->
      <div>
        <label for="status-filter" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Status
        </label>
        <select
          id="status-filter"
          bind:value={statusFilter}
          class="input-field"
        >
          {#each statusOptions as option}
            <option value={option.value}>{option.label}</option>
          {/each}
        </select>
      </div>

      <!-- Severity Filter -->
      <div>
        <label for="severity-filter" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          Severity
        </label>
        <select
          id="severity-filter"
          bind:value={severityFilter}
          class="input-field"
        >
          {#each severityOptions as option}
            <option value={option.value}>{option.label}</option>
          {/each}
        </select>
      </div>
    </div>
  </div>

  <!-- Results Summary -->
  <div class="flex items-center justify-between">
    <p class="text-sm text-gray-600 dark:text-gray-400">
      Showing {filteredIssues.length} of {issues.length} issues
    </p>
    {#if searchTerm || statusFilter !== 'ALL' || severityFilter !== 'ALL'}
      <button
        on:click={() => {
          searchTerm = '';
          statusFilter = 'ALL';
          severityFilter = 'ALL';
        }}
        class="text-sm text-blue-600 hover:text-blue-700"
      >
        Clear filters
      </button>
    {/if}
  </div>

  {#if loading}
    <div class="flex justify-center items-center py-12">
      <svg class="animate-spin h-8 w-8 text-blue-600" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <span class="ml-3 text-gray-600 dark:text-gray-400">Loading issues...</span>
    </div>
  {:else if error}
    <div class="card">
      <div class="flex items-center">
        <svg class="h-5 w-5 text-red-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <p class="text-red-800">{error}</p>
      </div>
    </div>
  {:else if filteredIssues.length === 0}
    <div class="card text-center py-12">
      <svg class="h-12 w-12 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
      </svg>
      <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">No issues found</h3>
      <p class="text-gray-500 dark:text-gray-400 mb-4">
        {issues.length === 0 ? 'Get started by creating your first issue.' : 'Try adjusting your filters.'}
      </p>
      <a href="/issues/new" class="btn-primary flex items-center justify-center">
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
        </svg>
        Create Issue
      </a>
    </div>
  {:else}
    <!-- Issues List -->
    <div class="space-y-4">
      {#each filteredIssues as issue (issue.id)}
        <IssueCard {issue} on:statusUpdate={updateIssueStatus} />
      {/each}
    </div>
  {/if}
</div>
