from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class AboutScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=50,
            spacing=20
        )

        layout.add_widget(
            Label(
                text="ℹ️ SOBRE O PETROQUIZ",
                font_size="40sp",
                bold=True
            )
        )

        layout.add_widget(
            Label(
                text="Aplicativo educativo sobre a indústria petrolífera.",
                font_size="22sp"
            )
        )

        back_button = Button(
            text="VOLTAR AO MENU",
            size_hint=(0.6, 0.15),
            pos_hint={"center_x": 0.5}
        )

        back_button.bind(
            on_press=lambda instance: self.go_to("main")
        )

        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_to(self, screen_name):
        self.manager.current = screen_name