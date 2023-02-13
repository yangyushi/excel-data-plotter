import sys
from PyQt5.QtWidgets import QApplication
from gui.gui_view import View
from data.data_model import DataModel
from gui.gui_controller import Controller

if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = DataModel()
    view = View()
    controller = Controller(model, view)
    view.show()
    sys.exit(app.exec_())

