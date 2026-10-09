import pygame
import math
import random
import re

WIDTH = 580
HEIGHT = 460
FPS = 30

IMAGE_PATH = "spr/img.png"

WHITE = (255, 255, 255)
BLACK = (25, 25, 25)
DARK_BLUE = (42, 83, 130)
BLUE = (65, 125, 190)
LIGHT_BLUE = (210, 230, 248)
GRAY = (235, 235, 235)
PED = (60, 33, 140)
PED2 = (239, 125, 0)
RED = (180, 30, 30)
GREEN = (20, 120, 50)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Вычислительные алгоритмы")

clock = pygame.time.Clock()

font_title = pygame.font.SysFont("arial", 21, bold=True)
font_button = pygame.font.SysFont("arial", 15, bold=True)
font_text = pygame.font.SysFont("arial", 17)
font_small = pygame.font.SysFont("arial", 14)
font_footer = pygame.font.SysFont("arial", 14)

try:
    image = pygame.image.load(IMAGE_PATH).convert_alpha()
    image = pygame.transform.smoothscale(image, (200, 80))
except pygame.error:
    image = None
    print(f"Не получилося: {IMAGE_PATH}")



buttons = [
    {
        "name": "Метод Пол. Деления",
        "rect": pygame.Rect(20, HEIGHT - 135, 170, 45)
    },
    {
        "name": "Общ. метода пол дел",
        "rect": pygame.Rect(205, HEIGHT - 135, 170, 45)
    },
    {
        "name": "Метод касательных",
        "rect": pygame.Rect(390, HEIGHT - 135, 170, 45)
    },
    {
        "name": "Метод хорд",
        "rect": pygame.Rect(390, HEIGHT - 195, 170, 45)
    },
    {
        "name": "Метод итераций",
        "rect": pygame.Rect(205, HEIGHT - 195, 170, 45)
    },
    {
        "name": "Метод наим. квадратов",
        "rect": pygame.Rect(20, HEIGHT - 195, 170, 45)
    },
    {
        "name": "Ньютон-Лейбниц",
        "rect": pygame.Rect(390, HEIGHT - 255, 170, 45)
    },
    {
        "name": "Метод Симпсона",
        "rect": pygame.Rect(205, HEIGHT - 255, 170, 45)
    },
    {
        "name": "Метод Монте-Карло",
        "rect": pygame.Rect(20, HEIGHT - 255, 170, 45)
    }
]

back_button = pygame.Rect(20, HEIGHT - 55, 160, 35)

calculate_button = pygame.Rect(390, HEIGHT - 55, 170, 35)

current_page = "Главная"
input_fields = []
result_text = ""
result_color = GREEN


# Функции матешы
SAFE_FUNCTIONS = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "sqrt": math.sqrt,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "abs": abs,
    "pi": math.pi,
    "e": math.e
}


class InputField:

    def __init__(self, label, x, y, width=330, default_text=""):
        self.label = label
        self.rect = pygame.Rect(x, y, width, 30)
        self.text = default_text
        self.active = False

    def draw(self):
        label_surface = font_small.render(self.label, True, BLACK)
        screen.blit(label_surface, (20, self.rect.y + 7))

        if self.active:
            border_color = BLUE
            background_color = (250, 253, 255)
        else:
            border_color = GRAY
            background_color = WHITE

        pygame.draw.rect(screen, background_color, self.rect)
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=4)

        shown_text = self.text

        # Если текст длиннее поля, показывается только его правая часть
        while font_small.size(shown_text)[0] > self.rect.width - 10:
            shown_text = shown_text[1:]

        text_surface = font_small.render(shown_text, True, BLACK)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 7))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]

            elif event.key == pygame.K_DELETE:
                self.text = ""

            elif event.key != pygame.K_RETURN:
                self.text += event.unicode


def draw_button_rect(rect, text):
    mouse_position = pygame.mouse.get_pos()

    if rect.collidepoint(mouse_position):
        color = BLUE
    else:
        color = DARK_BLUE

    pygame.draw.rect(screen, color, rect, border_radius=7)

    text_surface = font_button.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def draw_button(button):
    draw_button_rect(button["rect"], button["name"])


def draw_main_page():
    screen.fill(WHITE)

    pygame.draw.line(screen, PED, (0, 106), (WIDTH, 106), 4)
    pygame.draw.line(screen, PED2, (0, 110), (WIDTH, 110), 4)

    if image is not None:
        screen.blit(image, (15, 12))

    title = font_title.render("Вычислительные алгоритмы", True, BLACK)
    screen.blit(title, (260, 40))

    info = font_text.render("Выберите вычислительный агоритм:", True, BLACK)
    screen.blit(info, (20, 120))

    maker = font_footer.render(
        "Аникин Владимир | группа 1214 | Алгоритмы и структуры данных",
        True,
        BLACK
    )
    screen.blit(maker, (10, 435))

    for button in buttons:
        draw_button(button)


def draw_wrapped_text(text, x, y, color=BLACK, max_width=540):

    words = text.split()
    line = ""
    line_height = 18

    for word in words:
        test_line = line + word + " "

        if font_small.size(test_line)[0] <= max_width:
            line = test_line
        else:
            surface = font_small.render(line, True, color)
            screen.blit(surface, (x, y))
            y += line_height
            line = word + " "

    if line:
        surface = font_small.render(line, True, color)
        screen.blit(surface, (x, y))
        y += line_height

    return y


def draw_algorithm_page(page_name):
    screen.fill(WHITE)

    pygame.draw.line(screen, PED, (0, 48), (WIDTH, 48), 3)
    pygame.draw.line(screen, PED2, (0, 51), (WIDTH, 51), 3)

    title = font_title.render(page_name, True, BLACK)
    title_rect = title.get_rect(center=(WIDTH // 2, 23))
    screen.blit(title, title_rect)

    for field in input_fields:
        field.draw()

    if result_text:
        pygame.draw.rect(screen, (248, 248, 248), (20, 280, 540, 110))
        pygame.draw.rect(screen, GRAY, (20, 280, 540, 110), 1)

        result_title = font_small.render("Результат:", True, BLACK)
        screen.blit(result_title, (30, 290))

        draw_wrapped_text(
            result_text,
            30,
            315,
            result_color,
            520
        )

    draw_button_rect(back_button, "На главную")
    draw_button_rect(calculate_button, "Вычислить")


def safe_function(expression):

    expression = expression.replace("^", "**").replace(",", ".")

    def function(x):
        local_variables = {
            "x": x,
            **SAFE_FUNCTIONS
        }

        return eval(
            expression,
            {"__builtins__": {}},
            local_variables
        )

    function(1)

    return function


def number(text):
    return float(text.replace(",", "."))


def number_list(text):

    values = re.split(r"[,;\s]+", text.strip())
    return [float(value.replace(",", ".")) for value in values if value]


def get_field_value(label):

    for field in input_fields:
        if field.label == label:
            return field.text

    return ""


def bisection_method(function, a, b, epsilon):

    if function(a) * function(b) > 0:
        raise ValueError(
            "На концах отрезка функция должна иметь разные знаки."
        )

    iterations = 0

    while abs(b - a) > epsilon and iterations < 10000:
        middle = (a + b) / 2

        if function(a) * function(middle) <= 0:
            b = middle
        else:
            a = middle

        iterations += 1

    answer = (a + b) / 2

    return answer, iterations


def generalized_bisection(function, a, b, epsilon):

    parts = 300
    step = (b - a) / parts
    roots = []

    left = a

    for i in range(parts):
        right = a + (i + 1) * step
        f_left = function(left)
        f_right = function(right)

        if f_left == 0:
            roots.append(left)

        elif f_left * f_right < 0:
            root, _ = bisection_method(function, left, right, epsilon)
            roots.append(root)

        left = right

    unique_roots = []

    for root in roots:
        if not any(
            abs(root - existing) < epsilon * 10
            for existing in unique_roots
        ):
            unique_roots.append(root)

    return unique_roots


def newton_method(function, derivative, x0, epsilon):

    x = x0
    iterations = 0

    while iterations < 1000:
        derivative_value = derivative(x)

        if abs(derivative_value) < 0.0000000001:
            raise ValueError(
                "Производная равна нулю. Выберите другое x0."
            )

        next_x = x - function(x) / derivative_value

        if abs(next_x - x) < epsilon:
            return next_x, iterations + 1

        x = next_x
        iterations += 1

    raise ValueError("Превышено число итераций.")


def chord_method(function, x0, x1, epsilon):
    iterations = 0

    while iterations < 1000:
        f0 = function(x0)
        f1 = function(x1)

        if abs(f1 - f0) < 0.0000000001:
            raise ValueError("Деление на ноль в методе хорд.")

        next_x = x1 - f1 * (x1 - x0) / (f1 - f0)

        if abs(next_x - x1) < epsilon:
            return next_x, iterations + 1

        x0 = x1
        x1 = next_x
        iterations += 1

    raise ValueError("Превышено число итераций.")


def iteration_method(g_function, x0, epsilon):
    x = x0
    iterations = 0

    while iterations < 10000:
        next_x = g_function(x)

        if abs(next_x - x) < epsilon:
            return next_x, iterations + 1

        x = next_x
        iterations += 1

    raise ValueError("Метод не сошёлся за 10000 итераций.")


def least_squares_method(x_values, y_values):
    if len(x_values) != len(y_values):
        raise ValueError("Количество значений X и Y должно совпадать.")

    if len(x_values) < 2:
        raise ValueError("Нужно ввести минимум две точки.")

    n = len(x_values)
    sum_x = sum(x_values)
    sum_y = sum(y_values)
    sum_xy = sum(x * y for x, y in zip(x_values, y_values))
    sum_x2 = sum(x * x for x in x_values)

    denominator = n * sum_x2 - sum_x ** 2

    if abs(denominator) < 0.0000000001:
        raise ValueError("Невозможно построить прямую для таких X.")

    a = (n * sum_xy - sum_x * sum_y) / denominator
    b = (sum_y - a * sum_x) / n

    return a, b


def newton_leibniz_method(function, a, b, n):
    h = (b - a) / n
    total = 0

    for i in range(n):
        x = a + (i + 0.5) * h
        total += function(x)

    return total * h


def simpson_method(function, a, b, n):
    if n % 2 != 0:
        raise ValueError("Для метода Симпсона n должно быть чётным.")

    h = (b - a) / n
    total = function(a) + function(b)

    for i in range(1, n):
        x = a + i * h

        if i % 2 == 0:
            total += 2 * function(x)
        else:
            total += 4 * function(x)

    return total * h / 3


def monte_carlo_method(function, a, b, n):

    total = 0

    for _ in range(n):
        x = random.uniform(a, b)
        total += function(x)

    return (b - a) * total / n


def create_input_fields(page_name):

    fields = []

    if page_name == "Метод Пол. Деления":
        fields = [
            InputField("f(x):", 170, 70, 380, "x**3 - x - 2"),
            InputField("a:", 170, 110, 150, "1"),
            InputField("b:", 170, 150, 150, "2"),
            InputField("Точность eps:", 170, 190, 150, "0.0001")
        ]

    elif page_name == "Общ. метода пол дел":
        fields = [
            InputField("f(x):", 170, 70, 380, "sin(x)"),
            InputField("a:", 170, 110, 150, "-10"),
            InputField("b:", 170, 150, 150, "10"),
            InputField("Точность eps:", 170, 190, 150, "0.0001")
        ]

    elif page_name == "Метод касательных":
        fields = [
            InputField("f(x):", 170, 70, 380, "x**3 - x - 2"),
            InputField("f'(x):", 170, 110, 380, "3*x**2 - 1"),
            InputField("Начальное x0:", 170, 150, 150, "1.5"),
            InputField("Точность eps:", 170, 190, 150, "0.0001")
        ]

    elif page_name == "Метод хорд":
        fields = [
            InputField("f(x):", 170, 70, 380, "x**3 - x - 2"),
            InputField("x0:", 170, 110, 150, "1"),
            InputField("x1:", 170, 150, 150, "2"),
            InputField("Точность eps:", 170, 190, 150, "0.0001")
        ]

    elif page_name == "Метод итераций":
        fields = [
            InputField("g(x):", 170, 70, 380, "cos(x)"),
            InputField("Начальное x0:", 170, 110, 150, "0.5"),
            InputField("Точность eps:", 170, 150, 150, "0.0001")
        ]

    elif page_name == "Метод наим. квадратов":
        fields = [
            InputField("X через пробел:", 170, 80, 380, "1 2 3 4 5"),
            InputField("Y через пробел:", 170, 125, 380, "2 4 5 4 5")
        ]

    elif page_name == "Ньютон-Лейбниц":
        fields = [
            InputField("f(x):", 170, 70, 380, "x**2"),
            InputField("a:", 170, 110, 150, "0"),
            InputField("b:", 170, 150, 150, "2"),
            InputField("Число n:", 170, 190, 150, "1000")
        ]

    elif page_name == "Метод Симпсона":
        fields = [
            InputField("f(x):", 170, 70, 380, "x**2"),
            InputField("a:", 170, 110, 150, "0"),
            InputField("b:", 170, 150, 150, "2"),
            InputField("Чётное n:", 170, 190, 150, "100")
        ]

    elif page_name == "Метод Монте-Карло":
        fields = [
            InputField("f(x):", 170, 70, 380, "x**2"),
            InputField("a:", 170, 110, 150, "0"),
            InputField("b:", 170, 150, 150, "2"),
            InputField("Число точек n:", 170, 190, 150, "10000")
        ]

    return fields


def calculate():
    global result_text
    global result_color

    try:
        if current_page == "Метод Пол. Деления":
            function = safe_function(get_field_value("f(x):"))
            a = number(get_field_value("a:"))
            b = number(get_field_value("b:"))
            epsilon = number(get_field_value("Точность eps:"))

            root, iterations = bisection_method(function, a, b, epsilon)

            result_text = (
                f"Корень: x = {root:.8f}. "
                f"Количество итераций: {iterations}."
            )

        elif current_page == "Общ. метода пол дел":
            function = safe_function(get_field_value("f(x):"))
            a = number(get_field_value("a:"))
            b = number(get_field_value("b:"))
            epsilon = number(get_field_value("Точность eps:"))

            roots = generalized_bisection(function, a, b, epsilon)

            if roots:
                roots_string = ", ".join(
                    f"{root:.6f}" for root in roots
                )
                result_text = f"Найденные корни: {roots_string}"
            else:
                result_text = (
                    "Корни со сменой знака на данном отрезке не найдены."
                )

        elif current_page == "Метод касательных":
            function = safe_function(get_field_value("f(x):"))
            derivative = safe_function(get_field_value("f'(x):"))
            x0 = number(get_field_value("Начальное x0:"))
            epsilon = number(get_field_value("Точность eps:"))

            root, iterations = newton_method(
                function,
                derivative,
                x0,
                epsilon
            )

            result_text = (
                f"Корень: x = {root:.8f}. "
                f"Количество итераций: {iterations}."
            )

        elif current_page == "Метод хорд":
            function = safe_function(get_field_value("f(x):"))
            x0 = number(get_field_value("x0:"))
            x1 = number(get_field_value("x1:"))
            epsilon = number(get_field_value("Точность eps:"))

            root, iterations = chord_method(function, x0, x1, epsilon)

            result_text = (
                f"Корень: x = {root:.8f}. "
                f"Количество итераций: {iterations}."
            )

        elif current_page == "Метод итераций":
            g_function = safe_function(get_field_value("g(x):"))
            x0 = number(get_field_value("Начальное x0:"))
            epsilon = number(get_field_value("Точность eps:"))

            root, iterations = iteration_method(
                g_function,
                x0,
                epsilon
            )

            result_text = (
                f"Приближённое решение: x = {root:.8f}. "
                f"Количество итераций: {iterations}."
            )

        elif current_page == "Метод наим. квадратов":
            x_values = number_list(get_field_value("X через пробел:"))
            y_values = number_list(get_field_value("Y через пробел:"))

            a, b = least_squares_method(x_values, y_values)

            result_text = (
                f"Уравнение аппроксимирующей прямой: "
                f"y = {a:.6f}x + ({b:.6f})"
            )

        elif current_page == "Ньютон-Лейбниц":
            function = safe_function(get_field_value("f(x):"))
            a = number(get_field_value("a:"))
            b = number(get_field_value("b:"))
            n = int(number(get_field_value("Число n:")))

            if n <= 0:
                raise ValueError("n должно быть больше нуля.")

            integral = newton_leibniz_method(function, a, b, n)

            result_text = (
                f"Приближённое значение интеграла на [{a}; {b}]: "
                f"{integral:.8f}"
            )

        elif current_page == "Метод Симпсона":
            function = safe_function(get_field_value("f(x):"))
            a = number(get_field_value("a:"))
            b = number(get_field_value("b:"))
            n = int(number(get_field_value("Чётное n:")))

            integral = simpson_method(function, a, b, n)

            result_text = (
                f"Приближённое значение интеграла на [{a}; {b}]: "
                f"{integral:.8f}"
            )

        elif current_page == "Метод Монте-Карло":
            function = safe_function(get_field_value("f(x):"))
            a = number(get_field_value("a:"))
            b = number(get_field_value("b:"))
            n = int(number(get_field_value("Число точек n:")))

            if n <= 0:
                raise ValueError("n должно быть больше нуля.")

            integral = monte_carlo_method(function, a, b, n)

            result_text = (
                f"Приближённое значение интеграла на [{a}; {b}]: "
                f"{integral:.8f}. Точек: {n}."
            )

        result_color = GREEN

    except Exception as error:
        result_color = RED
        result_text = f"Ошибка: {error}"


done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Передаём события всем полям ввода на странице алгоритма
        if current_page != "Главная":
            for field in input_fields:
                field.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_position = event.pos

            if current_page == "Главная":
                for button in buttons:
                    if button["rect"].collidepoint(mouse_position):
                        current_page = button["name"]
                        input_fields = create_input_fields(current_page)
                        result_text = ""

            else:
                if back_button.collidepoint(mouse_position):
                    current_page = "Главная"
                    result_text = ""

                elif calculate_button.collidepoint(mouse_position):
                    calculate()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and current_page != "Главная":
                calculate()

    if current_page == "Главная":
        draw_main_page()
    else:
        draw_algorithm_page(current_page)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
