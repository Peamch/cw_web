#!/usr/bin/env python3
"""
Розширений скрипт для генерації курсової роботи з великою кількістю прикладів коду та поясненнями.
"""
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def set_font(run, name='Times New Roman', size=14, bold=False, color=None):
    """Встановлює шрифт для тексту."""
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = color
    r = run._element
    rPr = r.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    rFonts.set(qn('w:eastAsia'), name)

def add_para(doc, text, bold=False, color=None):
    """Додає параграф з форматуванням."""
    p = doc.add_paragraph()
    run = p.add_run(text)
    set_font(run, bold=bold, color=color)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = Inches(0.5)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    return p

def add_code_block(doc, code_lines, language="Java"):
    """Додає блок коду з сірим фоном."""
    p = doc.add_paragraph()
    run = p.add_run('\n'.join(code_lines))
    set_font(run, name='Courier New', size=10)
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    # Додаємо сірий фон
    shading_elm = OxmlElement('w:shd')
    shading_elm.set(qn('w:fill'), 'F5F5F5')
    p._element.get_or_add_pPr().append(shading_elm)
    return p

def add_explanation(doc, title, text):
    """Додає пояснення перед кодом."""
    p = doc.add_paragraph()
    run = p.add_run(title)
    set_font(run, bold=True, size=13)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    p.paragraph_format.space_before = Pt(12)
    
    p2 = doc.add_paragraph()
    run2 = p2.add_run(text)
    set_font(run2)
    p2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p2.paragraph_format.first_line_indent = Inches(0.5)
    p2.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    return p2

# Завантажуємо існуючий документ
doc = Document('/home/runner/work/cw_web/cw_web/Курсова_Робота_HabitTracker.docx')

# Додаємо РОЗДІЛ 4.1 з прикладами коду backend
doc.add_page_break()
doc.add_heading('РОЗДІЛ 4. РЕАЛІЗАЦІЯ ІНФОРМАЦІЙНОЇ СИСТЕМИ', level=1)
add_para(doc, 'У цьому розділі детально описано реалізацію веб-системи для відстеження звичок та досягнень. Представлено архітектуру системи, структуру проекту та конкретні приклади коду backend і frontend частин з детальними поясненнями.')

doc.add_heading('4.1 Реалізація backend частини системи', level=2)

# 4.1.1 Модель даних - Entity класи
doc.add_heading('4.1.1 Модель даних - Entity класи', level=3)

add_explanation(doc, 
    'Клас User - модель користувача системи:',
    'Клас User представляє сутність користувача в системі. Використовується MongoDB як база даних, тому клас анотується @Document. Lombok анотації (@Data, @Builder) автоматично генерують геттери, сеттери та builder pattern для зручного створення об\'єктів.')

add_code_block(doc, [
    'package com.example.cwweb.users;',
    '',
    'import lombok.AllArgsConstructor;',
    'import lombok.Builder;',
    'import lombok.Data;',
    'import lombok.NoArgsConstructor;',
    'import org.springframework.data.annotation.Id;',
    'import org.springframework.data.mongodb.core.mapping.Document;',
    'import java.time.LocalDateTime;',
    '',
    '@Data',
    '@Builder',
    '@NoArgsConstructor',
    '@AllArgsConstructor',
    '@Document(collection = "users")',
    'public class User {',
    '    @Id',
    '    private String id;',
    '    private String email;',
    '    private String passwordHash;',
    '    private String displayName;',
    '    private Role role;',
    '    private Status status;',
    '    private LocalDateTime createdAt;',
    '    private LocalDateTime updatedAt;',
    '',
    '    public enum Role {',
    '        USER, ADMIN',
    '    }',
    '',
    '    public enum Status {',
    '        ACTIVE, BLOCKED',
    '    }',
    '}'
])

add_para(doc, 'Поля класу: id - унікальний ідентифікатор MongoDB, email - електронна адреса користувача (унікальна), passwordHash - хеш пароля (використовується BCrypt), displayName - ім\'я для відображення, role - роль у системі (USER або ADMIN), status - статус акаунту (ACTIVE або BLOCKED), createdAt/updatedAt - часові мітки для аудиту.')

doc.add_paragraph()

add_explanation(doc,
    'Клас Goal - модель цілі користувача:',
    'Клас Goal представляє ціль або звичку, яку користувач хоче відстежувати. Містить інформацію про назву, опис, частоту виконання, статус та часові рамки. Використовується builder pattern для зручного створення цілей з різними параметрами.')

add_code_block(doc, [
    'package com.example.cwweb.goals;',
    '',
    'import lombok.AllArgsConstructor;',
    'import lombok.Builder;',
    'import lombok.Data;',
    'import lombok.NoArgsConstructor;',
    'import org.springframework.data.annotation.Id;',
    'import org.springframework.data.mongodb.core.mapping.Document;',
    'import java.time.LocalDate;',
    'import java.time.LocalDateTime;',
    '',
    '@Data',
    '@Builder',
    '@NoArgsConstructor',
    '@AllArgsConstructor',
    '@Document(collection = "goals")',
    'public class Goal {',
    '    @Id',
    '    private String id;',
    '    private String userId;',
    '    private String title;',
    '    private String description;',
    '    private Frequency frequency;',
    '    private LocalDate startDate;',
    '    private LocalDate endDate;',
    '    private boolean isPublic;',
    '    private GoalStatus status;',
    '    private LocalDateTime createdAt;',
    '    private LocalDateTime updatedAt;',
    '}'
])

add_para(doc, 'Поля класу: userId - посилання на власника цілі, title - назва цілі, description - детальний опис, frequency - частота виконання (DAILY, WEEKLY, MONTHLY), startDate/endDate - період дії цілі, isPublic - видимість для інших користувачів, status - поточний статус (ACTIVE, COMPLETED, PAUSED, ARCHIVED).')

doc.add_paragraph()

add_explanation(doc,
    'Клас Group - модель групи для спільного відстеження:',
    'Клас Group дозволяє користувачам об\'єднуватися в групи для спільної мотивації та відстеження прогресу. Група має власника, назву, опис та налаштування видимості.')

add_code_block(doc, [
    'package com.example.cwweb.groups;',
    '',
    'import lombok.AllArgsConstructor;',
    'import lombok.Builder;',
    'import lombok.Data;',
    'import lombok.NoArgsConstructor;',
    'import org.springframework.data.annotation.Id;',
    'import org.springframework.data.mongodb.core.mapping.Document;',
    'import java.time.LocalDateTime;',
    '',
    '@Data',
    '@Builder',
    '@NoArgsConstructor',
    '@AllArgsConstructor',
    '@Document(collection = "groups")',
    'public class Group {',
    '    @Id',
    '    private String id;',
    '    private String name;',
    '    private String description;',
    '    private Visibility visibility;',
    '    private String ownerId;',
    '    private LocalDateTime createdAt;',
    '    private LocalDateTime updatedAt;',
    '}'
])

add_para(doc, 'Поля класу: name - унікальна назва групи, visibility - рівень доступу (PUBLIC або PRIVATE), ownerId - ідентифікатор власника групи, який має розширені права.')

# 4.1.2 Controller Layer
doc.add_page_break()
doc.add_heading('4.1.2 Контролери - обробка HTTP запитів', level=3)

add_explanation(doc,
    'Клас AuthController - контролер автентифікації:',
    'AuthController відповідає за обробку запитів реєстрації, авторизації та оновлення токенів. Використовує анотацію @RestController для автоматичного перетворення об\'єктів у JSON. Всі endpoint\'и знаходяться за шляхом /auth.')

add_code_block(doc, [
    'package com.example.cwweb.auth;',
    '',
    'import com.example.cwweb.common.ApiResponse;',
    'import org.springframework.http.ResponseEntity;',
    'import org.springframework.web.bind.annotation.*;',
    '',
    '@RestController',
    '@RequestMapping("/auth")',
    'public class AuthController {',
    '',
    '    private final AuthService authService;',
    '',
    '    public AuthController(AuthService authService) {',
    '        this.authService = authService;',
    '    }',
    '',
    '    @PostMapping("/signup")',
    '    public ResponseEntity<ApiResponse<AuthResponse>> signup(',
    '            @RequestBody SignupRequest request) {',
    '        AuthResponse response = authService.signup(request);',
    '        return ResponseEntity.ok(ApiResponse.<AuthResponse>builder()',
    '                .success(true)',
    '                .message("Signup successful")',
    '                .data(response)',
    '                .build());',
    '    }',
    '',
    '    @PostMapping("/login")',
    '    public ResponseEntity<ApiResponse<AuthResponse>> login(',
    '            @RequestBody LoginRequest request) {',
    '        AuthResponse response = authService.login(request);',
    '        return ResponseEntity.ok(ApiResponse.<AuthResponse>builder()',
    '                .success(true)',
    '                .message("Login successful")',
    '                .data(response)',
    '                .build());',
    '    }',
    '',
    '    @PostMapping("/refresh")',
    '    public ResponseEntity<ApiResponse<AuthResponse>> refresh(',
    '            @RequestBody RefreshRequest request) {',
    '        AuthResponse response = authService.refresh(',
    '                request.getRefreshToken());',
    '        return ResponseEntity.ok(ApiResponse.<AuthResponse>builder()',
    '                .success(true)',
    '                .message("Token refreshed")',
    '                .data(response)',
    '                .build());',
    '    }',
    '}'
])

add_para(doc, 'Метод signup обробляє реєстрацію нового користувача, приймаючи email, пароль та displayName. Метод login виконує авторизацію користувача та повертає JWT токени. Метод refresh оновлює access token за допомогою refresh token. Всі відповіді загортаються в уніфікований ApiResponse для консистентності API.')

doc.add_paragraph()

add_explanation(doc,
    'Клас GoalController - контролер управління цілями:',
    'GoalController надає REST API для CRUD операцій над цілями. Використовує @AuthenticationPrincipal для отримання інформації про авторизованого користувача з JWT токена. Всі методи захищені автентифікацією.')

add_code_block(doc, [
    'package com.example.cwweb.goals;',
    '',
    'import com.example.cwweb.common.ApiResponse;',
    'import org.springframework.http.ResponseEntity;',
    'import org.springframework.security.core.annotation.AuthenticationPrincipal;',
    'import org.springframework.security.core.userdetails.UserDetails;',
    'import org.springframework.web.bind.annotation.*;',
    'import java.util.List;',
    '',
    '@RestController',
    '@RequestMapping("/goals")',
    'public class GoalController {',
    '    private final GoalService goalService;',
    '',
    '    public GoalController(GoalService goalService) {',
    '        this.goalService = goalService;',
    '    }',
    '',
    '    @PostMapping',
    '    public ResponseEntity<ApiResponse<Goal>> createGoal(',
    '            @AuthenticationPrincipal UserDetails userDetails,',
    '            @RequestBody CreateGoalRequest request) {',
    '        String userId = userDetails.getUsername();',
    '        Goal goal = goalService.createGoal(userId, request);',
    '        return ResponseEntity.ok(ApiResponse.<Goal>builder()',
    '                .success(true)',
    '                .message("Goal created")',
    '                .data(goal)',
    '                .build());',
    '    }',
    '',
    '    @GetMapping',
    '    public ResponseEntity<ApiResponse<List<Goal>>> getUserGoals(',
    '            @AuthenticationPrincipal UserDetails userDetails) {',
    '        String userId = userDetails.getUsername();',
    '        List<Goal> goals = goalService.getUserGoals(userId);',
    '        return ResponseEntity.ok(ApiResponse.<List<Goal>>builder()',
    '                .success(true)',
    '                .data(goals)',
    '                .build());',
    '    }',
    '',
    '    @PutMapping("/{id}")',
    '    public ResponseEntity<ApiResponse<Goal>> updateGoal(',
    '            @PathVariable String id,',
    '            @AuthenticationPrincipal UserDetails userDetails,',
    '            @RequestBody UpdateGoalRequest request) {',
    '        String userId = userDetails.getUsername();',
    '        Goal goal = goalService.updateGoal(id, userId, request);',
    '        return ResponseEntity.ok(ApiResponse.<Goal>builder()',
    '                .success(true)',
    '                .message("Goal updated")',
    '                .data(goal)',
    '                .build());',
    '    }',
    '',
    '    @DeleteMapping("/{id}")',
    '    public ResponseEntity<ApiResponse<Void>> deleteGoal(',
    '            @PathVariable String id,',
    '            @AuthenticationPrincipal UserDetails userDetails) {',
    '        String userId = userDetails.getUsername();',
    '        goalService.deleteGoal(id, userId);',
    '        return ResponseEntity.ok(ApiResponse.<Void>builder()',
    '                .success(true)',
    '                .message("Goal deleted")',
    '                .build());',
    '    }',
    '}'
])

add_para(doc, 'Контролер надає 5 основних endpoint\'ів: POST /goals - створення нової цілі, GET /goals - отримання всіх цілей користувача, GET /goals/{id} - отримання конкретної цілі, PUT /goals/{id} - оновлення цілі, DELETE /goals/{id} - видалення цілі. Автоматична валідація доступу забезпечується передачею userId до сервісного шару.')

doc.add_paragraph()

add_explanation(doc,
    'Клас ProgressController - контролер логування прогресу:',
    'ProgressController дозволяє користувачам логувати щоденний прогрес по цілях та отримувати історію виконання. Кожен запис прогресу зберігається з датою та опціональними нотатками.')

add_code_block(doc, [
    'package com.example.cwweb.progress;',
    '',
    'import com.example.cwweb.common.ApiResponse;',
    'import org.springframework.http.ResponseEntity;',
    'import org.springframework.security.core.annotation.AuthenticationPrincipal;',
    'import org.springframework.security.core.userdetails.UserDetails;',
    'import org.springframework.web.bind.annotation.*;',
    'import java.util.List;',
    '',
    '@RestController',
    '@RequestMapping("/progress")',
    'public class ProgressController {',
    '    private final ProgressService progressService;',
    '',
    '    public ProgressController(ProgressService progressService) {',
    '        this.progressService = progressService;',
    '    }',
    '',
    '    @PostMapping',
    '    public ResponseEntity<ApiResponse<ProgressLog>> logProgress(',
    '            @AuthenticationPrincipal UserDetails userDetails,',
    '            @RequestBody LogProgressRequest request) {',
    '        String userId = userDetails.getUsername();',
    '        ProgressLog log = progressService.logProgress(userId, request);',
    '        return ResponseEntity.ok(ApiResponse.<ProgressLog>builder()',
    '                .success(true)',
    '                .message("Progress logged")',
    '                .data(log)',
    '                .build());',
    '    }',
    '',
    '    @GetMapping("/goal/{goalId}")',
    '    public ResponseEntity<ApiResponse<List<ProgressLog>>> getGoalProgress(',
    '            @PathVariable String goalId,',
    '            @AuthenticationPrincipal UserDetails userDetails) {',
    '        String userId = userDetails.getUsername();',
    '        List<ProgressLog> logs = progressService.getGoalProgress(',
    '                goalId, userId);',
    '        return ResponseEntity.ok(ApiResponse.<List<ProgressLog>>builder()',
    '                .success(true)',
    '                .data(logs)',
    '                .build());',
    '    }',
    '}'
])

add_para(doc, 'Endpoint POST /progress приймає goalId, дату та опціональні нотатки для створення запису прогресу. GET /progress/goal/{goalId} повертає всю історію виконання конкретної цілі у хронологічному порядку.')

# 4.1.3 Service Layer
doc.add_page_break()
doc.add_heading('4.1.3 Сервісний шар - бізнес-логіка', level=3)

add_explanation(doc,
    'Клас GoalService - сервіс управління цілями:',
    'GoalService містить бізнес-логіку роботи з цілями. Виконує валідацію даних, перевірку прав доступу та взаємодію з репозиторієм. Використовує pattern Builder для створення об\'єктів Goal.')

add_code_block(doc, [
    'package com.example.cwweb.goals;',
    '',
    'import com.example.cwweb.common.NotFoundException;',
    'import com.example.cwweb.common.ForbiddenException;',
    'import org.springframework.stereotype.Service;',
    'import java.time.LocalDateTime;',
    'import java.util.List;',
    '',
    '@Service',
    'public class GoalService {',
    '    private final GoalRepository goalRepository;',
    '',
    '    public GoalService(GoalRepository goalRepository) {',
    '        this.goalRepository = goalRepository;',
    '    }',
    '',
    '    public Goal createGoal(String userId, CreateGoalRequest request) {',
    '        Goal goal = Goal.builder()',
    '                .userId(userId)',
    '                .title(request.getTitle())',
    '                .description(request.getDescription())',
    '                .frequency(request.getFrequency())',
    '                .startDate(request.getStartDate())',
    '                .endDate(request.getEndDate())',
    '                .isPublic(request.isPublic())',
    '                .status(GoalStatus.ACTIVE)',
    '                .createdAt(LocalDateTime.now())',
    '                .updatedAt(LocalDateTime.now())',
    '                .build();',
    '        return goalRepository.save(goal);',
    '    }',
    '',
    '    public List<Goal> getUserGoals(String userId) {',
    '        return goalRepository.findByUserId(userId);',
    '    }',
    '',
    '    public Goal getGoal(String goalId, String userId) {',
    '        Goal goal = goalRepository.findById(goalId)',
    '                .orElseThrow(() -> new NotFoundException("Goal not found"));',
    '        if (!goal.getUserId().equals(userId) && !goal.isPublic()) {',
    '            throw new ForbiddenException("Access denied");',
    '        }',
    '        return goal;',
    '    }',
    '',
    '    public Goal updateGoal(String goalId, String userId,',
    '                          UpdateGoalRequest request) {',
    '        Goal goal = goalRepository.findById(goalId)',
    '                .orElseThrow(() -> new NotFoundException("Goal not found"));',
    '        if (!goal.getUserId().equals(userId)) {',
    '            throw new ForbiddenException("Access denied");',
    '        }',
    '        if (request.getTitle() != null)',
    '            goal.setTitle(request.getTitle());',
    '        if (request.getDescription() != null)',
    '            goal.setDescription(request.getDescription());',
    '        if (request.getStatus() != null)',
    '            goal.setStatus(request.getStatus());',
    '        goal.setUpdatedAt(LocalDateTime.now());',
    '        return goalRepository.save(goal);',
    '    }',
    '',
    '    public void deleteGoal(String goalId, String userId) {',
    '        Goal goal = goalRepository.findById(goalId)',
    '                .orElseThrow(() -> new NotFoundException("Goal not found"));',
    '        if (!goal.getUserId().equals(userId)) {',
    '            throw new ForbiddenException("Access denied");',
    '        }',
    '        goalRepository.deleteById(goalId);',
    '    }',
    '}'
])

add_para(doc, 'Сервіс забезпечує безпеку через перевірку userId при кожній операції. Метод createGoal автоматично встановлює статус ACTIVE та поточний час створення. Метод getGoal дозволяє доступ до публічних цілей інших користувачів. Метод updateGoal використовує патерн часткового оновлення (patch), дозволяючи змінювати лише передані поля.')

# 4.2 Frontend реалізація
doc.add_page_break()
doc.add_heading('4.2 Реалізація frontend частини системи', level=2)

doc.add_heading('4.2.1 Структура React додатку', level=3)

add_explanation(doc,
    'Файл App.jsx - головний компонент додатку:',
    'App.jsx є точкою входу додатку. Налаштовує маршрутизацію за допомогою React Router v6, визначає захищені та публічні маршрути, підключає систему сповіщень (react-hot-toast). Використовує Zustand store для управління станом автентифікації.')

add_code_block(doc, [
    "import { BrowserRouter, Routes, Route, Navigate }",
    "        from 'react-router-dom'",
    "import { Toaster } from 'react-hot-toast'",
    "import { useAuthStore } from './store/authStore'",
    "import Layout from './components/Layout'",
    "import Login from './pages/Login'",
    "import Dashboard from './pages/Dashboard'",
    "import Goals from './pages/Goals'",
    "",
    "function ProtectedRoute({ children }) {",
    "  const { token } = useAuthStore()",
    "  return token ? children : <Navigate to='/login' />",
    "}",
    "",
    "function PublicRoute({ children }) {",
    "  const { token } = useAuthStore()",
    "  return !token ? children : <Navigate to='/dashboard' />",
    "}",
    "",
    "function App() {",
    "  return (",
    "    <BrowserRouter>",
    "      <Toaster position='top-right' />",
    "      <Routes>",
    "        <Route path='/login' element={",
    "          <PublicRoute><Login /></PublicRoute>",
    "        } />",
    "        <Route path='/' element={",
    "          <ProtectedRoute><Layout /></ProtectedRoute>",
    "        }>",
    "          <Route index element={<Navigate to='/dashboard' />} />",
    "          <Route path='dashboard' element={<Dashboard />} />",
    "          <Route path='goals' element={<Goals />} />",
    "        </Route>",
    "      </Routes>",
    "    </BrowserRouter>",
    "  )",
    "}",
    "",
    "export default App"
], "JavaScript")

add_para(doc, 'Компоненти ProtectedRoute та PublicRoute забезпечують контроль доступу: ProtectedRoute перенаправляє неавторизованих користувачів на /login, PublicRoute перенаправляє авторизованих на /dashboard. Використання вкладених маршрутів (nested routes) дозволяє Layout бути обгорткою для всіх захищених сторінок.')

doc.add_paragraph()

doc.add_heading('4.2.2 State Management - Zustand', level=3)

add_explanation(doc,
    'Файл authStore.js - глобальний стан автентифікації:',
    'Zustand store управляє станом автентифікації користувача. Використовує middleware persist для збереження токенів у localStorage, що дозволяє зберігати сесію після перезавантаження сторінки. Надає методи для login, logout та оновлення токенів.')

add_code_block(doc, [
    "import { create } from 'zustand'",
    "import { persist } from 'zustand/middleware'",
    "",
    "export const useAuthStore = create(",
    "  persist(",
    "    (set) => ({",
    "      token: null,",
    "      refreshToken: null,",
    "      user: null,",
    "      ",
    "      setTokens: (accessToken, refreshToken) => {",
    "        set({ token: accessToken, refreshToken })",
    "      },",
    "      ",
    "      setUser: (user) => {",
    "        set({ user })",
    "      },",
    "      ",
    "      login: (accessToken, refreshToken, user) => {",
    "        set({ token: accessToken, refreshToken, user })",
    "      },",
    "      ",
    "      logout: () => {",
    "        set({ token: null, refreshToken: null, user: null })",
    "      },",
    "    }),",
    "    {",
    "      name: 'auth-storage',",
    "    }",
    "  )",
    ")"
], "JavaScript")

add_para(doc, 'Store зберігає три основні поля: token (JWT access token), refreshToken (для оновлення токенів), user (дані користувача). Метод login встановлює всі три значення одночасно при успішній авторизації. Метод logout очищає стан. Persist middleware автоматично синхронізує зміни з localStorage.')

doc.add_paragraph()

doc.add_heading('4.2.3 API клієнти', level=3)

add_explanation(doc,
    'Файл client.js - налаштування Axios:',
    'Базовий HTTP клієнт на основі Axios з налаштованими interceptor\'ами. Request interceptor додає JWT токен до кожного запиту. Response interceptor обробляє помилки 401 та автоматично оновлює токени через refresh endpoint.')

add_code_block(doc, [
    "import axios from 'axios'",
    "import { useAuthStore } from '../store/authStore'",
    "",
    "const client = axios.create({",
    "  baseURL: '/api',",
    "  headers: { 'Content-Type': 'application/json' },",
    "})",
    "",
    "client.interceptors.request.use((config) => {",
    "  const token = useAuthStore.getState().token",
    "  if (token) {",
    "    config.headers.Authorization = `Bearer ${token}`",
    "  }",
    "  return config",
    "})",
    "",
    "client.interceptors.response.use(",
    "  (response) => response,",
    "  async (error) => {",
    "    const originalRequest = error.config",
    "    if (error.response?.status === 401 && !originalRequest._retry) {",
    "      originalRequest._retry = true",
    "      try {",
    "        const refreshToken = useAuthStore.getState().refreshToken",
    "        const { data } = await axios.post('/api/auth/refresh',",
    "                                          { refreshToken })",
    "        useAuthStore.getState().setTokens(",
    "          data.data.accessToken, data.data.refreshToken",
    "        )",
    "        originalRequest.headers.Authorization =",
    "          `Bearer ${data.data.accessToken}`",
    "        return client(originalRequest)",
    "      } catch (refreshError) {",
    "        useAuthStore.getState().logout()",
    "        window.location.href = '/login'",
    "        return Promise.reject(refreshError)",
    "      }",
    "    }",
    "    return Promise.reject(error)",
    "  }",
    ")",
    "",
    "export default client"
], "JavaScript")

add_para(doc, 'Response interceptor реалізує автоматичне оновлення токенів: при отриманні 401 помилки робиться спроба оновити токен через /auth/refresh, якщо успішно - повторюється оригінальний запит з новим токеном, якщо ні - користувач розлогінюється. Прапорець _retry запобігає нескінченним циклам.')

doc.add_paragraph()

add_explanation(doc,
    'Файл goals.js - API методи для роботи з цілями:',
    'Модуль goalsAPI інкапсулює всі HTTP запити для роботи з цілями. Кожен метод повертає Promise з розпакованими даними з ApiResponse. Використовує базовий client з автоматичною автентифікацією.')

add_code_block(doc, [
    "import client from './client'",
    "",
    "export const goalsAPI = {",
    "  getAll: async () => {",
    "    const { data } = await client.get('/goals')",
    "    return data.data",
    "  },",
    "  ",
    "  getById: async (id) => {",
    "    const { data } = await client.get(`/goals/${id}`)",
    "    return data.data",
    "  },",
    "  ",
    "  create: async (goalData) => {",
    "    const { data } = await client.post('/goals', goalData)",
    "    return data.data",
    "  },",
    "  ",
    "  update: async (id, goalData) => {",
    "    const { data } = await client.put(`/goals/${id}`, goalData)",
    "    return data.data",
    "  },",
    "  ",
    "  delete: async (id) => {",
    "    await client.delete(`/goals/${id}`)",
    "  },",
    "  ",
    "  logProgress: async (progressData) => {",
    "    const { data } = await client.post('/progress', progressData)",
    "    return data.data",
    "  },",
    "}"
], "JavaScript")

add_para(doc, 'API методи: getAll отримує список всіх цілей користувача, getById отримує конкретну ціль, create створює нову ціль, update оновлює існуючу (patch), delete видаляє ціль, logProgress логує прогрес виконання. Всі методи автоматично додають JWT токен через interceptor.')

doc.add_page_break()
doc.add_heading('4.2.4 React компоненти та сторінки', level=3)

add_explanation(doc,
    'Компонент Layout.jsx - загальна структура додатку:',
    'Layout компонент забезпечує консистентну структуру всіх сторінок. Містить бічну панель навігації з іконками (використовуючи lucide-react), шапку з інформацією користувача та основну область контенту. Використовує Outlet від React Router для рендерингу вкладених маршрутів.')

add_code_block(doc, [
    "import { Outlet, NavLink, useNavigate } from 'react-router-dom'",
    "import { useAuthStore } from '../store/authStore'",
    "import { Home, Target, Users, Award, LogOut } from 'lucide-react'",
    "",
    "export default function Layout() {",
    "  const { user, logout } = useAuthStore()",
    "  const navigate = useNavigate()",
    "",
    "  const handleLogout = () => {",
    "    logout()",
    "    navigate('/login')",
    "  }",
    "",
    "  const navItems = [",
    "    { to: '/dashboard', icon: Home, label: 'Dashboard' },",
    "    { to: '/goals', icon: Target, label: 'Goals' },",
    "    { to: '/groups', icon: Users, label: 'Groups' },",
    "    { to: '/achievements', icon: Award, label: 'Achievements' },",
    "  ]",
    "",
    "  return (",
    "    <div className='flex h-screen bg-gray-100'>",
    "      <aside className='w-64 bg-white shadow-lg'>",
    "        <div className='p-6'>",
    "          <h1 className='text-2xl font-bold text-gray-800'>",
    "            Habit Tracker",
    "          </h1>",
    "          <p className='text-sm text-gray-600 mt-1'>",
    "            {user?.displayName}",
    "          </p>",
    "        </div>",
    "        ",
    "        <nav className='mt-6'>",
    "          {navItems.map(({ to, icon: Icon, label }) => (",
    "            <NavLink key={to} to={to}",
    "              className={({ isActive }) =>",
    "                `flex items-center px-6 py-3 text-gray-700",
    "                hover:bg-gray-100 ${isActive ?",
    "                'bg-gray-100 border-r-4 border-blue-500' : ''}`",
    "              }",
    "            >",
    "              <Icon className='w-5 h-5 mr-3' />",
    "              {label}",
    "            </NavLink>",
    "          ))}",
    "        </nav>",
    "",
    "        <button onClick={handleLogout}",
    "          className='flex items-center px-6 py-3 mt-auto",
    "                     text-red-600 hover:bg-red-50 w-full'",
    "        >",
    "          <LogOut className='w-5 h-5 mr-3' />",
    "          Logout",
    "        </button>",
    "      </aside>",
    "",
    "      <main className='flex-1 overflow-y-auto p-8'>",
    "        <Outlet />",
    "      </main>",
    "    </div>",
    "  )",
    "}"
], "JavaScript")

add_para(doc, 'Layout використовує Flexbox для двоколонкової структури: фіксована бічна панель (264px) та основний контент (flex-1). NavLink автоматично додає клас активного стану для поточної сторінки. Компонент Outlet від React Router рендерить вкладені маршрути. Tailwind CSS класи забезпечують адаптивний дизайн.')

doc.add_paragraph()

add_explanation(doc,
    'Сторінка Login.jsx - форма авторизації:',
    'Login компонент реалізує сторінку входу з двоколонковим макетом: ліва частина з описом функціоналу, права - з формою. Використовує useState для управління локальним станом форми, react-hot-toast для сповіщень. Після успішного входу зберігає токени у Zustand store та перенаправляє на dashboard.')

add_code_block(doc, [
    "import { useState } from 'react'",
    "import { Link, useNavigate } from 'react-router-dom'",
    "import { authAPI } from '../api/auth'",
    "import { useAuthStore } from '../store/authStore'",
    "import toast from 'react-hot-toast'",
    "import { Target } from 'lucide-react'",
    "",
    "export default function Login() {",
    "  const [email, setEmail] = useState('')",
    "  const [password, setPassword] = useState('')",
    "  const [loading, setLoading] = useState(false)",
    "  const navigate = useNavigate()",
    "  const { login } = useAuthStore()",
    "",
    "  const handleSubmit = async (e) => {",
    "    e.preventDefault()",
    "    setLoading(true)",
    "    try {",
    "      const data = await authAPI.login(email, password)",
    "      login(data.accessToken, data.refreshToken, data.user)",
    "      toast.success('Login successful!')",
    "      navigate('/dashboard')",
    "    } catch (error) {",
    "      toast.error(error.response?.data?.message || 'Login failed')",
    "    } finally {",
    "      setLoading(false)",
    "    }",
    "  }",
    "",
    "  return (",
    "    <div className='min-h-screen flex bg-gradient-to-br",
    "                    from-blue-500 via-purple-500 to-pink-500'>",
    "      <div className='flex-1 flex items-center justify-center p-8'>",
    "        <div className='max-w-md w-full bg-white rounded-2xl",
    "                        shadow-2xl p-8'>",
    "          <div className='text-center mb-8'>",
    "            <div className='inline-block p-3 bg-gradient-to-br",
    "                            from-blue-500 to-purple-500",
    "                            rounded-full mb-4'>",
    "              <Target className='w-8 h-8 text-white' />",
    "            </div>",
    "            <h2 className='text-3xl font-bold text-gray-800 mb-2'>",
    "              Welcome Back",
    "            </h2>",
    "          </div>",
    "          ",
    "          <form onSubmit={handleSubmit} className='space-y-5'>",
    "            <div>",
    "              <input type='email' value={email}",
    "                onChange={(e) => setEmail(e.target.value)}",
    "                className='w-full px-4 py-3 border-2",
    "                           border-gray-200 rounded-lg",
    "                           focus:outline-none focus:border-blue-500'",
    "                placeholder='you@example.com' required",
    "              />",
    "            </div>",
    "            <div>",
    "              <input type='password' value={password}",
    "                onChange={(e) => setPassword(e.target.value)}",
    "                className='w-full px-4 py-3 border-2",
    "                           border-gray-200 rounded-lg'",
    "                placeholder='••••••••' required",
    "              />",
    "            </div>",
    "            <button type='submit' disabled={loading}",
    "              className='w-full py-3 bg-gradient-to-r",
    "                         from-blue-600 to-purple-600",
    "                         text-white rounded-lg font-semibold'>",
    "              {loading ? 'Signing in...' : 'Sign In'}",
    "            </button>",
    "          </form>",
    "        </div>",
    "      </div>",
    "    </div>",
    "  )",
    "}"
], "JavaScript")

add_para(doc, 'Форма використовує controlled components pattern - значення input\'ів зберігаються у стані компонента через useState. handleSubmit запобігає стандартній поведінці форми, встановлює loading стан, викликає API, та обробляє успіх/помилку. Градієнтний фон створено через Tailwind CSS утиліти.')

doc.add_page_break()

add_explanation(doc,
    'Сторінка Dashboard.jsx - головна панель користувача:',
    'Dashboard відображає огляд цілей користувача. Використовує useEffect для завантаження даних при монтуванні компонента. Показує статистику у вигляді карток (загальна кількість цілей, активні, завершені) та список цілей у вигляді адаптивної сітки.')

add_code_block(doc, [
    "import { useEffect, useState } from 'react'",
    "import { Link } from 'react-router-dom'",
    "import { goalsAPI } from '../api/goals'",
    "import { Plus, Target, TrendingUp } from 'lucide-react'",
    "import toast from 'react-hot-toast'",
    "",
    "export default function Dashboard() {",
    "  const [goals, setGoals] = useState([])",
    "  const [loading, setLoading] = useState(true)",
    "",
    "  useEffect(() => {",
    "    loadGoals()",
    "  }, [])",
    "",
    "  const loadGoals = async () => {",
    "    try {",
    "      const data = await goalsAPI.getAll()",
    "      setGoals(data)",
    "    } catch (error) {",
    "      toast.error('Failed to load goals')",
    "    } finally {",
    "      setLoading(false)",
    "    }",
    "  }",
    "",
    "  if (loading) {",
    "    return <div className='text-center py-12'>Loading...</div>",
    "  }",
    "",
    "  return (",
    "    <div>",
    "      <div className='mb-8'>",
    "        <h1 className='text-4xl font-bold bg-gradient-to-r",
    "                       from-blue-600 to-purple-600",
    "                       bg-clip-text text-transparent mb-2'>",
    "          Dashboard",
    "        </h1>",
    "      </div>",
    "",
    "      <div className='grid grid-cols-1 md:grid-cols-3 gap-6 mb-8'>",
    "        <div className='bg-gradient-to-br from-blue-500",
    "                        to-blue-600 rounded-2xl p-6",
    "                        text-white shadow-xl'>",
    "          <p className='text-blue-100 text-sm'>Total Goals</p>",
    "          <p className='text-3xl font-bold mt-1'>",
    "            {goals.length}",
    "          </p>",
    "        </div>",
    "        ",
    "        <div className='bg-gradient-to-br from-green-500",
    "                        to-green-600 rounded-2xl p-6",
    "                        text-white shadow-xl'>",
    "          <p className='text-green-100 text-sm'>Active Goals</p>",
    "          <p className='text-3xl font-bold mt-1'>",
    "            {goals.filter(g => g.status === 'ACTIVE').length}",
    "          </p>",
    "        </div>",
    "      </div>",
    "",
    "      <div className='grid grid-cols-1 md:grid-cols-2",
    "                      lg:grid-cols-3 gap-6'>",
    "        {goals.map((goal) => (",
    "          <Link key={goal.id} to={`/goals/${goal.id}`}",
    "            className='group bg-white rounded-2xl shadow-lg p-6",
    "                       hover:shadow-2xl transition-all",
    "                       transform hover:scale-105'>",
    "            <h3 className='text-lg font-bold text-gray-900",
    "                           group-hover:text-blue-600'>",
    "              {goal.title}",
    "            </h3>",
    "            <p className='text-gray-600 text-sm mt-2'>",
    "              {goal.description}",
    "            </p>",
    "          </Link>",
    "        ))}",
    "      </div>",
    "    </div>",
    "  )",
    "}"
], "JavaScript")

add_para(doc, 'useEffect з порожнім масивом залежностей [] виконується лише при монтуванні. loadGoals - async функція для завантаження даних з обробкою помилок через try-catch. Статистичні картки використовують filter для підрахунку цілей за статусом. Grid layout (grid-cols-1 md:grid-cols-3) забезпечує адаптивність: 1 колонка на мобільних, 3 на десктопі.')

doc.add_paragraph()

add_para(doc, 'Таким чином, frontend частина реалізована на сучасному стеку React 18 + Vite з використанням best practices: функціональні компоненти з хуками, централізоване управління станом через Zustand, модульна архітектура API клієнтів, автоматичне оновлення JWT токенів, адаптивний дизайн через Tailwind CSS.')

# Висновок до розділу 4
doc.add_paragraph()
add_para(doc, 'У даному розділі детально розглянуто реалізацію веб-системи для відстеження звичок. Backend побудовано на Spring Boot з трьохшаровою архітектурою (Controller-Service-Repository), використовуючи MongoDB як сховище даних. Frontend реалізовано на React 18 з використанням сучасних підходів: функціональні компоненти, хуки, Zustand для state management, React Router для навігації. Система забезпечує безпеку через JWT автентифікацію, автоматичне оновлення токенів, валідацію доступу на рівні сервісів. Код написано з дотриманням принципів чистого коду, SOLID та DRY.')

# Збереження документу
doc.save('/home/runner/work/cw_web/cw_web/Курсова_Робота_HabitTracker.docx')
print("✅ Документ успішно розширено!")
print("📊 Додано детальні приклади коду з поясненнями:")
print("   - Entity класи (User, Goal, Group)")
print("   - Controller класи (Auth, Goal, Progress)")
print("   - Service класи (GoalService)")
print("   - React компоненти (App, Layout, Login, Dashboard)")
print("   - API клієнти (client, goals)")
print("   - State management (Zustand)")
print("📖 Кожен приклад коду супроводжується детальним поясненням")
