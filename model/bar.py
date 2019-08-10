from chord import Chord
from enum import Enum, unique

class Bar:
    def __init__(self, bar_string):
        self.chords = self._parse_bar(bar_string)
        self.properties = []

    def _parse_bar(self, bar_string):
        """ Parses a single bar, which can contain more than one chord.

        Multiple chords per bar is supported using '_'.
        Empty bars are supported with asterisk (*).
        Returns a list of tuples of ('<chord_string>', sub_cell_width)
        """
        result = []
        chord_strings_in_bar = bar_string.split('_')

        for chord_string in chord_strings_in_bar:
            if chord_string != '':
                result.append( Chord(chord_string) )

        return result

    @unique
    class BarProperties(Enum):
        REPEAET_BEGIN = 'repeat_begin'
        REPEAET_END = 'repeat_end'
