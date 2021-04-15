import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import calc
from math import sqrt


class MainWindow(QMainWindow, calc.Ui_MainWindow):
    text: str = ''
    value: str = ''
    point: bool = False
    root: bool = False
    buffer: float = 0
    operator: str = ''
    pre_operation: str = ''
    n: int = 2
    begin: bool = False

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.begin = True
        # Setup buttons numpad
        for i in range(10):
            getattr(self, f'btn_{i}').pressed.connect(lambda n=i: self.numpad(n))
        # Setup other buttons
        self.btn_point.pressed.connect(lambda: self.real())
        self.btn_reverse.pressed.connect(lambda: self.reverse())

        self.btn_equal.pressed.connect(lambda: self.equal())
        self.btn_plus.pressed.connect(lambda: self.operation('+'))
        self.btn_minus.pressed.connect(lambda: self.operation('-'))
        self.btn_division.pressed.connect(lambda: self.operation('/'))
        self.btn_multiply.pressed.connect(lambda: self.operation('*'))

        self.btn_backspace.pressed.connect(lambda: self.backspace())
        self.btn_C.pressed.connect(lambda: self.clear())
        self.btn_CE.pressed.connect(lambda: self.ce())
        self.btn_sqrt.pressed.connect(lambda: self.sqrt())
        self.btn_percent.pressed.connect(lambda: self.operation('%'))

        self.show()

    def reverse(self):
        self.text = str(eval(f'-1*{self.text}'))
        self.setScore()

    def ce(self):
        self.text = '0'
        self.setScore()
        self.root = False
        self.point = False

    def clear(self, zero=None):
        self.text = '0'
        self.value = ''
        self.operator = ''
        self.setScore()
        if zero is None:
            self.setHistory()
        else:
            self.label_history.setText('N/a')
        self.root = False
        self.point = False

    def backspace(self):
        if len(self.text) > 0 and self.text[-1] == '.':
            self.point = False
        self.text = self.text[:-1]
        self.setScore()

    def real(self):
        if not self.point:
            self.point = True
            self.score('.')

    def numpad(self, num: int):
        self.score(str(num))

    def operation(self, operator: str = ''):
        # Move the operators
        self.pre_operation = self.operator
        self.operator = operator
        self.history()
        # Reset score
        self.text = '0'
        self.setScore()
        self.point = False
        self.root = False
        self.begin = False

    def equal(self):
        if self.point:
            setup: set = set([x for x in self.text if x != '.'])
            setup.discard('0')
            if len(setup) == 0:
                self.accuracy()
        self.operation()

    def sqrt(self):
        if not self.root:
            self.root = True
            self.score('√')

    def history(self):
        try:
            # Setup the first value
            if self.value == '' and not self.root:
                self.value = f'{self.text}{self.operator}'
                self.begin = True
            elif self.pre_operation == '%':
                self.value = f'{self.buffer}{self.operator} '
            # Calculate
            elif self.root:
                # Crutch for the empty value of the root argument
                if self.text == '√':
                    self.text = '√0'
                self.buffer = round(eval(f'{self.value[:-1]}{self.pre_operation}sqrt({self.text[1:]})'), self.n)
                self.value = f'{self.buffer} '
                # self.root = False
            elif self.operator == '%':
                percent = eval(f'{self.value[:-1]}/100*{self.text}')
                switch = {
                    '*': percent,
                    '+': f'{self.value}{percent}',
                    '-': f'{self.value}{percent}',
                    '/': f'{self.value[:-1]}*{percent}',
                }
                self.buffer = round(eval(f'{switch.get(self.pre_operation)}'), self.n)
                self.value = f'{self.buffer} '
            else:
                # Crutch for case when there is no previous operation or it is a "calculation"
                if self.pre_operation == '':
                    self.buffer = round(eval(f'{self.value[:-1]}'), self.n)
                else:
                    self.buffer = round(eval(f'{self.value[:-1]}{self.pre_operation}{self.text}'), self.n)
                if self.operator == '':
                    self.value = f'{self.buffer} '
                else:
                    self.value = f'{self.buffer}{self.operator}'
            if self.n == 0:
                self.value = f'{int(float(self.value[:-1]))}{self.value[-1]}'
            self.setHistory()
        except ZeroDivisionError:
            self.clear('')
        except Exception as err:
            print('error: ', err)

    def score(self, symbol: str):
        # Clears the history field if there is no operator to interact with it
        if (self.operator == '' or self.operator == '%') and not self.root and not self.begin:
            self.clear()
            # Adding zero before point in cases of operations percent, sqrt and equal
            if symbol == '.':
                self.point = True
            self.begin = True
        pre_symbol: str = self.text
        # Remove the first zero
        if pre_symbol == '0' and not self.point:
            pre_symbol = ''
        elif pre_symbol == '' and self.point:
            pre_symbol = '0'

        if symbol == '√':
            if self.label_score.text()[0] == '0':
                self.text = self.text[1:]
            self.text = f'√{self.text}'
        else:
            self.text = f'{pre_symbol}{symbol}'
        self.setScore()

    def setScore(self):
        self.label_score.setText(self.text)

    def setHistory(self):
        self.label_history.setText(self.value)

    def getScore(self):
        return self.label_score.text()

    def accuracy(self):
        self.n = len(self.text[2:])
        self.clear()


def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
