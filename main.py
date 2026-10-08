import json
import os

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

from screens.main_screen import MainScreen
from screens.quiz_screen import QuizScreen
from screens.categories_screen import CategoriesScreen
from screens.quiz_config_screen import QuizConfigScreen
from screens.progress_screen import ProgressScreen
from screens.about_screen import AboutScreen
from screens.results_screen import ResultsScreen
from screens.achievements_screen import AchievementsScreen
from screens.rewards_screen import RewardsScreen
from screens.profile_screen import ProfileScreen


# ============================================================
# CONFIGURAÇÕES
# ============================================================

# No Android, o Kivy usa automaticamente o tamanho do ecrã.
# No Windows, mantemos uma janela confortável para desenvolvimento.
if "ANDROID_ARGUMENT" not in os.environ:
    Window.size = (1000, 650)


# ============================================================
# APLICAÇÃO
# ============================================================

class PetroQuizApp(App):

    def build(self):

        screen_manager = ScreenManager()

        # ====================================================
        # CAMINHO DO PROGRESSO
        # ====================================================

        base_dir = os.path.dirname(
            os.path.abspath(__file__)
        )

        # ====================================================
        # ARMAZENAMENTO DO PROGRESSO
        # ====================================================
        # O Android permite escrever na pasta de utilizador do app.
        # No Windows, continuamos a usar a pasta data do projeto.
        if "ANDROID_ARGUMENT" in os.environ:
            data_dir = self.user_data_dir
        else:
            data_dir = os.path.join(base_dir, "data")

        os.makedirs(data_dir, exist_ok=True)

        progress_file = os.path.join(
            data_dir,
            "progress.json"
        )

        # Disponibilizar o caminho para as outras telas, se necessário.
        screen_manager.progress_file = progress_file

        # ====================================================
        # ESTADO GLOBAL DO JOGO
        # ====================================================

        screen_manager.selected_category = None
        screen_manager.new_achievements = []
        screen_manager.new_rewards = []
        screen_manager.level_up = None

        # ====================================================
        # ADICIONAR TELAS
        # ====================================================

        screen_manager.add_widget(
            ProfileScreen(name="profile")
        )

        screen_manager.add_widget(
            MainScreen(name="main")
        )

        screen_manager.add_widget(
            QuizScreen(name="quiz")
        )

        screen_manager.add_widget(
            CategoriesScreen(name="categories")
        )

        screen_manager.add_widget(
            QuizConfigScreen(name="quiz_config")
        )

        screen_manager.add_widget(
            ProgressScreen(name="progress")
        )

        screen_manager.add_widget(
            AboutScreen(name="about")
        )

        screen_manager.add_widget(
            ResultsScreen(name="results")
        )

        screen_manager.add_widget(
            AchievementsScreen(name="achievements")
        )

        screen_manager.add_widget(
            RewardsScreen(name="rewards")
        )

        # ====================================================
        # DECIDIR TELA INICIAL
        # ====================================================

        player_name = self.get_player_name(
            progress_file
        )

        if player_name:

            print(
                "👤 JOGADOR ENCONTRADO:",
                player_name
            )

            print(
                "🏠 A ENTRAR DIRETAMENTE NO MENU..."
            )

            screen_manager.current = "main"

        else:

            print(
                "👤 NENHUM JOGADOR ENCONTRADO."
            )

            print(
                "🎬 A ABRIR CONFIGURAÇÃO INICIAL..."
            )

            screen_manager.current = "profile"

        return screen_manager

    # ========================================================
    # OBTER NOME DO JOGADOR
    # ========================================================

    def get_player_name(
        self,
        progress_file
    ):

        # ====================================================
        # VERIFICAR SE O ARQUIVO EXISTE
        # ====================================================

        if not os.path.exists(
            progress_file
        ):

            print(
                "⚠️ progress.json ainda não existe."
            )

            return ""

        # ====================================================
        # LER PROGRESSO
        # ====================================================

        try:

            with open(
                progress_file,
                "r",
                encoding="utf-8"
            ) as file:

                progress = json.load(file)

            # =================================================
            # OBTER NOME
            # =================================================

            player_name = progress.get(
                "player_name",
                ""
            )

            # Garantir que seja texto
            if not isinstance(
                player_name,
                str
            ):

                return ""

            return player_name.strip()

        except FileNotFoundError:

            return ""

        except json.JSONDecodeError:

            print(
                "❌ progress.json contém JSON inválido."
            )

            return ""

        except Exception as error:

            print(
                "❌ ERRO AO LER progress.json:",
                error
            )

            return ""


# ============================================================
# EXECUTAR
# ============================================================

if __name__ == "__main__":
    PetroQuizApp().run()