Write-Host "Testing Habit Tracker API..." -ForegroundColor Cyan

# 1. Signup
Write-Host "`n1. Creating new user..." -ForegroundColor Yellow
$signupBody = @{
    email = "test@example.com"
    password = "test123"
    displayName = "Test User"
} | ConvertTo-Json

try {
    $signup = Invoke-RestMethod -Uri "http://localhost:8080/auth/signup" -Method Post -ContentType "application/json" -Body $signupBody
    Write-Host "✓ Signup successful" -ForegroundColor Green
    $token = $signup.data.accessToken
} catch {
    Write-Host "✗ Signup failed (user might already exist)" -ForegroundColor Red
    
    # Try login instead
    Write-Host "  Trying login..." -ForegroundColor Yellow
    $loginBody = @{
        email = "test@example.com"
        password = "test123"
    } | ConvertTo-Json
    
    $login = Invoke-RestMethod -Uri "http://localhost:8080/auth/login" -Method Post -ContentType "application/json" -Body $loginBody
    Write-Host "✓ Login successful" -ForegroundColor Green
    $token = $login.data.accessToken
}

$headers = @{
    Authorization = "Bearer $token"
    "Content-Type" = "application/json"
}

# 2. Create Goal
Write-Host "`n2. Creating goal..." -ForegroundColor Yellow
$goalBody = @{
    title = "Morning Exercise"
    description = "30 minutes of exercise"
    frequency = "DAILY"
    isPublic = $false
} | ConvertTo-Json

$goal = Invoke-RestMethod -Uri "http://localhost:8080/goals" -Method Post -Headers $headers -Body $goalBody
Write-Host "✓ Goal created: $($goal.data.id)" -ForegroundColor Green
$goalId = $goal.data.id

# 3. Log Progress
Write-Host "`n3. Logging progress..." -ForegroundColor Yellow
$progressBody = @{
    goalId = $goalId
    value = 1.0
    note = "Completed workout"
} | ConvertTo-Json

$progress = Invoke-RestMethod -Uri "http://localhost:8080/progress" -Method Post -Headers $headers -Body $progressBody
Write-Host "✓ Progress logged" -ForegroundColor Green

# 4. Get Goals
Write-Host "`n4. Getting goals..." -ForegroundColor Yellow
$goals = Invoke-RestMethod -Uri "http://localhost:8080/goals" -Method Get -Headers $headers
Write-Host "✓ Found $($goals.data.Count) goal(s)" -ForegroundColor Green

# 5. Create Group
Write-Host "`n5. Creating group..." -ForegroundColor Yellow
$groupBody = @{
    name = "Fitness Buddies"
    description = "Daily fitness goals"
    visibility = "PUBLIC"
} | ConvertTo-Json

$group = Invoke-RestMethod -Uri "http://localhost:8080/groups" -Method Post -Headers $headers -Body $groupBody
Write-Host "✓ Group created: $($group.data.id)" -ForegroundColor Green

# 6. Check Achievements
Write-Host "`n6. Checking achievements..." -ForegroundColor Yellow
$achievements = Invoke-RestMethod -Uri "http://localhost:8080/achievements" -Method Get -Headers $headers
Write-Host "✓ Found $($achievements.data.Count) achievement(s)" -ForegroundColor Green

$myAchievements = Invoke-RestMethod -Uri "http://localhost:8080/achievements/me" -Method Get -Headers $headers
Write-Host "✓ You earned $($myAchievements.data.Count) achievement(s)" -ForegroundColor Green

Write-Host "`n✅ All tests passed!" -ForegroundColor Green
Write-Host "`nYour token: $token" -ForegroundColor Gray
