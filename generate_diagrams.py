#!/usr/bin/env python3
"""
Генерація діаграм для курсової роботи.
Створює кілька діаграм як зображення для вставки в документ.
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Шлях до збереження діаграм
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'diagrams')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Кольори для діаграм
COLORS = {
    'bg': '#FFFFFF',
    'primary': '#3B82F6',      # Синій
    'secondary': '#10B981',     # Зелений
    'accent': '#F59E0B',        # Помаранчевий
    'text': '#1F2937',          # Темно-сірий
    'border': '#6B7280',        # Сірий
    'light': '#E5E7EB',         # Світло-сірий
}

def create_font(size=14, bold=False):
    """Створює шрифт для тексту."""
    try:
        if bold:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except:
        return ImageFont.load_default()

def draw_rounded_rectangle(draw, coords, radius=10, fill='white', outline='black', width=2):
    """Малює прямокутник із закругленими кутами."""
    x1, y1, x2, y2 = coords
    draw.rectangle([x1+radius, y1, x2-radius, y2], fill=fill, outline=outline, width=0)
    draw.rectangle([x1, y1+radius, x2, y2-radius], fill=fill, outline=outline, width=0)
    
    # Кути
    draw.pieslice([x1, y1, x1+2*radius, y1+2*radius], 180, 270, fill=fill, outline=outline, width=width)
    draw.pieslice([x2-2*radius, y1, x2, y1+2*radius], 270, 360, fill=fill, outline=outline, width=width)
    draw.pieslice([x1, y2-2*radius, x1+2*radius, y2], 90, 180, fill=fill, outline=outline, width=width)
    draw.pieslice([x2-2*radius, y2-2*radius, x2, y2], 0, 90, fill=fill, outline=outline, width=width)
    
    # Borders
    draw.line([x1+radius, y1, x2-radius, y1], fill=outline, width=width)
    draw.line([x1+radius, y2, x2-radius, y2], fill=outline, width=width)
    draw.line([x1, y1+radius, x1, y2-radius], fill=outline, width=width)
    draw.line([x2, y1+radius, x2, y2-radius], fill=outline, width=width)

def create_architecture_diagram():
    """Створює діаграму архітектури системи."""
    width, height = 1200, 800
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    title_font = create_font(24, bold=True)
    header_font = create_font(18, bold=True)
    text_font = create_font(14)
    small_font = create_font(12)
    
    # Заголовок
    draw.text((width//2, 30), "Архітектура системи Habit Tracker", 
              fill=COLORS['text'], font=title_font, anchor='mm')
    
    # Frontend блок
    draw_rounded_rectangle(draw, [100, 100, 450, 650], fill='#E0F2FE', outline=COLORS['primary'], width=3)
    draw.text((275, 120), "Frontend (React)", fill=COLORS['text'], font=header_font, anchor='mm')
    
    # Frontend компоненти
    components = [
        ("App.jsx", 160),
        ("Layout.jsx", 210),
        ("Login.jsx", 260),
        ("Dashboard.jsx", 310),
        ("Goals.jsx", 360),
        ("Progress.jsx", 410),
    ]
    
    for comp, y in components:
        draw_rounded_rectangle(draw, [120, y, 430, y+35], fill=COLORS['bg'], outline=COLORS['primary'], width=2)
        draw.text((275, y+17), comp, fill=COLORS['text'], font=text_font, anchor='mm')
    
    # State Management
    draw_rounded_rectangle(draw, [120, 470, 430, 520], fill='#FEF3C7', outline=COLORS['accent'], width=2)
    draw.text((275, 495), "Zustand Store (State)", fill=COLORS['text'], font=text_font, anchor='mm')
    
    # API Client
    draw_rounded_rectangle(draw, [120, 560, 430, 610], fill='#D1FAE5', outline=COLORS['secondary'], width=2)
    draw.text((275, 585), "Axios API Client", fill=COLORS['text'], font=text_font, anchor='mm')
    
    # Backend блок
    draw_rounded_rectangle(draw, [750, 100, 1100, 650], fill='#FEF3C7', outline=COLORS['accent'], width=3)
    draw.text((925, 120), "Backend (Spring Boot)", fill=COLORS['text'], font=header_font, anchor='mm')
    
    # Backend шари
    layers = [
        ("Controllers", 160, COLORS['primary']),
        ("Services", 260, COLORS['secondary']),
        ("Repositories", 360, COLORS['accent']),
    ]
    
    for layer, y, color in layers:
        draw_rounded_rectangle(draw, [770, y, 1080, y+80], fill=COLORS['bg'], outline=color, width=2)
        draw.text((925, y+15), layer, fill=COLORS['text'], font=header_font, anchor='mm')
        
        # Приклади класів
        if layer == "Controllers":
            classes = ["AuthController", "GoalController", "ProgressController"]
        elif layer == "Services":
            classes = ["AuthService", "GoalService", "ProgressService"]
        else:
            classes = ["UserRepository", "GoalRepository", "ProgressRepository"]
        
        for i, cls in enumerate(classes):
            draw.text((780 + i*100, y+45), cls, fill=COLORS['text'], font=small_font)
    
    # Security
    draw_rounded_rectangle(draw, [770, 470, 1080, 520], fill='#FCE7F3', outline='#EC4899', width=2)
    draw.text((925, 495), "Spring Security + JWT", fill=COLORS['text'], font=text_font, anchor='mm')
    
    # Database
    draw_rounded_rectangle(draw, [770, 560, 1080, 610], fill='#D1FAE5', outline=COLORS['secondary'], width=2)
    draw.text((925, 585), "MongoDB", fill=COLORS['text'], font=text_font, anchor='mm')
    
    # Стрілки між компонентами
    # Frontend -> Backend
    draw.line([450, 400, 750, 400], fill=COLORS['border'], width=3)
    draw.polygon([(750, 400), (735, 395), (735, 405)], fill=COLORS['border'])
    draw.text((600, 380), "HTTP/REST API", fill=COLORS['text'], font=small_font, anchor='mm')
    draw.text((600, 410), "(JSON)", fill=COLORS['text'], font=small_font, anchor='mm')
    
    # Backend -> Database
    draw.line([925, 440, 925, 560], fill=COLORS['border'], width=3)
    draw.polygon([(925, 560), (920, 545), (930, 545)], fill=COLORS['border'])
    
    # Легенда
    draw.text((600, 700), "Розроблено для курсової роботи - Habit Tracker Web System", 
              fill=COLORS['border'], font=small_font, anchor='mm')
    
    img.save(os.path.join(OUTPUT_DIR, '1_architecture.png'))
    print("✅ Створено діаграму архітектури: diagrams/1_architecture.png")

def create_usecase_diagram():
    """Створює діаграму прецедентів (Use Case)."""
    width, height = 1000, 900
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    title_font = create_font(24, bold=True)
    header_font = create_font(16, bold=True)
    text_font = create_font(13)
    
    # Заголовок
    draw.text((width//2, 30), "Діаграма прецедентів (Use Case)", 
              fill=COLORS['text'], font=title_font, anchor='mm')
    
    # Система (рамка)
    draw_rounded_rectangle(draw, [250, 80, 850, 820], fill=COLORS['bg'], outline=COLORS['border'], width=3)
    draw.text((550, 100), "Habit Tracker System", fill=COLORS['text'], font=header_font, anchor='mm')
    
    # Актор: Користувач
    draw.ellipse([50, 250, 130, 330], outline=COLORS['primary'], width=2)  # Голова
    draw.line([90, 330, 90, 450], fill=COLORS['primary'], width=3)  # Тіло
    draw.line([90, 370, 50, 420], fill=COLORS['primary'], width=3)  # Ліва рука
    draw.line([90, 370, 130, 420], fill=COLORS['primary'], width=3)  # Права рука
    draw.line([90, 450, 50, 520], fill=COLORS['primary'], width=3)  # Ліва нога
    draw.line([90, 450, 130, 520], fill=COLORS['primary'], width=3)  # Права нога
    draw.text((90, 540), "Користувач", fill=COLORS['text'], font=text_font, anchor='mm')
    
    # Use Cases
    use_cases = [
        ("Реєстрація", 300, 150),
        ("Авторизація", 500, 150),
        ("Створення цілі", 300, 250),
        ("Редагування цілі", 500, 250),
        ("Видалення цілі", 700, 250),
        ("Логування\nпрогресу", 300, 350),
        ("Перегляд\nстатистики", 500, 350),
        ("Перегляд\nдосягнень", 700, 350),
        ("Створення групи", 300, 450),
        ("Приєднання\nдо групи", 500, 450),
        ("Перегляд стрічки", 500, 550),
        ("Редагування\nпрофілю", 700, 550),
    ]
    
    for name, x, y in use_cases:
        # Овал для use case
        draw.ellipse([x-80, y-30, x+80, y+30], fill='#E0F2FE', outline=COLORS['primary'], width=2)
        draw.text((x, y), name, fill=COLORS['text'], font=text_font, anchor='mm', align='center')
        
        # Лінія від користувача до use case
        draw.line([130, 400, x-80, y], fill=COLORS['border'], width=1)
    
    # Легенда
    draw.text((500, 860), "UC діаграма системи відстеження звичок", 
              fill=COLORS['border'], font=text_font, anchor='mm')
    
    img.save(os.path.join(OUTPUT_DIR, '2_usecase.png'))
    print("✅ Створено діаграму прецедентів: diagrams/2_usecase.png")

def create_er_diagram():
    """Створює ER діаграму (модель даних MongoDB)."""
    width, height = 1100, 750
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    title_font = create_font(24, bold=True)
    header_font = create_font(16, bold=True)
    text_font = create_font(12)
    small_font = create_font(11)
    
    # Заголовок
    draw.text((width//2, 30), "ER Діаграма - Модель даних MongoDB", 
              fill=COLORS['text'], font=title_font, anchor='mm')
    
    # Entity: User
    user_x, user_y = 150, 150
    draw_rounded_rectangle(draw, [user_x, user_y, user_x+250, user_y+250], 
                          fill='#E0F2FE', outline=COLORS['primary'], width=3)
    draw_rounded_rectangle(draw, [user_x, user_y, user_x+250, user_y+40], 
                          fill=COLORS['primary'], outline=COLORS['primary'], width=3)
    draw.text((user_x+125, user_y+20), "User", fill='white', font=header_font, anchor='mm')
    
    user_fields = [
        "id: String (PK)",
        "email: String (unique)",
        "passwordHash: String",
        "displayName: String",
        "role: Enum",
        "status: Enum",
        "createdAt: DateTime",
        "updatedAt: DateTime",
    ]
    
    for i, field in enumerate(user_fields):
        draw.text((user_x+10, user_y+60+i*22), field, fill=COLORS['text'], font=text_font)
    
    # Entity: Goal
    goal_x, goal_y = 550, 150
    draw_rounded_rectangle(draw, [goal_x, goal_y, goal_x+250, goal_y+300], 
                          fill='#FEF3C7', outline=COLORS['accent'], width=3)
    draw_rounded_rectangle(draw, [goal_x, goal_y, goal_x+250, goal_y+40], 
                          fill=COLORS['accent'], outline=COLORS['accent'], width=3)
    draw.text((goal_x+125, goal_y+20), "Goal", fill='white', font=header_font, anchor='mm')
    
    goal_fields = [
        "id: String (PK)",
        "userId: String (FK)",
        "title: String",
        "description: String",
        "frequency: Enum",
        "startDate: Date",
        "endDate: Date",
        "isPublic: Boolean",
        "status: Enum",
        "createdAt: DateTime",
        "updatedAt: DateTime",
    ]
    
    for i, field in enumerate(goal_fields):
        draw.text((goal_x+10, goal_y+60+i*22), field, fill=COLORS['text'], font=text_font)
    
    # Entity: Progress
    prog_x, prog_y = 850, 480
    draw_rounded_rectangle(draw, [prog_x, prog_y, prog_x+220, prog_y+200], 
                          fill='#D1FAE5', outline=COLORS['secondary'], width=3)
    draw_rounded_rectangle(draw, [prog_x, prog_y, prog_x+220, prog_y+40], 
                          fill=COLORS['secondary'], outline=COLORS['secondary'], width=3)
    draw.text((prog_x+110, prog_y+20), "Progress", fill='white', font=header_font, anchor='mm')
    
    progress_fields = [
        "id: String (PK)",
        "goalId: String (FK)",
        "userId: String (FK)",
        "date: Date",
        "completed: Boolean",
        "notes: String",
        "createdAt: DateTime",
    ]
    
    for i, field in enumerate(progress_fields):
        draw.text((prog_x+10, prog_y+60+i*22), field, fill=COLORS['text'], font=text_font)
    
    # Entity: Group
    group_x, group_y = 150, 480
    draw_rounded_rectangle(draw, [group_x, group_y, group_x+250, group_y+200], 
                          fill='#FCE7F3', outline='#EC4899', width=3)
    draw_rounded_rectangle(draw, [group_x, group_y, group_x+250, group_y+40], 
                          fill='#EC4899', outline='#EC4899', width=3)
    draw.text((group_x+125, group_y+20), "Group", fill='white', font=header_font, anchor='mm')
    
    group_fields = [
        "id: String (PK)",
        "name: String",
        "description: String",
        "ownerId: String (FK)",
        "memberIds: Array<String>",
        "visibility: Enum",
        "createdAt: DateTime",
    ]
    
    for i, field in enumerate(group_fields):
        draw.text((group_x+10, group_y+60+i*22), field, fill=COLORS['text'], font=text_font)
    
    # Зв'язки
    # User -> Goal (1:N)
    draw.line([400, 250, 550, 250], fill=COLORS['border'], width=2)
    draw.polygon([(550, 250), (535, 245), (535, 255)], fill=COLORS['border'])
    draw.text((475, 230), "1:N", fill=COLORS['text'], font=small_font, anchor='mm')
    draw.text((475, 265), "has", fill=COLORS['text'], font=small_font, anchor='mm')
    
    # Goal -> Progress (1:N)
    draw.line([700, 450, 700, 520, 850, 520], fill=COLORS['border'], width=2)
    draw.polygon([(850, 520), (835, 515), (835, 525)], fill=COLORS['border'])
    draw.text((775, 505), "1:N", fill=COLORS['text'], font=small_font, anchor='mm')
    
    # User -> Group (1:N owner)
    draw.line([275, 400, 275, 480], fill=COLORS['border'], width=2)
    draw.polygon([(275, 480), (270, 465), (280, 465)], fill=COLORS['border'])
    draw.text((250, 440), "1:N", fill=COLORS['text'], font=small_font, anchor='mm')
    draw.text((310, 440), "owns", fill=COLORS['text'], font=small_font, anchor='mm')
    
    # Легенда
    draw.text((550, 720), "Структура колекцій MongoDB", 
              fill=COLORS['border'], font=text_font, anchor='mm')
    
    img.save(os.path.join(OUTPUT_DIR, '3_er_diagram.png'))
    print("✅ Створено ER діаграму: diagrams/3_er_diagram.png")

def create_sequence_diagram():
    """Створює діаграму послідовності для автентифікації."""
    width, height = 1000, 850
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    title_font = create_font(24, bold=True)
    header_font = create_font(14, bold=True)
    text_font = create_font(12)
    
    # Заголовок
    draw.text((width//2, 30), "Діаграма послідовності - Автентифікація користувача", 
              fill=COLORS['text'], font=title_font, anchor='mm')
    
    # Актори/Системи
    actors = [
        ("Користувач", 100),
        ("React App", 300),
        ("AuthController", 500),
        ("AuthService", 700),
        ("MongoDB", 900),
    ]
    
    # Малюємо заголовки акторів
    y_start = 80
    for name, x in actors:
        draw_rounded_rectangle(draw, [x-60, y_start, x+60, y_start+40], 
                              fill=COLORS['primary'], outline=COLORS['primary'], width=2)
        draw.text((x, y_start+20), name, fill='white', font=header_font, anchor='mm')
        # Лінія життя (пунктирна)
        for y in range(y_start+40, 750, 10):
            draw.line([x, y, x, y+5], fill=COLORS['border'], width=1)
    
    # Повідомлення (стрілки)
    messages = [
        (100, 300, "1. Введення email/password", 150, None),
        (300, 500, "2. POST /auth/login", 200, COLORS['primary']),
        (500, 700, "3. login(request)", 250, COLORS['accent']),
        (700, 900, "4. findByEmail(email)", 300, COLORS['secondary']),
        (900, 700, "5. User object", 350, COLORS['secondary']),
        (700, 700, "6. BCrypt.verify()", 400, None),
        (700, 700, "7. JwtUtils.generate()", 450, None),
        (700, 500, "8. AuthResponse + tokens", 500, COLORS['accent']),
        (500, 300, "9. {accessToken, refreshToken}", 550, COLORS['primary']),
        (300, 300, "10. Zustand.setTokens()", 600, None),
        (300, 100, "11. Redirect to Dashboard", 650, COLORS['secondary']),
    ]
    
    for x1, x2, text, y, color in messages:
        if color:
            draw.line([x1, y, x2, y], fill=color, width=2)
            if x1 < x2:
                draw.polygon([(x2, y), (x2-10, y-5), (x2-10, y+5)], fill=color)
            else:
                draw.polygon([(x2, y), (x2+10, y-5), (x2+10, y+5)], fill=color)
        else:
            draw.line([x1, y, x2, y], fill=COLORS['border'], width=1)
        
        # Текст повідомлення
        text_x = (x1 + x2) // 2
        draw.text((text_x, y-15), text, fill=COLORS['text'], font=text_font, anchor='mm')
    
    # Активація (прямокутники на лінії життя)
    activations = [
        (300, 150, 660),  # React App
        (500, 200, 560),  # AuthController
        (700, 250, 510),  # AuthService
        (900, 300, 360),  # MongoDB
    ]
    
    for x, y1, y2 in activations:
        draw_rounded_rectangle(draw, [x-10, y1, x+10, y2], 
                              fill='white', outline=COLORS['border'], width=2)
    
    # Нотатки
    draw_rounded_rectangle(draw, [50, 720, 950, 800], 
                          fill='#FEF3C7', outline=COLORS['accent'], width=2)
    notes = [
        "Примітки:",
        "• Пароль хешується за допомогою BCrypt перед збереженням",
        "• JWT токени мають термін дії: accessToken - 24 год, refreshToken - 30 днів",
        "• Токени зберігаються в Zustand store та localStorage для персистентності",
    ]
    for i, note in enumerate(notes):
        draw.text((60, 730+i*18), note, fill=COLORS['text'], font=text_font)
    
    img.save(os.path.join(OUTPUT_DIR, '4_sequence.png'))
    print("✅ Створено діаграму послідовності: diagrams/4_sequence.png")

def create_class_diagram():
    """Створює діаграму класів Backend."""
    width, height = 1200, 900
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    title_font = create_font(24, bold=True)
    header_font = create_font(14, bold=True)
    text_font = create_font(11)
    small_font = create_font(10)
    
    # Заголовок
    draw.text((width//2, 30), "Діаграма класів - Backend (Spring Boot)", 
              fill=COLORS['text'], font=title_font, anchor='mm')
    
    # Class: GoalController
    ctrl_x, ctrl_y = 80, 100
    draw_rounded_rectangle(draw, [ctrl_x, ctrl_y, ctrl_x+280, ctrl_y+220], 
                          fill='#E0F2FE', outline=COLORS['primary'], width=3)
    draw_rounded_rectangle(draw, [ctrl_x, ctrl_y, ctrl_x+280, ctrl_y+35], 
                          fill=COLORS['primary'], outline=COLORS['primary'], width=3)
    draw.text((ctrl_x+140, ctrl_y+17), "«Controller»\nGoalController", 
              fill='white', font=header_font, anchor='mm', align='center')
    
    draw.line([ctrl_x, ctrl_y+35, ctrl_x+280, ctrl_y+35], fill=COLORS['primary'], width=2)
    draw.text((ctrl_x+10, ctrl_y+45), "- goalService: GoalService", fill=COLORS['text'], font=text_font)
    
    draw.line([ctrl_x, ctrl_y+70, ctrl_x+280, ctrl_y+70], fill=COLORS['primary'], width=2)
    methods = [
        "+ createGoal(request): Goal",
        "+ getGoals(): List<Goal>",
        "+ getGoalById(id): Goal",
        "+ updateGoal(id, req): Goal",
        "+ deleteGoal(id): void",
    ]
    for i, method in enumerate(methods):
        draw.text((ctrl_x+10, ctrl_y+80+i*18), method, fill=COLORS['text'], font=text_font)
    
    # Class: GoalService
    svc_x, svc_y = 480, 100
    draw_rounded_rectangle(draw, [svc_x, svc_y, svc_x+280, svc_y+220], 
                          fill='#FEF3C7', outline=COLORS['accent'], width=3)
    draw_rounded_rectangle(draw, [svc_x, svc_y, svc_x+280, svc_y+35], 
                          fill=COLORS['accent'], outline=COLORS['accent'], width=3)
    draw.text((svc_x+140, svc_y+17), "«Service»\nGoalService", 
              fill='white', font=header_font, anchor='mm', align='center')
    
    draw.line([svc_x, svc_y+35, svc_x+280, svc_y+35], fill=COLORS['accent'], width=2)
    draw.text((svc_x+10, svc_y+45), "- goalRepo: GoalRepository", fill=COLORS['text'], font=text_font)
    
    draw.line([svc_x, svc_y+70, svc_x+280, svc_y+70], fill=COLORS['accent'], width=2)
    svc_methods = [
        "+ createGoal(userId, req): Goal",
        "+ findByUserId(userId): List",
        "+ findById(id): Optional<Goal>",
        "+ updateGoal(id, req): Goal",
        "+ deleteGoal(id): void",
    ]
    for i, method in enumerate(svc_methods):
        draw.text((svc_x+10, svc_y+80+i*18), method, fill=COLORS['text'], font=text_font)
    
    # Class: GoalRepository
    repo_x, repo_y = 880, 100
    draw_rounded_rectangle(draw, [repo_x, repo_y, repo_x+280, repo_y+180], 
                          fill='#D1FAE5', outline=COLORS['secondary'], width=3)
    draw_rounded_rectangle(draw, [repo_x, repo_y, repo_x+280, repo_y+35], 
                          fill=COLORS['secondary'], outline=COLORS['secondary'], width=3)
    draw.text((repo_x+140, repo_y+17), "«Interface»\nGoalRepository", 
              fill='white', font=header_font, anchor='mm', align='center')
    
    draw.line([repo_x, repo_y+35, repo_x+280, repo_y+35], fill=COLORS['secondary'], width=2)
    draw.text((repo_x+10, repo_y+45), "extends MongoRepository", fill=COLORS['text'], font=small_font)
    
    draw.line([repo_x, repo_y+70, repo_x+280, repo_y+70], fill=COLORS['secondary'], width=2)
    repo_methods = [
        "+ findByUserId(userId): List",
        "+ findByUserIdAndStatus(): List",
        "+ findByIsPublicTrue(): List",
    ]
    for i, method in enumerate(repo_methods):
        draw.text((repo_x+10, repo_y+80+i*25), method, fill=COLORS['text'], font=text_font)
    
    # Class: Goal (Entity)
    entity_x, entity_y = 480, 420
    draw_rounded_rectangle(draw, [entity_x, entity_y, entity_x+280, entity_y+380], 
                          fill='#FCE7F3', outline='#EC4899', width=3)
    draw_rounded_rectangle(draw, [entity_x, entity_y, entity_x+280, entity_y+35], 
                          fill='#EC4899', outline='#EC4899', width=3)
    draw.text((entity_x+140, entity_y+17), "«Entity»\nGoal", 
              fill='white', font=header_font, anchor='mm', align='center')
    
    draw.line([entity_x, entity_y+35, entity_x+280, entity_y+35], fill='#EC4899', width=2)
    entity_fields = [
        "- id: String",
        "- userId: String",
        "- title: String",
        "- description: String",
        "- frequency: Frequency",
        "- startDate: LocalDate",
        "- endDate: LocalDate",
        "- isPublic: boolean",
        "- status: GoalStatus",
        "- createdAt: LocalDateTime",
        "- updatedAt: LocalDateTime",
    ]
    for i, field in enumerate(entity_fields):
        draw.text((entity_x+10, entity_y+45+i*18), field, fill=COLORS['text'], font=text_font)
    
    draw.line([entity_x, entity_y+250, entity_x+280, entity_y+250], fill='#EC4899', width=2)
    entity_methods = [
        "+ getId(): String",
        "+ setId(id): void",
        "+ getTitle(): String",
        "+ setTitle(title): void",
        "...",
    ]
    for i, method in enumerate(entity_methods):
        draw.text((entity_x+10, entity_y+260+i*20), method, fill=COLORS['text'], font=text_font)
    
    # Зв'язки (залежності)
    # Controller -> Service
    draw.line([360, 200, 480, 200], fill=COLORS['border'], width=2)
    draw.polygon([(480, 200), (465, 195), (465, 205)], fill=COLORS['border'])
    draw.text((420, 180), "uses", fill=COLORS['text'], font=small_font, anchor='mm')
    
    # Service -> Repository
    draw.line([760, 200, 880, 200], fill=COLORS['border'], width=2)
    draw.polygon([(880, 200), (865, 195), (865, 205)], fill=COLORS['border'])
    draw.text((820, 180), "uses", fill=COLORS['text'], font=small_font, anchor='mm')
    
    # Service -> Entity
    draw.line([620, 320, 620, 420], fill=COLORS['border'], width=2)
    draw.polygon([(620, 420), (615, 405), (625, 405)], fill=COLORS['border'])
    draw.text((640, 370), "manages", fill=COLORS['text'], font=small_font, anchor='mm')
    
    # Repository -> Entity
    draw.line([1020, 280, 1020, 600, 760, 600], fill=COLORS['border'], width=2)
    draw.polygon([(760, 600), (775, 595), (775, 605)], fill=COLORS['border'])
    draw.text((890, 580), "persists", fill=COLORS['text'], font=small_font, anchor='mm')
    
    # Легенда
    draw.text((600, 860), "Структура класів шару Backend з залежностями", 
              fill=COLORS['border'], font=text_font, anchor='mm')
    
    img.save(os.path.join(OUTPUT_DIR, '5_class_diagram.png'))
    print("✅ Створено діаграму класів: diagrams/5_class_diagram.png")

if __name__ == '__main__':
    print("Генерація діаграм для курсової роботи...\n")
    
    create_architecture_diagram()
    create_usecase_diagram()
    create_er_diagram()
    create_sequence_diagram()
    create_class_diagram()
    
    print(f"\n✅ Всі діаграми створено в папці '{OUTPUT_DIR}'")
    print("\nГотові діаграми:")
    print("1. 1_architecture.png - Архітектура системи")
    print("2. 2_usecase.png - Діаграма прецедентів")
    print("3. 3_er_diagram.png - ER діаграма (модель даних)")
    print("4. 4_sequence.png - Діаграма послідовності (автентифікація)")
    print("5. 5_class_diagram.png - Діаграма класів (Backend)")
