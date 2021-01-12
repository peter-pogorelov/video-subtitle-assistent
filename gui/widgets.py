from PyQt5.QtWidgets import *
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

from tokenizer.base import BaseTokenizer


class TokenizedTextEdit(QTextEdit):
    selected_text:str = ''

    def __init__(self, tokenizer: BaseTokenizer, parent=None):
        super().__init__(parent)

        self.tokenizer = tokenizer
        self.tokens = list()

        self.fmt_green = QtGui.QTextCharFormat()
        self.fmt_green.setBackground(QtGui.QBrush(QtGui.QColor(200, 255, 200)))

        self.fmt_white = QtGui.QTextCharFormat()
        self.fmt_white.setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))

    def set_highlight(self, left, right, fmt):
        cursor = self.textCursor()
        cursor.setPosition(left, cursor.MoveAnchor)
        cursor.setPosition(right, cursor.KeepAnchor)
        cursor.setCharFormat(fmt)

    def find_cursor_token(self, cursor):
        pos = cursor.position()
        for tok, [l, r] in self.tokens:
            if l <= pos and pos < r:
                return tok, l, r
        return None

    def setText(self, text):
        parts = text.split() # initial split for chinese-like languages

        self.tokens = []

        cum_length = 0
        for offset, part in enumerate(parts):
            tokens = self.tokenizer.tokenize_base_language(part)
            for token in tokens:
                self.tokens.append([token, [cum_length, cum_length + len(token)]])
                cum_length += len(token)
            cum_length += 1

        super().setText(text)

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        self.set_highlight(0, len(self.toPlainText()), self.fmt_white)
        return super().mousePressEvent(e)

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent) -> None:
        cursor = self.textCursor()

        token = None

        if cursor.selectedText():
            token = cursor.selectedText()
        else:
            result = self.find_cursor_token(cursor)
            if result:
                token, left, right = result
                self.set_highlight(left, right, self.fmt_green)

        self.selected_text = token

        super().mouseReleaseEvent(e)


class DictionaryTableView(QTableWidget):
    def __init__(self, *args):
        super().__init__(0, 0)
        self.resizeColumnsToContents()
        self.horizontalHeader().setStretchLastSection(True)
        self.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)

    def add_from_list(self, table_as_list: list):
        self.setRowCount(0)
        self.setColumnCount(len(table_as_list[0]))
        self.setHorizontalHeaderLabels(table_as_list[0])

        if len(table_as_list) > 1:
            for row in table_as_list[1:]:
                self.addRecord(row)

    def addRecord(self, record: list):
        currentRow = self.rowCount()
        self.insertRow(currentRow)

        for i, item in enumerate(record):
            self.setItem(currentRow, i, QTableWidgetItem(item))

        self.resizeColumnsToContents()