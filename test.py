from nicegui import ui

username = ui.input('username')
ui.button('Show Username',on_click=lambda: show_username())


def show_username():
    internal_var = username.value
    print(internal_var)

ui.run()
