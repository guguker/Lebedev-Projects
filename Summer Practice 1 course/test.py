import flet as ft

class StyledButton(ft.GestureDetector):
    def __init__(self):
        super().__init__()
        self.mouse_cursor = ft.MouseCursor.CLICK
        self.content = ft.Container(
            content=ft.Text(value=""),
            width=0,
            height=0,
            bgcolor=None,
            border_radius=0,
            padding=0,
            alignment=ft.alignment.center
        )

    def set_text(self, text: str, text_color: str = ft.Colors.WHITE, font_size: int = 16, font_family: str = None):
        self.content.content.value = text
        self.content.content.color = text_color
        self.content.content.size = font_size
        self.content.content.font_family = font_family
        return self

    def set_size(self, width: float, height: float, padding: int = 10):
        self.content.width = width
        self.content.height = height
        self.content.padding = padding
        return self

    def set_style(self, bgcolor: str, border_radius: int = 8):
        self.content.bgcolor = bgcolor
        self.content.border_radius = border_radius
        return self

    def set_action(self, on_click):
        self.on_tap = on_click
        return self

def main(page: ft.Page):
    page.title = "Balance Game"
    page.window_width = 800
    page.window_height = 1000
    page.bgcolor = ft.Colors.DEEP_PURPLE_900

    game_paused = False

    def start_game_handler(e):
        page.clean()
        render_game_screen()

    def render_start_screen():
        page.overlay.clear()
        page.clean()
        
        def on_custom_click(e):
            start_game_handler(e)
        
        page.add(
            ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("BALANCE GAME 🥴", size=60, color="white"),
                                StyledButton()
                                    .set_text("Начать игру", text_color=ft.Colors.BLACK, font_size=20)
                                    .set_size(200, 60)
                                    .set_style(ft.Colors.BLUE_GREY, border_radius=20)
                                    .set_action(on_custom_click),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            expand=True
                        ),
                        alignment=ft.alignment.center_right,
                        width=page.window_width,
                        height=page.window_height,
                    ),
            )

    def handle_pause(e):
        nonlocal game_paused
        game_paused = not game_paused
        if game_paused:
            render_pause_menu()
        else:
            page.overlay.clear()
            page.update()

    def render_pause_menu():
        page.overlay.clear()
        pause_menu = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Игра на паузе! Отдохни :)", size=25, color="white"),
                    ft.ElevatedButton("Продолжить игру", on_click=handle_pause),
                    ft.ElevatedButton("Музыка: Вкл/Выкл", on_click=lambda e: print("Музыка переключена")),
                    ft.ElevatedButton("Выйти", on_click=lambda e: render_start_screen()),
                ],
                tight=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=ft.Colors.BLACK87,
            padding=30,
            border_radius=10,
            alignment=ft.alignment.center,
        )
        page.overlay.append(pause_menu)
        page.update()

    def render_game_screen():
        pause_button = ft.IconButton(icon=ft.Icons.PAUSE, on_click=handle_pause)

        page.add(
            ft.Stack(
                [
                    ft.Row([pause_button], alignment=ft.MainAxisAlignment.END),
                ]
            )
        )

    render_start_screen()

ft.app(main)