import re
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PySide6.QtCore import QRegularExpression

class SyntaxHighlighter(QSyntaxHighlighter):
    """
    Native PySide6 syntax highlighter to provide premium VS Code-like
    formatting for code pasted into the AutoTyper editor.
    """
    def __init__(self, document):
        super().__init__(document)
        self.highlighting_rules = []

        # Color Palette (Zinc Dark Theme based)
        keyword_color = QColor("#0ea5e9")   # Sky Blue
        class_color = QColor("#f43f5e")     # Rose
        string_color = QColor("#10b981")    # Emerald Green
        comment_color = QColor("#71717a")   # Zinc 500
        number_color = QColor("#f59e0b")    # Amber
        function_color = QColor("#a855f7")  # Purple
        
        # 1. Keywords
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(keyword_color)
        keyword_format.setFontWeight(QFont.Bold)
        keywords = [
            '\\band\\b', '\\bas\\b', '\\bassert\\b', '\\bbreak\\b',
            '\\bclass\\b', '\\bcontinue\\b', '\\bdef\\b', '\\bdel\\b',
            '\\belif\\b', '\\belse\\b', '\\bexcept\\b', '\\bFalse\\b',
            '\\bfinally\\b', '\\bfor\\b', '\\bfrom\\b', '\\bglobal\\b',
            '\\bif\\b', '\\bimport\\b', '\\bin\\b', '\\bis\\b', '\\blambda\\b',
            '\\bNone\\b', '\\bnonlocal\\b', '\\bnot\\b', '\\bor\\b',
            '\\bpass\\b', '\\braise\\b', '\\breturn\\b', '\\bTrue\\b',
            '\\btry\\b', '\\bwhile\\b', '\\bwith\\b', '\\byield\\b',
            # JS/HTML common keywords
            '\\bconst\\b', '\\blet\\b', '\\bvar\\b', '\\bfunction\\b',
            '\\b<!DOCTYPE\\b', '\\b<html>\\b', '\\b<body>\\b'
        ]
        for word in keywords:
            pattern = QRegularExpression(word)
            self.highlighting_rules.append((pattern, keyword_format))

        # 2. Classes
        class_format = QTextCharFormat()
        class_format.setForeground(class_color)
        class_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.append((QRegularExpression("\\bclass\\s+[A-Za-z_]+"), class_format))

        # 3. Functions
        function_format = QTextCharFormat()
        function_format.setForeground(function_color)
        self.highlighting_rules.append((QRegularExpression("\\bdef\\s+[A-Za-z_]+"), function_format))
        self.highlighting_rules.append((QRegularExpression("\\b[A-Za-z_]+\\s*(?=\\()"), function_format))

        # 4. Numbers
        number_format = QTextCharFormat()
        number_format.setForeground(number_color)
        self.highlighting_rules.append((QRegularExpression("\\b[0-9]+[a-zA-Z_]*\\b"), number_format))

        # 5. Strings (Double & Single Quotes)
        string_format = QTextCharFormat()
        string_format.setForeground(string_color)
        self.highlighting_rules.append((QRegularExpression("\".*\""), string_format))
        self.highlighting_rules.append((QRegularExpression("'.*'"), string_format))

        # 6. Comments (Python '#' and JS '//')
        comment_format = QTextCharFormat()
        comment_format.setForeground(comment_color)
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression("#[^\n]*"), comment_format))
        self.highlighting_rules.append((QRegularExpression("//[^\n]*"), comment_format))
        
        # HTML comments <!-- -->
        self.comment_start_expression = QRegularExpression("<!--")
        self.comment_end_expression = QRegularExpression("-->")
        self.multi_line_comment_format = comment_format

    def highlightBlock(self, text):
        """Applies formatting to a block of text."""
        for pattern, format in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

        # Multi-line HTML comments
        self.setCurrentBlockState(0)
        start_index = 0
        if self.previousBlockState() != 1:
            match = self.comment_start_expression.match(text)
            start_index = match.capturedStart()
        
        while start_index >= 0:
            match = self.comment_end_expression.match(text, start_index)
            end_index = match.capturedStart()
            comment_length = 0
            if end_index == -1:
                self.setCurrentBlockState(1)
                comment_length = len(text) - start_index
            else:
                comment_length = end_index - start_index + match.capturedLength()
            self.setFormat(start_index, comment_length, self.multi_line_comment_format)
            start_index = self.comment_start_expression.match(text, start_index + comment_length).capturedStart()
