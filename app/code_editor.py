from PySide6.QtWidgets import QPlainTextEdit, QWidget
from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtGui import QColor, QPainter, QPaintEvent, QTextFormat

class LineNumberArea(QWidget):
    """Widget to paint line numbers for the CodeEditor."""
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self) -> QSize:
        return QSize(self.code_editor.line_number_area_width(), 0)

    def paintEvent(self, event: QPaintEvent) -> None:
        self.code_editor.line_number_area_paint_event(event)

class CodeEditor(QPlainTextEdit):
    """A custom QPlainTextEdit that includes a line number area on the left."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.line_number_area = LineNumberArea(self)

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        self.update_line_number_area_width(0)
        self.highlight_current_line()
        
    def line_number_area_width(self) -> int:
        digits = 1
        max_blocks = max(1, self.blockCount())
        while max_blocks >= 10:
            max_blocks /= 10
            digits += 1
        
        # Calculate space using standard Qt font metrics
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def highlight_current_line(self):
        extra_selections = []

        if not self.isReadOnly():
            from PySide6.QtWidgets import QTextEdit
            selection = QTextEdit.ExtraSelection()
            # Fluent Theme: Zinc 800 for current line
            line_color = QColor("#27272a") 
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        # Fluent Theme: Zinc 950 for gutter background (matches editor)
        painter.fillRect(event.rect(), QColor("#09090b"))

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = round(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + round(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                # Fluent Theme: Zinc 500 for line numbers
                painter.setPen(QColor("#71717a")) 
                painter.drawText(0, top, self.line_number_area.width() - 2, 
                               self.fontMetrics().height(),
                               Qt.AlignRight | Qt.AlignVCenter, number)

            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            block_number += 1
