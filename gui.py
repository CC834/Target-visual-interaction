from nicegui import ui

class MyApp:
    def __init__(self):
        self.setup_ui()

    def setup_ui(self):
        with ui:
            ui.label('Welcome to my NiceGUI App!', style='font-size: 20px; color: blue')
            self.button = ui.button('Click me!', on_click=self.on_button_click)

    def on_button_click(self, event):
        self.button.text = 'You clicked me!'

if __name__ == '__main__':
    app = MyApp()
    ui.run()
