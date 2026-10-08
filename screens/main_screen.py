import json
import os

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class MainScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # =====================================================
        # CAMINHO DO PROGRESSO
        # =====================================================

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

        # =====================================================
        # LAYOUT PRINCIPAL
        # =====================================================

        layout = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=8
        )

        # =====================================================
        # TÍTULO
        # =====================================================

        layout.add_widget(
            Label(
                text="PETROQUIZ",
                font_size="44sp",
                bold=True,
                size_hint=(1, 0.12)
            )
        )

        # =====================================================
        # PERFIL DO JOGADOR
        # =====================================================

        self.player_label = Label(
            text="",
            font_size="20sp",
            bold=True,
            halign="center",
            valign="middle",
            size_hint=(1, 0.09)
        )

        self.player_label.bind(
            size=self.update_text_size
        )

        layout.add_widget(
            self.player_label
        )

        # =====================================================
        # STATUS DO JOGADOR
        # =====================================================

        self.status_label = Label(
            text="",
            font_size="15sp",
            halign="center",
            valign="middle",
            size_hint=(1, 0.08)
        )

        self.status_label.bind(
            size=self.update_text_size
        )

        layout.add_widget(
            self.status_label
        )

        # =====================================================
        # SUBTÍTULO
        # =====================================================

        layout.add_widget(
            Label(
                text=(
                    "Teste os teus conhecimentos "
                    "sobre a indústria petrolífera"
                ),
                font_size="17sp",
                halign="center",
                valign="middle",
                size_hint=(1, 0.07)
            )
        )

        # =====================================================
        # COMEÇAR QUIZ
        # =====================================================

        start_button = Button(
            text="COMEÇAR QUIZ",
            font_size="21sp",
            size_hint=(0.70, 0.10),
            pos_hint={"center_x": 0.5}
        )

        start_button.bind(
            on_release=self.start_general_quiz
        )

        layout.add_widget(
            start_button
        )

        # =====================================================
        # CATEGORIAS
        # =====================================================

        categories_button = Button(
            text="CATEGORIAS",
            font_size="19sp",
            size_hint=(0.70, 0.085),
            pos_hint={"center_x": 0.5}
        )

        categories_button.bind(
            on_release=lambda instance:
            self.go_to("categories")
        )

        layout.add_widget(
            categories_button
        )

        # =====================================================
        # PROGRESSO
        # =====================================================

        progress_button = Button(
            text="MEU PROGRESSO",
            font_size="19sp",
            size_hint=(0.70, 0.085),
            pos_hint={"center_x": 0.5}
        )

        progress_button.bind(
            on_release=lambda instance:
            self.go_to("progress")
        )

        layout.add_widget(
            progress_button
        )

        # =====================================================
        # CONQUISTAS
        # =====================================================

        achievements_button = Button(
            text="🏆 CONQUISTAS",
            font_size="19sp",
            size_hint=(0.70, 0.085),
            pos_hint={"center_x": 0.5}
        )

        achievements_button.bind(
            on_release=lambda instance:
            self.go_to("achievements")
        )

        layout.add_widget(
            achievements_button
        )

        # =====================================================
        # RECOMPENSAS
        # =====================================================

        rewards_button = Button(
            text="🎁 RECOMPENSAS",
            font_size="19sp",
            size_hint=(0.70, 0.085),
            pos_hint={"center_x": 0.5}
        )

        rewards_button.bind(
            on_release=lambda instance:
            self.go_to("rewards")
        )

        layout.add_widget(
            rewards_button
        )

        # =====================================================
        # MEU PERFIL
        # =====================================================

        profile_button = Button(
            text="👤 MEU PERFIL",
            font_size="19sp",
            size_hint=(0.70, 0.085),
            pos_hint={"center_x": 0.5}
        )

        profile_button.bind(
            on_release=lambda instance:
            self.go_to("profile")
        )

        layout.add_widget(
            profile_button
        )

        # =====================================================
        # SOBRE
        # =====================================================

        about_button = Button(
            text="SOBRE",
            font_size="17sp",
            size_hint=(0.70, 0.075),
            pos_hint={"center_x": 0.5}
        )

        about_button.bind(
            on_release=lambda instance:
            self.go_to("about")
        )

        layout.add_widget(
            about_button
        )

        # =====================================================
        # ADICIONAR LAYOUT
        # =====================================================

        self.add_widget(
            layout
        )

    # =========================================================
    # ENTRAR NO MENU
    # =========================================================

    def on_enter(self):

        self.load_player_info()

    # =========================================================
    # CARREGAR INFORMAÇÕES DO JOGADOR
    # =========================================================

    def load_player_info(self):

        progress = self.load_progress_file()

        player_name = progress.get(
            "player_name",
            "Jogador"
        )

        if not isinstance(
            player_name,
            str
        ) or not player_name.strip():

            player_name = "Jogador"

        player_name = player_name.strip()

        # =====================================================
        # NÍVEL
        # =====================================================

        level = progress.get(
            "level",
            1
        )

        title = progress.get(
            "title",
            "🛢️ Iniciante"
        )

        xp = progress.get(
            "xp",
            0
        )

        # =====================================================
        # STREAK
        # =====================================================

        current_streak = progress.get(
            "current_streak",
            0
        )

        # =====================================================
        # NOME
        # =====================================================

        self.player_label.text = (
            f"👋 Olá, {player_name}!"
        )

        # =====================================================
        # STATUS
        # =====================================================

        self.status_label.text = (
            f"🏆 Nível {level} • "
            f"{title}\n"
            f"⭐ {xp} XP • "
            f"🔥 Streak: {current_streak} dias"
        )

        print(
            "👤 JOGADOR:",
            player_name
        )

        print(
            "🏆 NÍVEL:",
            level
        )

        print(
            "⭐ XP:",
            xp
        )

        print(
            "🔥 STREAK:",
            current_streak
        )

    # =========================================================
    # CARREGAR PROGRESS.JSON
    # =========================================================

    def load_progress_file(self):

        try:

            if not os.path.exists(
                self.progress_file
            ):

                return {}

            with open(
                self.progress_file,
                "r",
                encoding="utf-8"
            ) as file:

                progress = json.load(file)

            if not isinstance(
                progress,
                dict
            ):

                return {}

            return progress

        except FileNotFoundError:

            return {}

        except json.JSONDecodeError:

            print(
                "❌ progress.json inválido."
            )

            return {}

        except Exception as error:

            print(
                "❌ ERRO AO LER progress.json:",
                error
            )

            return {}

    # =========================================================
    # COMEÇAR QUIZ GERAL
    # =========================================================

    def start_general_quiz(self, instance):

        self.manager.selected_category = None
        self.manager.selected_difficulty = "Fácil"
        self.manager.selected_amount = 10

        self.manager.current = "quiz_config"

    # =========================================================
    # NAVEGAÇÃO
    # =========================================================

    def go_to(self, screen_name):

        self.manager.current = screen_name

    # =========================================================
    # AJUSTAR TEXTO
    # =========================================================

    def update_text_size(
        self,
        instance,
        value
    ):

        instance.text_size = (
            instance.width - 20,
            None
        )