<script lang="ts">
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { user, logout } from '$lib/auth';
  import ThemeToggle from './ThemeToggle.svelte';
  import type { User } from '$lib/types';

  let currentUser: User | null = null;
  let showDropdown = false;
  let showMobileMenu = false;

  user.subscribe((v) => (currentUser = v));

  function handleLogout() {
    logout();
    goto('/login');
  }

  function isActive(path: string) {
    return $page.url.pathname === path;
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Escape') {
      showDropdown = false;
      showMobileMenu = false;
    }
  }

  function toggleMobileMenu() {
    showMobileMenu = !showMobileMenu;
  }
</script>

<nav class="bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm shadow-sm border-b border-gray-200/50 dark:border-gray-700/50 sticky top-0 z-40">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex justify-between h-16">
      <!-- Logo and Navigation -->
      <div class="flex items-center">
        <div class="flex-shrink-0 flex items-center">
          <div class="w-10 h-10 bg-gradient-to-br from-blue-600 to-blue-700 rounded-xl flex items-center justify-center mr-3 shadow-md">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <span class="text-xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 dark:from-white dark:to-gray-300 bg-clip-text text-transparent">IssueTracker</span>
        </div>
        
        <!-- Desktop Navigation -->
        <div class="hidden md:ml-10 md:flex md:space-x-1">
          <button
            on:click={() => goto('/dashboard')}
            class="nav-link {isActive('/dashboard') ? 'active' : ''}"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z"></path>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5a2 2 0 012-2h4a2 2 0 012 2v6H8V5z"></path>
            </svg>
            Dashboard
          </button>
          <button
            on:click={() => goto('/issues')}
            class="nav-link {isActive('/issues') ? 'active' : ''}"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
            Issues
          </button>
          <button
            on:click={() => goto('/analytics')}
            class="nav-link {isActive('/analytics') ? 'active' : ''}"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
            </svg>
            Analytics
          </button>
        </div>
      </div>

      <!-- User Menu and Mobile Menu Button -->
      <div class="flex items-center space-x-4">
        <!-- Theme Toggle -->
        <ThemeToggle />
        
        <!-- New Issue Button -->
        <button
          on:click={() => goto('/issues/new')}
          class="btn-primary hidden sm:flex items-center"
        >
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
          </svg>
          New Issue
        </button>

        <!-- User Menu -->
        <div class="relative">
          <button
            on:click={() => showDropdown = !showDropdown}
            class="flex items-center space-x-2 p-2 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center text-white font-semibold text-sm">
              {currentUser?.full_name?.charAt(0) || currentUser?.email?.charAt(0) || 'U'}
            </div>
            <div class="hidden sm:block text-left">
              <div class="text-sm font-medium text-gray-900 dark:text-white">{currentUser?.full_name || 'User'}</div>
              <div class="text-xs text-gray-500 dark:text-gray-400">{currentUser?.email || 'user@example.com'}</div>
            </div>
            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
            </svg>
          </button>

          <!-- Dropdown Menu -->
          {#if showDropdown}
            <div class="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 py-1 z-50 animate-in">
              <div class="px-4 py-2 border-b border-gray-100 dark:border-gray-700">
                <div class="text-sm font-medium text-gray-900 dark:text-white">{currentUser?.full_name || 'User'}</div>
                <div class="text-xs text-gray-500 dark:text-gray-400">{currentUser?.email || 'user@example.com'}</div>
              </div>
              <button
                on:click={handleLogout}
                class="w-full text-left px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
              >
                <svg class="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
                </svg>
                Sign out
              </button>
            </div>
          {/if}
        </div>

        <!-- Mobile menu button -->
        <button
          on:click={toggleMobileMenu}
          class="md:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors"
        >
          <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
          </svg>
        </button>
      </div>
    </div>
  </div>

  <!-- Mobile Menu -->
  {#if showMobileMenu}
    <div class="md:hidden bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 animate-in">
      <div class="px-2 pt-2 pb-3 space-y-1">
        <button
          on:click={() => { goto('/dashboard'); showMobileMenu = false; }}
          class="nav-link w-full justify-start {isActive('/dashboard') ? 'active' : ''}"
        >
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z"></path>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5a2 2 0 012-2h4a2 2 0 012 2v6H8V5z"></path>
          </svg>
          Dashboard
        </button>
        <button
          on:click={() => { goto('/issues'); showMobileMenu = false; }}
          class="nav-link w-full justify-start {isActive('/issues') ? 'active' : ''}"
        >
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          Issues
        </button>
        <button
          on:click={() => { goto('/analytics'); showMobileMenu = false; }}
          class="nav-link w-full justify-start {isActive('/analytics') ? 'active' : ''}"
        >
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
          </svg>
          Analytics
        </button>
        <button
          on:click={() => { goto('/issues/new'); showMobileMenu = false; }}
          class="btn-primary w-full justify-center mt-4"
        >
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
          </svg>
          New Issue
        </button>
      </div>
    </div>
  {/if}
</nav>

<!-- Click outside to close dropdown -->
{#if showDropdown}
  <div 
    class="fixed inset-0 z-30" 
    role="button"
    tabindex="0"
    on:click={() => showDropdown = false}
    on:keydown={handleKeydown}
    aria-label="Close dropdown menu"
  ></div>
{/if}

<!-- Click outside to close mobile menu -->
{#if showMobileMenu}
  <div 
    class="fixed inset-0 z-30 md:hidden" 
    role="button"
    tabindex="0"
    on:click={() => showMobileMenu = false}
    on:keydown={handleKeydown}
    aria-label="Close mobile menu"
  ></div>
{/if}
