from textual.app import App , ComposeResult
from textual.widgets import Header , Footer , Button , Static

class Launcher(App):
    CSS_PATH = "style.tcss" # import file css
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(
            "[bold cyan]⚡ CYBER LAUNCHER TUI ⚡[/bold cyan]\n\n"
            "Tampilan ini diatur 100% dari file [yellow]style.tcss[/yellow]!",
            id="kotak-launcher"
        )
        yield Button("Buka APP")
        yield Footer()

if __name__ == "__main__" :
    app = Launcher()
    app.run()