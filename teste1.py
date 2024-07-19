from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl

def teste(dados):
    session = PromptSession()
    
    
    start = 0
    display_limit = 10

    def get_display_text():
        return "\n".join(dados[start:start + display_limit])

    bindings = KeyBindings()

    @bindings.add('q')
    def _(event):
        event.app.exit()

    @bindings.add('down')
    def _(event):
        nonlocal start
        if start + display_limit < len(dados):
            start += 1
            display_text.text = get_display_text()

    @bindings.add('up')
    def _(event):
        nonlocal start
        if start > 0:
            start -= 1
            display_text.text = get_display_text()

    display_text = FormattedTextControl(text=get_display_text)
    window = Window(content=display_text, wrap_lines=True)
    layout = Layout(HSplit([window]))

    app = session.app
    app.layout = layout
    app.key_bindings = bindings

    app.run()


t = input("Digite 1: ")
data = [f"Item {i}" for i in range(100)]
if t == '1':
    teste(dados=data)

from prompt_toolkit.shortcuts import radiolist_dialog

result = radiolist_dialog(
    title="RadioList dialog",
    text="Which breakfast would you like ?",
    values=[
        ("breakfast1", "Eggs and beacon"),
        ("breakfast2", "French breakfast"),
        ("breakfast3", "Equestrian breakfast")
    ]
).run()