<script lang="ts">
  import { goto } from '$app/navigation';
  import { createEventDispatcher } from 'svelte';
  import { createIssue } from '$lib/api';

  let title = '';
  let description = '';
  let severity = 'LOW';
  let priority = 'MINOR';
  let file: File | null = null;
  let loading = false;
  let error = '';

  const dispatch = createEventDispatcher();

  async function handleSubmit() {
    if (!title.trim()) {
      error = 'Title is required';
      return;
    }

    loading = true;
    error = '';

    try {
      const formData = new FormData();
      formData.append('title', title);
      formData.append('severity', severity);
      if (description) formData.append('description', description);
      if (priority) formData.append('priority', priority);
      if (file) formData.append('file', file);

      await createIssue(formData);
      dispatch('created'); // optional, in case parent wants to listen
      goto('/issues');
    } catch (err) {
      error = err instanceof Error ? err.message : 'Failed to create issue';
    } finally {
      loading = false;
    }
  }
</script>

<form on:submit|preventDefault={handleSubmit} class="space-y-4 max-w-xl">
  <div>
    <label class="block mb-1 font-medium text-sm text-gray-700">Title</label>
    <input bind:value={title} type="text" required class="input-field w-full" />
  </div>

  <div>
    <label class="block mb-1 font-medium text-sm text-gray-700">Description</label>
    <textarea bind:value={description} class="input-field w-full" rows="4" />
  </div>

  <div>
    <label class="block mb-1 font-medium text-sm text-gray-700">Severity</label>
    <select bind:value={severity} class="input-field w-full">
      <option value="LOW">Low</option>
      <option value="MEDIUM">Medium</option>
      <option value="HIGH">High</option>
    </select>
  </div>

  <div>
    <label class="block mb-1 font-medium text-sm text-gray-700">Priority</label>
    <select bind:value={priority} class="input-field w-full">
      <option value="BLOCKER">Blocker</option>
      <option value="CRITICAL">Critical</option>
      <option value="MINOR">Minor</option>
      <option value="TRIVIAL">Trivial</option>
    </select>
  </div>

  <div>
    <label class="block mb-1 font-medium text-sm text-gray-700">File (optional)</label>
    <input type="file" on:change={(e) => file = e.target.files[0]} class="input-field w-full" />
  </div>

  {#if error}
    <div class="bg-red-50 border border-red-200 rounded-lg p-3">
      <p class="text-red-600 text-sm">{error}</p>
    </div>
  {/if}

  <button type="submit" disabled={loading} class="btn-primary mt-2">
    {#if loading}
      Creating Issue...
    {:else}
      Create Issue
    {/if}
  </button>
</form>
