from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from pathlib import Path
from .window import CoastProfileWindow

class CoastProfilePlugin:
    def __init__(self, iface): self.iface=iface; self.action=None; self.window=None
    def initGui(self):
        icon=QIcon(str(Path(__file__).with_name('icon.svg')))
        self.action=QAction(icon,"CoastProfile",self.iface.mainWindow())
        self.action.triggered.connect(self.run); self.iface.addPluginToMenu("CoastProfile",self.action); self.iface.addToolBarIcon(self.action)
    def unload(self):
        if self.action: self.iface.removePluginMenu("CoastProfile",self.action); self.iface.removeToolBarIcon(self.action)
        if self.window: self.window.close()
    def run(self):
        if self.window is None: self.window=CoastProfileWindow(self.iface)
        self.window.refresh_layers(); self.window.show(); self.window.raise_(); self.window.activateWindow()
