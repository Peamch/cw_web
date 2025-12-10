# Habit Tracker Frontend

React + Vite frontend for the Habit Tracker application.

## Setup

### 1. Create directory structure

```powershell
cd C:\Users\mormy\IdeaProjects\cw_web\frontend
```

Run this PowerShell command:
```powershell
"src", "src\api", "src\components", "src\pages", "src\store", "src\utils", "public" | ForEach-Object {
    New-Item -ItemType Directory -Force -Path $_
}
```

### 2. Copy source files

Copy all files from the following markdown files:
- `FRONTEND_CODE.md` - API and Store code
- `FRONTEND_PAGES.md` - Login, Register, Dashboard
- `FRONTEND_PAGES2.md` - Goals, GoalDetail
- `FRONTEND_PAGES3.md` - Groups, GroupDetail, Achievements

### 3. Install dependencies

```powershell
npm install
```

### 4. Run development server

```powershell
npm run dev
```

Frontend will be available at: **http://localhost:3000**

## Features

### ✅ Implemented

- **Authentication**
  - Login page
  - Register page
  - JWT token management
  - Auto token refresh
  - Protected routes

- **Dashboard**
  - Goals overview
  - Quick navigation
  - Status indicators

- **Goals Management**
  - Create/Edit/Delete goals
  - View goal details
  - Log progress
  - Progress history
  - Frequency options (Daily/Weekly/Monthly)

- **Groups**
  - Browse public groups
  - Create groups
  - Join/Leave groups
  - View group details
  - Activity feed
  - Members list

- **Achievements**
  - View all achievements
  - Track earned achievements
  - Achievement rules display

### UI/UX Features

- Responsive design with Tailwind CSS
- Toast notifications (react-hot-toast)
- Loading states
- Form validation
- Modal dialogs
- Clean navigation
- Icons (lucide-react)

## Project Structure

```
frontend/
├── public/
├── src/
│   ├── api/
│   │   ├── client.js          # Axios setup with interceptors
│   │   ├── auth.js            # Auth API calls
│   │   ├── goals.js           # Goals API calls
│   │   ├── groups.js          # Groups API calls
│   │   └── achievements.js    # Achievements API calls
│   │
│   ├── components/
│   │   └── Layout.jsx         # Main layout with sidebar
│   │
│   ├── pages/
│   │   ├── Login.jsx          # Login page
│   │   ├── Register.jsx       # Registration page
│   │   ├── Dashboard.jsx      # Main dashboard
│   │   ├── Goals.jsx          # Goals list
│   │   ├── GoalDetail.jsx     # Single goal view
│   │   ├── Groups.jsx         # Groups list
│   │   ├── GroupDetail.jsx    # Single group view
│   │   └── Achievements.jsx   # Achievements page
│   │
│   ├── store/
│   │   └── authStore.js       # Zustand auth state
│   │
│   ├── App.jsx                # Main app with routes
│   ├── main.jsx               # Entry point
│   └── index.css              # Global styles
│
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## API Integration

The frontend uses a proxy configuration in `vite.config.js` to route `/api/*` requests to the backend at `http://localhost:8080`.

**Note**: Make sure the backend is running on port 8080.

## State Management

Uses **Zustand** for simple state management:
- Auth state (token, user, refresh token)
- Persisted to localStorage

## Routing

Uses **React Router v6** with:
- Public routes (login, register)
- Protected routes (dashboard, goals, groups, achievements)
- Auto redirect based on auth state

## Styling

- **Tailwind CSS** for utility-first CSS
- Responsive design
- Custom color scheme
- Clean, modern UI

## Scripts

```json
{
  "dev": "vite",           // Start dev server
  "build": "vite build",   // Build for production
  "preview": "vite preview" // Preview production build
}
```

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- ES2020+ features

## Next Steps

1. Add more UI polish (animations, transitions)
2. Add form validation feedback
3. Add loading skeletons
4. Add error boundaries
5. Add E2E tests with Cypress
6. Add dark mode support

## Troubleshooting

### Port 3000 already in use

Change port in `vite.config.js`:
```js
server: {
  port: 3001,
  // ...
}
```

### API calls failing

1. Check backend is running on port 8080
2. Check proxy configuration in `vite.config.js`
3. Check browser console for errors
4. Verify JWT token in localStorage

### Build errors

```powershell
# Clear node_modules and reinstall
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install
```

## Resources

- [React Documentation](https://react.dev)
- [Vite Documentation](https://vitejs.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [React Router](https://reactrouter.com)
- [Zustand](https://github.com/pmndrs/zustand)
