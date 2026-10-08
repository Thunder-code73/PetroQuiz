import json
import os

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class ProfileScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ====================================================
        # CAMINHO DO PROJETO
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
            padding=35,
            spacing=12
        )

        # ====================================================
        # TÍTULO
        # ====================================================

        self.title_label = Label(
            text="🛢️ PETROQUIZ",
            font_size="40sp",
            bold=True,
            size_hint=(1, 0.15)
        )

        main_layout.add_widget(
            self.title_label
        )

        # ====================================================
        # CABEÇALHO
        # ====================================================

        self.welcome_label = Label(
            text="👤 BEM-VINDO!",
            font_size="28sp",
            bold=True,
            halign="center",
            valign="middle",
            size_hint=(1, 0.12)
        )

        self.welcome_label.bind(
            size=self.update_text_size
        )

        main_layout.add_widget(
            self.welcome_label
        )

        # ====================================================
        # DESCRIÇÃO
        # ====================================================

        self.question_label = Label(
            text="Como devemos chamar-te?",
            font_size="21sp",
            halign="center",
            valign="middle",
            size_hint=(1, 0.10)
        )

        self.question_label.bind(
            size=self.update_text_size
        )

        main_layout.add_widget(
            self.question_label
        )

        # ====================================================
        # CAMPO DO NOME
        # ====================================================

        self.name_input = TextInput(
            hint_text="Digite o teu nome",
            multiline=False,
            font_size="21sp",
            size_hint=(1, 0.10),
            padding=[15, 10]
        )

        self.name_input.bind(
            on_text_validate=self.save_name
        )

        main_layout.add_widget(
            self.name_input
        )

        # ====================================================
        # MENSAGEM
        # ====================================================

        self.info_label = Label(
            text="",
            font_size="15sp",
            halign="center",
            valign="middle",
            size_hint=(1, 0.10)
        )

        self.info_label.bind(
            size=self.update_text_size
        )

        main_layout.add_widget(
            self.info_label
        )

        # ====================================================
        # BOTÃO PRINCIPAL
        # ====================================================

        self.save_button = Button(
            text="💾 COMEÇAR",
            font_size="20sp",
            bold=True,
            size_hint=(1, 0.12)
        )

        self.save_button.bind(
            on_release=self.save_name
        )

        main_layout.add_widget(
            self.save_button
        )

        # ====================================================
        # BOTÃO VOLTAR
        # ====================================================

        self.back_button = Button(
            text="⬅️ VOLTAR",
            font_size="17sp",
            size_hint=(1, 0.08)
        )

        self.back_button.bind(
            on_release=self.go_back
        )

        main_layout.add_widget(
            self.back_button
        )

        # ====================================================
        # INFORMAÇÃO
        # ====================================================

        self.footer_label = Label(
            text=(
                "O teu progresso será guardado "
                "automaticamente neste dispositivo."
            ),
            font_size="14sp",
            halign="center",
            valign="middle",
            size_hint=(1, 0.10)
        )

        self.footer_label.bind(
            size=self.update_text_size
        )

        main_layout.add_widget(
            self.footer_label
        )

        # ====================================================
        # ADICIONAR LAYOUT
        # ====================================================

        self.add_widget(
            main_layout
        )

    # ========================================================
    # ENTRAR NA TELA
    # ========================================================

    def on_enter(self):

        self.info_label.text = ""

        saved_name = self.get_saved_name()

        # ====================================================
        # PRIMEIRA CONFIGURAÇÃO
        # ====================================================

        if not saved_name:

            self.title_label.text = "🛢️ PETROQUIZ"

            self.welcome_label.text = (
                "👤 BEM-VINDO!"
            )

            self.question_label.text = (
                "Como devemos chamar-te?"
            )

            self.name_input.text = ""

            self.name_input.hint_text = (
                "Digite o teu nome"
            )

            self.save_button.text = (
                "💾 COMEÇAR"
            )

            self.back_button.opacity = 0
            self.back_button.disabled = True

        # ====================================================
        # EDIÇÃO DO PERFIL
        # ====================================================

        else:

            self.title_label.text = (
                "👤 MEU PERFIL"
            )

            self.welcome_label.text = (
                f"Olá, {saved_name}!"
            )

            self.question_label.text = (
                "Altera o teu nome:"
            )

            self.name_input.text = saved_name

            self.name_input.hint_text = (
                "Digite o novo nome"
            )

            self.save_button.text = (
                "💾 GUARDAR ALTERAÇÕES"
            )

            self.back_button.opacity = 1
            self.back_button.disabled = False

        self.name_input.focus = True

    # ========================================================
    # OBTER NOME GUARDADO
    # ========================================================

    def get_saved_name(self):

        progress = self.load_progress_file()

        player_name = progress.get(
            "player_name",
            ""
        )

        if not isinstance(
            player_name,
            str
        ):
            return ""

        return player_name.strip()

    # ========================================================
    # SALVAR NOME
    # ========================================================

    def save_name(self, instance=None):

        player_name = self.name_input.text.strip()

        # ====================================================
        # NOME VAZIO
        # ====================================================

        if not player_name:

            self.info_label.text = (
                "⚠️ Digita o teu nome primeiro."
            )

            self.name_input.focus = True

            return

        # ====================================================
        # LIMITE DE CARACTERES
        # ====================================================

        if len(player_name) > 20:

            self.info_label.text = (
                "⚠️ O nome deve ter no máximo "
                "20 caracteres."
            )

            self.name_input.focus = True

            return

        # ====================================================
        # CARREGAR PROGRESSO
        # ====================================================

        progress = self.load_progress_file()

        old_name = progress.get(
            "player_name",
            ""
        )

        # ====================================================
        # ATUALIZAR NOME
        # ====================================================

        progress["player_name"] = player_name

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
                "👤 NOME DO JOGADOR SALVO:",
                player_name
            )

            # =================================================
            # PRIMEIRA CONFIGURAÇÃO
            # =================================================

            if not old_name:

                self.manager.current = "main"

            # =================================================
            # EDIÇÃO DO PERFIL
            # =================================================

            else:

                self.info_label.text = (
                    "✅ Nome atualizado com sucesso!"
                )

                self.welcome_label.text = (
                    f"Olá, {player_name}!"
                )

                self.manager.current = "main"

        except Exception as error:

            print(
                "❌ ERRO AO SALVAR NOME:",
                error
            )

            self.info_label.text = (
                "❌ Não foi possível salvar o nome."
            )

    # ========================================================
    # VOLTAR
    # ========================================================

    def go_back(self, instance=None):

        self.manager.current = "main"

    # ========================================================
    # CARREGAR PROGRESS.JSON
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

        except FileNotFoundError:

            return {}

        except json.JSONDecodeError:

            print(
                "❌ progress.json contém JSON inválido."
            )

            return {}

        except Exception as error:

            print(
                "❌ ERRO AO LER PROGRESS.JSON:",
                error
            )

            return {}

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