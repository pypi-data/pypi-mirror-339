from textual_englyph import EnGlyphText
from textual.app import App, ComposeResult
from textual.widgets import Button, Label
from textual.containers import Vertical


class Test(App):
    fsize = 11

    def compose(self) -> ComposeResult:
        with Vertical():
            self.enhello = EnGlyphText("Hello Textual!", id="enhello")
            yield Label("A Button", id="enlabel")
            yield EnGlyphText("+")
            yield self.enhello
            yield EnGlyphText("=")
            yield Button(str(self.enhello), variant="primary")
            yield Label(str(self.enhello))

    def on_button_pressed(self):
        self.fsize += 1
        H = self.query_one("#enhello")
        H.update(font_size=self.fsize)
        self.query_one("#enlabel").update(str(H._font_size) + "gx")


if __name__ == "__main__":
    Test().run()
