# Frontend Setup Instructions

## Step 1: Create Directory Structure

Run these commands in PowerShell from the `frontend` directory:

```powershell
# Create main directories
New-Item -ItemType Directory -Force -Path src
New-Item -ItemType Directory -Force -Path src\api
New-Item -ItemType Directory -Force -Path src\components
New-Item -ItemType Directory -Force -Path src\pages
New-Item -ItemType Directory -Force -Path src\store
New-Item -ItemType Directory -Force -Path src\utils
New-Item -ItemType Directory -Force -Path public
```

## Step 2: Install Dependencies

```powershell
npm install
```

## Step 3: Copy Source Files

The source files are ready to be created. After running Step 1, I'll provide all the source code.

## Directory Structure

```
frontend/
├── public/
├── src/
│   ├── api/           # API client & axios setup
│   ├── components/    # Reusable components
│   ├── pages/         # Page components
│   ├── store/         # Zustand stores
│   ├── utils/         # Utility functions
│   ├── App.jsx        # Main app component
│   ├── main.jsx       # Entry point
│   └── index.css      # Global styles
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## Step 4: Run Development Server

```powershell
npm run dev
```

Frontend will be available at: http://localhost:3000

## Quick Setup Script

Or run this all-in-one script:

```powershell
# Navigate to frontend directory
cd C:\Users\mormy\IdeaProjects\cw_web\frontend

# Create directories
"src", "src\api", "src\components", "src\pages", "src\store", "src\utils", "public" | ForEach-Object {
    New-Item -ItemType Directory -Force -Path $_
}

# Install dependencies
npm install

Write-Host "✓ Frontend structure created!" -ForegroundColor Green
Write-Host "Next: Copy the source files" -ForegroundColor Yellow
```
