from PyQt5.QtCore import QRegularExpression, QRegularExpressionMatch, QRegularExpressionMatchIterator
from PyQt5.QtGui import QSyntaxHighlighter

from src import utils

class IniHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(IniHighlighter, self).__init__(parent)

        self.rules = [
            ( QRegularExpression('\[.*\]'), utils.char_format(( 50, 50, 250 ), [ 'bold' ]) ),
            ( QRegularExpression('.+?(?=\=)'), utils.char_format(( 50, 50, 50 )) ),
            ( QRegularExpression('(?<=\=()).*'), utils.char_format(( 175, 5, 5 )) ),
            ( QRegularExpression('(?<=\=)\s*\-?\s*[\d]+(\.\d+)?$'), utils.char_format(( 175, 175, 5 )) ),
            ( QRegularExpression('#.*'), utils.char_format(( 15, 150, 15 ), [ 'italic' ]) ),
            ( QRegularExpression(';.*'), utils.char_format(( 15, 150, 15 ), [ 'italic' ]) )
        ]



    def highlightBlock(self, text):
        for ( regex, q_format ) in self.rules:
            iterator = regex.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()

                index = match.capturedStart()
                length = match.capturedLength()
                self.setFormat(index, length, q_format)
