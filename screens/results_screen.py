from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget

from systems.achievements import get_achievement


class ResultsScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main_layout = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=3
        )

        self.title_label = Label(
            text="🏆 RESULTADO DO QUIZ",
            font_size="27sp",
            bold=True,
            size_hint=(1, 0.065)
        )
        main_layout.add_widget(self.title_label)

        self.mode_label = Label(
            text="",
            font_size="13sp",
            size_hint=(1, 0.04)
        )
        main_layout.add_widget(self.mode_label)

        self.score_label = Label(
            text="",
            font_size="23sp",
            bold=True,
            size_hint=(1, 0.06)
        )
        main_layout.add_widget(self.score_label)

        # NOVO: pontuação do jogo
        self.points_label = Label(
            text="",
            font_size="25sp",
            bold=True,
            size_hint=(1, 0.065)
        )
        main_layout.add_widget(self.points_label)

        self.points_breakdown_label = Label(
            text="",
            font_size="12sp",
            halign="center",
            valign="middle",
            size_hint=(1, 0.065)
        )
        self.points_breakdown_label.bind(size=self.update_text_size)
        main_layout.add_widget(self.points_breakdown_label)

        self.percentage_label = Label(
            text="",
            font_size="18sp",
            size_hint=(1, 0.045)
        )
        main_layout.add_widget(self.percentage_label)

        self.classification_label = Label(
            text="",
            font_size="17sp",
            bold=True,
            size_hint=(1, 0.05)
        )
        main_layout.add_widget(self.classification_label)

        self.stats_label = Label(
            text="",
            font_size="13sp",
            halign="center",
            valign="middle",
            size_hint=(1, 0.06)
        )
        self.stats_label.bind(size=self.update_text_size)
        main_layout.add_widget(self.stats_label)

        self.xp_label = Label(
            text="",
            font_size="12sp",
            bold=True,
            halign="center",
            valign="middle",
            size_hint=(1, 0.16)
        )
        self.xp_label.bind(size=self.update_text_size)
        main_layout.add_widget(self.xp_label)

        self.level_up_label = Label(
            text="",
            font_size="11sp",
            bold=True,
            halign="center",
            valign="middle",
            size_hint=(1, 0.105)
        )
        self.level_up_label.bind(size=self.update_text_size)
        main_layout.add_widget(self.level_up_label)

        self.new_achievements_label = Label(
            text="",
            font_size="10sp",
            bold=True,
            halign="center",
            valign="middle",
            size_hint=(1, 0.06)
        )
        self.new_achievements_label.bind(size=self.update_text_size)
        main_layout.add_widget(self.new_achievements_label)

        spacer = Widget(size_hint=(1, 0.015))
        main_layout.add_widget(spacer)

        replay_button = Button(
            text="🔄 JOGAR NOVAMENTE",
            font_size="14sp",
            bold=True,
            size_hint=(1, 0.07)
        )
        replay_button.bind(on_press=self.replay_quiz)
        main_layout.add_widget(replay_button)

        menu_button = Button(
            text="🏠 VOLTAR AO MENU",
            font_size="13sp",
            size_hint=(1, 0.06)
        )
        menu_button.bind(on_press=self.back_to_menu)
        main_layout.add_widget(menu_button)

        self.add_widget(main_layout)

    def on_enter(self):

        score = getattr(self.manager, "quiz_score", 0)
        total = getattr(self.manager, "quiz_total", 0)
        mode = getattr(self.manager, "quiz_mode", "Geral")
        difficulty = getattr(
            self.manager,
            "quiz_difficulty",
            "Todas"
        )
        quiz_xp = getattr(self.manager, "quiz_xp", 0)

        # NOVO: pontos
        quiz_points = getattr(
            self.manager,
            "quiz_points",
            0
        )

        points_breakdown = getattr(
            self.manager,
            "quiz_points_breakdown",
            {}
        )

        if total > 0:
            percentage = (score / total) * 100
        else:
            percentage = 0

        if percentage >= 90:
            classification = "🏆 EXCELENTE!"
        elif percentage >= 70:
            classification = "🔥 MUITO BOM!"
        elif percentage >= 50:
            classification = "👍 BOM!"
        else:
            classification = "📚 PRECISAS ESTUDAR MAIS"

        self.mode_label.text = (
            f"📚 {mode}   |   🎯 {difficulty}"
        )

        self.score_label.text = (
            f"{score} / {total} ACERTOS"
        )

        self.points_label.text = (
            f"🏆 {quiz_points} PONTOS"
        )

        base_points = points_breakdown.get(
            "base_points",
            quiz_points
        )
        speed_bonus = points_breakdown.get(
            "speed_bonus",
            0
        )

        if speed_bonus > 0:
            self.points_breakdown_label.text = (
                f"🎯 Base: {base_points} pts   |   "
                f"⚡ Velocidade: +{speed_bonus} pts"
            )
        else:
            self.points_breakdown_label.text = (
                f"🎯 Pontos base: {base_points} pts"
            )

        self.percentage_label.text = (
            f"📊 {percentage:.0f}%"
        )

        self.classification_label.text = classification

        wrong = total - score

        self.stats_label.text = (
            f"✅ Acertos: {score}   |   "
            f"❌ Erros: {wrong}   |   "
            f"📝 Perguntas: {total}"
        )

        xp_breakdown = self.get_xp_breakdown()

        base_xp = xp_breakdown.get("base_xp", 0)
        completion_bonus = xp_breakdown.get(
            "completion_bonus",
            0
        )
        performance_bonus = xp_breakdown.get(
            "performance_bonus",
            0
        )
        perfect_bonus = xp_breakdown.get(
            "perfect_bonus",
            0
        )
        streak_bonus = xp_breakdown.get(
            "streak_bonus",
            0
        )
        total_xp = xp_breakdown.get(
            "total_xp",
            quiz_xp
        )

        xp_lines = [
            "⭐ XP GANHO",
            f"🧠 Corretas: +{base_xp} XP",
            f"🎁 Conclusão: +{completion_bonus} XP",
            f"🔥 Desempenho: +{performance_bonus} XP",
            f"🎯 Perfeito: +{perfect_bonus} XP",
            f"🔥 Streak: +{streak_bonus} XP",
            f"💰 TOTAL: +{total_xp} XP"
        ]

        self.xp_label.text = "\n".join(xp_lines)

        level_up = getattr(
            self.manager,
            "level_up",
            None
        )

        if level_up:

            old_level = level_up.get("old_level", 1)
            new_level = level_up.get(
                "new_level",
                old_level
            )
            title = level_up.get("title", "")
            level_xp = level_up.get("xp", 0)

            level_lines = [
                "🎉 LEVEL UP!",
                f"⬆️ NÍVEL {old_level} → NÍVEL {new_level}",
                f"🏅 {title}  |  ⭐ {level_xp} XP"
            ]

            rewards = level_up.get("rewards", [])

            if rewards:
                level_lines.append(
                    "🎁 RECOMPENSAS DESBLOQUEADAS"
                )

                for reward in rewards:
                    icon = reward.get("icon", "🎁")
                    reward_name = reward.get(
                        "reward",
                        "Nova recompensa"
                    )
                    level_lines.append(
                        f"{icon} {reward_name}"
                    )

            self.level_up_label.text = "\n".join(
                level_lines
            )

        else:
            self.level_up_label.text = ""

        new_achievements = getattr(
            self.manager,
            "new_achievements",
            []
        )

        if new_achievements:

            lines = ["🏆 NOVAS CONQUISTAS!"]

            for achievement_id in new_achievements:

                achievement = get_achievement(
                    achievement_id
                )

                if achievement:

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

                    lines.append(
                        f"{icon} {name}"
                    )
                    lines.append(description)

            self.new_achievements_label.text = (
                "\n".join(lines)
            )

        else:
            self.new_achievements_label.text = ""

    def get_xp_breakdown(self):

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

            last_quiz = progress.get(
                "last_quiz",
                {}
            )

            return last_quiz.get(
                "xp_breakdown",
                {}
            )

        except Exception as error:

            print(
                "⚠️ Erro ao carregar "
                "detalhamento do XP:",
                error
            )

            return {}

    def replay_quiz(self, instance):

        self.manager.current = "quiz"

    def back_to_menu(self, instance):

        self.manager.selected_category = None
        self.manager.selected_difficulty = None
        self.manager.selected_amount = "Todas"
        self.manager.current = "main"

    def update_text_size(self, instance, value):

        instance.text_size = (
            instance.width - 20,
            None
        )
