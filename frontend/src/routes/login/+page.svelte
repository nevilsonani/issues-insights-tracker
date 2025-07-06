<script lang="ts">
  import { goto } from '$app/navigation';
  import { login } from '$lib/api';
  import { setToken, setUser } from '$lib/auth';

  let email = '';
  let password = '';
  let loading = false;
  let error = '';
  let showPassword = false;

  async function handleLogin() {
    if (!email || !password) {
      error = 'Please fill in all fields';
      return;
    }

    loading = true;
    error = '';

    try {
      const response = await login({ email, password });
      setToken(response.access_token);
      
      // For now, we'll create a basic user object
      // In a real app, you'd decode the JWT or fetch user details
      setUser({
        id: 0,
        email,
        role: 'REPORTER' // Default role, would come from JWT
      });
      
      goto('/');
    } catch (err) {
      error = err instanceof Error ? err.message : 'Login failed';
    } finally {
      loading = false;
    }
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Enter') {
      handleLogin();
    }
  }

  function togglePassword() {
    showPassword = !showPassword;
  }
</script>

<svelte:head>
  <title>Login - IssueTracker Pro</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 relative overflow-hidden">
  <!-- Animated Background Elements -->
  <div class="absolute inset-0">
    <!-- Floating orbs -->
    <div class="absolute top-20 left-10 w-72 h-72 bg-blue-500/20 rounded-full blur-3xl animate-pulse"></div>
    <div class="absolute top-40 right-20 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
    <div class="absolute bottom-20 left-1/4 w-80 h-80 bg-indigo-500/20 rounded-full blur-3xl animate-pulse delay-2000"></div>
    <div class="absolute bottom-40 right-1/3 w-64 h-64 bg-pink-500/20 rounded-full blur-3xl animate-pulse delay-3000"></div>
    
    <!-- Grid pattern overlay -->
    <div class="absolute inset-0 opacity-50" style="background-image: url('data:image/svg+xml,%3Csvg width=%2260%22 height=%2260%22 viewBox=%220 0 60 60%22 xmlns=%22http://www.w3.org/2000/svg%22%3E%3Cg fill=%22none%22 fill-rule=%22evenodd%22%3E%3Cg fill=%22%23ffffff%22 fill-opacity=%220.03%22%3E%3Ccircle cx=%2230%22 cy=%2230%22 r=%221%22/%3E%3C/g%3E%3C/g%3E%3C/svg%3E');"></div>
  </div>

  <!-- Floating particles -->
  <div class="absolute inset-0 overflow-hidden pointer-events-none">
    <div class="absolute top-1/4 left-1/4 w-2 h-2 bg-white/60 rounded-full animate-bounce"></div>
    <div class="absolute top-1/3 right-1/4 w-1 h-1 bg-white/40 rounded-full animate-bounce delay-1000"></div>
    <div class="absolute bottom-1/4 left-1/3 w-3 h-3 bg-white/50 rounded-full animate-bounce delay-2000"></div>
    <div class="absolute bottom-1/3 right-1/3 w-1 h-1 bg-white/30 rounded-full animate-bounce delay-3000"></div>
    <div class="absolute top-1/2 left-1/6 w-2 h-2 bg-blue-300/40 rounded-full animate-bounce delay-500"></div>
    <div class="absolute top-2/3 right-1/6 w-1 h-1 bg-purple-300/40 rounded-full animate-bounce delay-1500"></div>
  </div>

  <div class="relative z-10 min-h-screen flex items-center justify-center py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <!-- Header Section -->
      <div class="text-center">
        <!-- Logo Container -->
        <div class="mx-auto w-24 h-24 bg-gradient-to-br from-blue-500 to-purple-600 rounded-3xl flex items-center justify-center shadow-2xl border border-white/20 mb-8 transform hover:scale-105 transition-transform duration-300">
          <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
        </div>
        
        <!-- Title -->
        <h1 class="text-4xl md:text-5xl font-bold text-white mb-4 leading-tight">
          Welcome to <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-300 via-purple-300 to-pink-300">IssueTracker Pro</span>
        </h1>
        <p class="text-lg md:text-xl text-blue-100/90 max-w-sm mx-auto">
          Sign in to your account to continue managing issues efficiently
        </p>
      </div>

      <!-- Login Form Card -->
      <div class="bg-white/10 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 p-8 md:p-10 transform hover:scale-[1.02] transition-all duration-300">
        <form class="space-y-6" on:submit|preventDefault={handleLogin}>
          <!-- Email Field -->
          <div class="space-y-2">
            <label for="email" class="block text-sm font-semibold text-white/90 mb-3">
              Email Address
            </label>
            <div class="relative group">
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-blue-300 group-focus-within:text-blue-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"></path>
                </svg>
              </div>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                bind:value={email}
                on:keydown={handleKeydown}
                class="block w-full pl-12 pr-4 py-4 bg-white/10 border border-white/20 rounded-2xl text-white placeholder-blue-200/70 focus:outline-none focus:ring-2 focus:ring-blue-400/50 focus:border-blue-400/50 backdrop-blur-sm transition-all duration-300 group-hover:bg-white/15"
                placeholder="Enter your email address"
              />
            </div>
          </div>

          <!-- Password Field -->
          <div class="space-y-2">
            <label for="password" class="block text-sm font-semibold text-white/90 mb-3">
              Password
            </label>
            <div class="relative group">
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-blue-300 group-focus-within:text-blue-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                </svg>
              </div>
              {#if showPassword}
                <input
                  id="password"
                  name="password"
                  type="text"
                  autoComplete="current-password"
                  required
                  bind:value={password}
                  on:keydown={handleKeydown}
                  class="block w-full pl-12 pr-12 py-4 bg-white/10 border border-white/20 rounded-2xl text-white placeholder-blue-200/70 focus:outline-none focus:ring-2 focus:ring-blue-400/50 focus:border-blue-400/50 backdrop-blur-sm transition-all duration-300 group-hover:bg-white/15"
                  placeholder="Enter your password"
                />
              {:else}
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  bind:value={password}
                  on:keydown={handleKeydown}
                  class="block w-full pl-12 pr-12 py-4 bg-white/10 border border-white/20 rounded-2xl text-white placeholder-blue-200/70 focus:outline-none focus:ring-2 focus:ring-blue-400/50 focus:border-blue-400/50 backdrop-blur-sm transition-all duration-300 group-hover:bg-white/15"
                  placeholder="Enter your password"
                />
              {/if}
              <button
                type="button"
                on:click={togglePassword}
                class="absolute inset-y-0 right-0 pr-4 flex items-center text-blue-300 hover:text-blue-400 transition-colors"
              >
                {#if showPassword}
                  <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"></path>
                  </svg>
                {:else}
                  <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                  </svg>
                {/if}
              </button>
            </div>
          </div>

          <!-- Error Message -->
          {#if error}
            <div class="bg-red-500/20 backdrop-blur-sm border border-red-400/30 rounded-2xl p-4 animate-in slide-in-from-top-2">
              <div class="flex items-start">
                <svg class="h-5 w-5 text-red-300 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <div class="ml-3">
                  <p class="text-sm text-red-200 font-medium">{error}</p>
                </div>
              </div>
            </div>
          {/if}

          <!-- Login Button -->
          <button
            type="submit"
            disabled={loading}
            class="w-full flex justify-center items-center py-4 px-6 border border-transparent rounded-2xl text-lg font-semibold text-white bg-gradient-to-r from-blue-600 via-purple-600 to-blue-700 hover:from-blue-700 hover:via-purple-700 hover:to-blue-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 transform hover:scale-[1.02] shadow-2xl"
          >
            {#if loading}
              <svg class="animate-spin -ml-1 mr-3 h-6 w-6" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Signing in...
            {:else}
              <svg class="-ml-1 mr-3 h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"></path>
              </svg>
              Sign in to Dashboard
            {/if}
          </button>
        </form>

        <!-- Demo Credentials Section -->
        <div class="mt-8 pt-6 border-t border-white/20">
          <div class="text-center">
            <h3 class="text-sm font-semibold text-white/90 mb-4 flex items-center justify-center">
              <svg class="w-4 h-4 mr-2 text-blue-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              Demo Credentials
            </h3>
            <div class="bg-white/10 backdrop-blur-sm rounded-2xl p-4 space-y-3 border border-white/20">
              <div class="flex items-center justify-between text-sm">
                <span class="text-blue-200 font-medium">Email:</span>
                <span class="font-mono text-white bg-white/10 px-3 py-1.5 rounded-lg text-xs md:text-sm">admin@example.com</span>
              </div>
              <div class="flex items-center justify-between text-sm">
                <span class="text-blue-200 font-medium">Password:</span>
                <span class="font-mono text-white bg-white/10 px-3 py-1.5 rounded-lg text-xs md:text-sm">admin123</span>
              </div>
            </div>
            <p class="text-xs text-blue-200/80 mt-3 max-w-xs mx-auto">
              Use these credentials to explore the application features
            </p>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="text-center">
        <p class="text-sm text-blue-200/70">
          © 2024 IssueTracker Pro. All rights reserved.
        </p>
        <div class="mt-2 flex items-center justify-center space-x-4 text-xs text-blue-200/50">
          <span>Secure Authentication</span>
          <span>•</span>
          <span>Data Protection</span>
          <span>•</span>
          <span>24/7 Support</span>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  /* Custom animations */
  @keyframes slide-in-from-top-2 {
    from {
      opacity: 0;
      transform: translateY(-0.5rem);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  .animate-in {
    animation: slide-in-from-top-2 0.3s ease-out;
  }
  
  /* Smooth transitions for all interactive elements */
  * {
    transition-property: color, background-color, border-color, text-decoration-color, fill, stroke, opacity, box-shadow, transform, filter, backdrop-filter;
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
    transition-duration: 150ms;
  }
</style>
