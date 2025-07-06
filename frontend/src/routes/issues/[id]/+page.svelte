<script lang="ts">
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import { fetchIssue, updateIssue } from '$lib/api';
  import type { Issue } from '$lib/types';
  import { user } from '$lib/auth';

  let issue: Issue | null = null;
  let loading = true;
  let error = '';
  let currentUser: any = null;
  let statusError = '';

  user.subscribe((v) => (currentUser = v));

  onMount(async () => {
    try {
      const issueId = parseInt($page.params.id);
      issue = await fetchIssue(issueId);
    } catch (err) {
      error = err instanceof Error ? err.message : 'Failed to load issue';
    } finally {
      loading = false;
    }
  });

  function getSeverityIcon(severity: string) {
    switch (severity) {
      case 'HIGH': return 'M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z';
      case 'MEDIUM': return 'M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z';
      case 'LOW': return 'M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zm-1 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z';
      default: return 'M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z';
    }
  }

  function getStatusIcon(status: string) {
    switch (status) {
      case 'OPEN': return 'M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z';
      case 'TRIAGED': return 'M10 12a2 2 0 100-4 2 2 0 000 4z M10 2C5.58 2 2 5.58 2 10s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8zm0 14c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6z';
      case 'IN_PROGRESS': return 'M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z';
      case 'DONE': return 'M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z';
      default: return 'M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zm-1 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z';
    }
  }

  function getPriorityIcon(priority: string) {
    switch (priority) {
      case 'BLOCKER': return 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z';
      case 'CRITICAL': return 'M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z';
      case 'MINOR': return 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z';
      case 'TRIVIAL': return 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z';
      default: return 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z';
    }
  }

  function formatDate(dateString: string) {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  function getNextStatuses(current: string): string[] {
    switch (current) {
      case 'OPEN': return ['TRIAGED'];
      case 'TRIAGED': return ['IN_PROGRESS'];
      case 'IN_PROGRESS': return ['DONE'];
      default: return [];
    }
  }

  async function handleStatusChange(e: Event) {
    const newStatus = (e.target as HTMLSelectElement).value;
    if (!issue) return;
    statusError = '';
    try {
      await updateIssue(issue.id, { status: newStatus });
      issue = { ...issue, status: newStatus };
    } catch (err) {
      statusError = err instanceof Error ? err.message : 'Failed to update status';
    }
  }
</script>

<svelte:head>
  <title>Issue #{$page.params.id} - IssueTracker Pro</title>
</svelte:head>

<div class="max-w-4xl mx-auto">
  <!-- Header -->
  <div class="flex items-center justify-between mb-8">
    <div class="flex items-center space-x-4">
      <button
        on:click={() => goto('/issues')}
        class="btn-secondary"
      >
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
        </svg>
        Back to Issues
      </button>
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Issue #{$page.params.id}</h1>
    </div>
  </div>

  {#if loading}
    <div class="card animate-pulse">
      <div class="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/3 mb-4"></div>
      <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2 mb-2"></div>
      <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-6"></div>
      <div class="h-32 bg-gray-200 dark:bg-gray-700 rounded"></div>
    </div>
  {:else if error}
    <div class="card">
      <div class="text-center py-12">
        <div class="w-16 h-16 bg-red-100 dark:bg-red-900/20 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">Error loading issue</h3>
        <p class="text-gray-500 dark:text-gray-400 mb-4">{error}</p>
        <button
          on:click={() => goto('/issues')}
          class="btn-primary"
        >
          Back to Issues
        </button>
      </div>
    </div>
  {:else if issue}
    <div class="space-y-6">
      <!-- Issue Header -->
      <div class="card">
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">{issue.title}</h2>
            <p class="text-gray-500 dark:text-gray-400">Created on {formatDate(issue.created_at)}</p>
          </div>
          <div class="flex items-center space-x-3">
            <!-- Severity Badge -->
            <span class="badge badge-{issue.severity.toLowerCase()}">
              <svg class="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="{getSeverityIcon(issue.severity)}" clip-rule="evenodd" />
              </svg>
              {issue.severity}
            </span>
            
            <!-- Priority Badge -->
            {#if issue.priority}
              <span class="badge badge-{issue.priority.toLowerCase()}">
                <svg class="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="{getPriorityIcon(issue.priority)}" clip-rule="evenodd" />
                </svg>
                {issue.priority}
              </span>
            {/if}
            
            <!-- Status Badge -->
            <span class="badge badge-{issue.status.toLowerCase().replace('_', '-')}">
              <svg class="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="{getStatusIcon(issue.status)}" clip-rule="evenodd" />
              </svg>
              {issue.status.replace('_', ' ')}
            </span>
          </div>
        </div>
      </div>

      <!-- Issue Description -->
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Description</h3>
        {#if issue.description}
          <div class="prose prose-gray dark:prose-invert max-w-none">
            <p class="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">{issue.description}</p>
          </div>
        {:else}
          <p class="text-gray-500 dark:text-gray-400 italic">No description provided</p>
        {/if}
      </div>

      <!-- Issue Details -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Issue Details</h3>
          <dl class="space-y-3">
            <div>
              <dt class="text-sm font-medium text-gray-500 dark:text-gray-400">Issue ID</dt>
              <dd class="text-sm text-gray-900 dark:text-white">#{issue.id}</dd>
            </div>
            <div>
              <dt class="text-sm font-medium text-gray-500 dark:text-gray-400">Reporter ID</dt>
              <dd class="text-sm text-gray-900 dark:text-white">{issue.reporter_id}</dd>
            </div>
            <div>
              <dt class="text-sm font-medium text-gray-500 dark:text-gray-400">Created</dt>
              <dd class="text-sm text-gray-900 dark:text-white">{formatDate(issue.created_at)}</dd>
            </div>
          </dl>
        </div>

        <!-- Attachments -->
        {#if issue.file_path}
          <div class="card">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Attachments</h3>
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-purple-100 dark:bg-purple-900/20 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-purple-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM6.293 6.707a1 1 0 010-1.414l3-3a1 1 0 011.414 0l3 3a1 1 0 01-1.414 1.414L11 5.414V13a1 1 0 11-2 0V5.414L7.707 6.707a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                </svg>
              </div>
              <div>
                <p class="text-sm font-medium text-gray-900 dark:text-white">Attachment</p>
                <p class="text-sm text-gray-500 dark:text-gray-400">{issue.file_path}</p>
              </div>
            </div>
          </div>
        {/if}
      </div>

      <!-- Status Change Dropdown (only for MAINTAINER/ADMIN and if not DONE) -->
      {#if issue && currentUser && (currentUser.role === 'ADMIN' || currentUser.role === 'MAINTAINER') && issue.status !== 'DONE'}
        <div class="card">
          <label for="status-select" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Change Status</label>
          <select id="status-select" class="input-field" on:change={handleStatusChange}>
            <option value="" disabled selected>Select next status</option>
            {#each getNextStatuses(issue.status) as next}
              <option value={next}>{next.replace('_', ' ')}</option>
            {/each}
          </select>
          {#if statusError}
            <div class="text-red-600 text-sm mt-2">{statusError}</div>
          {/if}
        </div>
      {/if}
    </div>
  {:else}
    <div class="card">
      <div class="text-center py-12">
        <div class="w-16 h-16 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">Issue not found</h3>
        <p class="text-gray-500 dark:text-gray-400 mb-4">The issue you're looking for doesn't exist or has been removed.</p>
        <button
          on:click={() => goto('/issues')}
          class="btn-primary"
        >
          Back to Issues
        </button>
      </div>
    </div>
  {/if}
</div> 