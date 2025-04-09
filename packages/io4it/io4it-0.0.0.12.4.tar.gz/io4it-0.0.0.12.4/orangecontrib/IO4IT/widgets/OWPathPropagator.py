import os
from pathlib import Path
import tempfile
import subprocess
from PyQt5.QtWidgets import QPushButton, QRadioButton, QApplication
from PyQt5 import uic
from AnyQt.QtWidgets import QFileDialog, QVBoxLayout, QWidget

from Orange.widgets.widget import OWWidget, Output, Input
from Orange.data import Table, Domain, StringVariable
from Orange.widgets.settings import Setting
class OWDirectorySelector(OWWidget):
    name = "Directory Selector"
    description = "Select a folder and assign it as input_dir or output_dir"
    icon = "icons/in_or_out.png"
    if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
        icon = "icons_dev/in_or_out.png"
    gui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "designer/ow_in_or_out_path.ui")
    priority = 10

    radio_value = Setting("")  # Par défaut

    class Inputs:
        in_data = Input("Data", Table)

    class Outputs:
        data = Output("Data", Table)

    def __init__(self):
        super().__init__()
        self.selected_path = ""
        self.in_data = None

        # Load UI
        uic.loadUi(self.gui_path, self)

        # Find widgets
        self.file_button = self.findChild(QPushButton, 'fileButton')
        self.input_dir_button = self.findChild(QRadioButton, 'input_dir')
        self.output_dir_button = self.findChild(QRadioButton, 'output_dir')

        # Connect signals
        self.file_button.clicked.connect(self.select_folder)
        self.input_dir_button.toggled.connect(self.set_radio_input)
        self.output_dir_button.toggled.connect(self.set_radio_output)

        if self.radio_value == "input_dir":
            self.input_dir_button.setChecked(True)
        else:
            self.output_dir_button.setChecked(True)

    @Inputs.in_data
    def set_input_data(self, data):
        self.in_data = data
        if data is not None:
            self.select_folder()

    def set_radio_input(self):
        self.radio_value = "input_dir"
        self.commit_path()

    def set_radio_output(self):
        self.radio_value = "output_dir"
        self.commit_path()

    def select_folder(self):
        vbs_code = '''
               Set objShell = CreateObject("Shell.Application")
               Set objFolder = objShell.BrowseForFolder(0, "Selectionnez un dossier", 1, "")

               If Not objFolder Is Nothing Then
                   folderPath = objFolder.Self.Path
                   WScript.Echo folderPath
               End If
           '''

        with tempfile.NamedTemporaryFile(delete=False, suffix=".vbs", mode="w", encoding="utf-8") as temp_vbs:
            temp_vbs.write(vbs_code)
            temp_vbs_path = temp_vbs.name

        try:
            completed = subprocess.run(["cscript", "//Nologo", temp_vbs_path], capture_output=True, text=True)
            folder = completed.stdout.strip()
            if folder:
                self.selected_path = folder
                self.commit_path()
        finally:
            os.remove(temp_vbs_path)

    def commit_path(self):
        if not self.selected_path:
            return

        col_name = self.radio_value
        var = StringVariable(col_name)

        if self.in_data is not None:
            domain = Domain(
                self.in_data.domain.attributes,
                self.in_data.domain.class_vars,
                list(self.in_data.domain.metas) + [var]
            )
            new_table = Table.from_table(domain, self.in_data)
            new_meta_column = [self.selected_path] * len(new_table)
            new_table.metas[:, -1] = new_meta_column
        else:
            domain = Domain([], metas=[var])
            new_table = Table(domain, [[]])
            new_table.metas[0] = [self.selected_path]

        self.Outputs.data.send(new_table)

    def handleNewSignals(self):
        pass


    # Test standalone
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = OWDirectorySelector()
    window.show()
    sys.exit(app.exec_())
