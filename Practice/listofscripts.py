import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class HoverButton(QPushButton):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.default_style = """
            QPushButton {
                background-color: #333333;  /* Darker gray */
                color: white;
                border: 2px solid red;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
            }
        """
        self.hover_style = """
            QPushButton:hover {
                background-color: #333333;  /* Darker gray */
                color: white;
                border: 2px solid red;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                margin-left: 5px;
            }
        """
        self.setStyleSheet(self.default_style + self.hover_style)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Script Selector")
        self.setGeometry(100, 100, 400, 600)
        self.setStyleSheet("background-color: black;")

        layout = QVBoxLayout()

        # Title
        title = QLabel("Select the script from the options below:")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setStyleSheet("color: white; margin-top: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Define script paths
        script_paths = {
            #"Show Mouse coordinates": r"C:\Users\Amosley\_DC_Scripts_active\show_mouse_coordinates.py",
            #"For Lucid": r"C:\Users\Amosley\_DC_Scripts_active\LucidG_Underscore.py",
            #"For Project Alpha": r"C:\Users\Amosley\_DC_Scripts_active\Project_Alpha_underscore.py",
            "Underscore only": r"C:\Users\Amosley\_DC_Scripts_active\Underscore_In_Front_Of_Gs.py",
            #"Combine Folders": r"C:\Users\Amosley\_DC_Scripts_active\CombineFoldersAndSubfolders.py",
            "Add or Subtract Text": r"C:\Users\Amosley\_DC_Scripts_active\Add_or_subtract_text_2.0.py",
            "2b.-Match files and cancel": r"C:\Users\Amosley\_DC_Scripts_active\fancy_matched.py",
            #"3-Update Combined Sets": r"C:\Users\Amosley\_DC_Scripts_active\UpdateCombinedSets.py",
            #"3 - Alpha-Update Combined Sets": r"C:\Users\Amosley\_DC_Scripts_active\UpdateCombinedSets_Alpha.py",
            "1-Start": r"C:\Users\Amosley\_DC_Scripts_active\DC_Workspace.py",
            "2-Match files from Current Set": r"C:\Users\Amosley\_DC_Scripts_active\fancy_matched_with_autocombine.py",
            "Start by reading from Smartsheet": r"C:\Users\Amosley\_DC_Scripts_active\smartsheet_connect_try.py"
        }

        # Create buttons and connect them to their scripts
        for text, script_path in script_paths.items():
            button = HoverButton(text)
            button.clicked.connect(lambda checked, path=script_path: self.run_script(path))
            layout.addWidget(button)

        self.setLayout(layout)

    def run_script(self, script_path):
        try:
            subprocess.run(["python", script_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running script {script_path}: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
