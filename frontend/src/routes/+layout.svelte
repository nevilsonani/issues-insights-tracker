<script lang="ts">
  import '../app.css';
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { browser } from '$app/environment';
  import Navbar from '$lib/components/Navbar.svelte';
  import { user, isAuthenticated, initializeAuth } from '$lib/auth';
  import type { User } from '$lib/types';

  let currentUser: User | null = null;
  user.subscribe((v) => (currentUser = v));

  // Protected routes that require authentication
  const protectedRoutes = ['/', '/issues', '/dashboard', '/issues/new'];
  const authRoutes = ['/login'];

  onMount(() => {
    initializeAuth();
    
    // Check if user is authenticated for protected routes
    const currentPath = $page.url.pathname;
    const isProtectedRoute = protectedRoutes.some(route => 
      currentPath === route || currentPath.startsWith('/issues/')
    );
    const isAuthRoute = authRoutes.includes(currentPath);

    if (isProtectedRoute && !isAuthenticated()) {
      goto('/login');
    } else if (isAuthRoute && isAuthenticated()) {
      goto('/');
    }
  });

  // Reactive authentication check - only run in browser
  $: if (browser && $page.url.pathname) {
    const currentPath = $page.url.pathname;
    const isProtectedRoute = protectedRoutes.some(route => 
      currentPath === route || currentPath.startsWith('/issues/')
    );
    const isAuthRoute = authRoutes.includes(currentPath);

    if (isProtectedRoute && !isAuthenticated()) {
      goto('/login');
    } else if (isAuthRoute && isAuthenticated()) {
      goto('/');
    }
  }
</script>

{#if $page.url.pathname !== '/login'}
  <Navbar />
{/if}

<main class="min-h-screen">
  {#if $page.url.pathname !== '/login'}
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-in">
      <slot />
    </div>
  {:else}
    <div class="min-h-screen flex items-center justify-center">
    <slot />
    </div>
  {/if}
</main>

<!-- Global loading indicator -->
{#if $page.url.pathname !== '/login' && browser}
  <div class="fixed top-4 right-4 z-50">
    <!-- Loading indicator can be added here when needed -->
  </div>
{/if}
