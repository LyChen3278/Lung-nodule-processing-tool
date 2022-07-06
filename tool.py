import sys
import warnings
from PyQt5 import QtWidgets
from layouts.mainLayout import mainLayout
from layouts.compareLayout import compare

warnings.filterwarnings('ignore')
app = QtWidgets.QApplication(sys.argv)
main = mainLayout()
compare = compare()
main.btn_compare.clicked.connect(compare.handle_click)
main.show()
sys.exit(app.exec_())
