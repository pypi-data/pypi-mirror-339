import sys
import os
import subprocess
import threading
import importlib.resources
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
    QMessageBox, QSystemTrayIcon, QMenu
)
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QCoreApplication, Qt, QTimer, QEvent

class NerdDictationGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nerd Dictation GUI")
        self.setGeometry(100, 100, 300, 200)

        self.process = None

        layout = QVBoxLayout()

        self.start_button = QPushButton("Start Dictation")
        self.start_button.clicked.connect(self.start_dictation)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Dictation")
        self.stop_button.clicked.connect(self.stop_dictation)
        layout.addWidget(self.stop_button)

        self.status_label = QLabel("Status: Idle")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

        self.init_tray()
        QTimer.singleShot(0, self.hide)  # Start minimized to tray

    def get_resource_path(self, filename):
        """Get the path to a resource file"""
        try:
            # When running as installed package
            with importlib.resources.path('nerd_dictation_gui.resources', filename) as path:
                return str(path)
        except (ImportError, ModuleNotFoundError):
            # When running directly from source
            base_dir = Path(__file__).parent
            return str(base_dir / 'resources' / filename)

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage("Nerd Dictation", "Application minimized to tray.", QSystemTrayIcon.MessageIcon.Information, 2000)

    def init_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        
        # Use resource paths for icons
        idle_icon_path = self.get_resource_path('mic_idle.png')
        active_icon_path = self.get_resource_path('mic_recording.png')
        
        self.icon_idle = QIcon(idle_icon_path)
        self.icon_active = QIcon(active_icon_path)
        
        self.tray_icon.setIcon(self.icon_idle)
        self.tray_icon.setToolTip("Nerd Dictation")

        tray_menu = QMenu()

        show_window_action = QAction("Show Window", self)
        show_window_action.triggered.connect(self.show)
        tray_menu.addAction(show_window_action)

        start_action = QAction("Start Dictation", self)
        start_action.triggered.connect(self.start_dictation)
        tray_menu.addAction(start_action)

        stop_action = QAction("Stop Dictation", self)
        stop_action.triggered.connect(self.stop_dictation)
        tray_menu.addAction(stop_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.quit_application)
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_activated)
        self.tray_icon.show()
        self.tray_icon.showMessage("Nerd Dictation", "Started minimized in system tray.", QSystemTrayIcon.MessageIcon.Information, 3000)

    def quit_application(self):
        """Clean up and exit application"""
        self.stop_dictation()  # Ensure dictation is stopped before quitting
        QCoreApplication.quit()

    def tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:  # Left click
            if self.process is None:
                self.start_dictation()
            else:
                self.stop_dictation()

    def start_dictation(self):
        if self.process is None:
            self.status_label.setText("Status: Starting...")
            threading.Thread(target=self._start_process, daemon=True).start()
        else:
            QMessageBox.information(self, "Info", "Dictation is already running.")

    def _start_process(self):
        try:
            # Check if nerd-dictation is available
            try:
                subprocess.run(["nerd-dictation", "--version"], check=True, 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except (subprocess.SubprocessError, FileNotFoundError):
                raise Exception("nerd-dictation command not found. Please ensure it's installed and in your PATH.")
            
            self.process = subprocess.Popen(["nerd-dictation", "begin"], 
                                           stdout=subprocess.PIPE, 
                                           stderr=subprocess.PIPE)
            
            # Update UI from the main thread
            QTimer.singleShot(0, lambda: self.status_label.setText("Status: Running"))
            QTimer.singleShot(0, lambda: self.tray_icon.setIcon(self.icon_active))
            QTimer.singleShot(0, lambda: self.tray_icon.showMessage(
                "Nerd Dictation", "Dictation started.", 
                QSystemTrayIcon.MessageIcon.Information, 2000))
            
        except Exception as e:
            QTimer.singleShot(0, lambda: self.status_label.setText("Status: Error"))
            QTimer.singleShot(0, lambda: QMessageBox.critical(self, "Error", str(e)))
            QTimer.singleShot(0, lambda: self.tray_icon.showMessage(
                "Nerd Dictation", f"Error: {str(e)}", 
                QSystemTrayIcon.MessageIcon.Critical, 2000))
            self.process = None

    def stop_dictation(self):
        if self.process:
            try:
                subprocess.run(["nerd-dictation", "end"], check=True)
                self.status_label.setText("Status: Stopped")
                self.tray_icon.setIcon(self.icon_idle)
                self.tray_icon.showMessage("Nerd Dictation", "Dictation stopped.", 
                                          QSystemTrayIcon.MessageIcon.Information, 2000)
                self.process = None
            except subprocess.CalledProcessError as e:
                self.status_label.setText("Status: Error")
                QMessageBox.critical(self, "Error", str(e))
                self.tray_icon.showMessage("Nerd Dictation", f"Error: {str(e)}", 
                                          QSystemTrayIcon.MessageIcon.Critical, 2000)
        else:
            QMessageBox.information(self, "Info", "No dictation is running.")


def main():
    app = QApplication(sys.argv)
    window = NerdDictationGUI()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
