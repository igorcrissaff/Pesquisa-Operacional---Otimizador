from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon


class Msg(QMessageBox):
    def __init__(self):
        super(Msg, self).__init__()
        self.setWindowTitle('Programa de Programação Linear')

    def show_error(self, txt):
        self.setText(txt)
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.exec()

    def show_question(self, txt):
        self.setText(txt)
        self.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        confirm = self.exec()
        return True if confirm == QMessageBox.StandardButton.Ok else False

    def show_info(self, txt):
        self.setText(txt)
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.exec()


if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication
    app = QApplication([])
    msg = Msg()
    msg.info('123')
