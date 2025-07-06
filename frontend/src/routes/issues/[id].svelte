<script lang="ts">
  import { onMount } from 'svelte';
  import { get, page } from '$app/stores';
  import { fetchIssue, updateIssue } from '$lib/api';
  import { user } from '$lib/auth';
  import { marked } from 'marked';
  import type { Issue, Status } from '$lib/types';

  let issue: Issue | null = null;
  let loading = true;
  let error = '';
  let currentUser: any = null;
  let updatingStatus = false;

  // Subscribe to auth store
  user.subscribe((v) => (currentUser = v));

  const statusOptions = [
    { value: 'OPEN', label: 'Open' },
    { value: 'TRIAGED', label: 'Triaged' },
    { value: 'IN_PROGRESS', label: 'In Progress' },
    { value: 'DONE', label: 'Done' }
  ];

  async function loadIssue() {
    const issueId = parseInt(get(page).params.id); // fixed access to $page
    loading = true;
    try {
      issue = await fetchIssue(issueId);
      error = '';
    } catch (err) {
      error = 'Failed to load issue';
      console.error(err);
    } finally {
      loading = false;
    }
  }

  async function updateStatus(newStatus: Status) {
    if (!issue) return;
    updatingStatus = true;
    try {
      await updateIssue(issue.id, { status: newStatus });
      issue = { ...issue, status: newStatus };
    } catch (err) {
      console.error('Failed to update status:', err);
    } finally {
      updatingStatus = false;
    }
  }

  function formatDate(dateString: string) {
    return new Date(dateString).toLocaleString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  function canUpdateStatus(): boolean {
    if (!currentUser || !issue) return false;
    return currentUser.role === 'ADMIN' || 
           currentUser.role === 'MAINTAINER' || 
           issue.reporter_id === currentUser.id;
  }

  onMount(() => {
    loadIssue();
  });
</script>

<svelte:head>
  <title>{issue ? `${issue.title} - Issues & Insights Tracker` : 'Issue Details'}</title>
</svelte:head>

<div class="max-w-4xl mx-auto">
  {#if loading}
    <p class="text-center text-gray-600 py-8">Loading issue...</p>
  {:else if error}
    <div class="text-center text-red-600 py-8">{error}</div>
  {:else if issue}
    <!-- Header -->
    <div class="flex items-start justify-between mb-6">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">{issue.title}</h1>
        <p class="text-sm text-gray-500 mt-1">Issue #{issue.id} • Created {formatDate(issue.created_at)}</p>
      </div>

      {#if canUpdateStatus()}
        <div class="flex items-center space-x-2">
          <label class="text-sm font-medium">Status:</label>
          <select
            bind:value={issue.status}
            on:change={(e) => updateStatus(e.target.value as Status)}
            class="input-field"
            disabled={updatingStatus}
          >
            {#each statusOptions as opt}
              <option value={opt.value}>{opt.label}</option>
            {/each}
          </select>
        </div>
      {/if}
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Left: Description -->
      <div class="lg:col-span-2">
        <div class="card mb-6">
          <h2 class="text-xl font-semibold mb-4">Description</h2>
          <div class="prose max-w-none">
            {@html marked(issue.description || '')}
          </div>
        </div>

        {#if issue.file_path}
          <div class="card">
            <h2 class="text-xl font-semibold mb-4">Attachment</h2>
            <a
              class="btn-secondary"
              href={`http://localhost:8000/api/issues/${issue.id}/file`}
              target="_blank"
            >
              Download File
            </a>
          </div>
        {/if}
      </div>

      <!-- Right: Sidebar -->
      <div class="card space-y-4">
        <div>
          <p class="text-sm font-medium text-gray-600">Severity</p>
          <p class="text-base text-gray-800">{issue.severity}</p>
        </div>
        <div>
          <p class="text-sm font-medium text-gray-600">Priority</p>
          <p class="text-base text-gray-800">{issue.priority || 'Not set'}</p>
        </div>
        <div>
          <p class="text-sm font-medium text-gray-600">Status</p>
          <p class="text-base text-gray-800">{issue.status.replace('_', ' ')}</p>
        </div>
        <div>
          <p class="text-sm font-medium text-gray-600">Reporter ID</p>
          <p class="text-base text-gray-800">#{issue.reporter_id}</p>
        </div>
        <div>
          <a href="/issues" class="btn-secondary block w-full text-center">← Back to Issues</a>
        </div>
      </div>
    </div>
  {:else}
    <p class="text-center text-gray-500 py-8">Issue not found.</p>
  {/if}
</div>
