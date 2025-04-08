import os
from pathlib import Path
import tempfile
import subprocess
from PyQt5.QtWidgets import QPushButton, QRadioButton, QApplication
from PyQt5 import uic
from AnyQt.QtWidgets import QFileDialog, QVBoxLayout, QWidget

from Orange.widgets.widget import OWWidget, Output
from Orange.data import Table, Domain, StringVariable

class OWDirectorySelector(OWWidget):
    name = "Directory Selector"
    description = "Select a folder and assign it as input_dir or output_dir"
    icon = "icons/in_or_out.png"
    if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
        icon = "icons_dev/in_or_out.png"
    gui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "designer/ow_in_or_out_path.ui")
    priority = 10

    class Outputs:
        data = Output("Data", Table)

    def __init__(self):
        super().__init__()
        self.selected_path = ""

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

        # Default state
        self.radio_value = "input_dir"
        self.input_dir_button.setChecked(True)

    def set_radio_input(self):
        self.radio_value = "input_dir"
        self.commit_path()

    def set_radio_output(self):
        self.radio_value = "output_dir"
        self.commit_path()

    def select_folder(self):
        if os.name == 'nt':  # Windows
            vbs_script = """
            Set objShell = CreateObject("Shell.Application")
            Set objFolder = objShell.BrowseForFolder(0, "Select Folder", 0, 0)
            If Not objFolder Is Nothing Then
                Set objFolderItem = objFolder.Self
                Wscript.Echo objFolderItem.Path
            End If
            """
            with tempfile.NamedTemporaryFile(delete=False, suffix='.vbs', mode='w', encoding='utf-8') as vbs:
                vbs.write(vbs_script)
                vbs_path = vbs.name

            try:
                result = subprocess.run(['cscript.exe', '//Nologo', vbs_path], capture_output=True, text=True)
                folder = result.stdout.strip()
                if folder:
                    self.selected_path = folder
                    self.commit_path()
            finally:
                os.unlink(vbs_path)
        else:
            folder = QFileDialog.getExistingDirectory(self, "Select Folder")
            if folder:
                self.selected_path = folder
                self.commit_path()

    def commit_path(self):
        if not self.selected_path:
            return

        var = StringVariable(self.radio_value)
        domain = Domain([], metas=[var])

        # Crée une table vide avec une ligne, puis affecte la valeur au niveau des metas
        table = Table(domain, [[]])  # Une ligne vide
        table.metas[0] = [self.selected_path]  # Affecte la valeur dans les metas

        self.Outputs.data.send(table)


# Test standalone
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = OWDirectorySelector()
    window.show()
    sys.exit(app.exec_())
