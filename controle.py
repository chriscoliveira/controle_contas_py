import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow, QApplication
from layout import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from funcoes import Funcoes
import matplotlib.pyplot as plt


class Novo(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        funcoes = Funcoes('contas.db')
        funcoes.criaBanco()
        self.frame_cadastro.setVisible(False)
        self.frame_lista.setVisible(False)
        self.verticalLayout.setAlignment(Qt.AlignTop)
        self.exibeResumo()

    def exibeResumo(self):
        funcoes = Funcoes('contas.db')
        pagar, receber, cartao, falta, antes = funcoes.exibeResumo(
            "3", "2020")
        self.lbl_pagar.setText(str(pagar))
        self.lbl_receber.setText(str(receber))
        self.lbl_cartao.setText(str(cartao))
        self.lbl_falta.setText(str(falta))
        self.lbl_sobra.setText(str(receber-pagar))
        self.lbl_antes20.setText(str(antes))
        self.lbl_depois20.setText(str(pagar-antes))

        labels = ['Pagar', 'Receber']
        sizes = [pagar, receber]

        colors = ['gold', 'yellowgreen']
        explode = (0.1, 0.1)
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True,
                startangle=140, colors=colors, explode=explode)
        plt.axis('equal')
        plt.savefig('pie.png', dpi=60)
        self.lbl_grafico.setPixmap(QPixmap('pie.png'))


qt = QApplication(sys.argv)

novo = Novo()
novo.show()
qt.exec_()
