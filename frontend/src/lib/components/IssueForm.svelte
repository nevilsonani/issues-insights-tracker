<script lang="ts">
  import { createIssue } from '$lib/api';
  import { goto } from '$app/navigation';
  import type { Severity } from '$lib/types';

  let title = '';
  let description = '';
  let severity: Severity = 'MEDIUM';
  let file: File | null = null;
  let loading = false;
  let error = '';

  const severityOptions = [
    { value: 'LOW', label: 'Low', color: 'text-green-600' },
    { value: 'MEDIUM', label: 'Medium', color: 'text-yellow-600' },
    { value: 'HIGH', label: 'High', color: 'text-red-600' }
  ];

  function handleFileChange(event: Event) {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files[0]) {
      file = target.files[0];
    }
  }

  async function handleSubmit() {
    if (!title.trim() || !description.trim()) {
      error = 'Please fill in all required fields';
      return;
    }

    loading = true;
    error = '';

    try {
      const formData = new FormData();
      formData.append('title', title);
      formData.append('description', description);
      formData.append('severity', severity);
      
      if (file) {
        formData.append('file', file);
      }

      await createIssue(formData);
      goto('/issues');
    } catch (err) {
      error = err instanceof Error ? err.message : 'Failed to create issue';
    } finally {
      loading = false;
    }
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Enter' && event.ctrlKey) {
      handleSubmit();
    }
  }
</script>

<svelte:head>
  <title>Create Issue - Issues & Insights Tracker</title>
</svelte:head>

<div class="max-w-2xl mx-auto">
  <div class="mb-6">
    <h1 class="text-3xl font-bold text-gray-900">Create New Issue</h1>
    <p class="text-gray-600 mt-1">Report a bug or request a new feature</p>
  </div>

  <div class="card">
    <form on:submit|preventDefault={handleSubmit} class="space-y-6">
      <!-- Title -->
      <div>
        <label for="title" class="block text-sm font-medium text-gray-700">
          Title *
        </label>
        <div class="mt-1">
          <input
            id="title"
            type="text"
            bind:value={title}
            required
            class="input-field"
            placeholder="Brief description of the issue"
          />
        </div>
      </div>

      <!-- Severity -->
      <div>
        <label for="severity" class="block text-sm font-medium text-gray-700">
          Severity *
        </label>
        <div class="mt-1">
          <select
            id="severity"
            bind:value={severity}
            class="input-field"
          >
            {#each severityOptions as option}
              <option value={option.value} class={option.color}>
                {option.label}
              </option>
            {/each}
          </select>
        </div>
        <p class="mt-1 text-sm text-gray-500">
          Choose the impact level of this issue
        </p>
      </div>

      <!-- Description -->
      <div>
        <label for="description" class="block text-sm font-medium text-gray-700">
          Description *
        </label>
        <div class="mt-1">
          <textarea
            id="description"
            bind:value={description}
            on:keydown={handleKeydown}
            rows="8"
            required
            class="input-field"
            placeholder="Provide detailed information about the issue. You can use Markdown formatting."
          ></textarea>
        </div>
        <p class="mt-1 text-sm text-gray-500">
          Use Markdown for formatting. Press Ctrl+Enter to submit.
        </p>
      </div>

      <!-- File Upload -->
      <div>
        <label for="file" class="block text-sm font-medium text-gray-700">
          Attachment (Optional)
        </label>
        <div class="mt-1">
          <div class="flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-lg hover:border-blue-400 transition-colors">
            <div class="space-y-1 text-center">
              <svg class="mx-auto h-12 w-12 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM6.293 6.707a1 1 0 010-1.414l3-3a1 1 0 011.414 0l3 3a1 1 0 01-1.414 1.414L11 5.414V13a1 1 0 11-2 0V5.414L7.707 6.707a1 1 0 01-1.414 0z" clip-rule="evenodd" />
              </svg>
              <div class="flex text-sm text-gray-600">
                <label
                  for="file-upload"
                  class="relative cursor-pointer bg-white rounded-md font-medium text-blue-600 hover:text-blue-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-blue-500"
                >
                  <span>Upload a file</span>
                  <input
                    id="file-upload"
                    name="file-upload"
                    type="file"
                    class="sr-only"
                    on:change={handleFileChange}
                    accept=".pdf,.doc,.docx,.txt,.png,.jpg,.jpeg,.gif"
                  />
                </label>
                <p class="pl-1">or drag and drop</p>
              </div>
              <p class="text-xs text-gray-500">
                PDF, DOC, TXT, PNG, JPG up to 10MB
              </p>
            </div>
          </div>
        </div>
        {#if file}
          <div class="mt-2 flex items-center space-x-2">
            <svg class="h-4 w-4 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM6.293 6.707a1 1 0 010-1.414l3-3a1 1 0 011.414 0l3 3a1 1 0 01-1.414 1.414L11 5.414V13a1 1 0 11-2 0V5.414L7.707 6.707a1 1 0 01-1.414 0z" clip-rule="evenodd" />
            </svg>
            <span class="text-sm text-gray-600">{file.name}</span>
            <button
              type="button"
              on:click={() => file = null}
              class="text-red-600 hover:text-red-700 text-sm"
            >
              Remove
            </button>
          </div>
        {/if}
      </div>

      <!-- Error Message -->
      {#if error}
        <div class="bg-red-50 border border-red-200 rounded-md p-4">
          <div class="flex">
            <svg class="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
            <div class="ml-3">
              <p class="text-sm text-red-800">{error}</p>
            </div>
          </div>
        </div>
      {/if}

      <!-- Submit Button -->
      <div class="flex justify-end space-x-3">
        <a href="/issues" class="btn-secondary">
          Cancel
        </a>
        <button
          type="submit"
          disabled={loading}
          class="btn-primary flex items-center"
        >
          {#if loading}
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Creating...
          {:else}
            <svg class="-ml-1 mr-3 h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
            </svg>
            Create Issue
          {/if}
        </button>
      </div>
    </form>
  </div>
</div>
