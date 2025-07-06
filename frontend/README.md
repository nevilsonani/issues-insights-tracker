# Issues & Insights Tracker - Frontend

A modern SvelteKit frontend for the Issues & Insights Tracker application.

## Features

- 🎨 Modern, responsive UI with Tailwind CSS
- 🔐 Authentication with JWT tokens
- 📊 Interactive charts and analytics
- 🔍 Real-time issue filtering and search
- 📱 Mobile-friendly design
- 🚀 Fast development with hot reload

## Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend API running (see backend README)

## Quick Start

1. **Install dependencies:**
   ```bash
   npm install --legacy-peer-deps
   ```

2. **Start the development server:**
   ```bash
   npm run dev
   ```

3. **Open your browser:**
   Navigate to `http://localhost:5173`

## Development

- **Build for production:**
  ```bash
  npm run build
  ```

- **Preview production build:**
  ```bash
  npm run preview
  ```

- **Type checking:**
  ```bash
  npm run check
  ```

## Project Structure

```
src/
├── lib/
│   ├── api.ts          # API client functions
│   ├── auth.ts         # Authentication store
│   ├── types.ts        # TypeScript type definitions
│   └── components/     # Reusable Svelte components
├── routes/             # SvelteKit pages
└── app.css            # Global styles
```

## API Configuration

The frontend expects the backend API at `http://localhost:8000`. To change this:

1. Edit `src/lib/api.ts`
2. Update the `API_BASE` constant

## Authentication

The app uses JWT tokens stored in localStorage. Demo credentials:
- Email: `demo@example.com`
- Password: `password123`

## Technologies Used

- **SvelteKit** - Full-stack framework
- **Tailwind CSS** - Utility-first CSS framework
- **TypeScript** - Type safety
- **Marked** - Markdown rendering
- **SVG Icons** - Custom icon set

## Docker

To run with Docker:

```bash
# From the project root
docker compose up frontend
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request
