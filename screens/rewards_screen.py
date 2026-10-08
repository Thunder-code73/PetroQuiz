from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

from systems.rewards import get_all_rewards


class RewardsScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # =====================================================
        # LAYOUT PRINCIPAL
        # =====================================================

        main_layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=8
        )

        # =====================================================
        # TÍTULO
        # =====================================================

        title = Label(
            text="🎁 RECOMPENSAS",
            font_size="34sp",
            bold=True,
            size_hint=(1, 0.09)
        )

        main_layout.add_widget(title)

        # =====================================================
        # CONTADOR
        # =====================================================

        self.counter_label = Label(
            text="",
            font_size="17sp",
            bold=True,
            size_hint=(1, 0.06)
        )

        main_layout.add_widget(
            self.counter_label
        )

        # =====================================================
        # SCROLL
        # =====================================================

        scroll = ScrollView(
            size_hint=(1, 0.75)
        )

        self.rewards_layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=8,
            size_hint_y=None
        )

        self.rewards_layout.bind(
            minimum_height=self.rewards_layout.setter(
                "height"
            )
        )

        scroll.add_widget(
            self.rewards_layout
        )

        main_layout.add_widget(scroll)

        # =====================================================
        # BOTÃO VOLTAR
        # =====================================================

        back_button = Button(
            text="🏠 VOLTAR",
            font_size="16sp",
            bold=True,
            size_hint=(1, 0.10)
        )

        back_button.bind(
            on_press=self.back_to_menu
        )

        main_layout.add_widget(
            back_button
        )

        self.add_widget(
            main_layout
        )

    # =========================================================
    # ENTRAR NA TELA
    # =========================================================

    def on_enter(self):

        self.load_rewards()

    # =========================================================
    # CARREGAR RECOMPENSAS
    # =========================================================

    def load_rewards(self):

        self.rewards_layout.clear_widgets()

        all_rewards = get_all_rewards()

        unlocked_rewards = []

        # =====================================================
        # LER PROGRESSO
        # =====================================================

        try:

            quiz_screen = self.manager.get_screen(
                "quiz"
            )

            progress_file = (
                quiz_screen.progress_file
            )

            import json

            with open(
                progress_file,
                "r",
                encoding="utf-8"
            ) as file:

                progress = json.load(file)

            saved_rewards = progress.get(
                "rewards",
                []
            )

            for reward in saved_rewards:

                if isinstance(reward, dict):

                    level = reward.get(
                        "level"
                    )

                    if level is not None:

                        unlocked_rewards.append(
                            level
                        )

        except Exception as error:

            print(
                "⚠️ Erro ao carregar "
                "recompensas:",
                error
            )

        # =====================================================
        # CONTADOR
        # =====================================================

        unlocked_count = len(
            unlocked_rewards
        )

        total_count = len(
            all_rewards
        )

        self.counter_label.text = (
            f"🏆 {unlocked_count} / {total_count} "
            f"RECOMPENSAS DESBLOQUEADAS"
        )

        # =====================================================
        # CARDS
        # =====================================================

        for level, reward in all_rewards.items():

            unlocked = (
                level in unlocked_rewards
            )

            # -------------------------------------------------
            # CARD
            # -------------------------------------------------

            card = BoxLayout(
                orientation="vertical",
                spacing=2,
                padding=8,
                size_hint_y=None,
                height=105
            )

            # -------------------------------------------------
            # TEXTO
            # -------------------------------------------------

            if unlocked:

                icon = reward.get(
                    "icon",
                    "🎁"
                )

                name = reward.get(
                    "name",
                    "Recompensa"
                )

                reward_text = reward.get(
                    "reward",
                    ""
                )

                text = (
                    f"{icon}  NÍVEL {level}  |  "
                    f"🏅 {name}\n"
                    f"🎁 {reward_text}\n"
                    f"✅ DESBLOQUEADA"
                )

            else:

                name = reward.get(
                    "name",
                    "Recompensa"
                )

                reward_text = reward.get(
                    "reward",
                    ""
                )

                text = (
                    f"🔒  NÍVEL {level}  |  "
                    f"🏅 {name}\n"
                    f"🎁 {reward_text}\n"
                    f"🔒 BLOQUEADA"
                )

            # -------------------------------------------------
            # LABEL
            # -------------------------------------------------

            reward_label = Label(
                text=text,
                font_size="16sp",
                bold=unlocked,
                halign="center",
                valign="middle"
            )

            reward_label.bind(
                size=self.update_text_size
            )

            card.add_widget(
                reward_label
            )

            self.rewards_layout.add_widget(
                card
            )

    # =========================================================
    # VOLTAR AO MENU
    # =========================================================

    def back_to_menu(self, instance):

        self.manager.current = "main"

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