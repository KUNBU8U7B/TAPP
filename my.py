from textual.app import App , ComposeResult
from textual.widgets import Header , Footer , Button , Static
from textual.containers import Horizontal , Vertical

class Launcher(App):
    on_btn = False
    # CSS_PATH = "style.tcss" # import file css
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Hello")
        yield Static("button : off" , id="text-b")
        yield Button("Clicks" , id="btn-1")
        yield Static("kondisi : " , id="text-c")
        yield Horizontal(
            Button("Setuju" , id="yes"),
            Button("Tidak Setuju" , id="no")
        )

    def on_button_pressed(self , event : Button.Pressed) -> None:
        if event.button.id == "btn-1":
            self.query_one("#text-b" , Static).update("button : on" if self.on_btn else "button : off")
            self.on_btn = not self.on_btn

        elif event.button.id == "yes":
            self.query_one("#text-c" , Static).update("Kondisi : Setuju")
        elif event.button.id == "no":
            self.query_one("#text-c" , Static).update("Kondisi : Tidak Setuju")


if __name__ == "__main__" :
    app = Launcher()
    app.run()