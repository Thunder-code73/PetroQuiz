from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView


class CategoriesScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout principal
        main_layout = BoxLayout(
            orientation="vertical",
            padding=25,
            spacing=15
        )

        # ====================================================
        # TÍTULO
        # ====================================================

        title = Label(
            text="📚 CATEGORIAS",
            font_size="38sp",
            bold=True,
            size_hint=(1, 0.12)
        )

        main_layout.add_widget(title)

        # ====================================================
        # SUBTÍTULO
        # ====================================================

        subtitle = Label(
            text="Escolhe uma área para testar os teus conhecimentos",
            font_size="18sp",
            size_hint=(1, 0.08)
        )

        main_layout.add_widget(subtitle)

        # ====================================================
        # ÁREA DE SCROLL
        # ====================================================

        scroll = ScrollView()

        categories_layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint_y=None
        )

        categories_layout.bind(
            minimum_height=categories_layout.setter(
                "height"
            )
        )

        # ====================================================
        # CATEGORIAS
        # ====================================================

        categories = [
            "🧭 EXPLORAÇÃO",
            "🪨 GEOLOGIA",
            "📡 GEOFÍSICA",
            "🛠️ PERFURAÇÃO",
            "⚙️ PRODUÇÃO",
            "🏭 PROCESSAMENTO",
            "🚢 TRANSPORTE",
            "🔥 REFINAÇÃO",
            "⛽ DISTRIBUIÇÃO",
            "🦺 HSE",
            "🌱 AMBIENTE",
            "💰 ECONOMIA",
            "🇦🇴 PETRÓLEO EM ANGOLA"
        ]

        for category in categories:

            button = Button(
                text=category,
                font_size="20sp",
                size_hint_y=None,
                height=55
            )

            button.bind(
                on_press=lambda instance,
                category=category:
                self.select_category(category)
            )

            categories_layout.add_widget(button)

        scroll.add_widget(categories_layout)

        main_layout.add_widget(scroll)

        # ====================================================
        # BOTÃO VOLTAR
        # ====================================================

        back_button = Button(
            text="VOLTAR AO MENU",
            font_size="18sp",
            size_hint=(1, 0.10)
        )

        back_button.bind(
            on_press=self.back_to_menu
        )

        main_layout.add_widget(back_button)

        self.add_widget(main_layout)

    # ========================================================
    # SELECIONAR CATEGORIA
    # ========================================================

    def select_category(self, category):

        print(
            f"CATEGORIA SELECIONADA: {category}"
        )

        # Guardar categoria escolhida
        self.manager.selected_category = category

        # Ir para o quiz
        self.manager.current = "quiz_config"

    # ========================================================
    # VOLTAR
    # ========================================================

    def back_to_menu(self, instance):

        self.manager.current = "main"