import json
import os
from datetime import date

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar

from systems.achievements import get_all_achievements
from systems.rewards import get_all_rewards


class ProgressScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ====================================================
        # CAMINHO DO PROGRESS.JSON
        # ====================================================

        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        self.progress_file = os.path.join(
            base_dir,
            "data",
            "progress.json"
        )

        # ====================================================
        # LAYOUT PRINCIPAL
        # ====================================================

        main_layout = BoxLayout(
            orientation="vertical",
            padding=18,
            spacing=7
        )

        # ====================================================
        # TÍTULO
        # ====================================================

        title = Label(
            text="📊 MEU PROGRESSO",
            font_size="32sp",
            bold=True,
            size_hint=(1, 0.09)
        )

        main_layout.add_widget(title)

        # ====================================================
        # SCROLL
        # ====================================================

        scroll = ScrollView()

        stats_layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=8,
            size_hint_y=None
        )

        stats_layout.bind(
            minimum_height=stats_layout.setter("height")
        )

        # ====================================================
        # PERFIL
        # ====================================================

        self.profile_label = Label(
            text="",
            font_size="21sp",
            bold=True,
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=140
        )

        self.profile_label.bind(
            size=self.update_text_size
        )

        stats_layout.add_widget(
            self.profile_label
        )

        # ====================================================
        # RESUMO GERAL
        # ====================================================

        self.summary_label = Label(
            text="",
            font_size="18sp",
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=210
        )

        self.summary_label.bind(
            size=self.update_text_size
        )

        stats_layout.add_widget(
            self.summary_label
        )

        # ====================================================
        # STREAK
        # ====================================================

        self.streak_label = Label(
            text="",
            font_size="19sp",
            bold=True,
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=200
        )

        self.streak_label.bind(
            size=self.update_text_size
        )

        stats_layout.add_widget(
            self.streak_label
        )

        # ====================================================
        # XP
        # ====================================================

        xp_box = BoxLayout(
            orientation="vertical",
            spacing=5,
            size_hint_y=None,
            height=260
        )

        self.xp_label = Label(
            text="",
            font_size="18sp",
            bold=True,
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=190
        )

        self.xp_label.bind(
            size=self.update_text_size
        )

        xp_box.add_widget(
            self.xp_label
        )

        # ====================================================
        # BARRA XP
        # ====================================================

        self.xp_bar = ProgressBar(
            max=100,
            value=0,
            size_hint=(0.90, None),
            height=22,
            pos_hint={
                "center_x": 0.5
            }
        )

        xp_box.add_widget(
            self.xp_bar
        )

        # ====================================================
        # PERCENTAGEM
        # ====================================================

        self.xp_percentage_label = Label(
            text="0%",
            font_size="14sp",
            bold=True,
            size_hint_y=None,
            height=28
        )

        xp_box.add_widget(
            self.xp_percentage_label
        )

        stats_layout.add_widget(
            xp_box
        )

        # ====================================================
        # DESEMPENHO
        # ====================================================

        self.performance_label = Label(
            text="",
            font_size="18sp",
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=210
        )

        self.performance_label.bind(
            size=self.update_text_size
        )

        stats_layout.add_widget(
            self.performance_label
        )

        # ====================================================
        # DIFICULDADE
        # ====================================================

        self.difficulty_label = Label(
            text="",
            font_size="18sp",
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=160
        )

        self.difficulty_label.bind(
            size=self.update_text_size
        )

        stats_layout.add_widget(
            self.difficulty_label
        )

        # ====================================================
        # ÚLTIMO QUIZ
        # ====================================================

        self.last_quiz_label = Label(
            text="",
            font_size="18sp",
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=180
        )

        self.last_quiz_label.bind(
            size=self.update_text_size
        )

        stats_layout.add_widget(
            self.last_quiz_label
        )

        # ====================================================
        # CATEGORIAS
        # ====================================================

        self.categories_label = Label(
            text="",
            font_size="18sp",
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=220
        )

        self.categories_label.bind(
            size=self.update_text_size
        )

        stats_layout.add_widget(
            self.categories_label
        )

        # ====================================================
        # CONQUISTAS
        # ====================================================

        self.achievements_label = Label(
            text="",
            font_size="18sp",
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=160
        )

        self.achievements_label.bind(
            size=self.update_text_size
        )

        stats_layout.add_widget(
            self.achievements_label
        )

        # ====================================================
        # RECOMPENSAS
        # ====================================================

        self.rewards_label = Label(
            text="",
            font_size="18sp",
            bold=True,
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=220
        )

        self.rewards_label.bind(
            size=self.update_text_size
        )

        stats_layout.add_widget(
            self.rewards_label
        )

        scroll.add_widget(
            stats_layout
        )

        main_layout.add_widget(
            scroll
        )

        # ====================================================
        # EDITAR PERFIL
        # ====================================================

        profile_button = Button(
            text="👤 EDITAR PERFIL",
            font_size="17sp",
            size_hint=(1, 0.07)
        )

        profile_button.bind(
            on_release=self.edit_profile
        )

        main_layout.add_widget(
            profile_button
        )

        # ====================================================
        # ATUALIZAR
        # ====================================================

        refresh_button = Button(
            text="🔄 ATUALIZAR PROGRESSO",
            font_size="17sp",
            size_hint=(1, 0.07)
        )

        refresh_button.bind(
            on_release=self.refresh_progress
        )

        main_layout.add_widget(
            refresh_button
        )

        # ====================================================
        # RESETAR
        # ====================================================

        reset_button = Button(
            text="🗑️ RESETAR PROGRESSO",
            font_size="17sp",
            size_hint=(1, 0.07)
        )

        reset_button.bind(
            on_release=self.confirm_reset
        )

        main_layout.add_widget(
            reset_button
        )

        # ====================================================
        # MENSAGEM
        # ====================================================

        self.refresh_label = Label(
            text="",
            font_size="14sp",
            size_hint=(1, 0.04)
        )

        main_layout.add_widget(
            self.refresh_label
        )

        # ====================================================
        # VOLTAR
        # ====================================================

        back_button = Button(
            text="🏠 VOLTAR AO MENU",
            font_size="17sp",
            size_hint=(1, 0.07)
        )

        back_button.bind(
            on_release=self.back_to_menu
        )

        main_layout.add_widget(
            back_button
        )

        # ====================================================
        # ADICIONAR
        # ====================================================

        self.add_widget(
            main_layout
        )

    # ========================================================
    # ENTRAR NA TELA
    # ========================================================

    def on_enter(self):

        self.load_progress()

    # ========================================================
    # PROGRESSO DO NÍVEL
    # ========================================================

    def get_level_progress(
        self,
        xp,
        level
    ):

        levels = [
            (1, 0, 100, "🛢️ Iniciante"),
            (2, 100, 250, "🔧 Aprendiz"),
            (3, 250, 500, "⚙️ Técnico"),
            (4, 500, 1000, "🧭 Explorador"),
            (5, 1000, 2000, "🛠️ Especialista"),
            (6, 2000, 5000, "👷 Engenheiro"),
            (7, 5000, 10000, "🏆 Mestre do Petróleo"),
            (8, 10000, None, "👑 Lenda do Petróleo")
        ]

        for (
            current_level,
            min_xp,
            max_xp,
            level_title
        ) in levels:

            if level == current_level:

                if max_xp is None:

                    return {
                        "current_xp": xp,
                        "required_xp": None,
                        "progress": 100,
                        "remaining_xp": 0,
                        "title": level_title
                    }

                level_xp = (
                    max_xp - min_xp
                )

                current_xp = xp - min_xp

                if current_xp < 0:
                    current_xp = 0

                progress = (
                    current_xp / level_xp
                ) * 100

                remaining_xp = (
                    max_xp - xp
                )

                if remaining_xp < 0:
                    remaining_xp = 0

                return {
                    "current_xp": current_xp,
                    "required_xp": level_xp,
                    "progress": progress,
                    "remaining_xp": remaining_xp,
                    "title": level_title
                }

        return {
            "current_xp": 0,
            "required_xp": 100,
            "progress": 0,
            "remaining_xp": 100,
            "title": "🛢️ Iniciante"
        }

    # ========================================================
    # ATUALIZAR
    # ========================================================

    def refresh_progress(self, instance):

        print(
            "🔄 ATUALIZANDO PROGRESSO..."
        )

        self.load_progress()

        self.refresh_label.text = (
            "✅ Progresso atualizado!"
        )

    # ========================================================
    # EDITAR PERFIL
    # ========================================================

    def edit_profile(self, instance):

        self.manager.current = "profile"

    # ========================================================
    # CONFIRMAR RESET
    # ========================================================

    def confirm_reset(self, instance):

        content = BoxLayout(
            orientation="vertical",
            spacing=15,
            padding=20
        )

        message = Label(
            text=(
                "⚠️ ATENÇÃO!\n\n"
                "Tens certeza que queres resetar "
                "todo o teu progresso?\n\n"
                "Esta ação não pode ser desfeita."
            ),
            font_size="18sp",
            halign="center",
            valign="middle"
        )

        message.bind(
            size=self.update_text_size
        )

        content.add_widget(
            message
        )

        buttons_layout = BoxLayout(
            spacing=10,
            size_hint_y=0.35
        )

        cancel_button = Button(
            text="CANCELAR",
            font_size="17sp"
        )

        reset_confirm_button = Button(
            text="RESETAR",
            font_size="17sp"
        )

        buttons_layout.add_widget(
            cancel_button
        )

        buttons_layout.add_widget(
            reset_confirm_button
        )

        content.add_widget(
            buttons_layout
        )

        popup = Popup(
            title="🗑️ RESETAR PROGRESSO",
            content=content,
            size_hint=(0.75, 0.55),
            auto_dismiss=False
        )

        cancel_button.bind(
            on_release=popup.dismiss
        )

        reset_confirm_button.bind(
            on_release=lambda instance:
            self.reset_progress(popup)
        )

        popup.open()

    # ========================================================
    # RESETAR PROGRESSO
    # ========================================================

    def reset_progress(self, popup):

        progress = self.load_progress_file()

        # Preservar o nome do jogador
        # para não obrigar nova configuração.

        player_name = progress.get(
            "player_name",
            ""
        )

        default_progress = {

            "player_name": player_name,

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

                "xp_earned": 0
            }
        }

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
                    default_progress,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            print(
                "🗑️ PROGRESSO RESETADO!"
            )

            popup.dismiss()

            self.load_progress()

            self.refresh_label.text = (
                "🗑️ Progresso resetado com sucesso!"
            )

        except Exception as error:

            print(
                "❌ ERRO AO RESETAR PROGRESSO:",
                error
            )

            popup.dismiss()

            self.refresh_label.text = (
                "❌ Não foi possível resetar o progresso."
            )

    # ========================================================
    # CARREGAR PROGRESSO
    # ========================================================

    def load_progress(
        self,
        instance=None
    ):

        print(
            f"📂 LENDO PROGRESSO: "
            f"{self.progress_file}"
        )

        if not os.path.exists(
            self.progress_file
        ):

            print(
                "⚠️ progress.json não encontrado."
            )

            self.show_empty_progress()

            return

        try:

            with open(
                self.progress_file,
                "r",
                encoding="utf-8"
            ) as file:

                progress = json.load(file)

        except json.JSONDecodeError as error:

            print(
                "❌ progress.json inválido:",
                error
            )

            self.show_empty_progress()

            return

        except Exception as error:

            print(
                "❌ ERRO AO CARREGAR:",
                error
            )

            self.show_empty_progress()

            return

        # ====================================================
        # PERFIL
        # ====================================================

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

        # ====================================================
        # ESTATÍSTICAS
        # ====================================================

        total_quizzes = progress.get(
            "total_quizzes",
            0
        )

        total_questions = progress.get(
            "total_questions",
            0
        )

        correct_answers = progress.get(
            "correct_answers",
            0
        )

        wrong_answers = progress.get(
            "wrong_answers",
            0
        )

        best_score = progress.get(
            "best_score",
            0
        )

        best_percentage = progress.get(
            "best_percentage",
            0
        )

        # ====================================================
        # STREAK
        # ====================================================

        current_streak = progress.get(
            "current_streak",
            0
        )

        best_streak = progress.get(
            "best_streak",
            0
        )

        last_quiz_date = progress.get(
            "last_quiz_date",
            None
        )

        # ====================================================
        # STATUS DO STREAK
        # ====================================================

        today = date.today()

        streak_status = ""
        last_quiz_status = ""

        if last_quiz_date:

            try:

                last_date = date.fromisoformat(
                    last_quiz_date
                )

                days_since_quiz = (
                    today - last_date
                ).days

                if days_since_quiz == 0:

                    streak_status = (
                        "🟢 SEQUÊNCIA ATIVA"
                    )

                    last_quiz_status = (
                        "📅 Último quiz: HOJE"
                    )

                elif days_since_quiz == 1:

                    streak_status = (
                        "⚠️ JOGA HOJE PARA "
                        "MANTER A SEQUÊNCIA!"
                    )

                    last_quiz_status = (
                        "📅 Último quiz: ONTEM"
                    )

                elif days_since_quiz > 1:

                    streak_status = (
                        "🔴 SEQUÊNCIA QUEBRADA"
                    )

                    last_quiz_status = (
                        f"📅 Último quiz: "
                        f"HÁ {days_since_quiz} DIAS"
                    )

                else:

                    streak_status = (
                        "🟢 SEQUÊNCIA ATIVA"
                    )

                    last_quiz_status = (
                        "📅 Último quiz: HOJE"
                    )

            except (
                ValueError,
                TypeError
            ):

                streak_status = (
                    "⚠️ DATA DO QUIZ INVÁLIDA"
                )

                last_quiz_status = (
                    "📅 Último quiz: desconhecido"
                )

        else:

            if current_streak > 0:

                streak_status = (
                    "⚠️ JOGA HOJE PARA "
                    "MANTER A SEQUÊNCIA!"
                )

            else:

                streak_status = (
                    "⚪ NENHUMA SEQUÊNCIA ATIVA"
                )

            last_quiz_status = (
                "📅 Último quiz: "
                "ainda não realizado"
            )

        # ====================================================
        # XP
        # ====================================================

        xp = progress.get(
            "xp",
            0
        )

        level = progress.get(
            "level",
            1
        )

        title = progress.get(
            "title",
            "🛢️ Iniciante"
        )

        level_progress = self.get_level_progress(
            xp,
            level
        )

        current_xp = level_progress[
            "current_xp"
        ]

        required_xp = level_progress[
            "required_xp"
        ]

        progress_percentage = level_progress[
            "progress"
        ]

        remaining_xp = level_progress[
            "remaining_xp"
        ]

        self.xp_bar.value = min(
            max(progress_percentage, 0),
            100
        )

        self.xp_percentage_label.text = (
            f"{progress_percentage:.0f}%"
        )

        # ====================================================
        # CATEGORIAS
        # ====================================================

        categories_played = progress.get(
            "categories_played",
            {}
        )

        # ====================================================
        # DIFICULDADES
        # ====================================================

        difficulty_played = progress.get(
            "difficulty_played",
            {}
        )

        if not isinstance(
            difficulty_played,
            dict
        ):

            difficulty_played = {}

        difficulty_played.setdefault(
            "Fácil",
            0
        )

        difficulty_played.setdefault(
            "Médio",
            0
        )

        difficulty_played.setdefault(
            "Difícil",
            0
        )

        # ====================================================
        # ÚLTIMO QUIZ
        # ====================================================

        last_quiz = progress.get(
            "last_quiz",
            {}
        )

        if not isinstance(
            last_quiz,
            dict
        ):

            last_quiz = {}

        # ====================================================
        # CONQUISTAS
        # ====================================================

        achievements = progress.get(
            "achievements",
            []
        )

        if not isinstance(
            achievements,
            list
        ):

            achievements = []

        all_achievements = get_all_achievements()

        total_achievements = len(
            all_achievements
        )

        unlocked_achievements = min(
            len(achievements),
            total_achievements
        )

        # ====================================================
        # RECOMPENSAS
        # ====================================================

        rewards = progress.get(
            "rewards",
            []
        )

        if not isinstance(
            rewards,
            list
        ):

            rewards = []

        all_rewards = get_all_rewards()

        total_rewards = len(
            all_rewards
        )

        unlocked_rewards = min(
            len(rewards),
            total_rewards
        )

        # ====================================================
        # PRECISÃO
        # ====================================================

        if total_questions > 0:

            accuracy = (
                correct_answers
                / total_questions
            ) * 100

        else:

            accuracy = 0

        # ====================================================
        # PERFIL
        # ====================================================

        self.profile_label.text = (

            "👤 PERFIL DO JOGADOR\n\n"

            f"Olá, {player_name}!\n"

            f"{title}\n"

            f"🏆 Nível {level}"
        )

        # ====================================================
        # RESUMO
        # ====================================================

        self.summary_label.text = (

            "📈 RESUMO GERAL\n\n"

            f"🔥 Quizzes realizados: "
            f"{total_quizzes}\n"

            f"📝 Perguntas respondidas: "
            f"{total_questions}\n"

            f"✅ Respostas corretas: "
            f"{correct_answers}\n"

            f"📚 Categorias exploradas: "
            f"{len(categories_played)}\n"

            f"🏆 Conquistas: "
            f"{unlocked_achievements}/"
            f"{total_achievements}\n"

            f"🎁 Recompensas: "
            f"{unlocked_rewards}/"
            f"{total_rewards}"
        )

        # ====================================================
        # STREAK
        # ====================================================

        if current_streak > 0:

            self.streak_label.text = (

                "🔥 SEQUÊNCIA DIÁRIA\n\n"

                f"🔥 STREAK ATUAL: "
                f"{current_streak} DIAS\n"

                f"🏆 MELHOR STREAK: "
                f"{best_streak} DIAS\n\n"

                f"{streak_status}\n"

                f"{last_quiz_status}\n\n"

                "💪 Continua assim!"
            )

        else:

            self.streak_label.text = (

                "🔥 SEQUÊNCIA DIÁRIA\n\n"

                "🔥 STREAK ATUAL: 0 DIAS\n"

                f"🏆 MELHOR STREAK: "
                f"{best_streak} DIAS\n\n"

                f"{streak_status}\n"

                f"{last_quiz_status}\n\n"

                "🎯 Completa um quiz para "
                "começar uma sequência!"
            )

        # ====================================================
        # XP / NÍVEL
        # ====================================================

        if required_xp is None:

            self.xp_label.text = (

                "⭐ EXPERIÊNCIA\n\n"

                f"💎 XP TOTAL: {xp}\n"

                f"🏆 NÍVEL {level}\n"

                f"👑 {title}\n\n"

                "🔥 NÍVEL MÁXIMO ATINGIDO!\n"

                "💯 PROGRESSO COMPLETO"
            )

        else:

            self.xp_label.text = (

                "⭐ EXPERIÊNCIA\n\n"

                f"💎 XP TOTAL: {xp}\n"

                f"🏆 NÍVEL {level}  |  "
                f"👑 {title}\n\n"

                f"📈 PROGRESSO: "
                f"{progress_percentage:.0f}%\n"

                f"⚡ XP NO NÍVEL: "
                f"{current_xp}/{required_xp}\n"

                f"🔥 FALTAM {remaining_xp} XP "
                f"PARA O PRÓXIMO NÍVEL"
            )

        # ====================================================
        # DESEMPENHO
        # ====================================================

        self.performance_label.text = (

            "🎯 DESEMPENHO GERAL\n\n"

            f"📊 Precisão: "
            f"{accuracy:.1f}%\n"

            f"📝 Respostas: "
            f"{total_questions}\n"

            f"✅ Corretas: "
            f"{correct_answers}\n"

            f"❌ Erradas: "
            f"{wrong_answers}\n\n"

            f"🥇 Melhor pontuação: "
            f"{best_score}\n"

            f"🔥 Melhor resultado: "
            f"{best_percentage:.1f}%"
        )

        # ====================================================
        # DIFICULDADE
        # ====================================================

        self.difficulty_label.text = (

            "🎯 QUIZZES POR DIFICULDADE\n\n"

            f"🟢 Fácil: "
            f"{difficulty_played.get('Fácil', 0)} quiz(es)\n"

            f"🟡 Médio: "
            f"{difficulty_played.get('Médio', 0)} quiz(es)\n"

            f"🔴 Difícil: "
            f"{difficulty_played.get('Difícil', 0)} quiz(es)"
        )

        # ====================================================
        # ÚLTIMO QUIZ
        # ====================================================

        if last_quiz:

            last_mode = last_quiz.get(
                "mode",
                ""
            )

            last_difficulty = last_quiz.get(
                "difficulty",
                ""
            )

            last_score = last_quiz.get(
                "score",
                0
            )

            last_total = last_quiz.get(
                "total",
                0
            )

            last_percentage = last_quiz.get(
                "percentage",
                0
            )

            last_xp = last_quiz.get(
                "xp_earned",
                0
            )

            if last_total > 0:

                self.last_quiz_label.text = (

                    "🕐 ÚLTIMO QUIZ\n\n"

                    f"📚 {last_mode}\n"

                    f"🎯 {last_difficulty}\n"

                    f"🏆 Resultado: "
                    f"{last_score}/{last_total}\n"

                    f"📊 Percentagem: "
                    f"{last_percentage:.1f}%\n"

                    f"⭐ XP ganho: "
                    f"{last_xp}\n\n"

                    f"{last_quiz_status}"
                )

            else:

                self.last_quiz_label.text = (
                    "🕐 ÚLTIMO QUIZ\n\n"
                    "Ainda não realizaste nenhum quiz."
                )

        else:

            self.last_quiz_label.text = (
                "🕐 ÚLTIMO QUIZ\n\n"
                "Ainda não realizaste nenhum quiz."
            )

        # ====================================================
        # CATEGORIAS
        # ====================================================

        if categories_played:

            categories_text = (
                "📚 CATEGORIAS EXPLORADAS\n\n"
            )

            for category, amount in (
                categories_played.items()
            ):

                categories_text += (
                    f"• {category}: "
                    f"{amount} quiz(es)\n"
                )

            self.categories_label.text = (
                categories_text
            )

        else:

            self.categories_label.text = (
                "📚 CATEGORIAS EXPLORADAS\n\n"
                "Nenhuma categoria jogada ainda."
            )

        # ====================================================
        # CONQUISTAS
        # ====================================================

        if unlocked_achievements > 0:

            self.achievements_label.text = (

                "🏆 CONQUISTAS\n\n"

                f"Desbloqueadas: "
                f"{unlocked_achievements}/"
                f"{total_achievements}\n\n"

                "Continua a jogar para desbloquear "
                "mais conquistas! 🔥"
            )

        else:

            self.achievements_label.text = (

                "🏆 CONQUISTAS\n\n"

                f"Desbloqueadas: "
                f"0/{total_achievements}\n\n"

                "Completa quizzes para começar!"
            )

        # ====================================================
        # RECOMPENSAS
        # ====================================================

        if unlocked_rewards > 0:

            reward_lines = [
                "🎁 RECOMPENSAS",
                "",
                f"Desbloqueadas: "
                f"{unlocked_rewards}/"
                f"{total_rewards}",
                ""
            ]

            for reward in rewards:

                if isinstance(
                    reward,
                    dict
                ):

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

                    reward_lines.append(
                        f"{icon} {name}"
                    )

                    if reward_text:

                        reward_lines.append(
                            f"🎁 {reward_text}"
                        )

            self.rewards_label.text = (
                "\n".join(reward_lines)
            )

        else:

            self.rewards_label.text = (

                "🎁 RECOMPENSAS\n\n"

                f"Desbloqueadas: "
                f"0/{total_rewards}\n\n"

                "Sobe de nível para desbloquear "
                "novas recompensas!"
            )

        # ====================================================
        # DEBUG
        # ====================================================

        print(
            "👤 JOGADOR:",
            player_name
        )

        print(
            "⭐ XP TOTAL:",
            xp
        )

        print(
            "🏆 NÍVEL:",
            level
        )

        print(
            "📈 PROGRESSO:",
            f"{progress_percentage:.1f}%"
        )

        print(
            "🔥 STREAK:",
            current_streak
        )

        print(
            "🏆 MELHOR STREAK:",
            best_streak
        )

        print(
            "🎁 RECOMPENSAS:",
            f"{unlocked_rewards}/{total_rewards}"
        )

        print(
            "📅 ÚLTIMO QUIZ:",
            last_quiz_date
        )

        print(
            "✅ PROGRESSO CARREGADO!"
        )

    # ========================================================
    # SEM PROGRESSO
    # ========================================================

    def show_empty_progress(self):

        all_rewards = get_all_rewards()
        total_rewards = len(all_rewards)

        all_achievements = get_all_achievements()
        total_achievements = len(all_achievements)

        progress = self.load_progress_file()

        player_name = progress.get(
            "player_name",
            "Jogador"
        )

        self.profile_label.text = (
            "👤 PERFIL DO JOGADOR\n\n"
            f"Olá, {player_name}!\n"
            "🛢️ Iniciante\n"
            "🏆 Nível 1"
        )

        self.summary_label.text = (
            "📈 RESUMO GERAL\n\n"
            "Ainda não tens progresso.\n\n"
            f"🏆 Conquistas: "
            f"0/{total_achievements}\n"
            f"🎁 Recompensas: "
            f"0/{total_rewards}"
        )

        self.streak_label.text = (
            "🔥 SEQUÊNCIA DIÁRIA\n\n"
            "🔥 STREAK ATUAL: 0 DIAS\n"
            "🏆 MELHOR STREAK: 0 DIAS\n\n"
            "⚪ NENHUMA SEQUÊNCIA ATIVA\n"
            "📅 Último quiz: ainda não realizado\n\n"
            "🎯 Completa um quiz para começar!"
        )

        self.xp_label.text = (
            "⭐ EXPERIÊNCIA\n\n"
            "💎 XP TOTAL: 0\n"
            "🏆 NÍVEL 1  |  👑 🛢️ Iniciante\n\n"
            "📈 PROGRESSO: 0%\n"
            "⚡ XP NO NÍVEL: 0/100\n"
            "🔥 FALTAM 100 XP PARA O PRÓXIMO NÍVEL"
        )

        self.xp_bar.value = 0

        self.xp_percentage_label.text = "0%"

        self.performance_label.text = (
            "🎯 DESEMPENHO GERAL\n\n"
            "Faz o teu primeiro quiz!"
        )

        self.difficulty_label.text = (
            "🎯 QUIZZES POR DIFICULDADE\n\n"
            "🟢 Fácil: 0 quiz(es)\n"
            "🟡 Médio: 0 quiz(es)\n"
            "🔴 Difícil: 0 quiz(es)"
        )

        self.last_quiz_label.text = (
            "🕐 ÚLTIMO QUIZ\n\n"
            "Nenhum quiz realizado."
        )

        self.categories_label.text = (
            "📚 CATEGORIAS EXPLORADAS\n\n"
            "Nenhuma categoria jogada."
        )

        self.achievements_label.text = (
            "🏆 CONQUISTAS\n\n"
            "Nenhuma conquista desbloqueada.\n"
            f"0/{total_achievements}"
        )

        self.rewards_label.text = (
            "🎁 RECOMPENSAS\n\n"
            "Nenhuma recompensa desbloqueada.\n"
            f"0/{total_rewards}\n\n"
            "Sobe de nível para começar!"
        )

    # ========================================================
    # CARREGAR FICHEIRO
    # ========================================================

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

        except Exception as error:

            print(
                "❌ ERRO AO LER PROGRESS.JSON:",
                error
            )

            return {}

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
            instance.width - 30,
            None
        )