import flet as ft


def main(page: ft.Page):
    page.title = "Игра Найди пары"
    page.window.width = 600
    page.window.height = 600
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    print(page.window.width, page.window.height)

    page.add(
        ft.Stack(  # Используем Stack для наложения элементов
            controls=[

                ft.Image(
                    src="/Users/guguk/Documents/Lebedev-Projects/Summer Practice 1 course/bg.jpg",  # Путь к изображению
                    fit=ft.ImageFit.COVER,  # Растянуть изображение
                    width=page.window.width,
                    height=page.window.height,
                ),
                ft.Row(
                [
                    ft.Text(
                        "Image title",
                        color=ft.Colors.ON_SURFACE,
                        size=20,
                        weight=ft.FontWeight.BOLD,  
                        text_align=ft.alignment.top_center,     
                    )
                ],
                left = page.window.width / 2,  # Центрирование по горизонтали
                top = page.window.height / 2,  # Центрирование по вертикали 
                expand=True,  # Контейнер займет все доступное пространство  
                vertical_alignment=  ft.alignment.top_center,  # Центрирование по вертикали
                alignment=ft.alignment.top_center,  # Центрирование по горизонтали
            ),
        ],
        )
        
    )

    page.update()

ft.app(main)
