from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup


class QuizConfigScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.selected_difficulty = "Fácil"
        self.selected_amount = 10

        # ====================================================
        # MODOS ESPECIAIS
        # ====================================================

        self.lives_enabled = False
        self.max_lives = 3

        self.timer_enabled = False
        self.timer_seconds = 30

        # ====================================================
        # LAYOUT PRINCIPAL
        # ====================================================

        main_layout = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=10
        )

        # ====================================================
        # TÍTULO
        # ====================================================

        self.title = Label(
            text="⚙️ CONFIGURAR QUIZ",
            font_size="34sp",
            bold=True,
            size_hint=(1, 0.10)
        )

        main_layout.add_widget(self.title)

        # ====================================================
        # MODO / CATEGORIA
        # ====================================================

        self.category_label = Label(
            text="🌎 QUIZ GERAL",
            font_size="21sp",
            bold=True,
            size_hint=(1, 0.09)
        )

        main_layout.add_widget(self.category_label)

        # ====================================================
        # DIFICULDADE
        # ====================================================

        difficulty_label = Label(
            text="🎯 DIFICULDADE",
            font_size="20sp",
            bold=True,
            size_hint=(1, 0.06)
        )

        main_layout.add_widget(difficulty_label)

        difficulty_layout = BoxLayout(
            spacing=8,
            size_hint=(1, 0.09)
        )

        for difficulty in [
            "Fácil",
            "Médio",
            "Difícil"
        ]:

            button = Button(
                text=difficulty,
                font_size="17sp"
            )

            button.bind(
                on_press=lambda instance,
                value=difficulty:
                self.select_difficulty(value)
            )

            difficulty_layout.add_widget(button)

        main_layout.add_widget(difficulty_layout)

        # ====================================================
        # QUANTIDADE
        # ====================================================

        amount_label = Label(
            text="🔢 NÚMERO DE PERGUNTAS",
            font_size="20sp",
            bold=True,
            size_hint=(1, 0.06)
        )

        main_layout.add_widget(amount_label)

        amount_layout = BoxLayout(
            spacing=8,
            size_hint=(1, 0.09)
        )

        self.amount_input = TextInput(
            text="10",
            font_size="20sp",
            multiline=False,
            input_filter="int",
            halign="center",
            size_hint=(0.7, 1)
        )

        amount_layout.add_widget(self.amount_input)

        all_button = Button(
            text="TODAS",
            font_size="17sp",
            size_hint=(0.3, 1)
        )

        all_button.bind(
            on_press=self.select_all
        )

        amount_layout.add_widget(all_button)

        main_layout.add_widget(amount_layout)

        # ====================================================
        # MODO DE JOGO
        # ====================================================

        mode_label = Label(
            text="🎮 MODO DE JOGO",
            font_size="20sp",
            bold=True,
            size_hint=(1, 0.06)
        )

        main_layout.add_widget(mode_label)

        mode_layout = BoxLayout(
            spacing=8,
            size_hint=(1, 0.10)
        )

        normal_button = Button(
            text="NORMAL\nSem vidas • Sem tempo",
            font_size="14sp"
        )

        lives_button = Button(
            text="❤️ VIDAS\n3 tentativas",
            font_size="14sp"
        )

        timer_button = Button(
            text="⏱️ CRONÓMETRO\nTempo por pergunta",
            font_size="14sp"
        )

        lives_timer_button = Button(
            text="❤️ + ⏱️\nVidas + Tempo",
            font_size="14sp"
        )

        normal_button.bind(
            on_press=lambda instance:
            self.select_game_mode(
                lives=False,
                timer=False
            )
        )

        lives_button.bind(
            on_press=lambda instance:
            self.select_game_mode(
                lives=True,
                timer=False
            )
        )

        timer_button.bind(
            on_press=lambda instance:
            self.select_game_mode(
                lives=False,
                timer=True
            )
        )

        lives_timer_button.bind(
            on_press=lambda instance:
            self.select_game_mode(
                lives=True,
                timer=True
            )
        )

        mode_layout.add_widget(normal_button)
        mode_layout.add_widget(lives_button)
        mode_layout.add_widget(timer_button)
        mode_layout.add_widget(lives_timer_button)

        main_layout.add_widget(mode_layout)

        # ====================================================
        # TEMPO
        # ====================================================

        timer_layout = BoxLayout(
            spacing=8,
            size_hint=(1, 0.07)
        )

        timer_label = Label(
            text="⏱️ TEMPO:",
            font_size="17sp",
            bold=True,
            size_hint=(0.25, 1)
        )

        timer_layout.add_widget(timer_label)

        self.timer_button = Button(
            text="30 segundos",
            font_size="16sp",
            size_hint=(0.75, 1)
        )

        self.timer_button.bind(
            on_press=self.cycle_timer
        )

        timer_layout.add_widget(self.timer_button)

        main_layout.add_widget(timer_layout)

        # ====================================================
        # STATUS DO MODO
        # ====================================================

        self.mode_status_label = Label(
            text="🎮 NORMAL • Sem vidas • Sem cronómetro",
            font_size="15sp",
            bold=True,
            size_hint=(1, 0.06)
        )

        main_layout.add_widget(self.mode_status_label)

        # ====================================================
        # MENSAGEM
        # ====================================================

        self.message_label = Label(
            text="",
            font_size="14sp",
            size_hint=(1, 0.06)
        )

        main_layout.add_widget(self.message_label)

        # ====================================================
        # INICIAR
        # ====================================================

        start_button = Button(
            text="▶️ INICIAR QUIZ",
            font_size="22sp",
            bold=True,
            size_hint=(1, 0.10)
        )

        start_button.bind(
            on_press=self.start_quiz
        )

        main_layout.add_widget(start_button)

        # ====================================================
        # VOLTAR
        # ====================================================

        back_button = Button(
            text="VOLTAR",
            font_size="16sp",
            size_hint=(1, 0.07)
        )

        back_button.bind(
            on_press=self.back
        )

        main_layout.add_widget(back_button)

        self.add_widget(main_layout)

    # ========================================================
    # AO ENTRAR NA TELA
    # ========================================================

    def on_enter(self):

        category = getattr(
            self.manager,
            "selected_category",
            None
        )

        if category:

            self.category_label.text = (
                f"📚 {category}"
            )

        else:

            self.category_label.text = (
                "🌎 QUIZ GERAL\n"
                "Perguntas de todas as categorias"
            )

        self.message_label.text = ""

        self.update_mode_status()

    # ========================================================
    # DIFICULDADE
    # ========================================================

    def select_difficulty(self, difficulty):

        self.selected_difficulty = difficulty

        self.selected_amount = (
            self.selected_amount
            if self.selected_amount == "Todas"
            else self.selected_amount
        )

        self.message_label.text = (
            f"Dificuldade selecionada: {difficulty}"
        )

        print(
            f"DIFICULDADE: {difficulty}"
        )

    # ========================================================
    # TODAS AS PERGUNTAS
    # ========================================================

    def select_all(self, instance):

        self.selected_amount = "Todas"

        self.amount_input.text = ""

        self.message_label.text = (
            "Serão utilizadas todas as perguntas disponíveis."
        )

        print(
            "QUANTIDADE: Todas"
        )

    # ========================================================
    # SELECIONAR MODO
    # ========================================================

    def select_game_mode(self, lives, timer):

        self.lives_enabled = lives
        self.timer_enabled = timer

        self.update_mode_status()

        if timer:

            self.message_label.text = (
                f"⏱️ Cronómetro: {self.timer_seconds} segundos por pergunta."
            )

        elif lives:

            self.message_label.text = (
                "❤️ Terás 3 vidas durante o quiz."
            )

        else:

            self.message_label.text = (
                "Modo normal selecionado."
            )

    # ========================================================
    # CICLAR TEMPO
    # ========================================================

    def cycle_timer(self, instance):

        options = [10, 20, 30, 60]

        try:
            current_index = options.index(
                self.timer_seconds
            )
        except ValueError:
            current_index = 2

        next_index = (
            current_index + 1
        ) % len(options)

        self.timer_seconds = (
            options[next_index]
        )

        self.timer_button.text = (
            f"{self.timer_seconds} segundos"
        )

        self.message_label.text = (
            f"Tempo definido: "
            f"{self.timer_seconds} segundos por pergunta."
        )

        print(
            f"TEMPO: {self.timer_seconds}s"
        )

    # ========================================================
    # ATUALIZAR STATUS
    # ========================================================

    def update_mode_status(self):

        if self.lives_enabled and self.timer_enabled:

            self.mode_status_label.text = (
                f"❤️ 3 VIDAS • ⏱️ {self.timer_seconds}s POR PERGUNTA"
            )

        elif self.lives_enabled:

            self.mode_status_label.text = (
                "❤️ 3 VIDAS • SEM CRONÓMETRO"
            )

        elif self.timer_enabled:

            self.mode_status_label.text = (
                f"⏱️ {self.timer_seconds}s POR PERGUNTA • SEM VIDAS"
            )

        else:

            self.mode_status_label.text = (
                "🎮 NORMAL • SEM VIDAS • SEM CRONÓMETRO"
            )

    # ========================================================
    # INICIAR QUIZ
    # ========================================================

    def start_quiz(self, instance):

        # ====================================================
        # VALIDAR QUANTIDADE
        # ====================================================

        if self.selected_amount == "Todas":

            amount = "Todas"

        else:

            amount_text = (
                self.amount_input.text.strip()
            )

            if not amount_text:

                self.message_label.text = (
                    "⚠️ Digita o número de perguntas."
                )

                return

            try:

                amount = int(amount_text)

            except ValueError:

                self.message_label.text = (
                    "⚠️ Digita apenas números."
                )

                return

            if amount <= 0:

                self.message_label.text = (
                    "⚠️ A quantidade deve ser maior que 0."
                )

                return

            self.selected_amount = amount

        # ====================================================
        # GUARDAR CONFIGURAÇÃO NO MANAGER
        # ====================================================

        self.manager.selected_amount = amount

        self.manager.selected_difficulty = (
            self.selected_difficulty
        )

        self.manager.quiz_lives_enabled = (
            self.lives_enabled
        )

        self.manager.quiz_max_lives = (
            self.max_lives
        )

        self.manager.quiz_timer_enabled = (
            self.timer_enabled
        )

        self.manager.quiz_timer_seconds = (
            self.timer_seconds
        )

        print(
            f"DIFICULDADE: "
            f"{self.selected_difficulty}"
        )

        print(
            f"QUANTIDADE: "
            f"{amount}"
        )

        print(
            f"VIDAS: "
            f"{self.lives_enabled}"
        )

        print(
            f"CRONÓMETRO: "
            f"{self.timer_enabled}"
        )

        print(
            f"TEMPO: "
            f"{self.timer_seconds}s"
        )

        self.manager.current = "quiz"

    # ========================================================
    # VOLTAR
    # ========================================================

    def back(self, instance):

        if getattr(
            self.manager,
            "selected_category",
            None
        ) is None:

            self.manager.current = "main"

        else:

            self.manager.current = "categories"