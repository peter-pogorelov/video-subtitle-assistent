from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

from server import UDPServer
from jisho import get_tokens, WordRecord, Jisho

from itertools import accumulate

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


class JTextEdit(QTextEdit):
    selected_text:str = ''

    def __init__(self, parent=None):
        super().__init__(parent)

        self.fmt_green = QtGui.QTextCharFormat()
        self.fmt_green.setBackground(QtGui.QBrush(QtGui.QColor(200, 255, 200)))

        self.fmt_white = QtGui.QTextCharFormat()
        self.fmt_white.setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))

        self.tokens = list()

    def setText(self, text):
        tokens = get_tokens(text)
        toklens = [len(token) for token in get_tokens(text)]
        right = list(accumulate(toklens))
        left = [0] + right[:-1]

        self.tokens = [(t, [l, r]) for t, l, r in zip(tokens, left, right)]
        print(self.tokens)

        super().setText(''.join(tokens))

    def set_highlight(self, left, right, fmt):
        cursor = self.textCursor()
        cursor.setPosition(left, cursor.MoveAnchor)
        cursor.setPosition(right, cursor.KeepAnchor)
        cursor.setCharFormat(fmt)

    def findCursorToken(self, cursor):
        pos = cursor.position()
        for tok, [l, r] in self.tokens:
            if l <= pos and pos < r:
                return tok, l, r
        return None

    def highlightCursorSelection(self, cursor):
        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        self.set_highlight(start, end, self.fmt_blue)

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        self.set_highlight(0, len(self.toPlainText()), self.fmt_white)
        return super().mousePressEvent(e)

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent) -> None:
        cursor = self.textCursor()

        token = None
        left = right = None

        if cursor.selectedText():
            token = cursor.selectedText()
            left = cursor.selectionStart()
            right = cursor.selectionEnd()
        else:
            result = self.findCursorToken(cursor)
            if result:
                token, left, right = result
                self.set_highlight(left, right, self.fmt_green)

        self.selected_text = token

        super().mouseReleaseEvent(e)


class TableView(QTableWidget):
    def __init__(self, *args):
        super().__init__(0, 4)
        #self.setData()
        self.setHorizontalHeaderLabels(['kanji', 'kana', 'english', 'POS'])
        self.resizeColumnsToContents()
        self.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.horizontalHeader().setStretchLastSection(True)

    def addRecord(self, record: WordRecord):
        currentRow = self.rowCount()
        self.insertRow(currentRow)

        self.setItem(currentRow, 0, QTableWidgetItem(record.kanji))
        self.setItem(currentRow, 1, QTableWidgetItem(record.kana))
        self.setItem(currentRow, 2, QTableWidgetItem(record.english))
        self.setItem(currentRow, 3, QTableWidgetItem(record.pos))

        self.resizeColumnsToContents()


class JSubFocusWindow(QMainWindow):
    info_text = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.jisho = Jisho()

        self.resize(640, 840)
        self.jedit = JTextEdit()
        self.table = TableView()
        self.search_button = QPushButton('search in jisho.org')
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
        self.table.setRowCount(0)
        for rec in self.jisho.lookup(self.jedit.selected_text):
            self.table.addRecord(rec)

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
        self.centralWidget.addItem(item)

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