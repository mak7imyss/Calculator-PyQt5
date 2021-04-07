import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import calc
from math import sqrt


class MainWindow(QMainWindow, calc.Ui_MainWindow):
    text = ''
    history = None
    point = False

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        # super(Calc, self).__init__(*args, **kwargs)
        # self.setupUi(self)
        for i in range(10):
            getattr(self, f'btn_{i}').pressed.connect(lambda n=i: self.input_num(n))
        self.btn_point.pressed.connect(lambda: self.input_num(self.btn_point.text()))

        self.btn_equal.pressed.connect(lambda: self.equal())
        self.btn_plus.pressed.connect(lambda: self.operation('+'))
        self.btn_minus.pressed.connect(lambda: self.operation('-'))
        self.btn_division.pressed.connect(lambda: self.operation('/'))
        self.btn_multiply.pressed.connect(lambda: self.operation('*'))

        self.btn_backspace.pressed.connect(lambda: self.backspace())
        self.btn_C.pressed.connect(lambda: self.clear())
        self.btn_sqrt.pressed.connect(lambda: self.input_num(self.btn_sqrt.text()))
        self.btn_percent.pressed.connect(lambda: self.operation('/100*'))
        # self.btn_0.clicked.connect(lambda: self.input_num(self.btn_0.text()))
        # self.btn_1.clicked.connect(lambda: self.input_num(self.btn_1.text()))
        # self.btn_2.clicked.connect(lambda: self.input_num(self.btn_2.text()))
        # self.btn_3.clicked.connect(lambda: self.input_num(self.btn_3.text()))
        # self.btn_4.clicked.connect(lambda: self.input_num(self.btn_4.text()))
        # self.btn_5.clicked.connect(lambda: self.input_num(self.btn_5.text()))
        # self.btn_6.clicked.connect(lambda: self.input_num(self.btn_6.text()))
        # self.btn_7.clicked.connect(lambda: self.input_num(self.btn_7.text()))
        # self.btn_8.clicked.connect(lambda: self.input_num(self.btn_8.text()))
        # self.btn_9.clicked.connect(lambda: self.input_num(self.btn_9.text()))
        self.show()

    def equal(self):
        result = eval(f'{self.history}{self.label_score.text()}')
        self.history = None
        self.text = result
        self.label_history.setText(str(result))
        self.label_score.setText('')
        self.point = False

    def clear(self):
        self.history = None
        self.label_history.setText(None)
        self.label_score.setText('0')

    def backspace(self):
        if self.label_score.text() != '':
            self.text = self.text[0:-1]
            self.label_score.setText(self.text)

    def score(self, num):
        pre_text = self.label_score.text()
        if pre_text == '0':
            pre_text = ''
        self.text = f'{pre_text}{num}'
        self.label_score.setText(self.text)

    def input_num(self, num):
        if num == '.' and self.point:
            num = ''
        if num == '.' and not self.point:
            self.point = True
        self.score(num)

    def operation(self, op):
        if self.history is None:
            self.history = f'{self.text}{op}'
        else:
            result = eval(f'{self.history}{self.text}')
            self.label_score.setText(self.history)
            self.history = f'{result}{op}'
        self.label_history.setText(self.history)
        self.label_score.setText('0')
        self.point = False


def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

    # app = QApplication(sys.argv)
    # windows = Window()
    #
    # windows.show()
    # sys.exit(app.exec())
