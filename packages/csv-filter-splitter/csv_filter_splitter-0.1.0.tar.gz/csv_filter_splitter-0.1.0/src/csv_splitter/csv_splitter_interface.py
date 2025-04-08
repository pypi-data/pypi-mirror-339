import pathlib
from textual import on
from textual.app import ComposeResult, App
from textual.screen import Screen, ModalScreen
from textual.widgets import DirectoryTree, Static, Button, Select,Header, Footer, DataTable, Label
from textual.reactive import reactive
from textual.containers import Container, Horizontal, Grid
from csv_splitter.csv_filter_spliter import *
from csv_splitter.pd_datatable import DataFrameTable
import pandas as pd

import os

def count_rows(path, filename):
    with open(os.path.join(path, filename), "r", encoding="utf-8") as f:
        return sum(1 for line in f)

class QuitScreen(ModalScreen[bool]):


    """Screen with a dialog to quit."""

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Are you sure you want to quit?", id="question"),
            Button("Quit", variant="error", id="quit", classes='quit_screen_buttons'),
            Button("Cancel", variant="primary", id="cancel", classes='quit_screen_buttons'),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.dismiss(True)
        else:
            self.dismiss(False)


class CSVSelectorApp(Screen):
    """A Textual app to select and process a CSV file using DirectoryTree."""

    TITLE = 'csv splitter'
    CSS_PATH = 'csv_splitter.tcss'
    selected_filter = reactive(None)
    output = reactive(pathlib.Path('~/Documents/ccc1_python_tools/csv_splitter/output_files').expanduser())
    selected_file = reactive(None)
    files_path = reactive(pathlib.Path('~/Documents/ccc1_python_tools/csv_splitter').expanduser())

    BINDINGS = [("ctrl+q", "request_quit", "Quit"),
                ("ctrl+r", "refresh_file_tree", "Refresh"),
                ("ctrl+e", "show_in_explorer", "Show in explorer"), ]

    def create_output_dir(self):
        output = self.output
        output.mkdir(parents=True, exist_ok=True)

    def __init__(self, on_logout):
            super().__init__()
            self.on_logout = on_logout

    def deliver_binary(self, output_file):
        self.app.deliver_binary(
            self.output + '/' + output_file,
            save_directory=None,
            save_filename=None,
            open_method="download",
            mime_type=None,
            name=None
        )

    def action_request_quit(self) -> None:
        """Action to display the quit dialog."""

        def check_quit(quit: bool | None) -> None:
            """Called when QuitScreen is dismissed."""
            if quit:
                self.app.exit()

        self.app.push_screen(QuitScreen(), callback = check_quit)

    def action_refresh_file_tree(self) -> None:
        self.query_one("#directory-tree", DirectoryTree).reload()

    def action_show_in_explorer(self) -> None:
        if self.selected_file:
            os.startfile(self.selected_file.parents[0])
        else:
            os.startfile(self.files_path)


    def compose(self) -> ComposeResult:


        """Compose the app layout."""
        yield Header()
        with Horizontal():
            with Container(id='directory_tree_container'):

                #yield Static("Browse to select a CSV file:", id="instructions")
                yield DirectoryTree(self.files_path, id="directory-tree")
                yield Static("No file selected.", id="selected-file")
                yield DataTable(id="metadata")



            with Container(id='datatable_container'):

                #yield Static("Preview:", id="preview")
                yield DataFrameTable()
                yield Static("Column to use as filter:", id="static_filter")

                with Container(id='run_container'):
                    yield Select(options=[], id="select_filter")
                    yield Button("Split by filter", id="run", disabled=True)

                yield Static('', id="status")
        yield Footer()

    def on_mount(self):
        self.create_output_dir()
        self.query_one(DataFrameTable).border_title = 'Preview:'
        self.query_one('#directory_tree_container', Container).border_title = 'Select a csv file:'

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """Handle file selection from the DirectoryTree."""
        self.query_one("#run", Button).disabled = True
        self.selected_file  = event.path
        table = self.query_one(DataFrameTable)
        metadata = self.query_one("#metadata", DataTable)


        if str(self.selected_file).endswith(".csv"):

            self.query_one("#selected-file", Static).update("Selected:")


            df_preview = pd.read_csv(self.selected_file, nrows=1000)
            columns = list(df_preview.columns)
            table.clear(columns=True)
            table.add_df(df_preview)

            count = count_rows(self.files_path, self.selected_file)
            n_cols = len(df_preview.columns)
            ROWS = [
                ('Filename: ', str(self.selected_file).split("\\")[-1]),
                ('Columns', n_cols),
                ('Aproximated records: ', count)
            ]

            metadata.clear(columns=True)
            metadata.add_columns(*ROWS[0])
            metadata.add_rows(ROWS[1:])
            self.query_one("#select_filter", Select).set_options((column, column) for column in columns)

        else:
            self.query_one("#selected-file", Static).update("Please select a CSV file!")
            self.query_one("#run", Button).disabled = True
            table.clear(columns=True)
            metadata.clear(columns=True)
            self.query_one("#select_filter", Select).set_options([])


    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle CSV processing when the button is pressed."""
        try:
            match event.button.id:

                case 'upload-csv':
                    self.app.open_url("http://10.105.43.114:8080/", new_tab=True)

                case 'refresh':
                    self.query_one("#directory-tree", DirectoryTree).reload()

                case 'run':
                    self.query_one("#selected-file", Static).update("Processing...")
                    self.query_one("#status", Static).update(f"Processing... please wait.")
                    output_file = splitByFilter(pd.read_csv(self.selected_file), self.selected_filter, self.output)
                    self.query_one("#status", Static).update(f"Done!")
                    os.startfile(pathlib.Path(self.output,output_file))
                    #self.deliver_binary(output_file)

                case 'logout':
                    self.on_logout()
        except Exception as e:
            self.app.notify(str(e))

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        self.selected_filter = str(event.value)

        if not self.query_one("#select_filter", Select).is_blank():
            self.query_one("#run", Button).disabled = False


class DevApp(App):
    BINDINGS = [("ctrl+q", "request_quit", "Quit")]
    def on_mount(self) -> None:

        self.push_screen(CSVSelectorApp(on_logout=None))
        self.switch_screen(CSVSelectorApp(on_logout=None))
        self.theme = 'nord'

def launch_app():
    input_folder = pathlib.Path('~/Documents/ccc1_python_tools/csv_splitter/input_files').expanduser()
    input_folder.mkdir(parents=True, exist_ok=True)
    csv_app = DevApp()
    csv_app.run()


if __name__ == "__main__":
    app = DevApp()
    app.run()