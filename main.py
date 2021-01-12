import pathlib

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import PyQt5.QtGui as QtGui
from dictionary.jap2eng.jmdict import JMDict
from gui.widgets import TokenizedTextEdit, DictionaryTableView
from server import UDPServer

from itertools import accumulate

from tokenizer.jap2eng.wakati import WakatiTokenizer

STYLE = """
    QListView { 
        background: white;
        font-family: Times New Roman;font-size: 30pt
    }
    
    QListView::item { 
        height: 40px;
    }
    
    QListView::item:selected { 
        background: rgb(128,128,255);
    }
    
    QTextEdit {
        font-family: Times New Roman;font-size: 30pt
    }
    
    QTableWidget {
        font-family: Times New Roman;font-size: 16pt
    }
"""


class JSubFocusWindow(QMainWindow):
    info_text = None

    def __init__(self, parent=None):
        super().__init__(parent)
        #self.jisho = Jisho()
        self.jisho = JMDict(pathlib.Path('/database/test.db'))
        self.tokenizer = WakatiTokenizer()

        self.resize(640, 480)
        self.jedit = TokenizedTextEdit(self.tokenizer)
        self.jedit.setFixedHeight(640//5)
        self.table = DictionaryTableView()
        self.search_button = QPushButton('translate...')
        self.layout = QVBoxLayout()
        self.centralWidget = QWidget()

        self.setCentralWidget(self.centralWidget)

        self.centralWidget.setStyleSheet(STYLE)
        self.centralWidget.setLayout(self.layout)

        self.layout.addWidget(self.jedit)
        self.layout.addWidget(self.search_button)
        self.layout.addWidget(self.table)

        self.search_button.clicked.connect(self.update_with_selection)

    def update_with_selection(self):
        found_records = self.jisho.find_from_base_language(self.jedit.selected_text)[:10]
        self.table.add_from_list(self.jisho.to_table(found_records))

    def update_with_text(self, text):
        self.jedit.setText(text)
        self.show()


class JSubWindow(QMainWindow):
    def addNewItem(self, text):
        n_items = self.centralWidget.count()
        item = QListWidgetItem(text)
        n_lines = max(text.count('\n')+1, 1)
        item.setSizeHint(QSize(0, 40 * n_lines))
        if n_items % 2 == 0:
            item.setBackground(QtGui.QBrush(QtGui.QColor(200, 255, 200)))
        #self.centralWidget.addItem(item)
        self.centralWidget.insertItem(0, item)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.focus_window = JSubFocusWindow(self)

        self.setWindowTitle("Anime Subtitle Assistor")
        self.resize(640, 480)
        self.centralWidget = QListWidget()
        self.centralWidget.setStyleSheet(STYLE)
        self.centralWidget.setSizeAdjustPolicy(QListWidget.AdjustToContents)
        self.centralWidget.doubleClicked.connect(self.text_focus)
        self.setCentralWidget(self.centralWidget)

    def text_focus(self, data: QModelIndex):
        item = self.centralWidget.item(data.row())
        self.focus_window.update_with_text(item.text().strip())


if __name__ == '__main__':
    app = QApplication([])
    server = UDPServer()
    window = JSubWindow()
    server.subscribe(window.addNewItem)
    server.run()
    window.show()
    app.exec_()
    pass