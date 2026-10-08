import json
import random
import os
from datetime import date

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.clock import Clock


from systems.achievements import (
    check_achievements,
    get_achievement
)

from systems.rewards import (
    get_level_reward
)


class QuizScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ====================================================
        # CAMINHO PRINCIPAL DO PROJETO
        # ====================================================

        self.base_dir = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        self.questions_file = os.path.join(
            self.base_dir,
            "data",
            "questions.json"
        )

        self.progress_file = os.path.join(
            self.base_dir,
            "data",
            "progress.json"
        )

        # ====================================================
        # VARIÁVEIS DO QUIZ
        # ====================================================

        self.questions = []
        self.current_question = 0
        self.score = 0
        self.answered = False

        self.quiz_mode = "Geral"

        self.correct_answer_index = None

        # ====================================================
        # SISTEMA DE PONTUAÇÃO
        # ====================================================

        self.quiz_points = 0
        self.question_points = 0
        self.base_points = 75
        self.max_speed_bonus = 25
        self.speed_bonus = 0
        self.total_speed_bonus = 0

        # ====================================================
        # MODOS OPCIONAIS — VIDAS E CRONÓMETRO
        # ====================================================

        self.lives_enabled = False
        self.max_lives = 3
        self.lives = 3

        self.timer_enabled = False
        self.timer_seconds = 30
        self.timer_remaining = 0
        self.timer_event = None

        # ====================================================
        # XP DO QUIZ
        # ====================================================

        self.quiz_xp = 0

        # ====================================================
        # CONTROLE DOS BÓNUS DE XP
        # ====================================================

        self.completion_bonus = 0
        self.performance_bonus = 0
        self.perfect_bonus = 0
        self.streak_bonus = 0
        self.base_xp = 0

        # ====================================================
        # CONTROLE DO LEVEL UP
        # ====================================================

        self.level_up = None

        # ====================================================
        # CONTROLE DAS RECOMPENSAS
        # ====================================================

        self.new_rewards = []

        # ====================================================
        # CONTROLE DO POPUP DE CONQUISTAS
        # ====================================================

        self.achievement_popup = None
        self.achievement_queue = []

        # ====================================================
        # CARREGAR PERGUNTAS
        # ====================================================

        self.load_questions()

        # ====================================================
        # LAYOUT PRINCIPAL
        # ====================================================

        self.layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=8
        )

        # ====================================================
        # BARRA SUPERIOR
        # ====================================================

        self.top_bar = BoxLayout(
            orientation="horizontal",
            size_hint=(1, 0.07),
            spacing=10
        )

        self.top_spacer = Label(
            text="",
            size_hint=(1, 1)
        )

        self.top_bar.add_widget(
            self.top_spacer
        )

        # ====================================================
        # BOTÃO OPÇÕES
        # ====================================================

        self.options_button = Button(
            text="⚙",
            font_size="22sp",
            bold=True,
            size_hint=(None, 1),
            width=55
        )

        self.options_button.bind(
            on_press=self.show_quiz_options
        )

        self.top_bar.add_widget(
            self.options_button
        )

        # ====================================================
        # BOTÃO X
        # ====================================================

        self.exit_button = Button(
            text="✕",
            font_size="22sp",
            bold=True,
            size_hint=(None, 1),
            width=55
        )

        self.exit_button.bind(
            on_press=self.exit_quiz
        )

        self.top_bar.add_widget(
            self.exit_button
        )

        self.layout.add_widget(
            self.top_bar
        )

        # ====================================================
        # CONTADOR
        # ====================================================

        self.counter_label = Label(
            text="",
            font_size="20sp",
            size_hint=(1, 0.05)
        )

        self.layout.add_widget(
            self.counter_label
        )

        # ====================================================
        # BARRA DE PROGRESSO
        # ====================================================

        self.progress_bar = ProgressBar(
            max=1,
            value=0,
            size_hint=(1, 0.02)
        )

        self.layout.add_widget(
            self.progress_bar
        )

        # ====================================================
        # MODO / CATEGORIA
        # ====================================================

        self.mode_label = Label(
            text="🌎 QUIZ GERAL",
            font_size="17sp",
            size_hint=(1, 0.04)
        )

        self.layout.add_widget(
            self.mode_label
        )

        # ====================================================
        # DIFICULDADE
        # ====================================================

        self.difficulty_label = Label(
            text="🎯 DIFICULDADE: Todas",
            font_size="16sp",
            size_hint=(1, 0.03)
        )

        self.layout.add_widget(
            self.difficulty_label
        )

        # ====================================================
        # STATUS DOS MODOS
        # ====================================================

        self.special_modes_label = Label(
            text="❤️ VIDAS: OFF   |   ⏱️ CRONÓMETRO: OFF",
            font_size="14sp",
            size_hint=(1, 0.03)
        )

        self.layout.add_widget(
            self.special_modes_label
        )

        # ====================================================
        # PONTUAÇÃO
        # ====================================================

        self.points_label = Label(
            text="🏆 PONTOS: 0",
            font_size="16sp",
            bold=True,
            size_hint=(1, 0.035)
        )

        self.layout.add_widget(
            self.points_label
        )

        # ====================================================
        # PERGUNTA
        # ====================================================

        self.question_label = Label(
            text="",
            font_size="25sp",
            bold=True,
            halign="center",
            valign="middle",
            size_hint=(1, 0.17)
        )

        self.question_label.bind(
            size=self.update_text_size
        )

        self.layout.add_widget(
            self.question_label
        )

        # ====================================================
        # BOTÕES DAS RESPOSTAS
        # ====================================================

        self.answer_buttons = []

        for i in range(4):

            button = Button(
                text="",
                font_size="15sp",
                size_hint=(1, 0.075)
            )

            button.halign = "center"
            button.valign = "middle"
            button.bind(size=self.update_text_size)

            button.bind(
                on_press=lambda instance, index=i:
                self.check_answer(index)
            )

            self.answer_buttons.append(
                button
            )

            self.layout.add_widget(
                button
            )

        # ====================================================
        # EXPLICAÇÃO
        # ====================================================

        self.explanation_label = Label(
            text="",
            font_size="11sp",
            halign="center",
            valign="middle",
            size_hint=(1, 0.075)
        )

        self.explanation_label.bind(
            size=self.update_text_size
        )

        self.layout.add_widget(
            self.explanation_label
        )

        self.explanation_spacer = Widget(
            size_hint=(1, 0.025)
        )

        self.layout.add_widget(
            self.explanation_spacer
        )

        # ====================================================
        # BOTÃO PRINCIPAL
        # ====================================================

        self.next_button = Button(
            text="PRÓXIMA PERGUNTA",
            font_size="13sp",
            size_hint=(1, 0.055),
            disabled=True
        )

        self.layout.add_widget(
            self.next_button
        )

        self.add_widget(
            self.layout
        )

    # ========================================================
    # SAIR DO QUIZ
    # ========================================================

    def exit_quiz(self, instance):

        print(
            "🚪 QUIZ ABANDONADO — "
            "REGRESSANDO AO MENU PRINCIPAL."
        )

        if self.achievement_popup:
            self.achievement_popup.dismiss()
            self.achievement_popup = None

        self.stop_timer()

        self.achievement_queue = []
        self.new_rewards = []
        self.level_up = None

        self.manager.new_achievements = []
        self.manager.new_rewards = []
        self.manager.level_up = None

        self.manager.selected_category = None
        self.manager.selected_difficulty = None
        self.manager.selected_amount = "Todas"
        self.manager.quiz_lives_enabled = False
        self.manager.quiz_timer_enabled = False

        self.manager.current = "main"

    # ========================================================
    # DEFINIR AÇÃO DO BOTÃO
    # ========================================================

    def set_next_button_action(self, callback):

        self.next_button.unbind(
            on_press=self.next_question
        )

        self.next_button.unbind(
            on_press=self.back_to_categories
        )

        self.next_button.unbind(
            on_press=self.back_to_menu
        )

        self.next_button.bind(
            on_press=callback
        )

    # ========================================================
    # CARREGAR PERGUNTAS
    # ========================================================

    def load_questions(self):

        try:

            with open(
                self.questions_file,
                "r",
                encoding="utf-8"
            ) as file:

                self.questions = json.load(file)

            print(
                f"✅ {len(self.questions)} perguntas carregadas."
            )

        except Exception as error:

            print(
                "❌ Erro ao carregar perguntas:",
                error
            )

            self.questions = []

    # ========================================================
    # INICIAR QUIZ
    # ========================================================

    def on_enter(self):

        self.current_question = 0
        self.score = 0
        self.quiz_points = 0
        self.question_points = 0
        self.speed_bonus = 0
        self.answered = False
        self.correct_answer_index = None

        self.quiz_xp = 0

        self.completion_bonus = 0
        self.performance_bonus = 0
        self.perfect_bonus = 0
        self.streak_bonus = 0
        self.base_xp = 0

        self.stop_timer()

        self.lives_enabled = getattr(
            self.manager,
            "quiz_lives_enabled",
            False
        )

        self.max_lives = getattr(
            self.manager,
            "quiz_max_lives",
            3
        )

        self.timer_enabled = getattr(
            self.manager,
            "quiz_timer_enabled",
            False
        )

        self.timer_seconds = getattr(
            self.manager,
            "quiz_timer_seconds",
            30
        )

        self.lives = self.max_lives

        self.update_special_modes_label()
        self.update_points_label()

        self.level_up = None
        self.manager.level_up = None

        self.new_rewards = []
        self.manager.new_rewards = []

        self.manager.new_achievements = []
        self.achievement_queue = []

        self.load_questions()

        selected_category = getattr(
            self.manager,
            "selected_category",
            None
        )

        selected_difficulty = getattr(
            self.manager,
            "selected_difficulty",
            None
        )

        selected_amount = getattr(
            self.manager,
            "selected_amount",
            "Todas"
        )

        if selected_category:

            self.quiz_mode = selected_category

            self.mode_label.text = (
                f"📚 {selected_category}"
            )

        else:

            self.quiz_mode = "Geral"

            self.mode_label.text = (
                "🌎 QUIZ GERAL"
            )

        if selected_difficulty:
            self.difficulty_label.text = (
                f"🎯 DIFICULDADE: {selected_difficulty}"
            )
        else:
            self.difficulty_label.text = (
                "🎯 DIFICULDADE: Todas"
            )

        if selected_category:

            category_name = selected_category.split(
                " ",
                1
            )[-1].strip()

            self.questions = [
                question
                for question in self.questions
                if question.get(
                    "category",
                    ""
                ).upper()
                == category_name.upper()
            ]

        if selected_difficulty:

            self.questions = [
                question
                for question in self.questions
                if question.get(
                    "difficulty",
                    ""
                ).upper()
                == selected_difficulty.upper()
            ]

        random.shuffle(
            self.questions
        )

        if selected_amount != "Todas":

            try:

                amount = int(
                    selected_amount
                )

                if amount > 0:

                    self.questions = (
                        self.questions[:amount]
                    )

            except (
                ValueError,
                TypeError
            ):

                print(
                    "⚠️ Quantidade inválida. "
                    "Serão usadas todas as perguntas disponíveis."
                )

        if not self.questions:

            self.show_no_questions()
            return

        print(
            f"QUIZ INICIADO | "
            f"Modo: {self.quiz_mode} | "
            f"Dificuldade: {selected_difficulty} | "
            f"Perguntas: {len(self.questions)}"
        )

        self.show_question()

    # ========================================================
    # SEM PERGUNTAS
    # ========================================================

    def show_no_questions(self):

        self.counter_label.text = "SEM PERGUNTAS"

        self.progress_bar.max = 1
        self.progress_bar.value = 0

        self.points_label.text = "🏆 PONTOS: 0"

        self.question_label.text = (
            "😕 Ainda não existem perguntas "
            "para esta combinação."
        )

        self.explanation_label.text = (
            "Tenta outra dificuldade, "
            "categoria ou quantidade."
        )

        for button in self.answer_buttons:

            button.text = ""
            button.disabled = True

            button.background_color = (
                1, 1, 1, 1
            )

            button.color = (
                1, 1, 1, 1
            )

        self.next_button.text = "VOLTAR"
        self.next_button.disabled = False

        if self.quiz_mode == "Geral":

            self.set_next_button_action(
                self.back_to_menu
            )

        else:

            self.set_next_button_action(
                self.back_to_categories
            )

    # ========================================================
    # MOSTRAR PERGUNTA
    # ========================================================

    def show_question(self):

        self.answered = False
        self.question_points = 0
        self.speed_bonus = 0

        self.next_button.text = (
            "PRÓXIMA PERGUNTA"
        )

        self.next_button.disabled = True

        self.set_next_button_action(
            self.next_question
        )

        self.explanation_label.text = ""

        question = self.questions[
            self.current_question
        ]

        original_options = question["options"]

        correct_index_original = question["answer"]

        correct_answer = (
            original_options[
                correct_index_original
            ]
        )

        shuffled_options = list(
            original_options
        )

        random.shuffle(
            shuffled_options
        )

        self.correct_answer_index = (
            shuffled_options.index(
                correct_answer
            )
        )

        total_questions = len(self.questions)
        question_number = self.current_question + 1

        progress_percent = (
            question_number / total_questions * 100
            if total_questions > 0
            else 0
        )

        self.counter_label.text = (
            f"PERGUNTA {question_number}/{total_questions}"
            f"   •   {progress_percent:.0f}%"
        )

        if total_questions > 0:
            self.progress_bar.max = total_questions
            self.progress_bar.value = question_number

        self.question_label.text = (
            question["question"]
        )

        for i, button in enumerate(
            self.answer_buttons
        ):

            button.text = (
                f"{chr(65 + i)}) "
                f"{shuffled_options[i]}"
            )

            button.disabled = False

            button.background_color = (
                1, 1, 1, 1
            )

            button.color = (
                1, 1, 1, 1
            )

        self.start_timer()

    # ========================================================
    # VERIFICAR RESPOSTA
    # ========================================================

    def check_answer(self, selected_index):

        if self.answered:
            return

        self.answered = True

        self.stop_timer()

        question = self.questions[
            self.current_question
        ]

        for button in self.answer_buttons:
            button.disabled = True

        # ====================================================
        # RESPOSTA CORRETA
        # ====================================================

        if selected_index == self.correct_answer_index:

            self.score += 1

            # ================================================
            # PONTUAÇÃO BASE
            # ================================================

            self.question_points = self.base_points

            # ================================================
            # BÓNUS DE VELOCIDADE
            # ================================================

            if self.timer_enabled and self.timer_seconds > 0:

                self.speed_bonus = int(
                    (
                        self.timer_remaining
                        / self.timer_seconds
                    )
                    * self.max_speed_bonus
                )

                self.speed_bonus = max(
                    0,
                    min(
                        self.max_speed_bonus,
                        self.speed_bonus
                    )
                )

            else:

                self.speed_bonus = 0

            self.question_points += (
                self.speed_bonus
            )

            self.total_speed_bonus += self.speed_bonus

            self.quiz_points += (
                self.question_points
            )

            self.update_points_label()

            # ================================================
            # XP
            # ================================================

            difficulty = question.get(
                "difficulty",
                "Fácil"
            )

            if difficulty == "Fácil":
                xp_earned = 10
            elif difficulty == "Médio":
                xp_earned = 20
            elif difficulty == "Difícil":
                xp_earned = 35
            else:
                xp_earned = 10

            self.quiz_xp += xp_earned
            self.base_xp += xp_earned

            self.answer_buttons[
                selected_index
            ].background_color = (
                0, 1, 0, 1
            )

            if self.speed_bonus > 0:

                self.explanation_label.text = (
                    f"✅ CORRETO! "
                    f"+{self.question_points} PONTOS "
                    f"(+{self.speed_bonus} velocidade)\n"
                    f"+{xp_earned} XP\n"
                    + question.get(
                        "explanation",
                        "Muito bem!"
                    )
                )

            else:

                self.explanation_label.text = (
                    f"✅ CORRETO! "
                    f"+{self.question_points} PONTOS\n"
                    f"+{xp_earned} XP\n"
                    + question.get(
                        "explanation",
                        "Muito bem!"
                    )
                )

            print(
                f"✅ RESPOSTA CORRETA | "
                f"+{self.question_points} PONTOS | "
                f"+{xp_earned} XP"
            )

        # ====================================================
        # RESPOSTA INCORRETA
        # ====================================================

        else:

            self.question_points = 0
            self.speed_bonus = 0

            self.answer_buttons[
                selected_index
            ].background_color = (
                1, 0, 0, 1
            )

            self.answer_buttons[
                self.correct_answer_index
            ].background_color = (
                0, 1, 0, 1
            )

            correct_button = (
                self.answer_buttons[
                    self.correct_answer_index
                ]
            )

            correct_text = (
                correct_button.text
            )

            self.explanation_label.text = (
                "❌ INCORRETO! +0 PONTOS\n"
                f"Resposta correta: {correct_text}\n"
                f"{question.get(
                    'explanation',
                    'Sem explicação disponível.'
                )}"
            )

            print(
                "❌ RESPOSTA INCORRETA | +0 PONTOS | +0 XP"
            )

            if self.lives_enabled:

                self.lives -= 1
                self.update_special_modes_label()

                print(
                    f"❤️ VIDA PERDIDA | "
                    f"Restam: {self.lives}"
                )

                if self.lives <= 0:

                    self.next_button.disabled = True

                    self.explanation_label.text += (
                        "\n💀 FICASTE SEM VIDAS! "
                        "O quiz terminou."
                    )

                    Clock.schedule_once(
                        lambda dt: self.finish_quiz(),
                        1.5
                    )

                    return

        self.next_button.disabled = False

    # ========================================================
    # PRÓXIMA PERGUNTA
    # ========================================================

    def next_question(self, instance):

        self.stop_timer()

        self.current_question += 1

        if self.current_question >= len(
            self.questions
        ):

            self.finish_quiz()

        else:

            self.show_question()

    # ========================================================
    # ATUALIZAR PONTUAÇÃO
    # ========================================================

    def update_points_label(self):

        self.points_label.text = (
            f"🏆 PONTOS: {self.quiz_points}"
        )

    # ========================================================
    # ATUALIZAR STATUS DOS MODOS
    # ========================================================

    def update_special_modes_label(self):

        if self.lives_enabled:
            lives_text = (
                f"❤️ VIDAS: {self.lives}/{self.max_lives}"
            )
        else:
            lives_text = "❤️ VIDAS: OFF"

        if self.timer_enabled:
            timer_text = (
                f"⏱️ CRONÓMETRO: {self.timer_seconds}s"
            )
        else:
            timer_text = "⏱️ CRONÓMETRO: OFF"

        self.special_modes_label.text = (
            f"{lives_text}   |   {timer_text}"
        )

    # ========================================================
    # CRONÓMETRO
    # ========================================================

    def start_timer(self):

        self.stop_timer()

        if not self.timer_enabled:
            self.timer_remaining = 0
            return

        self.timer_remaining = self.timer_seconds
        self.update_timer_label()

        self.timer_event = Clock.schedule_interval(
            self.update_timer,
            1
        )

    def stop_timer(self):

        if self.timer_event is not None:
            self.timer_event.cancel()
            self.timer_event = None

    def update_timer(self, dt):

        if self.answered:
            self.stop_timer()
            return

        self.timer_remaining -= 1
        self.update_timer_label()

        if self.timer_remaining <= 0:

            self.timer_remaining = 0
            self.stop_timer()

            self.handle_timeout()

    def update_timer_label(self):

        if not self.timer_enabled:
            self.update_special_modes_label()
            return

        if self.lives_enabled:
            lives_text = (
                f"❤️ {self.lives}/{self.max_lives}"
            )
        else:
            lives_text = "❤️ OFF"

        self.special_modes_label.text = (
            f"{lives_text}   |   "
            f"⏱️ TEMPO: {self.timer_remaining}s"
        )

    def handle_timeout(self):

        if self.answered:
            return

        self.answered = True

        question = self.questions[
            self.current_question
        ]

        for button in self.answer_buttons:
            button.disabled = True

        self.question_points = 0
        self.speed_bonus = 0

        self.answer_buttons[
            self.correct_answer_index
        ].background_color = (
            0, 1, 0, 1
        )

        correct_text = self.answer_buttons[
            self.correct_answer_index
        ].text

        self.explanation_label.text = (
            "⏰ TEMPO ESGOTADO! +0 PONTOS\n\n"
            f"Resposta correta: {correct_text}\n\n"
            f"{question.get(
                'explanation',
                'Sem explicação disponível.'
            )}"
        )

        if self.lives_enabled:

            self.lives -= 1
            self.update_special_modes_label()

            if self.lives <= 0:

                self.next_button.disabled = True

                self.explanation_label.text += (
                    "\n\n💀 FICASTE SEM VIDAS! "
                    "O quiz terminou."
                )

                Clock.schedule_once(
                    lambda dt: self.finish_quiz(),
                    1.5
                )

                return

        self.next_button.disabled = False

    # ========================================================
    # OPÇÕES DOS MODOS ESPECIAIS
    # ========================================================

    def show_quiz_options(self, instance):

        content = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=12
        )

        title = Label(
            text="⚙️ OPÇÕES DO QUIZ",
            font_size="24sp",
            bold=True,
            size_hint_y=None,
            height=50
        )

        content.add_widget(title)

        lives_button = Button(
            text=(
                "❤️ VIDAS: 3"
                if self.lives_enabled
                else "❤️ VIDAS: DESLIGADO"
            ),
            size_hint_y=None,
            height=55
        )

        def toggle_lives(btn):

            self.lives_enabled = not self.lives_enabled

            if self.lives_enabled:
                self.lives = self.max_lives
                btn.text = f"❤️ VIDAS: {self.max_lives}"
            else:
                btn.text = "❤️ VIDAS: DESLIGADO"

            self.update_special_modes_label()

        lives_button.bind(
            on_press=toggle_lives
        )

        content.add_widget(
            lives_button
        )

        timer_button = Button(
            text=(
                f"⏱️ CRONÓMETRO: {self.timer_seconds}s"
                if self.timer_enabled
                else "⏱️ CRONÓMETRO: DESLIGADO"
            ),
            size_hint_y=None,
            height=55
        )

        def toggle_timer(btn):

            self.timer_enabled = not self.timer_enabled

            if self.timer_enabled:
                btn.text = (
                    f"⏱️ CRONÓMETRO: "
                    f"{self.timer_seconds}s"
                )
            else:
                btn.text = (
                    "⏱️ CRONÓMETRO: DESLIGADO"
                )

            self.update_special_modes_label()

        timer_button.bind(
            on_press=toggle_timer
        )

        content.add_widget(
            timer_button
        )

        time_button = Button(
            text=(
                f"⏱️ TEMPO POR PERGUNTA: "
                f"{self.timer_seconds}s"
            ),
            size_hint_y=None,
            height=55
        )

        def cycle_time(btn):

            options = [10, 20, 30, 60]

            try:
                index = options.index(
                    self.timer_seconds
                )
            except ValueError:
                index = 2

            self.timer_seconds = options[
                (index + 1) % len(options)
            ]

            btn.text = (
                f"⏱️ TEMPO POR PERGUNTA: "
                f"{self.timer_seconds}s"
            )

            if self.timer_enabled:
                self.start_timer()
            else:
                self.update_special_modes_label()

        time_button.bind(
            on_press=cycle_time
        )

        content.add_widget(
            time_button
        )

        info = Label(
            text=(
                "As vidas e o cronómetro são opcionais.\n"
                "Erros consomem 1 vida quando o modo está ativo.\n"
                "O cronómetro reinicia a cada pergunta."
            ),
            halign="center",
            valign="middle"
        )

        info.bind(
            size=self.update_text_size
        )

        content.add_widget(
            info
        )

        close_button = Button(
            text="APLICAR E FECHAR",
            size_hint_y=None,
            height=55
        )

        popup = Popup(
            title="",
            content=content,
            size_hint=(0.85, 0.75),
            auto_dismiss=False
        )

        def close_popup(btn):

            self.update_special_modes_label()
            popup.dismiss()

            if self.timer_enabled and not self.answered:
                self.start_timer()

        close_button.bind(
            on_press=close_popup
        )

        content.add_widget(
            close_button
        )

        popup.open()

    # ========================================================
    # CALCULAR NÍVEL
    # ========================================================

    def calculate_level(self, xp):

        levels = [
            (10000, 8, "👑 Lenda do Petróleo"),
            (5000, 7, "🏆 Mestre do Petróleo"),
            (2000, 6, "👷 Engenheiro"),
            (1000, 5, "🛠️ Especialista"),
            (500, 4, "🧭 Explorador"),
            (250, 3, "⚙️ Técnico"),
            (100, 2, "🔧 Aprendiz"),
            (0, 1, "🛢️ Iniciante")
        ]

        for required_xp, level, title in levels:

            if xp >= required_xp:
                return level, title

        return 1, "🛢️ Iniciante"

    # ========================================================
    # FINALIZAR QUIZ
    # ========================================================

    def finish_quiz(self):

        self.stop_timer()

        total_questions = len(
            self.questions
        )

        print(
            f"QUIZ TERMINADO! "
            f"Pontuação: "
            f"{self.score}/"
            f"{total_questions} | "
            f"Pontos: {self.quiz_points}"
        )

        if total_questions > 0:

            percentage = (
                self.score / total_questions
            ) * 100

        else:

            percentage = 0

        # ====================================================
        # BÓNUS DE CONCLUSÃO
        # ====================================================

        self.completion_bonus = 10

        self.quiz_xp += self.completion_bonus

        print(
            f"🎁 BÓNUS DE CONCLUSÃO: "
            f"+{self.completion_bonus} XP"
        )

        # ====================================================
        # BÓNUS DE DESEMPENHO
        # ====================================================

        self.performance_bonus = 0

        if percentage >= 90:
            self.performance_bonus = 50

        elif percentage >= 70:
            self.performance_bonus = 25

        self.quiz_xp += self.performance_bonus

        if self.performance_bonus > 0:

            print(
                f"🔥 BÓNUS DE DESEMPENHO: "
                f"+{self.performance_bonus} XP"
            )

        # ====================================================
        # BÓNUS DE QUIZ PERFEITO
        # ====================================================

        self.perfect_bonus = 0

        if percentage >= 100:

            self.perfect_bonus = 50

            self.quiz_xp += self.perfect_bonus

            print(
                f"🎯 BÓNUS DE QUIZ PERFEITO: "
                f"+{self.perfect_bonus} XP"
            )

        print(
            f"📊 XP BASE: "
            f"{self.base_xp}"
        )

        print(
            f"⭐ XP ANTES DO STREAK: "
            f"{self.quiz_xp}"
        )

        self.save_progress(
            total_questions,
            percentage
        )

        self.manager.quiz_score = (
            self.score
        )

        self.manager.quiz_total = (
            total_questions
        )

        self.manager.quiz_mode = (
            self.quiz_mode
        )

        self.manager.quiz_difficulty = getattr(
            self.manager,
            "selected_difficulty",
            "Todas"
        )

        self.manager.quiz_xp = (
            self.quiz_xp
        )

        # ====================================================
        # GUARDAR PONTUAÇÃO
        # ====================================================

        self.manager.quiz_points = (
            self.quiz_points
        )

        self.manager.quiz_points_breakdown = {
            "base_points": self.score * self.base_points,
            "speed_bonus": self.total_speed_bonus,
        }

        self.manager.quiz_max_points = (
            total_questions * self.base_points
            + (
                total_questions
                * self.max_speed_bonus
                if self.timer_enabled
                else 0
            )
        )

        self.manager.quiz_level_up = (
            self.level_up
        )

        self.manager.level_up = (
            self.level_up
        )

        self.manager.new_rewards = (
            self.new_rewards
        )

        self.manager.current = "results"

        if self.achievement_queue:
            self.show_next_achievement()

    # ========================================================
    # POPUP DE CONQUISTA
    # ========================================================

    def show_next_achievement(self):

        if not self.achievement_queue:
            return

        achievement_id = (
            self.achievement_queue.pop(0)
        )

        achievement = get_achievement(
            achievement_id
        )

        if not achievement:
            self.show_next_achievement()
            return

        icon = achievement.get(
            "icon",
            "🏆"
        )

        name = achievement.get(
            "name",
            "Conquista"
        )

        description = achievement.get(
            "description",
            ""
        )

        content = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        title = Label(
            text="🏆 CONQUISTA DESBLOQUEADA!",
            font_size="23sp",
            bold=True,
            size_hint=(1, 0.25)
        )

        content.add_widget(title)

        achievement_label = Label(
            text=f"{icon} {name}",
            font_size="28sp",
            bold=True,
            halign="center",
            valign="middle",
            size_hint=(1, 0.30)
        )

        achievement_label.bind(
            size=self.update_text_size
        )

        content.add_widget(
            achievement_label
        )

        description_label = Label(
            text=description,
            font_size="17sp",
            halign="center",
            valign="middle",
            size_hint=(1, 0.25)
        )

        description_label.bind(
            size=self.update_text_size
        )

        content.add_widget(
            description_label
        )

        continue_button = Button(
            text="CONTINUAR",
            font_size="19sp",
            bold=True,
            size_hint=(1, 0.20)
        )

        content.add_widget(
            continue_button
        )

        popup = Popup(
            title="",
            content=content,
            size_hint=(0.70, 0.55),
            auto_dismiss=False
        )

        self.achievement_popup = popup

        continue_button.bind(
            on_press=lambda instance:
            self.close_achievement_popup()
        )

        popup.open()

    # ========================================================
    # FECHAR POPUP
    # ========================================================

    def close_achievement_popup(self):

        if self.achievement_popup:

            self.achievement_popup.dismiss()
            self.achievement_popup = None

        if self.achievement_queue:
            self.show_next_achievement()

    # ========================================================
    # GUARDAR PROGRESSO
    # ========================================================

    def save_progress(
        self,
        total_questions,
        percentage
    ):

        print("💾 A GUARDAR PROGRESSO...")
        print(f"📂 Ficheiro: {self.progress_file}")

        try:

            with open(
                self.progress_file,
                "r",
                encoding="utf-8"
            ) as file:

                progress = json.load(file)

        except (
            FileNotFoundError,
            json.JSONDecodeError
        ):

            print(
                "⚠️ progress.json inexistente "
                "ou inválido. Criando novo progresso."
            )

            progress = {
                "total_quizzes": 0,
                "total_questions": 0,
                "correct_answers": 0,
                "wrong_answers": 0,
                "best_score": 0,
                "best_percentage": 0,
                "xp": 0,
                "level": 1,
                "title": "🛢️ Iniciante",
                "current_streak": 0,
                "best_streak": 0,
                "last_quiz_date": None,
                "categories_played": {},
                "difficulty_played": {
                    "Fácil": 0,
                    "Médio": 0,
                    "Difícil": 0
                },
                "achievements": [],
                "rewards": [],
                "last_quiz": {
                    "mode": "",
                    "difficulty": "",
                    "score": 0,
                    "total": 0,
                    "percentage": 0,
                    "xp_earned": 0,
                    "xp_breakdown": {},
                    "points": 0,
                    "max_points": 0
                }
            }

        progress.setdefault("total_quizzes", 0)
        progress.setdefault("total_questions", 0)
        progress.setdefault("correct_answers", 0)
        progress.setdefault("wrong_answers", 0)
        progress.setdefault("best_score", 0)
        progress.setdefault("best_percentage", 0)
        progress.setdefault("xp", 0)
        progress.setdefault("level", 1)
        progress.setdefault("title", "🛢️ Iniciante")
        progress.setdefault("current_streak", 0)
        progress.setdefault("best_streak", 0)
        progress.setdefault("last_quiz_date", None)
        progress.setdefault("categories_played", {})
        progress.setdefault("achievements", [])
        progress.setdefault("rewards", [])

        progress.setdefault(
            "difficulty_played",
            {
                "Fácil": 0,
                "Médio": 0,
                "Difícil": 0
            }
        )

        progress["difficulty_played"].setdefault(
            "Fácil",
            0
        )

        progress["difficulty_played"].setdefault(
            "Médio",
            0
        )

        progress["difficulty_played"].setdefault(
            "Difícil",
            0
        )

        progress.setdefault(
            "last_quiz",
            {}
        )

        progress["total_quizzes"] += 1

        progress["total_questions"] += (
            total_questions
        )

        progress["correct_answers"] += (
            self.score
        )

        progress["wrong_answers"] += (
            total_questions - self.score
        )

        # ====================================================
        # STREAK DIÁRIO
        # ====================================================

        today = date.today()
        today_str = today.isoformat()

        last_quiz_date = progress.get(
            "last_quiz_date"
        )

        if not last_quiz_date:

            current_streak = 1

            print(
                "🔥 PRIMEIRO QUIZ DO STREAK DIÁRIO!"
            )

        else:

            try:

                last_date = date.fromisoformat(
                    last_quiz_date
                )

                difference = (
                    today - last_date
                ).days

                if difference == 0:

                    current_streak = progress.get(
                        "current_streak",
                        1
                    )

                    print(
                        "🔥 QUIZ NO MESMO DIA — "
                        "STREAK NÃO AUMENTA."
                    )

                elif difference == 1:

                    current_streak = (
                        progress.get(
                            "current_streak",
                            0
                        ) + 1
                    )

                    print(
                        "🔥 QUIZ NO DIA SEGUINTE — "
                        "STREAK AUMENTOU!"
                    )

                else:

                    current_streak = 1

                    print(
                        "💔 STREAK QUEBRADO — "
                        "NOVA SEQUÊNCIA COMEÇOU."
                    )

            except (
                ValueError,
                TypeError
            ):

                print(
                    "⚠️ Data do último quiz inválida. "
                    "Reiniciando streak."
                )

                current_streak = 1

        progress["current_streak"] = current_streak
        progress["last_quiz_date"] = today_str

        if current_streak > progress.get(
            "best_streak",
            0
        ):

            progress["best_streak"] = current_streak

        print(
            f"🔥 STREAK ATUAL: {current_streak}"
        )

        print(
            f"🏆 MELHOR STREAK: "
            f"{progress['best_streak']}"
        )

        print(
            f"📅 ÚLTIMO QUIZ: {today_str}"
        )

        # ====================================================
        # BÓNUS DE STREAK
        # ====================================================

        self.streak_bonus = 0

        if current_streak >= 30:
            self.streak_bonus = 100
        elif current_streak >= 14:
            self.streak_bonus = 50
        elif current_streak >= 7:
            self.streak_bonus = 25
        elif current_streak >= 3:
            self.streak_bonus = 10

        if self.streak_bonus > 0:

            self.quiz_xp += self.streak_bonus

            print(
                f"🔥 BÓNUS DE STREAK "
                f"({current_streak} dias): "
                f"+{self.streak_bonus} XP"
            )

        # ====================================================
        # XP E LEVEL UP
        # ====================================================

        old_xp = progress["xp"]

        old_level = progress.get(
            "level",
            1
        )

        progress["xp"] += self.quiz_xp

        level, title = self.calculate_level(
            progress["xp"]
        )

        progress["level"] = level
        progress["title"] = title

        self.level_up = None
        self.new_rewards = []

        if level > old_level:

            self.level_up = {
                "old_level": old_level,
                "new_level": level,
                "title": title,
                "xp": progress["xp"],
                "rewards": []
            }

            print("🎉 LEVEL UP!")

            print(
                f"📈 NÍVEL: "
                f"{old_level} → {level}"
            )

            print(
                f"👑 NOVO TÍTULO: {title}"
            )

            for unlocked_level in range(
                old_level + 1,
                level + 1
            ):

                reward = get_level_reward(
                    unlocked_level
                )

                if reward:

                    reward_data = {
                        "level": unlocked_level,
                        "name": reward.get(
                            "name",
                            ""
                        ),
                        "reward": reward.get(
                            "reward",
                            ""
                        ),
                        "icon": reward.get(
                            "icon",
                            "🎁"
                        )
                    }

                    self.new_rewards.append(
                        reward_data
                    )

                    self.level_up[
                        "rewards"
                    ].append(
                        reward_data
                    )

                    already_unlocked = False

                    for saved_reward in progress[
                        "rewards"
                    ]:

                        if (
                            isinstance(
                                saved_reward,
                                dict
                            )
                            and saved_reward.get(
                                "level"
                            ) == unlocked_level
                        ):

                            already_unlocked = True
                            break

                    if not already_unlocked:

                        progress[
                            "rewards"
                        ].append(
                            reward_data
                        )

                    print(
                        f"🎁 RECOMPENSA DESBLOQUEADA | "
                        f"Nível {unlocked_level}: "
                        f"{reward_data['icon']} "
                        f"{reward_data['reward']}"
                    )

        else:

            print(
                "📈 SEM LEVEL UP NESTE QUIZ."
            )

        print(
            f"⭐ XP ANTERIOR: {old_xp}"
        )

        print(
            f"⭐ XP GANHO: +{self.quiz_xp}"
        )

        print(
            f"⭐ XP TOTAL: {progress['xp']}"
        )

        print(
            f"📈 NÍVEL: {level} | {title}"
        )

        # ====================================================
        # MELHOR PONTUAÇÃO
        # ====================================================

        if self.score > progress["best_score"]:

            progress["best_score"] = self.score

        if percentage > progress["best_percentage"]:

            progress["best_percentage"] = percentage

        # ====================================================
        # CATEGORIAS
        # ====================================================

        category = self.quiz_mode

        if category not in progress[
            "categories_played"
        ]:

            progress[
                "categories_played"
            ][category] = 0

        progress[
            "categories_played"
        ][category] += 1

        # ====================================================
        # DIFICULDADE
        # ====================================================

        difficulty = getattr(
            self.manager,
            "selected_difficulty",
            None
        )

        if difficulty in (
            "Fácil",
            "Médio",
            "Difícil"
        ):

            progress[
                "difficulty_played"
            ][difficulty] += 1

        # ====================================================
        # ÚLTIMO QUIZ
        # ====================================================

        progress["last_quiz"] = {

            "mode": self.quiz_mode,

            "difficulty": (
                difficulty
                if difficulty
                else "Todas"
            ),

            "score": self.score,

            "total": total_questions,

            "percentage": percentage,

            "xp_earned": self.quiz_xp,

            "points": self.quiz_points,

            "points_breakdown": {
                "base_points": self.score * self.base_points,
                "speed_bonus": self.total_speed_bonus,
            },

            "max_points": (
                total_questions * self.base_points
                + (
                    total_questions
                    * self.max_speed_bonus
                    if self.timer_enabled
                    else 0
                )
            ),

            "xp_breakdown": {

                "base_xp": self.base_xp,

                "completion_bonus": (
                    self.completion_bonus
                ),

                "performance_bonus": (
                    self.performance_bonus
                ),

                "perfect_bonus": (
                    self.perfect_bonus
                ),

                "streak_bonus": (
                    self.streak_bonus
                ),

                "total_xp": self.quiz_xp
            }
        }

        # ====================================================
        # VERIFICAR CONQUISTAS
        # ====================================================

        new_achievements = check_achievements(
            progress
        )

        self.manager.new_achievements = (
            new_achievements
        )

        self.achievement_queue = list(
            new_achievements
        )

        if new_achievements:

            print(
                "🏆 NOVAS CONQUISTAS DESBLOQUEADAS:"
            )

            for achievement_id in new_achievements:

                print(
                    f"   🏆 {achievement_id}"
                )

        # ====================================================
        # RECOMPENSAS
        # ====================================================

        self.manager.new_rewards = (
            self.new_rewards
        )

        if self.new_rewards:

            print(
                "🎁 NOVAS RECOMPENSAS:"
            )

            for reward in self.new_rewards:

                print(
                    f"   {reward['icon']} "
                    f"{reward['reward']}"
                )

        # ====================================================
        # SALVAR ARQUIVO
        # ====================================================

        try:

            os.makedirs(
                os.path.dirname(
                    self.progress_file
                ),
                exist_ok=True
            )

            with open(
                self.progress_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    progress,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            print(
                "✅ PROGRESSO GUARDADO COM SUCESSO!"
            )

        except Exception as error:

            print(
                "❌ ERRO AO GUARDAR PROGRESSO:",
                error
            )

    # ========================================================
    # VOLTAR AO MENU
    # ========================================================

    def back_to_menu(self, instance):

        self.manager.selected_category = None
        self.manager.selected_difficulty = None
        self.manager.selected_amount = "Todas"

        self.manager.current = "main"

    # ========================================================
    # VOLTAR ÀS CATEGORIAS
    # ========================================================

    def back_to_categories(self, instance):

        self.manager.current = "categories"

    # ========================================================
    # AJUSTAR TEXTO
    # ========================================================

    def update_text_size(
        self,
        instance,
        value
    ):

        instance.text_size = (
            instance.width - 20,
            None
        )