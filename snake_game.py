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
        self.head.color("#2ecc71")  # Verde claro para distinguir la cabeza
        self.head.penup()
        self.head.goto(0, 0)
        self.direction = "stop"
        
        # Bloqueo para evitar giros dobles en un mismo frame
        self.direction_locked = False

        # 4.2 Cuerpo / Segmentos (Snake Body)
        self.segments = []
        
        # Guarda la última posición libre de la cola antes de avanzar (t-1)
        self.last_tail_pos = (0, 0)

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
        """
        Crea un nuevo segmento en la posición donde estaba la cola 
        antes de dar el último paso, evitando que nazca sobre la cabeza.
        """
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("#27ae60")  # Verde cuerpo
        new_segment.penup()
        new_segment.goto(self.last_tail_pos[0], self.last_tail_pos[1])
        self.segments.append(new_segment)

    # 5.1 Algoritmo de Movimiento Inverso
    def move(self):
        # Guardar la posición de la cola (o cabeza si no hay cuerpo) en t-1
        if self.segments:
            self.last_tail_pos = (self.segments[-1].xcor(), self.segments[-1].ycor())
        else:
            self.last_tail_pos = (self.head.xcor(), self.head.ycor())

        # 1. Propagar movimiento desde la cola (N-1) hasta el segmento 1
        for i in range(len(self.segments) - 1, 0, -1):
            prev_x = self.segments[i - 1].xcor()
            prev_y = self.segments[i - 1].ycor()
            self.segments[i].goto(prev_x, prev_y)

        # 2. Mover el primer segmento (índice 0) a la posición de la cabeza (t-1)
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

        # Liberar bloqueo de dirección tras completar el movimiento
        self.direction_locked = False

    def get_all_positions(self):
        """Devuelve un conjunto con las coordenadas (x, y) ocupadas por la serpiente."""
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
            seg.goto(1000, 1000)
            seg.hideturtle()
        self.segments.clear()
        self.last_tail_pos = (0, 0)


# =====================================================================
# 4.3 CLASE COMIDA (Food)
# =====================================================================
class Food(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.speed(0)
        self.shape("circle")
        self.color("#e74c3c")  # Círculo rojo
        self.penup()
        self.relocate(set())

    def relocate(self, occupied_positions):
        """Ubica la comida en la grilla [-280, 280] fuera del cuerpo de la serpiente."""
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
        self.screen = turtle.Screen()
        self.screen.title("Snake - Python Turtle")
        self.screen.bgcolor("#1e272e")
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        
        # 3.1 Desactivar auto-dibujado
        self.screen.tracer(0)

        # Instanciar entidades
        self.snake = Snake()
        self.food = Food()
        self.food.relocate(self.snake.get_all_positions())
        self.scoreboard = Scoreboard()

        self.delay = INITIAL_DELAY
        self.state = "RUNNING"

        self._setup_controls()

    def _setup_controls(self):
        self.screen.listen()
        self.screen.onkey(self.snake.go_up, "Up")
        self.screen.onkey(self.snake.go_down, "Down")
        self.screen.onkey(self.snake.go_left, "Left")
        self.screen.onkey(self.snake.go_right, "Right")
        self.screen.onkey(self.snake.go_up, "w")
        self.screen.onkey(self.snake.go_down, "s")
        self.screen.onkey(self.snake.go_left, "a")
        self.screen.onkey(self.snake.go_right, "d")
        self.screen.onkey(self.toggle_pause, "space")

    def toggle_pause(self):
        if self.state == "RUNNING":
            self.state = "PAUSED"
            self.scoreboard.update_display("PAUSADO")
        elif self.state == "PAUSED":
            self.state = "RUNNING"
            self.scoreboard.update_display()

    def trigger_game_over(self):
        """Reinicia la partida tras chocar con bordes o con el cuerpo."""
        self.snake.reset()
        self.scoreboard.reset_score()
        self.delay = INITIAL_DELAY
        self.food.relocate(self.snake.get_all_positions())

    # 6. Ciclo de Ejecución Principal
    def game_loop(self):
        try:
            if self.state == "RUNNING" and self.snake.direction != "stop":
                # 1. Mover segmentos y cabeza
                self.snake.move()

                # 2. ¿Colisión con Comida?
                if self.snake.head.distance(self.food) < GRID_SIZE:
                    self.snake.add_segment()
                    self.food.relocate(self.snake.get_all_positions())
                    self.scoreboard.increase_score()
                    self.delay = max(MIN_DELAY, self.delay - DELAY_REDUCTION)

                # 3. ¿Colisión con Bordes?
                head_x = self.snake.head.xcor()
                head_y = self.snake.head.ycor()
                if abs(head_x) > LIMIT_X or abs(head_y) > LIMIT_Y:
                    self.trigger_game_over()

                # 4. ¿Colisión con el Propio Cuerpo?
                else:
                    for segment in self.snake.segments:
                        if self.snake.head.distance(segment) < 10:
                            self.trigger_game_over()
                            break

            # 5. Actualizar pantalla
            self.screen.update()

            # 6. Programar siguiente iteración
            self.screen.ontimer(self.game_loop, self.delay)

        except (turtle.Terminator, Exception):
            pass

    def run(self):
        self.game_loop()
        self.screen.mainloop()


if __name__ == "__main__":
    try:
        game = GameEngine()
        game.run()
    except turtle.Terminator:
        pass