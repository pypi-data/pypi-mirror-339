from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, OptionList, Label, Markdown, Button
from textual.containers import Horizontal, Vertical, VerticalScroll,Container
from textual.widgets.option_list import Option
from textual import on
from textual.reactive import reactive

import urllib.request
import yaml

from shoestring_assembler.engine import step_definitions

class SolutionPicker(Container):
    pass

class SolutionAssemblerApp(App):
    CSS_PATH = "layout.tcss"
    current_ui = reactive(None, recompose=True)

    def __init__(self, engine, **kwargs):
        super().__init__(**kwargs)
        self.engine = engine
        self.set_reactive(SolutionAssemblerApp.current_ui,self.engine.get_ui)

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        match(self.current_ui):
            case step_definitions.ChooseSolution():
                yield SolutionPicker()
            case step_definitions.ChooseSolutionVersion():
                yield 
            case _:
                yield

    def on_mount(self):
        self.title = "Select a Shoestring Solution"
        self.engine.start()
        self.mutate_reactive(SolutionAssemblerApp.mutate_reactive)
