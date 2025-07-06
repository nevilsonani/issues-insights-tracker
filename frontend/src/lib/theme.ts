import { writable } from 'svelte/store';
import { browser } from '$app/environment';

type Theme = 'light' | 'dark';

// Get initial theme from localStorage or system preference
function getInitialTheme(): Theme {
  if (!browser) return 'light';
  
  const saved = localStorage.getItem('theme') as Theme;
  if (saved && (saved === 'light' || saved === 'dark')) {
    return saved;
  }
  
  // Check system preference
  if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    return 'dark';
  }
  
  return 'light';
}

// Create the store
export const theme = writable<Theme>(getInitialTheme());

// Apply theme to document
function applyTheme(newTheme: Theme) {
  if (!browser) return;
  
  const root = document.documentElement;
  
  if (newTheme === 'dark') {
    root.classList.add('dark');
  } else {
    root.classList.remove('dark');
  }
  
  // Save to localStorage
  localStorage.setItem('theme', newTheme);
}

// Subscribe to theme changes and apply them
if (browser) {
  theme.subscribe(applyTheme);
  
  // Apply initial theme
  applyTheme(getInitialTheme());
}

// Toggle theme function
export function toggleTheme() {
  theme.update(current => current === 'light' ? 'dark' : 'light');
}

// Set specific theme
export function setTheme(newTheme: Theme) {
  theme.set(newTheme);
} 