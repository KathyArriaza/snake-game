import turtle
import random

# =====================================================================
# 2. PARÁMETROS Y CONSTANTES DE CONFIGURACIÓN
# =====================================================================
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 20
LIMIT_X = 290
LIMIT_Y = 290
INITIAL_DELAY = 100        # Retardo inicial en milisegundos (0.1 s)
DELAY_REDUCTION = 2        # Reducción de retardo por fruta (1 a 2 ms)
MIN_DELAY = 40             # Límite mínimo para mantener jugabilidad


# =====================================================================
# 4.1 & 4.2 CLASE SERPIENTE (Snake Head & Snake Body)
# =====================================================================
class Snake:
    def __init__(self):
        # 4.1 Cabeza (Snake Head)
        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.shape("square")
        self.head.color("#2ecc71")  # Verde brillante para la cabeza
        self.head.penup()
        self.head.goto(0, 0)
        self.direction = "stop"
        
        # Bloqueo para evitar múltiples cambios de dirección en un solo frame
        self.direction_locked = False

        # 4.2 Cuerpo / Segmentos (Snake Body)
        self.segments = []

    # 3.3 Prevención de Giros Inválidos (180°)
    def go_up(self):
        if self.direction != "down" and not self.direction_locked:
            self.direction = "up"
            self.direction_locked = True

    def go_down(self):
        if self.direction != "up" and not self.direction_locked:
            self.direction = "down"
            self.direction_locked = True

    def go_left(self):
        if self.direction != "right" and not self.direction_locked:
            self.direction = "left"
            self.direction_locked = True

    def go_right(self):
        if self.direction != "left" and not self.direction_locked:
            self.direction = "right"
            self.direction_locked = True

    def add_segment(self):
        """Instancia un nuevo segmento y lo agrega al final de la colección."""
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("#27ae60")  # Verde ligeramente más oscuro para el cuerpo
        new_segment.penup()
        
        # Posicionar inicialmente en las coordenadas de la cola o de la cabeza
        if self.segments:
            tail_x, tail_y = self.segments[-1].xcor(), self.segments[-1].ycor()
        else:
            tail_x, tail_y = self.head.xcor(), self.head.ycor()
            
        new_segment.goto(tail_x, tail_y)
        self.segments.append(new_segment)

    # 5.1 Algoritmo de Movimiento Inverso
    def move(self):
        # 1. Propagar movimiento desde la cola (N-1) hasta el segmento 1
        for i in range(len(self.segments) - 1, 0, -1):
            prev_x = self.segments[i - 1].xcor()
            prev_y = self.segments[i - 1].ycor()
            self.segments[i].goto(prev_x, prev_y)

        # 2. Mover el primer segmento (índice 0) a la posición actual de la cabeza
        if len(self.segments) > 0:
            self.segments[0].goto(self.head.xcor(), self.head.ycor())

        # 3. Mover la cabeza a su nueva coordenada según el vector de dirección
        if self.direction == "up":
            self.head.sety(self.head.ycor() + GRID_SIZE)
        elif self.direction == "down":
            self.head.sety(self.head.ycor() - GRID_SIZE)
        elif self.direction == "left":
            self.head.setx(self.head.xcor() - GRID_SIZE)
        elif self.direction == "right":
            self.head.setx(self.head.xcor() + GRID_SIZE)

        # Desbloquear el cambio de dirección para el siguiente frame
        self.direction_locked = False

    def get_all_positions(self):
        """Devuelve un conjunto con las coordenadas (x, y) ocupadas por toda la serpiente."""
        positions = {(round(self.head.xcor()), round(self.head.ycor()))}
        for seg in self.segments:
            positions.add((round(seg.xcor()), round(seg.ycor())))
        return positions

    # 7.3 Optimización de Memoria en Reinicio
    def reset(self):
        self.head.goto(0, 0)
        self.direction = "stop"
        self.direction_locked = False
        for seg in self.segments:
            seg.goto(1000, 1000)  # Mover fuera de la pantalla
            seg.hideturtle()
        self.segments.clear()


# =====================================================================
# 4.3 CLASE COMIDA (Food)
# =====================================================================
class Food(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.speed(0)
        self.shape("circle")
        self.color("#e74c3c")  # Rojo para la fruta
        self.penup()
        self.relocate(set())

    def relocate(self, occupied_positions):
        """
        Genera coordenadas en [-280, 280] en pasos múltiplos exactos de 20 px,
        validando que no colisionen con la serpiente.
        """
        while True:
            x = random.randrange(-280, 281, GRID_SIZE)
            y = random.randrange(-280, 281, GRID_SIZE)
            if (x, y) not in occupied_positions:
                self.goto(x, y)
                break


# =====================================================================
# 4.4 CLASE MARCADOR (Scoreboard)
# =====================================================================
class Scoreboard(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.high_score = 0
        self.speed(0)
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(0, 260)
        self.update_display()

    def update_display(self, status_text=""):
        self.clear()
        base_text = f"Score: {self.score}  High Score: {self.high_score}"
        if status_text:
            base_text += f"  [{status_text}]"
        self.write(base_text, align="center", font=("Courier", 18, "bold"))

    def increase_score(self):
        self.score += 10
        if self.score > self.high_score:
            self.high_score = self.score
        self.update_display()

    def reset_score(self):
        self.score = 0
        self.update_display()


# =====================================================================
# 4. MOTOR DEL JUEGO (Game Engine)
# =====================================================================
class GameEngine:
    def __init__(self):
        # Inicialización de la pantalla
        self.screen = turtle.Screen()
        self.screen.title("Snake - Python Turtle")
        self.screen.bgcolor("#1e272e")  # Gris oscuro / pizarra para buen contraste
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        
        # 3.1 Control del Renderizado: Desactivar auto-dibujado
        self.screen.tracer(0)

        # Instanciar entidades
        self.snake = Snake()
        self.food = Food()
        self.food.relocate(self.snake.get_all_positions())
        self.scoreboard = Scoreboard()

        # Variables de estado y temporizador
        self.delay = INITIAL_DELAY
        self.state = "RUNNING"  # Estados soportados: RUNNING, PAUSED

        # Configurar controles
        self._setup_controls()

    def _setup_controls(self):
        self.screen.listen()
        # Controles con flechas de dirección
        self.screen.onkey(self.snake.go_up, "Up")
        self.screen.onkey(self.snake.go_down, "Down")
        self.screen.onkey(self.snake.go_left, "Left")
        self.screen.onkey(self.snake.go_right, "Right")
        # Controles con WASD
        self.screen.onkey(self.snake.go_up, "w")
        self.screen.onkey(self.snake.go_down, "s")
        self.screen.onkey(self.snake.go_left, "a")
        self.screen.onkey(self.snake.go_right, "d")
        # Tecla de Pausa
        self.screen.onkey(self.toggle_pause, "space")

    def toggle_pause(self):
        if self.state == "RUNNING":
            self.state = "PAUSED"
            self.scoreboard.update_display("PAUSADO")
        elif self.state == "PAUSED":
            self.state = "RUNNING"
            self.scoreboard.update_display()

    def trigger_game_over(self):
        """5.2.B / 5.2.C Rutina de fin de juego y reinicio de tablero."""
        self.snake.reset()
        self.scoreboard.reset_score()
        self.delay = INITIAL_DELAY
        self.food.relocate(self.snake.get_all_positions())

    # 6. Diagrama de Flujo del Ciclo de Ejecución
    def game_loop(self):
        try:
            if self.state == "RUNNING" and self.snake.direction != "stop":
                # 1. Mover segmentos del cuerpo y cabeza
                self.snake.move()

                # 2. ¿Colisión con Comida? (distancia < GRID_SIZE)
                if self.snake.head.distance(self.food) < GRID_SIZE:
                    self.snake.add_segment()
                    self.food.relocate(self.snake.get_all_positions())
                    self.scoreboard.increase_score()
                    self.delay = max(MIN_DELAY, self.delay - DELAY_REDUCTION)

                # 3. ¿Colisión con Bordes? (|x| > LIMIT_X o |y| > LIMIT_Y)
                head_x = self.snake.head.xcor()
                head_y = self.snake.head.ycor()
                if abs(head_x) > LIMIT_X or abs(head_y) > LIMIT_Y:
                    self.trigger_game_over()

                # 4. ¿Colisión con el Propio Cuerpo? (distancia < 10)
                else:
                    for segment in self.snake.segments:
                        if self.snake.head.distance(segment) < 10:
                            self.trigger_game_over()
                            break

            # 5. Renderizado manual en pantalla
            self.screen.update()

            # 6. Programar siguiente frame asíncrono (3.2 ontimer vs while True)
            self.screen.ontimer(self.game_loop, self.delay)

        except (turtle.Terminator, Exception):
            # 7.2 Manejo seguro del cierre de ventana
            pass

    def run(self):
        self.game_loop()
        self.screen.mainloop()


# =====================================================================
# PUNTO DE ENTRADA (main)
# =====================================================================
if __name__ == "__main__":
    try:
        game = GameEngine()
        game.run()
    except turtle.Terminator:
        pass