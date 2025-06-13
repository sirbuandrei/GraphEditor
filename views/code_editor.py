from PyQt5.Qsci import QsciScintilla, QsciLexerPython
from PyQt5.QtGui import QColor, QFont, QTextCharFormat, QSyntaxHighlighter

class PyCharmLexer(QsciLexerPython):
    """Custom Python lexer with PyCharm-like colors"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_pycharm_colors()

    def setup_pycharm_colors(self):
        """Setup PyCharm-like color scheme"""
        self.setDefaultPaper(QColor("#2b2b2b"))  # Dark background
        self.setPaper(QColor("#2b2b2b"))

        # Default text - light gray
        self.setDefaultColor(QColor("#a9b7c6"))
        self.setColor(QColor("#a9b7c6"), QsciLexerPython.Default)

        # Comments - Gray and Green (like in your screenshot)
        self.setColor(QColor("#808080"), QsciLexerPython.Comment)  # Gray comments
        self.setColor(QColor("#629755"), QsciLexerPython.CommentBlock)  # Green block comments

        # Keywords - Orange (def, class, if, for, in, etc.)
        self.setColor(QColor("#cc7832"), QsciLexerPython.Keyword)

        # Strings - Light green for single/double quotes
        self.setColor(QColor("#a5c261"), QsciLexerPython.SingleQuotedString)  # Light green
        self.setColor(QColor("#a5c261"), QsciLexerPython.DoubleQuotedString)  # Light green

        # Triple quoted strings - Darker green
        self.setColor(QColor("#629755"), QsciLexerPython.TripleSingleQuotedString)  # Darker green
        self.setColor(QColor("#629755"), QsciLexerPython.TripleDoubleQuotedString)  # Darker green

        # F-strings and format strings - Orange (like f"Error...")
        self.setColor(QColor("#cc7832"), QsciLexerPython.SingleQuotedFString)
        self.setColor(QColor("#cc7832"), QsciLexerPython.DoubleQuotedFString)
        self.setColor(QColor("#cc7832"), QsciLexerPython.TripleSingleQuotedFString)
        self.setColor(QColor("#cc7832"), QsciLexerPython.TripleDoubleQuotedFString)

        # Numbers - Blue
        self.setColor(QColor("#6897bb"), QsciLexerPython.Number)

        # Operators - Light gray
        self.setColor(QColor("#a9b7c6"), QsciLexerPython.Operator)

        # Identifiers (variable names) - Light gray
        self.setColor(QColor("#a9b7c6"), QsciLexerPython.Identifier)

        # Function/method names - Blue (like setup_pycharm_colors, setDefaultPaper)
        self.setColor(QColor("#56a8f5"), QsciLexerPython.FunctionMethodName)  # Blue

        # Class names - Normal light gray
        self.setColor(QColor("#a9b7c6"), QsciLexerPython.ClassName)

        # Special identifiers (self, cls) - Normal light gray, not purple
        self.setColor(QColor("#a9b7c6"), QsciLexerPython.HighlightedIdentifier)

        # Decorators (@property, @staticmethod) - Yellow/Olive
        self.setColor(QColor("#bbb529"), QsciLexerPython.Decorator)

        # Unclosed strings - Red
        self.setColor(QColor("#ff6b68"), QsciLexerPython.UnclosedString)

        # Set fonts
        font = QFont("JetBrains Mono", 11)
        if not font.exactMatch():
            font = QFont("Consolas", 11)
        if not font.exactMatch():
            font = QFont("Courier New", 11)

        font.setFixedPitch(True)

        # Apply font to all styles
        for style in range(128):
            self.setFont(font, style)

        # Make keywords bold
        keyword_font = QFont(font)
        keyword_font.setBold(True)
        self.setFont(keyword_font, QsciLexerPython.Keyword)

        # Make decorators italic
        decorator_font = QFont(font)
        decorator_font.setItalic(True)
        self.setFont(decorator_font, QsciLexerPython.Decorator)


class PythonEditor(QsciScintilla):
    """Python editor with PyCharm-like appearance and behavior"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_editor()
        self.setup_lexer()

    def setup_editor(self):
        """Setup basic editor properties"""
        # Font
        font = QFont("JetBrains Mono", 11)
        if not font.exactMatch():
            font = QFont("Consolas", 11)
        if not font.exactMatch():
            font = QFont("Courier New", 11)

        font.setFixedPitch(True)
        self.setFont(font)

        # Brace matching
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # Indentation
        self.setIndentationGuides(True)
        self.setIndentationGuidesBackgroundColor(QColor("#3c3c3c"))
        self.setIndentationGuidesForegroundColor(QColor("#606060"))
        self.setTabWidth(4)
        self.setIndentationsUseTabs(False)
        self.setAutoIndent(True)

        # Autocomplete
        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.setAutoCompletionThreshold(2)
        self.setAutoCompletionCaseSensitivity(False)
        self.setAutoCompletionUseSingle(QsciScintilla.AcusNever)

        # EOL
        self.setEolMode(QsciScintilla.EolWindows)
        self.setEolVisibility(False)

        # Wrap mode
        self.setWrapMode(QsciScintilla.WrapNone)

        # Background
        self.setCaretLineBackgroundColor(QColor("#323232"))
        self.setCaretLineVisible(True)

        # Caret
        self.setCaretForegroundColor(QColor("#ffffff"))
        self.setCaretWidth(2)

        # Margins
        self.setMarginType(0, QsciScintilla.NumberMargin)
        self.setMarginWidth(0, "000")
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("#313335"))
        self.setMarginsForegroundColor(QColor("#606366"))

    def setup_lexer(self):
        lexer = PyCharmLexer(self)
        self.setLexer(lexer)