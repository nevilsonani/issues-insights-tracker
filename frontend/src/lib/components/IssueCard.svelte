<script lang="ts">
  import type { Issue } from '$lib/types';
  import { marked } from 'marked';

  export let issue: Issue;

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

  function getPriorityBadgeClass(priority: string) {
    switch (priority) {
      case 'BLOCKER': return 'badge-blocker';
      case 'CRITICAL': return 'badge-critical';
      case 'MINOR': return 'badge-minor';
      case 'TRIVIAL': return 'badge-trivial';
      default: return 'badge-trivial';
    }
  }

  function formatDate(dateString: string) {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  function truncateText(text: string | null | undefined, maxLength: number = 150) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  }
</script>

{#if issue}
<div class="card-hover group">
  <div class="flex items-start justify-between">
    <div class="flex-1 min-w-0">
      <!-- Header with title and icons -->
      <div class="flex items-center space-x-3 mb-3">
        <div class="flex-shrink-0">
          <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center shadow-sm group-hover:shadow-md transition-shadow">
            <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="{getSeverityIcon(issue.severity)}" clip-rule="evenodd" />
        </svg>
          </div>
        </div>
        <div class="flex-1 min-w-0">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white truncate group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
          {issue.title}
        </h3>
          <p class="text-sm text-gray-500 dark:text-gray-400">Issue #{issue.id}</p>
        </div>
      </div>
      
      <!-- Description -->
      {#if issue.description}
        <div class="prose prose-sm text-gray-600 dark:text-gray-300 mb-4 max-w-none line-clamp-2">
          {@html marked(truncateText(issue.description, 120))}
        </div>
      {/if}
      
      <!-- Badges and metadata -->
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-2 flex-wrap">
          <!-- Severity Badge -->
          <span class="badge badge-{issue.severity.toLowerCase()}">
            <svg class="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="{getSeverityIcon(issue.severity)}" clip-rule="evenodd" />
            </svg>
            {issue.severity}
          </span>
          
          <!-- Priority Badge -->
          {#if issue.priority}
            <span class="badge {getPriorityBadgeClass(issue.priority)}">
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
          
          <!-- Tags Badges -->
          {#if issue.tags && issue.tags.length > 0}
            {#each issue.tags as tag}
              <span class="badge bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 border border-gray-200 dark:border-gray-600">
                #{tag}
              </span>
            {/each}
          {/if}
          
          <!-- Attachment Badge -->
          {#if issue.file_path}
            <span class="badge bg-purple-50 dark:bg-purple-900/20 text-purple-700 dark:text-purple-400 border border-purple-200 dark:border-purple-800">
              <svg class="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM6.293 6.707a1 1 0 010-1.414l3-3a1 1 0 011.414 0l3 3a1 1 0 01-1.414 1.414L11 5.414V13a1 1 0 11-2 0V5.414L7.707 6.707a1 1 0 01-1.414 0z" clip-rule="evenodd" />
              </svg>
              Attachment
            </span>
          {/if}
        </div>
        
        <!-- Date and Actions -->
        <div class="flex items-center space-x-3">
          <div class="text-sm text-gray-500 dark:text-gray-400 flex items-center">
            <svg class="mr-1 h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd" />
          </svg>
          {formatDate(issue.created_at)}
    </div>
    
      <a 
        href="/issues/{issue.id}" 
            class="btn-secondary text-sm group-hover:shadow-md transition-all duration-200"
      >
        <svg class="mr-1 h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
          <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
          <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
        </svg>
        View
      </a>
        </div>
      </div>
    </div>
  </div>
</div>
{/if}
