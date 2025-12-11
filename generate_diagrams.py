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
        draw.rectangle([x-10, y1, x+10, y2], fill='white', outline=COLORS['border'], width=2)
    
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

def create_component_diagram():
    """Створює діаграму компонентів Frontend."""
    width, height = 1100, 850
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    title_font = create_font(24, bold=True)
    header_font = create_font(16, bold=True)
    text_font = create_font(12)
    small_font = create_font(11)
    
    # Заголовок
    draw.text((width//2, 30), "Діаграма компонентів - Frontend React", 
              fill=COLORS['text'], font=title_font, anchor='mm')
    
    # Main App Component
    draw_rounded_rectangle(draw, [80, 80, 1020, 780], 
                          fill='#F0F9FF', outline=COLORS['primary'], width=3)
    draw.text((550, 100), "App.jsx", fill=COLORS['text'], font=header_font, anchor='mm')
    
    # Layout Component
    draw_rounded_rectangle(draw, [100, 140, 1000, 240], 
                          fill='#E0F2FE', outline=COLORS['primary'], width=2)
    draw.text((550, 160), "Layout.jsx", fill=COLORS['text'], font=header_font, anchor='mm')
    draw.text((120, 190), "• Navigation Bar", fill=COLORS['text'], font=text_font)
    draw.text((120, 210), "• User Menu & Logout", fill=COLORS['text'], font=text_font)
    
    # Pages Column 1
    pages_col1 = [
        ("Login.jsx", 280, "• Email/Password form\n• JWT authentication\n• Redirect on success"),
        ("Register.jsx", 400, "• User registration\n• Email validation\n• Password strength"),
        ("Dashboard.jsx", 520, "• Goal statistics\n• Recent activity\n• Quick actions"),
    ]
    
    x_offset = 100
    for name, y, desc in pages_col1:
        draw_rounded_rectangle(draw, [x_offset, y, x_offset+280, y+100], 
                              fill='#FEF3C7', outline=COLORS['accent'], width=2)
        draw.text((x_offset+140, y+15), name, fill=COLORS['text'], font=header_font, anchor='mm')
        for i, line in enumerate(desc.split('\n')):
            draw.text((x_offset+10, y+40+i*15), line, fill=COLORS['text'], font=small_font)
    
    # Pages Column 2
    pages_col2 = [
        ("Goals.jsx", 280, "• Goal list view\n• Filter & search\n• Create new goal"),
        ("GoalDetail.jsx", 400, "• Goal information\n• Progress chart\n• Update/Delete"),
        ("Achievements.jsx", 520, "• Earned badges\n• Progress stats\n• Milestones"),
    ]
    
    x_offset = 420
    for name, y, desc in pages_col2:
        draw_rounded_rectangle(draw, [x_offset, y, x_offset+280, y+100], 
                              fill='#D1FAE5', outline=COLORS['secondary'], width=2)
        draw.text((x_offset+140, y+15), name, fill=COLORS['text'], font=header_font, anchor='mm')
        for i, line in enumerate(desc.split('\n')):
            draw.text((x_offset+10, y+40+i*15), line, fill=COLORS['text'], font=small_font)
    
    # Pages Column 3
    pages_col3 = [
        ("Groups.jsx", 280, "• Group list\n• Join/Create group\n• Search groups"),
        ("GroupDetail.jsx", 400, "• Group info\n• Members list\n• Shared activity"),
    ]
    
    x_offset = 740
    for name, y, desc in pages_col3:
        draw_rounded_rectangle(draw, [x_offset, y, x_offset+250, y+100], 
                              fill='#FCE7F3', outline='#EC4899', width=2)
        draw.text((x_offset+125, y+15), name, fill=COLORS['text'], font=header_font, anchor='mm')
        for i, line in enumerate(desc.split('\n')):
            draw.text((x_offset+10, y+40+i*15), line, fill=COLORS['text'], font=small_font)
    
    # State Management
    draw_rounded_rectangle(draw, [100, 650, 480, 740], 
                          fill='#FEF3C7', outline=COLORS['accent'], width=3)
    draw.text((290, 670), "Zustand Store", fill=COLORS['text'], font=header_font, anchor='mm')
    draw.text((110, 695), "• authStore (user, tokens)", fill=COLORS['text'], font=text_font)
    draw.text((110, 715), "• Persist to localStorage", fill=COLORS['text'], font=text_font)
    
    # API Layer
    draw_rounded_rectangle(draw, [520, 650, 1000, 740], 
                          fill='#D1FAE5', outline=COLORS['secondary'], width=3)
    draw.text((760, 670), "API Clients (Axios)", fill=COLORS['text'], font=header_font, anchor='mm')
    draw.text((530, 695), "• auth.js   • goals.js   • groups.js", fill=COLORS['text'], font=text_font)
    draw.text((530, 715), "• achievements.js   • client.js (base)", fill=COLORS['text'], font=text_font)
    
    # Стрілки взаємодії
    draw.line([550, 240, 550, 280], fill=COLORS['border'], width=2)
    draw.polygon([(550, 280), (545, 265), (555, 265)], fill=COLORS['border'])
    
    img.save(os.path.join(OUTPUT_DIR, '6_component_diagram.png'))
    print("✅ Створено діаграму компонентів: diagrams/6_component_diagram.png")

def create_deployment_diagram():
    """Створює діаграму розгортання (Deployment)."""
    width, height = 1200, 900
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    title_font = create_font(24, bold=True)
    header_font = create_font(16, bold=True)
    text_font = create_font(13)
    small_font = create_font(11)
    
    # Заголовок
    draw.text((width//2, 30), "Діаграма розгортання системи", 
              fill=COLORS['text'], font=title_font, anchor='mm')
    
    # Client Device
    draw_rounded_rectangle(draw, [80, 100, 380, 350], 
                          fill='#E0F2FE', outline=COLORS['primary'], width=3)
    draw.text((230, 120), "Client Device", fill=COLORS['text'], font=header_font, anchor='mm')
    
    # Browser
    draw_rounded_rectangle(draw, [100, 160, 360, 320], 
                          fill='white', outline=COLORS['primary'], width=2)
    draw.text((230, 180), "Web Browser", fill=COLORS['text'], font=header_font, anchor='mm')
    
    # React App
    draw_rounded_rectangle(draw, [120, 220, 340, 300], 
                          fill='#FEF3C7', outline=COLORS['accent'], width=2)
    draw.text((230, 240), "React SPA", fill=COLORS['text'], font=text_font, anchor='mm')
    draw.text((130, 265), "• Vite bundled", fill=COLORS['text'], font=small_font)
    draw.text((130, 280), "• Tailwind CSS", fill=COLORS['text'], font=small_font)
    
    # Web Server
    draw_rounded_rectangle(draw, [480, 100, 780, 400], 
                          fill='#FEF3C7', outline=COLORS['accent'], width=3)
    draw.text((630, 120), "Web Server", fill=COLORS['text'], font=header_font, anchor='mm')
    
    # Nginx
    draw_rounded_rectangle(draw, [500, 160, 760, 240], 
                          fill='white', outline=COLORS['secondary'], width=2)
    draw.text((630, 180), "Nginx", fill=COLORS['text'], font=header_font, anchor='mm')
    draw.text((510, 205), "• Reverse proxy", fill=COLORS['text'], font=small_font)
    draw.text((510, 220), "• Static files serving", fill=COLORS['text'], font=small_font)
    
    # Docker Container
    draw_rounded_rectangle(draw, [500, 260, 760, 380], 
                          fill='#E0F2FE', outline=COLORS['primary'], width=2)
    draw.text((630, 280), "Docker Container", fill=COLORS['text'], font=header_font, anchor='mm')
    
    # Spring Boot App
    draw_rounded_rectangle(draw, [520, 310, 740, 360], 
                          fill='#D1FAE5', outline=COLORS['secondary'], width=2)
    draw.text((630, 335), "Spring Boot App", fill=COLORS['text'], font=text_font, anchor='mm')
    
    # Database Server
    draw_rounded_rectangle(draw, [880, 100, 1120, 400], 
                          fill='#D1FAE5', outline=COLORS['secondary'], width=3)
    draw.text((1000, 120), "Database Server", fill=COLORS['text'], font=header_font, anchor='mm')
    
    # MongoDB
    draw_rounded_rectangle(draw, [900, 160, 1100, 280], 
                          fill='white', outline=COLORS['secondary'], width=2)
    draw.text((1000, 180), "MongoDB", fill=COLORS['text'], font=header_font, anchor='mm')
    draw.text((910, 210), "Collections:", fill=COLORS['text'], font=small_font)
    draw.text((920, 230), "• users", fill=COLORS['text'], font=small_font)
    draw.text((920, 245), "• goals", fill=COLORS['text'], font=small_font)
    draw.text((920, 260), "• progress", fill=COLORS['text'], font=small_font)
    
    # Docker Volume
    draw_rounded_rectangle(draw, [900, 300, 1100, 370], 
                          fill='#FEF3C7', outline=COLORS['accent'], width=2)
    draw.text((1000, 320), "Docker Volume", fill=COLORS['text'], font=text_font, anchor='mm')
    draw.text((910, 345), "/data/db (persistent)", fill=COLORS['text'], font=small_font)
    
    # Docker Network
    draw_rounded_rectangle(draw, [480, 480, 1120, 600], 
                          fill='#F0F9FF', outline=COLORS['border'], width=3)
    draw.text((800, 500), "Docker Network: habit-tracker-net", fill=COLORS['text'], font=header_font, anchor='mm')
    draw.text((500, 530), "• Bridge network for container communication", fill=COLORS['text'], font=text_font)
    draw.text((500, 555), "• Internal DNS resolution", fill=COLORS['text'], font=text_font)
    draw.text((500, 575), "• Port mapping: 8080:8080 (backend), 27017:27017 (mongodb)", fill=COLORS['text'], font=small_font)
    
    # Connections
    # Client -> Web Server
    draw.line([380, 225, 480, 225], fill=COLORS['primary'], width=3)
    draw.polygon([(480, 225), (465, 220), (465, 230)], fill=COLORS['primary'])
    draw.text((430, 205), "HTTP/HTTPS", fill=COLORS['text'], font=small_font, anchor='mm')
    
    # Web Server -> Database
    draw.line([780, 300, 880, 220], fill=COLORS['secondary'], width=3)
    draw.polygon([(880, 220), (865, 220), (875, 230)], fill=COLORS['secondary'])
    draw.text((830, 250), "MongoDB", fill=COLORS['text'], font=small_font, anchor='mm')
    draw.text((830, 265), "Protocol", fill=COLORS['text'], font=small_font, anchor='mm')
    
    # Technologies
    draw_rounded_rectangle(draw, [80, 680, 1120, 850], 
                          fill='#F9FAFB', outline=COLORS['border'], width=2)
    draw.text((600, 700), "Технології та інструменти розгортання", 
              fill=COLORS['text'], font=header_font, anchor='mm')
    
    tech_items = [
        "• Docker & Docker Compose для контейнеризації",
        "• Nginx як reverse proxy та для статичних файлів",
        "• MongoDB в Docker контейнері з persistent volume",
        "• Spring Boot JAR у Docker контейнері",
        "• React SPA побудований з Vite та розміщений через Nginx",
        "• Docker networks для ізоляції та комунікації",
        "• Environment variables для конфігурації",
        "• Health checks для моніторингу стану сервісів",
    ]
    
    for i, item in enumerate(tech_items):
        row = i // 2
        col = i % 2
        x = 100 + col * 520
        y = 730 + row * 25
        draw.text((x, y), item, fill=COLORS['text'], font=small_font)
    
    img.save(os.path.join(OUTPUT_DIR, '7_deployment_diagram.png'))
    print("✅ Створено діаграму розгортання: diagrams/7_deployment_diagram.png")

def create_state_diagram():
    """Створює діаграму станів для Goal lifecycle."""
    width, height = 1100, 800
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    title_font = create_font(24, bold=True)
    header_font = create_font(16, bold=True)
    text_font = create_font(13)
    small_font = create_font(11)
    
    # Заголовок
    draw.text((width//2, 30), "Діаграма станів - Життєвий цикл Goal", 
              fill=COLORS['text'], font=title_font, anchor='mm')
    
    # Initial state (black circle)
    draw.ellipse([530, 80, 550, 100], fill='black', outline='black')
    
    # DRAFT state
    draw_rounded_rectangle(draw, [220, 140, 440, 220], 
                          fill='#FEF3C7', outline=COLORS['accent'], width=3, radius=20)
    draw.text((330, 180), "DRAFT", fill=COLORS['text'], font=header_font, anchor='mm')
    
    # ACTIVE state
    draw_rounded_rectangle(draw, [220, 280, 440, 360], 
                          fill='#D1FAE5', outline=COLORS['secondary'], width=3, radius=20)
    draw.text((330, 320), "ACTIVE", fill=COLORS['text'], font=header_font, anchor='mm')
    
    # PAUSED state
    draw_rounded_rectangle(draw, [660, 280, 880, 360], 
                          fill='#FEF3C7', outline=COLORS['accent'], width=3, radius=20)
    draw.text((770, 320), "PAUSED", fill=COLORS['text'], font=header_font, anchor='mm')
    
    # COMPLETED state
    draw_rounded_rectangle(draw, [220, 440, 440, 520], 
                          fill='#E0F2FE', outline=COLORS['primary'], width=3, radius=20)
    draw.text((330, 480), "COMPLETED", fill=COLORS['text'], font=header_font, anchor='mm')
    
    # ABANDONED state
    draw_rounded_rectangle(draw, [660, 440, 880, 520], 
                          fill='#FCE7F3', outline='#EC4899', width=3, radius=20)
    draw.text((770, 480), "ABANDONED", fill=COLORS['text'], font=header_font, anchor='mm')
    
    # Final state (double circle)
    draw.ellipse([515, 600, 565, 650], fill='white', outline='black', width=3)
    draw.ellipse([525, 610, 555, 640], fill='black', outline='black')
    
    # Transitions - simplified approach
    # Initial -> DRAFT
    draw.line([540, 100, 360, 140], fill=COLORS['border'], width=2)
    draw.polygon([(360, 140), (365, 125), (355, 125)], fill=COLORS['border'])
    draw.text((450, 115), "create()", fill=COLORS['text'], font=small_font)
    
    # DRAFT -> ACTIVE
    draw.line([330, 220, 330, 280], fill=COLORS['border'], width=2)
    draw.polygon([(330, 280), (325, 265), (335, 265)], fill=COLORS['border'])
    draw.text((370, 250), "start()", fill=COLORS['text'], font=small_font)
    
    # ACTIVE -> PAUSED
    draw.line([440, 320, 660, 320], fill=COLORS['border'], width=2)
    draw.polygon([(660, 320), (645, 315), (645, 325)], fill=COLORS['border'])
    draw.text((550, 305), "pause()", fill=COLORS['text'], font=small_font)
    
    # PAUSED -> ACTIVE (curved back)
    draw.line([770, 360, 770, 400], fill=COLORS['border'], width=2)
    draw.line([770, 400, 440, 340], fill=COLORS['border'], width=2)
    draw.polygon([(440, 340), (455, 340), (445, 350)], fill=COLORS['border'])
    draw.text((600, 380), "resume()", fill=COLORS['text'], font=small_font)
    
    # ACTIVE -> COMPLETED
    draw.line([330, 360, 330, 440], fill=COLORS['border'], width=2)
    draw.polygon([(330, 440), (325, 425), (335, 425)], fill=COLORS['border'])
    draw.text((370, 400), "complete()", fill=COLORS['text'], font=small_font)
    
    # ACTIVE -> ABANDONED
    draw.line([400, 360, 700, 440], fill=COLORS['border'], width=2)
    draw.polygon([(700, 440), (685, 435), (695, 430)], fill=COLORS['border'])
    draw.text((550, 395), "abandon()", fill=COLORS['text'], font=small_font)
    
    # PAUSED -> ABANDONED
    draw.line([770, 360, 770, 440], fill=COLORS['border'], width=2)
    draw.polygon([(770, 440), (765, 425), (775, 425)], fill=COLORS['border'])
    draw.text((810, 400), "abandon()", fill=COLORS['text'], font=small_font)
    
    # COMPLETED -> final
    draw.line([330, 520, 330, 580], fill=COLORS['border'], width=2)
    draw.line([330, 580, 520, 625], fill=COLORS['border'], width=2)
    draw.polygon([(520, 625), (505, 620), (515, 615)], fill=COLORS['border'])
    draw.text((400, 600), "archive()", fill=COLORS['text'], font=small_font)
    
    # ABANDONED -> final
    draw.line([770, 520, 770, 580], fill=COLORS['border'], width=2)
    draw.line([770, 580, 560, 625], fill=COLORS['border'], width=2)
    draw.polygon([(560, 625), (575, 620), (565, 615)], fill=COLORS['border'])
    draw.text((670, 600), "archive()", fill=COLORS['text'], font=small_font)
    
    # Legend
    draw_rounded_rectangle(draw, [50, 680, 1050, 760], 
                          fill='#F9FAFB', outline=COLORS['border'], width=2)
    draw.text((550, 700), "Можливі переходи між станами", 
              fill=COLORS['text'], font=header_font, anchor='mm')
    
    legend_text = [
        "• create() - створення нової цілі у статусі DRAFT",
        "• start() - активація цілі, початок відстеження",
        "• pause() - призупинення відстеження (тимчасово)",
        "• resume() - відновлення активної цілі після паузи",
        "• complete() - успішне завершення цілі",
        "• abandon() - відмова від цілі (з будь-якого стану)",
        "• archive() - архівування завершеної або покинутої цілі",
    ]
    
    for i, text in enumerate(legend_text):
        draw.text((60, 720 + i*20), text, fill=COLORS['text'], font=small_font)
    
    img.save(os.path.join(OUTPUT_DIR, '8_state_diagram.png'))
    print("✅ Створено діаграму станів: diagrams/8_state_diagram.png")

def create_activity_diagram():
    """Створює діаграму діяльності для процесу створення та відстеження цілі."""
    width, height = 900, 1100
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    title_font = create_font(22, bold=True)
    header_font = create_font(14, bold=True)
    text_font = create_font(12)
    small_font = create_font(11)
    
    # Заголовок
    draw.text((width//2, 30), "Діаграма діяльності - Створення та відстеження цілі", 
              fill=COLORS['text'], font=title_font, anchor='mm')
    
    # Start node
    draw.ellipse([430, 70, 470, 110], fill='black', outline='black')
    
    y_pos = 130
    actions = [
        ("Користувач натискає\n'Створити ціль'", '#E0F2FE', COLORS['primary']),
        ("Відкривається форма\nствор ення цілі", '#FEF3C7', COLORS['accent']),
        ("Заповнення полів:\n• Назва\n• Опис\n• Частота", '#D1FAE5', COLORS['secondary']),
    ]
    
    for i, (action, fill, outline) in enumerate(actions):
        draw_rounded_rectangle(draw, [250, y_pos, 650, y_pos+70], 
                              fill=fill, outline=outline, width=2, radius=15)
        draw.text((450, y_pos+35), action, fill=COLORS['text'], font=text_font, 
                 anchor='mm', align='center')
        
        # Arrow down
        draw.line([450, y_pos+70, 450, y_pos+90], fill=COLORS['border'], width=2)
        draw.polygon([(450, y_pos+90), (445, y_pos+75), (455, y_pos+75)], fill=COLORS['border'])
        
        y_pos += 110
    
    # Decision diamond
    decision_y = y_pos
    draw.polygon([
        (450, decision_y), (550, decision_y+50), (450, decision_y+100), (350, decision_y+50)
    ], fill='#FEF3C7', outline=COLORS['accent'], width=3)
    draw.text((450, decision_y+50), "Валідація\nуспішна?", fill=COLORS['text'], 
             font=text_font, anchor='mm', align='center')
    
    # No branch (left)
    draw.line([350, decision_y+50, 200, decision_y+50], fill=COLORS['border'], width=2)
    draw.line([200, decision_y+50, 200, 280], fill=COLORS['border'], width=2)
    draw.line([200, 280, 250, 280], fill=COLORS['border'], width=2)
    draw.polygon([(250, 280), (235, 275), (235, 285)], fill=COLORS['border'])
    draw.text((275, decision_y+50), "Ні", fill='#DC2626', font=text_font, anchor='mm')
    
    # Yes branch (down)
    y_pos = decision_y + 120
    draw.line([450, decision_y+100, 450, y_pos], fill=COLORS['border'], width=2)
    draw.polygon([(450, y_pos), (445, y_pos-15), (455, y_pos-15)], fill=COLORS['border'])
    draw.text((480, decision_y+110), "Так", fill=COLORS['secondary'], font=text_font)
    
    # Save goal
    draw_rounded_rectangle(draw, [250, y_pos, 650, y_pos+60], 
                          fill='#D1FAE5', outline=COLORS['secondary'], width=2, radius=15)
    draw.text((450, y_pos+30), "Збереження цілі в БД\n(статус: ACTIVE)", 
             fill=COLORS['text'], font=text_font, anchor='mm', align='center')
    
    y_pos += 80
    draw.line([450, y_pos-20, 450, y_pos], fill=COLORS['border'], width=2)
    draw.polygon([(450, y_pos), (445, y_pos-15), (455, y_pos-15)], fill=COLORS['border'])
    
    # Show success
    draw_rounded_rectangle(draw, [250, y_pos, 650, y_pos+60], 
                          fill='#E0F2FE', outline=COLORS['primary'], width=2, radius=15)
    draw.text((450, y_pos+30), "Відображення повідомлення\nпро успіх", 
             fill=COLORS['text'], font=text_font, anchor='mm', align='center')
    
    y_pos += 80
    draw.line([450, y_pos-20, 450, y_pos], fill=COLORS['border'], width=2)
    draw.polygon([(450, y_pos), (445, y_pos-15), (455, y_pos-15)], fill=COLORS['border'])
    
    # Daily tracking loop
    draw_rounded_rectangle(draw, [150, y_pos, 750, y_pos+180], 
                          fill='#F0F9FF', outline=COLORS['border'], width=3)
    draw.text((450, y_pos+20), "Щоденне відстеження прогресу", 
             fill=COLORS['text'], font=header_font, anchor='mm')
    
    loop_y = y_pos + 50
    draw_rounded_rectangle(draw, [250, loop_y, 650, loop_y+50], 
                          fill='#FEF3C7', outline=COLORS['accent'], width=2, radius=15)
    draw.text((450, loop_y+25), "Користувач відмічає\nвиконання за день", 
             fill=COLORS['text'], font=text_font, anchor='mm', align='center')
    
    loop_y += 70
    draw.line([450, loop_y-20, 450, loop_y], fill=COLORS['border'], width=2)
    draw.polygon([(450, loop_y), (445, loop_y-15), (455, loop_y-15)], fill=COLORS['border'])
    
    draw_rounded_rectangle(draw, [250, loop_y, 650, loop_y+50], 
                          fill='#D1FAE5', outline=COLORS['secondary'], width=2, radius=15)
    draw.text((450, loop_y+25), "Оновлення статистики\nта прогресу", 
             fill=COLORS['text'], font=text_font, anchor='mm', align='center')
    
    # Loop back arrow
    draw.line([750, y_pos+90, 800, y_pos+90], fill=COLORS['border'], width=2)
    draw.line([800, y_pos+90, 800, loop_y-30], fill=COLORS['border'], width=2)
    draw.line([800, loop_y-30, 250, loop_y-30], fill=COLORS['border'], width=2)
    draw.polygon([(250, loop_y-30), (265, loop_y-35), (265, loop_y-25)], fill=COLORS['border'])
    draw.text((810, y_pos+120), "Повтор\nщодня", fill=COLORS['text'], 
             font=small_font, align='center')
    
    # End node
    y_pos += 200
    draw.line([450, y_pos-20, 450, y_pos+20], fill=COLORS['border'], width=2)
    draw.ellipse([430, y_pos+20, 470, y_pos+60], fill='white', outline='black', width=3)
    draw.ellipse([440, y_pos+30, 460, y_pos+50], fill='black', outline='black')
    
    img.save(os.path.join(OUTPUT_DIR, '9_activity_diagram.png'))
    print("✅ Створено діаграму діяльності: diagrams/9_activity_diagram.png")

def create_sequence_progress_diagram():
    """Створює діаграму послідовності для логування прогресу."""
    width, height = 1000, 800
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    title_font = create_font(22, bold=True)
    header_font = create_font(14, bold=True)
    text_font = create_font(12)
    
    # Заголовок
    draw.text((width//2, 25), "Діаграма послідовності - Логування прогресу", 
              fill=COLORS['text'], font=title_font, anchor='mm')
    
    # Актори
    actors = [
        ("User", 100),
        ("GoalDetail\nPage", 300),
        ("ProgressAPI", 500),
        ("ProgressCtrl", 700),
        ("ProgressSvc", 900),
    ]
    
    y_start = 70
    for name, x in actors:
        draw_rounded_rectangle(draw, [x-50, y_start, x+50, y_start+40], 
                              fill=COLORS['primary'], outline=COLORS['primary'], width=2)
        draw.text((x, y_start+20), name, fill='white', font=header_font, 
                 anchor='mm', align='center')
        # Lifeline
        for y in range(y_start+40, 700, 10):
            draw.line([x, y, x, y+5], fill=COLORS['border'], width=1)
    
    # Messages
    messages = [
        (100, 300, "1. Click 'Mark Done'", 140),
        (300, 500, "2. POST /progress", 190, COLORS['primary']),
        (500, 700, "3. createProgress()", 240, COLORS['accent']),
        (700, 900, "4. saveProgress()", 290, COLORS['secondary']),
        (900, 700, "5. Progress saved", 340, COLORS['secondary']),
        (700, 700, "6. updateGoalStats()", 390, None),
        (700, 500, "7. ProgressResponse", 440, COLORS['accent']),
        (500, 300, "8. {progress, updated}", 490, COLORS['primary']),
        (300, 300, "9. Update UI state", 540, None),
        (300, 100, "10. Show checkmark", 590, COLORS['secondary']),
    ]
    
    for msg in messages:
        x1, x2, text, y = msg[0], msg[1], msg[2], msg[3]
        color = msg[4] if len(msg) > 4 else COLORS['border']
        
        if color:
            draw.line([x1, y, x2, y], fill=color, width=2)
            if x1 < x2:
                draw.polygon([(x2, y), (x2-10, y-5), (x2-10, y+5)], fill=color)
            else:
                draw.polygon([(x2, y), (x2+10, y-5), (x2+10, y+5)], fill=color)
        else:
            draw.line([x1, y, x2, y], fill=COLORS['border'], width=1)
        
        text_x = (x1 + x2) // 2
        draw.text((text_x, y-15), text, fill=COLORS['text'], font=text_font, anchor='mm')
    
    # Activations
    activations = [
        (300, 140, 600),
        (500, 190, 500),
        (700, 240, 450),
        (900, 290, 350),
    ]
    
    for x, y1, y2 in activations:
        draw.rectangle([x-10, y1, x+10, y2], fill='white', outline=COLORS['border'], width=2)
    
    # Notes
    draw_rounded_rectangle(draw, [50, 650, 950, 750], 
                          fill='#FEF3C7', outline=COLORS['accent'], width=2)
    notes = [
        "Примітки:",
        "• Кожне логування прогресу оновлює статистику цілі (completion rate, streak)",
        "• Система автоматично перевіряє досягнення milestone'ів",
        "• UI оновлюється реактивно без перезавантаження сторінки",
    ]
    for i, note in enumerate(notes):
        draw.text((60, 660+i*25), note, fill=COLORS['text'], font=text_font)
    
    img.save(os.path.join(OUTPUT_DIR, '10_sequence_progress.png'))
    print("✅ Створено діаграму послідовності (прогрес): diagrams/10_sequence_progress.png")

def create_sequence_group_diagram():
    """Створює діаграму послідовності для створення групи."""
    width, height = 1100, 850
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    title_font = create_font(22, bold=True)
    header_font = create_font(14, bold=True)
    text_font = create_font(11)
    small_font = create_font(10)
    
    # Заголовок
    draw.text((width//2, 25), "Діаграма послідовності - Створення та приєднання до групи", 
              fill=COLORS['text'], font=title_font, anchor='mm')
    
    # Actors
    actors = [
        ("User A\n(Creator)", 80),
        ("Groups\nPage", 250),
        ("GroupsAPI", 420),
        ("GroupCtrl", 590),
        ("GroupSvc", 760),
        ("User B\n(Member)", 930),
    ]
    
    y_start = 70
    for name, x in actors:
        draw_rounded_rectangle(draw, [x-45, y_start, x+45, y_start+40], 
                              fill=COLORS['primary'], outline=COLORS['primary'], width=2)
        draw.text((x, y_start+20), name, fill='white', font=header_font, 
                 anchor='mm', align='center')
        # Lifeline
        for y in range(y_start+40, 750, 10):
            draw.line([x, y, x, y+5], fill=COLORS['border'], width=1)
    
    # Phase 1: Create Group
    draw.text((550, 140), "Phase 1: Створення групи", fill=COLORS['accent'], 
             font=header_font, anchor='mm')
    
    messages_phase1 = [
        (80, 250, "1. Fill group form", 165),
        (250, 420, "2. POST /groups", 190, COLORS['primary']),
        (420, 590, "3. createGroup()", 215, COLORS['accent']),
        (590, 760, "4. saveGroup()", 240, COLORS['secondary']),
        (760, 590, "5. Group created", 265, COLORS['secondary']),
        (590, 420, "6. GroupResponse", 290, COLORS['accent']),
        (420, 250, "7. {group, code}", 315, COLORS['primary']),
        (250, 80, "8. Show invite code", 340, COLORS['secondary']),
    ]
    
    for msg in messages_phase1:
        x1, x2, text, y = msg[0], msg[1], msg[2], msg[3]
        color = msg[4] if len(msg) > 4 else COLORS['border']
        
        draw.line([x1, y, x2, y], fill=color, width=2)
        if x1 < x2:
            draw.polygon([(x2, y), (x2-8, y-4), (x2-8, y+4)], fill=color)
        else:
            draw.polygon([(x2, y), (x2+8, y-4), (x2+8, y+4)], fill=color)
        
        text_x = (x1 + x2) // 2
        draw.text((text_x, y-12), text, fill=COLORS['text'], font=small_font, anchor='mm')
    
    # Phase separator
    draw.line([50, 380, 1050, 380], fill=COLORS['border'], width=2)
    
    # Phase 2: Join Group
    draw.text((550, 400), "Phase 2: Приєднання до групи", fill=COLORS['secondary'], 
             font=header_font, anchor='mm')
    
    messages_phase2 = [
        (930, 250, "9. Enter code", 425),
        (250, 420, "10. POST /groups/join", 450, COLORS['primary']),
        (420, 590, "11. joinGroup(code)", 475, COLORS['accent']),
        (590, 760, "12. addMember()", 500, COLORS['secondary']),
        (760, 590, "13. Membership OK", 525, COLORS['secondary']),
        (590, 420, "14. Success response", 550, COLORS['accent']),
        (420, 250, "15. {membership}", 575, COLORS['primary']),
        (250, 930, "16. Welcome msg", 600, COLORS['secondary']),
    ]
    
    for msg in messages_phase2:
        x1, x2, text, y = msg[0], msg[1], msg[2], msg[3]
        color = msg[4] if len(msg) > 4 else COLORS['border']
        
        draw.line([x1, y, x2, y], fill=color, width=2)
        if x1 < x2:
            draw.polygon([(x2, y), (x2-8, y-4), (x2-8, y+4)], fill=color)
        else:
            draw.polygon([(x2, y), (x2+8, y-4), (x2+8, y+4)], fill=color)
        
        text_x = (x1 + x2) // 2
        draw.text((text_x, y-12), text, fill=COLORS['text'], font=small_font, anchor='mm')
    
    # Activations
    activations = [
        (250, 165, 345),
        (420, 190, 320),
        (590, 215, 295),
        (760, 240, 270),
        (250, 425, 605),
        (420, 450, 580),
        (590, 475, 555),
        (760, 500, 530),
    ]
    
    for x, y1, y2 in activations:
        draw.rectangle([x-8, y1, x+8, y2], fill='white', outline=COLORS['border'], width=1)
    
    # Notes
    draw_rounded_rectangle(draw, [50, 680, 1050, 800], 
                          fill='#FEF3C7', outline=COLORS['accent'], width=2)
    notes = [
        "Примітки:",
        "• Група створюється з унікальним invite code для приєднання інших користувачів",
        "• Власник групи (creator) автоматично стає ADMIN",
        "• Нові члени приєднуються зі статусом MEMBER за кодом запрошення",
        "• Система валідує права доступу перед кожною операцією",
    ]
    for i, note in enumerate(notes):
        draw.text((60, 690+i*22), note, fill=COLORS['text'], font=text_font)
    
    img.save(os.path.join(OUTPUT_DIR, '11_sequence_group.png'))
    print("✅ Створено діаграму послідовності (група): diagrams/11_sequence_group.png")

def create_api_diagram():
    """Створює діаграму REST API endpoints."""
    width, height = 1200, 1000
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    title_font = create_font(24, bold=True)
    header_font = create_font(16, bold=True)
    text_font = create_font(11)
    small_font = create_font(10)
    
    # Заголовок
    draw.text((width//2, 30), "REST API Endpoints - Habit Tracker", 
              fill=COLORS['text'], font=title_font, anchor='mm')
    
    # Base URL
    draw_rounded_rectangle(draw, [350, 70, 850, 110], 
                          fill='#E0F2FE', outline=COLORS['primary'], width=2)
    draw.text((600, 90), "Base URL: http://localhost:8080/api", 
             fill=COLORS['text'], font=header_font, anchor='mm')
    
    # Auth endpoints
    y = 140
    draw_rounded_rectangle(draw, [50, y, 1150, y+180], 
                          fill='#FEF3C7', outline=COLORS['accent'], width=3)
    draw.text((600, y+20), "/auth - Автентифікація", fill=COLORS['text'], 
             font=header_font, anchor='mm')
    
    auth_endpoints = [
        ("POST", "/auth/signup", "Реєстрація користувача", "SignupRequest → AuthResponse"),
        ("POST", "/auth/login", "Вхід в систему", "LoginRequest → AuthResponse + JWT"),
        ("POST", "/auth/refresh", "Оновлення токена", "RefreshRequest → TokenResponse"),
        ("POST", "/auth/logout", "Вихід з системи", "- → Success"),
    ]
    
    for i, (method, endpoint, desc, params) in enumerate(auth_endpoints):
        y_pos = y + 50 + i * 30
        color = '#10B981' if method == 'POST' else '#3B82F6'
        draw_rounded_rectangle(draw, [70, y_pos, 140, y_pos+20], 
                              fill=color, outline=color, width=1)
        draw.text((105, y_pos+10), method, fill='white', font=small_font, anchor='mm')
        draw.text((160, y_pos+10), endpoint, fill=COLORS['text'], font=text_font)
        draw.text((450, y_pos+10), desc, fill=COLORS['text'], font=small_font)
        draw.text((800, y_pos+10), params, fill=COLORS['border'], font=small_font)
    
    # Goals endpoints
    y = 340
    draw_rounded_rectangle(draw, [50, y, 1150, y+240], 
                          fill='#D1FAE5', outline=COLORS['secondary'], width=3)
    draw.text((600, y+20), "/goals - Управління цілями", fill=COLORS['text'], 
             font=header_font, anchor='mm')
    
    goals_endpoints = [
        ("GET", "/goals", "Список цілей користувача", "- → List<Goal>"),
        ("POST", "/goals", "Створення нової цілі", "CreateGoalRequest → Goal"),
        ("GET", "/goals/{id}", "Деталі цілі", "- → Goal"),
        ("PUT", "/goals/{id}", "Оновлення цілі", "UpdateGoalRequest → Goal"),
        ("DELETE", "/goals/{id}", "Видалення цілі", "- → void"),
        ("GET", "/goals/public", "Публічні цілі", "?page=0&size=20 → Page<Goal>"),
    ]
    
    for i, (method, endpoint, desc, params) in enumerate(goals_endpoints):
        y_pos = y + 50 + i * 30
        color = '#10B981' if method == 'POST' else ('#3B82F6' if method == 'GET' else '#F59E0B' if method == 'PUT' else '#DC2626')
        draw_rounded_rectangle(draw, [70, y_pos, 140, y_pos+20], 
                              fill=color, outline=color, width=1)
        draw.text((105, y_pos+10), method, fill='white', font=small_font, anchor='mm')
        draw.text((160, y_pos+10), endpoint, fill=COLORS['text'], font=text_font)
        draw.text((450, y_pos+10), desc, fill=COLORS['text'], font=small_font)
        draw.text((800, y_pos+10), params, fill=COLORS['border'], font=small_font)
    
    # Progress endpoints
    y = 600
    draw_rounded_rectangle(draw, [50, y, 1150, y+150], 
                          fill='#FCE7F3', outline='#EC4899', width=3)
    draw.text((600, y+20), "/progress - Логування прогресу", fill=COLORS['text'], 
             font=header_font, anchor='mm')
    
    progress_endpoints = [
        ("GET", "/progress/goal/{goalId}", "Прогрес по цілі", "- → List<Progress>"),
        ("POST", "/progress", "Логування прогресу", "ProgressRequest → Progress"),
        ("GET", "/progress/stats/{goalId}", "Статистика цілі", "- → GoalStats"),
    ]
    
    for i, (method, endpoint, desc, params) in enumerate(progress_endpoints):
        y_pos = y + 50 + i * 30
        color = '#10B981' if method == 'POST' else '#3B82F6'
        draw_rounded_rectangle(draw, [70, y_pos, 140, y_pos+20], 
                              fill=color, outline=color, width=1)
        draw.text((105, y_pos+10), method, fill='white', font=small_font, anchor='mm')
        draw.text((160, y_pos+10), endpoint, fill=COLORS['text'], font=text_font)
        draw.text((450, y_pos+10), desc, fill=COLORS['text'], font=small_font)
        draw.text((800, y_pos+10), params, fill=COLORS['border'], font=small_font)
    
    # Groups endpoints
    y = 770
    draw_rounded_rectangle(draw, [50, y, 1150, y+180], 
                          fill='#E0F2FE', outline=COLORS['primary'], width=3)
    draw.text((600, y+20), "/groups - Групи користувачів", fill=COLORS['text'], 
             font=header_font, anchor='mm')
    
    groups_endpoints = [
        ("GET", "/groups", "Список груп", "- → List<Group>"),
        ("POST", "/groups", "Створення групи", "CreateGroupRequest → Group"),
        ("POST", "/groups/join", "Приєднання до групи", "JoinRequest → Membership"),
        ("GET", "/groups/{id}/members", "Члени групи", "- → List<Member>"),
    ]
    
    for i, (method, endpoint, desc, params) in enumerate(groups_endpoints):
        y_pos = y + 50 + i * 30
        color = '#10B981' if method == 'POST' else '#3B82F6'
        draw_rounded_rectangle(draw, [70, y_pos, 140, y_pos+20], 
                              fill=color, outline=color, width=1)
        draw.text((105, y_pos+10), method, fill='white', font=small_font, anchor='mm')
        draw.text((160, y_pos+10), endpoint, fill=COLORS['text'], font=text_font)
        draw.text((450, y_pos+10), desc, fill=COLORS['text'], font=small_font)
        draw.text((800, y_pos+10), params, fill=COLORS['border'], font=small_font)
    
    img.save(os.path.join(OUTPUT_DIR, '12_api_endpoints.png'))
    print("✅ Створено діаграму API endpoints: diagrams/12_api_endpoints.png")

def create_dataflow_diagram():
    """Створює діаграму потоку даних (Data Flow Diagram)."""
    width, height = 1100, 900
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    title_font = create_font(24, bold=True)
    header_font = create_font(15, bold=True)
    text_font = create_font(12)
    small_font = create_font(10)
    
    # Заголовок
    draw.text((width//2, 30), "Діаграма потоку даних (DFD Level 1)", 
              fill=COLORS['text'], font=title_font, anchor='mm')
    
    # External Entity: User
    draw_rounded_rectangle(draw, [50, 180, 200, 280], 
                          fill='#E0F2FE', outline=COLORS['primary'], width=3)
    draw.text((125, 200), "Користувач", fill=COLORS['text'], font=header_font, anchor='mm')
    draw.text((60, 230), "• Реєстрація", fill=COLORS['text'], font=small_font)
    draw.text((60, 250), "• Логін", fill=COLORS['text'], font=small_font)
    draw.text((60, 265), "• Перегляд даних", fill=COLORS['text'], font=small_font)
    
    # Process 1: Authentication
    draw.ellipse([280, 80, 480, 180], fill='#FEF3C7', outline=COLORS['accent'], width=3)
    draw.text((380, 120), "1.0", fill=COLORS['text'], font=header_font, anchor='mm')
    draw.text((380, 145), "Автентифікація", fill=COLORS['text'], font=text_font, anchor='mm')
    
    # Process 2: Goal Management
    draw.ellipse([280, 220, 480, 320], fill='#D1FAE5', outline=COLORS['secondary'], width=3)
    draw.text((380, 260), "2.0", fill=COLORS['text'], font=header_font, anchor='mm')
    draw.text((380, 285), "Управління цілями", fill=COLORS['text'], font=text_font, anchor='mm')
    
    # Process 3: Progress Tracking
    draw.ellipse([280, 360, 480, 460], fill='#FCE7F3', outline='#EC4899', width=3)
    draw.text((380, 400), "3.0", fill=COLORS['text'], font=header_font, anchor='mm')
    draw.text((380, 425), "Відстеження\nпрогресу", fill=COLORS['text'], 
             font=text_font, anchor='mm', align='center')
    
    # Process 4: Group Management
    draw.ellipse([280, 500, 480, 600], fill='#E0F2FE', outline=COLORS['primary'], width=3)
    draw.text((380, 540), "4.0", fill=COLORS['text'], font=header_font, anchor='mm')
    draw.text((380, 565), "Управління\nгрупами", fill=COLORS['text'], 
             font=text_font, anchor='mm', align='center')
    
    # Data Store 1: Users DB
    draw.line([620, 120, 750, 120], fill='black', width=3)
    draw.line([620, 160, 750, 160], fill='black', width=3)
    draw.line([620, 120, 620, 160], fill='black', width=3)
    draw.text((685, 140), "D1: Users", fill=COLORS['text'], font=header_font, anchor='mm')
    
    # Data Store 2: Goals DB
    draw.line([620, 270, 750, 270], fill='black', width=3)
    draw.line([620, 310, 750, 310], fill='black', width=3)
    draw.line([620, 270, 620, 310], fill='black', width=3)
    draw.text((685, 290), "D2: Goals", fill=COLORS['text'], font=header_font, anchor='mm')
    
    # Data Store 3: Progress DB
    draw.line([620, 410, 750, 410], fill='black', width=3)
    draw.line([620, 450, 750, 450], fill='black', width=3)
    draw.line([620, 410, 620, 450], fill='black', width=3)
    draw.text((685, 430), "D3: Progress", fill=COLORS['text'], font=header_font, anchor='mm')
    
    # Data Store 4: Groups DB
    draw.line([620, 550, 750, 550], fill='black', width=3)
    draw.line([620, 590, 750, 590], fill='black', width=3)
    draw.line([620, 550, 620, 590], fill='black', width=3)
    draw.text((685, 570), "D4: Groups", fill=COLORS['text'], font=header_font, anchor='mm')
    
    # External Entity: Achievement System
    draw_rounded_rectangle(draw, [850, 350, 1050, 450], 
                          fill='#FEF3C7', outline=COLORS['accent'], width=3)
    draw.text((950, 375), "Система\nДосягнень", fill=COLORS['text'], 
             font=header_font, anchor='mm', align='center')
    draw.text((860, 415), "• Нарахування", fill=COLORS['text'], font=small_font)
    draw.text((860, 430), "• Бейджі", fill=COLORS['text'], font=small_font)
    
    # Data Flows
    flows = [
        # User -> Auth
        (200, 200, 280, 140, "Credentials"),
        # Auth -> User
        (300, 180, 200, 240, "JWT Token"),
        # Auth -> Users DB
        (480, 130, 620, 130, "User data"),
        # Users DB -> Auth
        (640, 150, 480, 150, "User info"),
        
        # User -> Goals
        (200, 250, 280, 270, "Goal data"),
        # Goals -> User
        (300, 320, 200, 260, "Goal list"),
        # Goals -> Goals DB
        (480, 270, 620, 280, "Save goal"),
        # Goals DB -> Goals
        (640, 300, 480, 290, "Goal data"),
        
        # User -> Progress
        (200, 320, 280, 400, "Progress log"),
        # Progress -> User
        (300, 460, 200, 330, "Statistics"),
        # Progress -> Progress DB
        (480, 420, 620, 420, "Save progress"),
        # Progress DB -> Progress
        (640, 440, 480, 430, "Progress data"),
        
        # Progress -> Achievement
        (480, 410, 850, 390, "Trigger check"),
        # Achievement -> Progress
        (900, 450, 480, 440, "Badge earned"),
        
        # User -> Groups
        (200, 400, 280, 540, "Group action"),
        # Groups -> User
        (300, 600, 200, 410, "Group data"),
        # Groups -> Groups DB
        (480, 560, 620, 560, "Save group"),
        # Groups DB -> Groups
        (640, 580, 480, 570, "Group info"),
    ]
    
    for x1, y1, x2, y2, label in flows:
        # Draw arrow
        draw.line([x1, y1, x2, y2], fill=COLORS['border'], width=2)
        
        # Arrow head
        import math
        angle = math.atan2(y2 - y1, x2 - x1)
        arrow_size = 10
        draw.polygon([
            (x2, y2),
            (x2 - arrow_size * math.cos(angle - math.pi/6), 
             y2 - arrow_size * math.sin(angle - math.pi/6)),
            (x2 - arrow_size * math.cos(angle + math.pi/6), 
             y2 - arrow_size * math.sin(angle + math.pi/6))
        ], fill=COLORS['border'])
        
        # Label
        mid_x = (x1 + x2) // 2
        mid_y = (y1 + y2) // 2
        draw.text((mid_x, mid_y - 10), label, fill=COLORS['text'], 
                 font=small_font, anchor='mm')
    
    # Legend
    draw_rounded_rectangle(draw, [50, 700, 1050, 850], 
                          fill='#F9FAFB', outline=COLORS['border'], width=2)
    draw.text((550, 720), "Легенда", fill=COLORS['text'], font=header_font, anchor='mm')
    
    legend_items = [
        ("Прямокутник", "Зовнішня сутність (користувач, система)"),
        ("Коло/Еліпс", "Процес обробки даних"),
        ("Паралельні лінії", "Сховище даних (база даних)"),
        ("Стрілка", "Потік даних між компонентами"),
    ]
    
    for i, (shape, desc) in enumerate(legend_items):
        y = 750 + i * 25
        draw.text((70, y), f"• {shape}:", fill=COLORS['text'], font=text_font)
        draw.text((220, y), desc, fill=COLORS['text'], font=small_font)
    
    img.save(os.path.join(OUTPUT_DIR, '13_dataflow_diagram.png'))
    print("✅ Створено діаграму потоку даних: diagrams/13_dataflow_diagram.png")

def create_package_diagram():
    """Створює діаграму пакетів Backend структури."""
    width, height = 1100, 900
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    title_font = create_font(24, bold=True)
    header_font = create_font(15, bold=True)
    text_font = create_font(12)
    small_font = create_font(10)
    
    # Заголовок
    draw.text((width//2, 30), "Діаграма пакетів - Backend структура", 
              fill=COLORS['text'], font=title_font, anchor='mm')
    
    # Root package
    draw_rounded_rectangle(draw, [50, 70, 1050, 830], 
                          fill='#F9FAFB', outline=COLORS['border'], width=3)
    draw.text((550, 95), "com.example.cwweb", fill=COLORS['text'], 
             font=header_font, anchor='mm')
    
    # Config package
    draw_rounded_rectangle(draw, [80, 130, 330, 280], 
                          fill='#E0F2FE', outline=COLORS['primary'], width=2)
    draw.text((205, 155), "config", fill=COLORS['text'], font=header_font, anchor='mm')
    classes = [
        "SecurityConfig.java",
        "JwtAuthFilter.java",
        "JwtUtils.java",
        "CorsConfig.java",
        "MongoConfig.java",
    ]
    for i, cls in enumerate(classes):
        draw.text((100, 185 + i*17), f"• {cls}", fill=COLORS['text'], font=small_font)
    
    # Auth package
    draw_rounded_rectangle(draw, [360, 130, 690, 280], 
                          fill='#FEF3C7', outline=COLORS['accent'], width=2)
    draw.text((525, 155), "auth", fill=COLORS['text'], font=header_font, anchor='mm')
    classes = [
        "AuthController.java",
        "AuthService.java",
        "SignupRequest.java",
        "LoginRequest.java",
        "AuthResponse.java",
    ]
    for i, cls in enumerate(classes):
        draw.text((380, 185 + i*17), f"• {cls}", fill=COLORS['text'], font=small_font)
    
    # Users package
    draw_rounded_rectangle(draw, [720, 130, 1020, 280], 
                          fill='#D1FAE5', outline=COLORS['secondary'], width=2)
    draw.text((870, 155), "users", fill=COLORS['text'], font=header_font, anchor='mm')
    classes = [
        "User.java",
        "UserRepository.java",
        "UserService.java",
        "UserRole.java",
        "UserStatus.java",
    ]
    for i, cls in enumerate(classes):
        draw.text((740, 185 + i*17), f"• {cls}", fill=COLORS['text'], font=small_font)
    
    # Goals package
    draw_rounded_rectangle(draw, [80, 310, 400, 530], 
                          fill='#FCE7F3', outline='#EC4899', width=2)
    draw.text((240, 335), "goals", fill=COLORS['text'], font=header_font, anchor='mm')
    classes = [
        "GoalController.java",
        "GoalService.java",
        "GoalRepository.java",
        "Goal.java",
        "CreateGoalRequest.java",
        "UpdateGoalRequest.java",
        "GoalStatus.java",
        "Frequency.java",
        "GoalResponse.java",
    ]
    for i, cls in enumerate(classes):
        draw.text((100, 365 + i*17), f"• {cls}", fill=COLORS['text'], font=small_font)
    
    # Progress package
    draw_rounded_rectangle(draw, [430, 310, 750, 490], 
                          fill='#E0F2FE', outline=COLORS['primary'], width=2)
    draw.text((590, 335), "progress", fill=COLORS['text'], font=header_font, anchor='mm')
    classes = [
        "ProgressController.java",
        "ProgressService.java",
        "ProgressRepository.java",
        "Progress.java",
        "ProgressRequest.java",
        "GoalStats.java",
    ]
    for i, cls in enumerate(classes):
        draw.text((450, 365 + i*17), f"• {cls}", fill=COLORS['text'], font=small_font)
    
    # Groups package
    draw_rounded_rectangle(draw, [80, 560, 430, 780], 
                          fill='#D1FAE5', outline=COLORS['secondary'], width=2)
    draw.text((255, 585), "groups", fill=COLORS['text'], font=header_font, anchor='mm')
    classes = [
        "GroupController.java",
        "GroupService.java",
        "GroupRepository.java",
        "Group.java",
        "GroupMembership.java",
        "GroupMembershipRepo.java",
        "CreateGroupRequest.java",
        "Visibility.java",
        "MembershipRole.java",
    ]
    for i, cls in enumerate(classes):
        draw.text((100, 615 + i*17), f"• {cls}", fill=COLORS['text'], font=small_font)
    
    # Achievements package
    draw_rounded_rectangle(draw, [460, 520, 750, 700], 
                          fill='#FEF3C7', outline=COLORS['accent'], width=2)
    draw.text((605, 545), "achievements", fill=COLORS['text'], font=header_font, anchor='mm')
    classes = [
        "AchievementCtrl.java",
        "AchievementSvc.java",
        "AchievementRepo.java",
        "Achievement.java",
        "AchievementType.java",
        "UserAchievement.java",
    ]
    for i, cls in enumerate(classes):
        draw.text((480, 575 + i*17), f"• {cls}", fill=COLORS['text'], font=small_font)
    
    # Common/Utils package
    draw_rounded_rectangle(draw, [780, 310, 1020, 470], 
                          fill='#F9FAFB', outline=COLORS['border'], width=2)
    draw.text((900, 335), "common", fill=COLORS['text'], font=header_font, anchor='mm')
    classes = [
        "ApiResponse.java",
        "ErrorResponse.java",
        "ValidationUtils.java",
        "DateUtils.java",
        "Constants.java",
    ]
    for i, cls in enumerate(classes):
        draw.text((800, 365 + i*17), f"• {cls}", fill=COLORS['text'], font=small_font)
    
    # Dependencies (arrows)
    # Auth -> Users
    draw.line([690, 205, 720, 205], fill=COLORS['border'], width=2)
    draw.polygon([(720, 205), (705, 200), (705, 210)], fill=COLORS['border'])
    
    # Goals -> Users
    draw.line([400, 350, 780, 200], fill=COLORS['border'], width=2)
    draw.polygon([(780, 200), (765, 205), (775, 195)], fill=COLORS['border'])
    
    # Progress -> Goals
    draw.line([430, 400, 400, 400], fill=COLORS['border'], width=2)
    draw.polygon([(400, 400), (415, 395), (415, 405)], fill=COLORS['border'])
    
    # Groups -> Users
    draw.line([430, 620, 800, 280], fill=COLORS['border'], width=2)
    draw.polygon([(800, 280), (785, 285), (795, 275)], fill=COLORS['border'])
    
    img.save(os.path.join(OUTPUT_DIR, '14_package_diagram.png'))
    print("✅ Створено діаграму пакетів: diagrams/14_package_diagram.png")

def create_routing_diagram():
    """Створює діаграму роутингу Frontend (React Router)."""
    width, height = 1000, 900
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    title_font = create_font(24, bold=True)
    header_font = create_font(16, bold=True)
    text_font = create_font(13)
    small_font = create_font(11)
    
    # Заголовок
    draw.text((width//2, 30), "Діаграма роутингу - React Router v6", 
              fill=COLORS['text'], font=title_font, anchor='mm')
    
    # App root
    draw_rounded_rectangle(draw, [350, 80, 650, 140], 
                          fill=COLORS['primary'], outline=COLORS['primary'], width=3)
    draw.text((500, 110), "/ (App Root)", fill='white', font=header_font, anchor='mm')
    
    # Public routes
    draw_rounded_rectangle(draw, [50, 200, 450, 440], 
                          fill='#E0F2FE', outline=COLORS['primary'], width=3)
    draw.text((250, 225), "Public Routes (Unauthorized)", fill=COLORS['text'], 
             font=header_font, anchor='mm')
    
    public_routes = [
        ("/login", "Login.jsx", "Сторінка входу"),
        ("/register", "Register.jsx", "Реєстрація користувача"),
        ("/", "Landing Page", "Головна сторінка"),
    ]
    
    y = 265
    for route, component, desc in public_routes:
        draw_rounded_rectangle(draw, [70, y, 430, y+45], 
                              fill='white', outline=COLORS['primary'], width=2)
        draw.text((90, y+10), route, fill=COLORS['primary'], font=text_font, anchor='lm')
        draw.text((90, y+28), f"→ {component}", fill=COLORS['text'], font=small_font, anchor='lm')
        draw.text((250, y+28), desc, fill=COLORS['border'], font=small_font, anchor='lm')
        y += 55
    
    # Protected routes
    draw_rounded_rectangle(draw, [550, 200, 950, 800], 
                          fill='#D1FAE5', outline=COLORS['secondary'], width=3)
    draw.text((750, 225), "Protected Routes (Authorized)", fill=COLORS['text'], 
             font=header_font, anchor='mm')
    
    protected_routes = [
        ("/dashboard", "Dashboard.jsx", "Панель управління"),
        ("/goals", "Goals.jsx", "Список цілей"),
        ("/goals/:id", "GoalDetail.jsx", "Деталі цілі"),
        ("/achievements", "Achievements.jsx", "Досягнення"),
        ("/groups", "Groups.jsx", "Список груп"),
        ("/groups/:id", "GroupDetail.jsx", "Деталі групи"),
        ("/profile", "Profile.jsx", "Профіль користувача"),
        ("/settings", "Settings.jsx", "Налаштування"),
    ]
    
    y = 265
    for route, component, desc in protected_routes:
        draw_rounded_rectangle(draw, [570, y, 930, y+45], 
                              fill='white', outline=COLORS['secondary'], width=2)
        draw.text((590, y+10), route, fill=COLORS['secondary'], font=text_font, anchor='lm')
        draw.text((590, y+28), f"→ {component}", fill=COLORS['text'], font=small_font, anchor='lm')
        draw.text((750, y+28), desc, fill=COLORS['border'], font=small_font, anchor='lm')
        y += 60
    
    # Route Guards
    draw_rounded_rectangle(draw, [50, 480, 450, 640], 
                          fill='#FEF3C7', outline=COLORS['accent'], width=3)
    draw.text((250, 505), "Route Guards & Navigation", fill=COLORS['text'], 
             font=header_font, anchor='mm')
    
    guards = [
        "• PrivateRoute wrapper",
        "• JWT token перевірка",
        "• Redirect to /login якщо не авторизований",
        "• Redirect to /dashboard після логіну",
        "• React Router Navigate",
    ]
    
    for i, guard in enumerate(guards):
        draw.text((70, 540 + i*20), guard, fill=COLORS['text'], font=text_font)
    
    # Error routes
    draw_rounded_rectangle(draw, [50, 680, 450, 800], 
                          fill='#FCE7F3', outline='#EC4899', width=3)
    draw.text((250, 705), "Error Handling", fill=COLORS['text'], 
             font=header_font, anchor='mm')
    
    error_routes = [
        ("/404", "NotFound.jsx", "Сторінка не знайдена"),
        ("/403", "Forbidden.jsx", "Доступ заборонено"),
        ("*", "NotFound.jsx", "Catch-all route"),
    ]
    
    y = 740
    for route, component, desc in error_routes:
        draw.text((70, y), f"{route} → {component}", fill=COLORS['text'], font=small_font)
        draw.text((280, y), desc, fill=COLORS['border'], font=small_font)
        y += 20
    
    # Arrows from App to sections
    draw.line([500, 140, 250, 200], fill=COLORS['border'], width=2)
    draw.polygon([(250, 200), (255, 185), (245, 185)], fill=COLORS['border'])
    
    draw.line([500, 140, 750, 200], fill=COLORS['border'], width=2)
    draw.polygon([(750, 200), (755, 185), (745, 185)], fill=COLORS['border'])
    
    img.save(os.path.join(OUTPUT_DIR, '15_routing_diagram.png'))
    print("✅ Створено діаграму роутингу: diagrams/15_routing_diagram.png")

if __name__ == '__main__':
    print("Генерація діаграм для курсової роботи...\n")
    print("=" * 60)
    
    # Основні діаграми
    create_architecture_diagram()
    create_usecase_diagram()
    create_er_diagram()
    create_sequence_diagram()
    create_class_diagram()
    
    # Додаткові діаграми
    create_component_diagram()
    create_deployment_diagram()
    create_state_diagram()
    create_activity_diagram()
    create_sequence_progress_diagram()
    create_sequence_group_diagram()
    create_api_diagram()
    create_dataflow_diagram()
    create_package_diagram()
    create_routing_diagram()
    
    print("\n" + "=" * 60)
    print(f"✅ Всі діаграми створено в папці '{OUTPUT_DIR}'")
    print("=" * 60)
    print("\n📊 Список створених діаграм (15 штук):\n")
    print("Основні діаграми:")
    print("  1. 1_architecture.png       - Архітектура системи")
    print("  2. 2_usecase.png            - Діаграма прецедентів (Use Case)")
    print("  3. 3_er_diagram.png         - ER діаграма (модель даних MongoDB)")
    print("  4. 4_sequence.png           - Діаграма послідовності (автентифікація)")
    print("  5. 5_class_diagram.png      - Діаграма класів (Backend)")
    print("\nДодаткові діаграми:")
    print("  6. 6_component_diagram.png  - Діаграма компонентів (Frontend React)")
    print("  7. 7_deployment_diagram.png - Діаграма розгортання (Docker)")
    print("  8. 8_state_diagram.png      - Діаграма станів (Goal lifecycle)")
    print("  9. 9_activity_diagram.png   - Діаграма діяльності (User flow)")
    print(" 10. 10_sequence_progress.png - Діаграма послідовності (логування прогресу)")
    print(" 11. 11_sequence_group.png    - Діаграма послідовності (створення групи)")
    print(" 12. 12_api_endpoints.png     - REST API endpoints структура")
    print(" 13. 13_dataflow_diagram.png  - Діаграма потоку даних (DFD)")
    print(" 14. 14_package_diagram.png   - Діаграма пакетів (Backend структура)")
    print(" 15. 15_routing_diagram.png   - Діаграма роутингу (React Router)")
    print("\n" + "=" * 60)
    print("🎨 Всі діаграми у форматі PNG, готові до вставки в документ!")
    print("=" * 60)
