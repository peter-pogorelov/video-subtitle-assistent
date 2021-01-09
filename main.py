from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import PyQt5.QtGui as QtGui

from server import UDPServer
from jisho import get_tokens

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
"""


class JTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()

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

    def mouseDoubleClickEvent(self, e: QtGui.QMouseEvent) -> None:
        print('executed')

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

        if cursor.selectedText():
            token = cursor.selectedText()
            left = cursor.selectionStart()
            right = cursor.selectionEnd()
        else:
            token, left, right = self.findCursorToken(cursor)
            self.set_highlight(left, right, self.fmt_green)

        super().mouseReleaseEvent(e)


class JSubFocusWindow(QMainWindow):
    info_text = None

    def __init__(self, parent):
        super().__init__(parent)
        self.resize(640, 240)
        self.centralWidget = JTextEdit()
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setStyleSheet(STYLE)

    def update_with_text(self, text):
        self.centralWidget.setText(text)
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

        self.setWindowTitle("Anime Subtitle Analyzer")
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