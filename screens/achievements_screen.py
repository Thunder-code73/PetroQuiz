import json
import os

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

from systems.achievements import get_all_achievements


class AchievementsScreen(Screen):

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

        self.progress_file = os.path.join(
            self.base_dir,
            "data",
            "progress.json"
        )

        # ====================================================
        # LAYOUT PRINCIPAL
        # ====================================================

        main_layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=8
        )

        # ====================================================
        # TÍTULO
        # ====================================================

        title = Label(
            text="🏆 CONQUISTAS",
            font_size="34sp",
            bold=True,
            size_hint=(1, 0.09)
        )

        main_layout.add_widget(title)

        # ====================================================
        # CONTADOR
        # ====================================================

        self.counter_label = Label(
            text="0 / 0 DESBLOQUEADAS",
            font_size="19sp",
            bold=True,
            size_hint=(1, 0.07)
        )

        main_layout.add_widget(
            self.counter_label
        )

        # ====================================================
        # RESUMO
        # ====================================================

        self.progress_summary_label = Label(
            text="",
            font_size="14sp",
            halign="center",
            valign="middle",
            size_hint=(1, 0.06)
        )

        self.progress_summary_label.bind(
            size=self.update_text_size
        )

        main_layout.add_widget(
            self.progress_summary_label
        )

        # ====================================================
        # SCROLL
        # ====================================================

        scroll = ScrollView()

        self.achievements_layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=8,
            size_hint_y=None
        )

        self.achievements_layout.bind(
            minimum_height=self.achievements_layout.setter(
                "height"
            )
        )

        scroll.add_widget(
            self.achievements_layout
        )

        main_layout.add_widget(
            scroll
        )

        # ====================================================
        # BOTÃO VOLTAR
        # ====================================================

        back_button = Button(
            text="🏠 VOLTAR AO MENU",
            font_size="17sp",
            size_hint=(1, 0.08)
        )

        back_button.bind(
            on_release=self.back_to_menu
        )

        main_layout.add_widget(
            back_button
        )

        self.add_widget(
            main_layout
        )

    # ========================================================
    # ENTRAR NA TELA
    # ========================================================

    def on_enter(self):
        self.load_achievements()

    # ========================================================
    # CALCULAR PROGRESSO DE UMA CONQUISTA
    # ========================================================

    def get_achievement_progress(
        self,
        achievement_id,
        progress
    ):

        total_quizzes = progress.get(
            "total_quizzes",
            0
        )

        total_questions = progress.get(
            "total_questions",
            0
        )

        level = progress.get(
            "level",
            1
        )

        current_streak = progress.get(
            "current_streak",
            0
        )

        categories_played = progress.get(
            "categories_played",
            {}
        )

        difficulty_played = progress.get(
            "difficulty_played",
            {}
        )

        last_quiz = progress.get(
            "last_quiz",
            {}
        )

        # ====================================================
        # PRIMEIRO QUIZ
        # ====================================================

        if achievement_id == "first_quiz":
            return {
                "current": min(total_quizzes, 1),
                "target": 1
            }

        # ====================================================
        # QUIZ PERFEITO
        # ====================================================

        if achievement_id == "perfect_quiz":

            percentage = last_quiz.get(
                "percentage",
                0
            )

            return {
                "current": min(percentage, 100),
                "target": 100,
                "suffix": "%"
            }

        # ====================================================
        # 5 QUIZZES
        # ====================================================

        if achievement_id == "five_quizzes":
            return {
                "current": min(total_quizzes, 5),
                "target": 5
            }

        # ====================================================
        # 100 PERGUNTAS
        # ====================================================

        if achievement_id == "hundred_questions":
            return {
                "current": min(total_questions, 100),
                "target": 100
            }

        # ====================================================
        # NÍVEL 3
        # ====================================================

        if achievement_id == "level_3":
            return {
                "current": min(level, 3),
                "target": 3
            }

        # ====================================================
        # NÍVEL 6
        # ====================================================

        if achievement_id == "level_6":
            return {
                "current": min(level, 6),
                "target": 6
            }

        # ====================================================
        # NÍVEL 7
        # ====================================================

        if achievement_id == "level_7":
            return {
                "current": min(level, 7),
                "target": 7
            }

        # ====================================================
        # NÍVEL 8
        # ====================================================

        if achievement_id == "level_8":
            return {
                "current": min(level, 8),
                "target": 8
            }

        # ====================================================
        # QUIZ DIFÍCIL
        # ====================================================

        if achievement_id == "hard_quiz":

            difficult_quizzes = difficulty_played.get(
                "Difícil",
                0
            )

            return {
                "current": min(difficult_quizzes, 1),
                "target": 1
            }

        # ====================================================
        # EXPLORADOR DE CATEGORIAS
        # ====================================================

        if achievement_id == "category_explorer":

            return {
                "current": min(
                    len(categories_played),
                    5
                ),
                "target": 5
            }

        # ====================================================
        # STREAK 3
        # ====================================================

        if achievement_id == "streak_3":
            return {
                "current": min(current_streak, 3),
                "target": 3
            }

        # ====================================================
        # STREAK 10
        # ====================================================

        if achievement_id == "streak_10":
            return {
                "current": min(current_streak, 10),
                "target": 10
            }

        # ====================================================
        # STREAK 25
        # ====================================================

        if achievement_id == "streak_25":
            return {
                "current": min(current_streak, 25),
                "target": 25
            }

        # ====================================================
        # SEM PROGRESSO DEFINIDO
        # ====================================================

        return None

    # ========================================================
    # FORMATAR PROGRESSO
    # ========================================================

    def format_progress(
        self,
        achievement_id,
        progress
    ):

        if not progress:
            return ""

        current = progress.get(
            "current",
            0
        )

        target = progress.get(
            "target",
            1
        )

        suffix = progress.get(
            "suffix",
            ""
        )

        if target <= 0:
            percentage = 100
        else:
            percentage = (
                current / target
            ) * 100

        percentage = min(
            max(percentage, 0),
            100
        )

        # ====================================================
        # TEXTO
        # ====================================================

        if suffix == "%":

            progress_text = (
                f"📈 Progresso: "
                f"{current:.0f}{suffix}/"
                f"{target}{suffix}"
            )

        else:

            progress_text = (
                f"📈 Progresso: "
                f"{int(current)}/{int(target)}"
            )

        progress_text += (
            f"  •  {percentage:.0f}%"
        )

        return progress_text

    # ========================================================
    # CARREGAR CONQUISTAS
    # ========================================================

    def load_achievements(self):

        self.achievements_layout.clear_widgets()

        # ====================================================
        # CARREGAR PROGRESSO
        # ====================================================

        progress = self.load_progress_file()

        unlocked = progress.get(
            "achievements",
            []
        )

        if not isinstance(unlocked, list):
            unlocked = []

        achievements = get_all_achievements()

        total_achievements = len(
            achievements
        )

        unlocked_count = len(
            unlocked
        )

        locked_count = (
            total_achievements
            - unlocked_count
        )

        # ====================================================
        # CONTADOR
        # ====================================================

        self.counter_label.text = (
            f"🏆 {unlocked_count} / "
            f"{total_achievements} "
            f"DESBLOQUEADAS"
        )

        # ====================================================
        # RESUMO
        # ====================================================

        if total_achievements > 0:

            overall_percentage = (
                unlocked_count
                / total_achievements
            ) * 100

        else:

            overall_percentage = 0

        self.progress_summary_label.text = (
            f"📊 Progresso geral: "
            f"{overall_percentage:.0f}%"
            f"   •   "
            f"🔒 Restam: {locked_count}"
        )

        # ====================================================
        # TÍTULO — DESBLOQUEADAS
        # ====================================================

        if unlocked_count > 0:

            unlocked_title = Label(
                text="🔓 DESBLOQUEADAS",
                font_size="22sp",
                bold=True,
                size_hint_y=None,
                height=45
            )

            self.achievements_layout.add_widget(
                unlocked_title
            )

        # ====================================================
        # ADICIONAR DESBLOQUEADAS
        # ====================================================

        for achievement_id, achievement in achievements.items():

            if achievement_id not in unlocked:
                continue

            self.add_achievement_card(
                achievement_id,
                achievement,
                progress,
                True
            )

        # ====================================================
        # TÍTULO — BLOQUEADAS
        # ====================================================

        if locked_count > 0:

            locked_title = Label(
                text="🔒 BLOQUEADAS",
                font_size="22sp",
                bold=True,
                size_hint_y=None,
                height=50
            )

            self.achievements_layout.add_widget(
                locked_title
            )

        # ====================================================
        # ADICIONAR BLOQUEADAS
        # ====================================================

        for achievement_id, achievement in achievements.items():

            if achievement_id in unlocked:
                continue

            self.add_achievement_card(
                achievement_id,
                achievement,
                progress,
                False
            )

    # ========================================================
    # CRIAR CARTÃO
    # ========================================================

    def add_achievement_card(
        self,
        achievement_id,
        achievement,
        progress,
        unlocked
    ):

        # ====================================================
        # CARTÃO
        # ====================================================

        card = BoxLayout(
            orientation="horizontal",
            spacing=8,
            padding=8,
            size_hint_y=None,
            height=125
        )

        # ====================================================
        # ÍCONE
        # ====================================================

        if unlocked:

            icon_text = achievement.get(
                "icon",
                "🏆"
            )

        else:

            icon_text = "🔒"

        icon_label = Label(
            text=icon_text,
            font_size="34sp",
            size_hint=(0.14, 1)
        )

        card.add_widget(
            icon_label
        )

        # ====================================================
        # INFORMAÇÕES
        # ====================================================

        info_layout = BoxLayout(
            orientation="vertical",
            spacing=1,
            size_hint=(0.71, 1)
        )

        name = achievement.get(
            "name",
            "Conquista"
        )

        description = achievement.get(
            "description",
            ""
        )

        # ====================================================
        # NOME
        # ====================================================

        if unlocked:

            name_text = (
                f"🏆 {name}"
            )

        else:

            name_text = (
                f"🔒 {name}"
            )

        name_label = Label(
            text=name_text,
            font_size="18sp",
            bold=True,
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=30
        )

        name_label.bind(
            size=self.update_text_size
        )

        info_layout.add_widget(
            name_label
        )

        # ====================================================
        # DESCRIÇÃO
        # ====================================================

        description_label = Label(
            text=description,
            font_size="13sp",
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=38
        )

        description_label.bind(
            size=self.update_text_size
        )

        info_layout.add_widget(
            description_label
        )

        # ====================================================
        # PROGRESSO
        # ====================================================

        achievement_progress = (
            self.get_achievement_progress(
                achievement_id,
                progress
            )
        )

        if unlocked:

            progress_text = (
                "✓ OBJETIVO CONCLUÍDO"
            )

        else:

            progress_text = (
                self.format_progress(
                    achievement_id,
                    achievement_progress
                )
            )

            if not progress_text:

                progress_text = (
                    "🎯 Continua a jogar!"
                )

        progress_label = Label(
            text=progress_text,
            font_size="12sp",
            bold=True,
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=25
        )

        progress_label.bind(
            size=self.update_text_size
        )

        info_layout.add_widget(
            progress_label
        )

        # ====================================================
        # ESTADO
        # ====================================================

        if unlocked:

            status_text = (
                "🔓 DESBLOQUEADA"
            )

        else:

            status_text = (
                "🔒 BLOQUEADA"
            )

        status_label = Label(
            text=status_text,
            font_size="11sp",
            bold=True,
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=22
        )

        status_label.bind(
            size=self.update_text_size
        )

        info_layout.add_widget(
            status_label
        )

        card.add_widget(
            info_layout
        )

        # ====================================================
        # INDICADOR
        # ====================================================

        if unlocked:

            indicator = Label(
                text="✓",
                font_size="34sp",
                bold=True,
                size_hint=(0.15, 1)
            )

        else:

            indicator = Label(
                text="?",
                font_size="34sp",
                size_hint=(0.15, 1)
            )

        card.add_widget(
            indicator
        )

        self.achievements_layout.add_widget(
            card
        )

    # ========================================================
    # CARREGAR PROGRESS.JSON
    # ========================================================

    def load_progress_file(self):

        print(
            "📂 A LER PROGRESSO DE:"
        )

        print(
            self.progress_file
        )

        try:

            with open(
                self.progress_file,
                "r",
                encoding="utf-8"
            ) as file:

                progress = json.load(file)

            print(
                "✅ PROGRESSO CARREGADO!"
            )

            print(
                "🏆 CONQUISTAS SALVAS:",
                progress.get(
                    "achievements",
                    []
                )
            )

            return progress

        except FileNotFoundError:

            print(
                "❌ progress.json NÃO ENCONTRADO!"
            )

            return {
                "achievements": []
            }

        except json.JSONDecodeError:

            print(
                "❌ progress.json ESTÁ INVÁLIDO!"
            )

            return {
                "achievements": []
            }

        except Exception as error:

            print(
                "❌ ERRO AO LER PROGRESS.JSON:",
                error
            )

            return {
                "achievements": []
            }

    # ========================================================
    # VOLTAR AO MENU
    # ========================================================

    def back_to_menu(self, instance):

        self.manager.current = "main"

    # ========================================================
    # AJUSTAR TEXTO
    # ========================================================

    def update_text_size(
        self,
        instance,
        value
    ):

        instance.text_size = (
            instance.width - 10,
            None
        )