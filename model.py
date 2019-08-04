# Module model

#== PASSAGE ========================================================================
class Passage(object):
    """ Describes a sequence of bars. """
    def __init__(self, passage_string):
        self.bars = self._parse_passage(passage_string)

    def _parse_passage(self, passage_string):
        result = []
        for bar_string in passage_string.split():
            result.append(Bar(bar_string))

        return result

class Repeat(Passage):
    def __init__(self, repeat_string):
        if repeat_string[0] == '(' and repeat_string[-1] == ')':
            passage_string = repeat_string[1:-1]
            super(Repeat, self).__init__(passage_string)
        else:
            raise ValueError('Repeat string has the wrong format!')

#== BAR ============================================================================
class Bar:
    def __init__(self, bar_string):
        self.chords = self._parse_bar(bar_string)

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


#== CHORD ==========================================================================
class Chord:
    def __init__(self, chord_string):
        self.chord_symbol = self._parse_chord(chord_string)

    def _parse_chord(self, chord_word):
        """ Used to parse a single word containing a 'chord' - if necessary.

        As of 2019-08-03 only supports major (A -> A) and minor (Am, a -> Am)
        This is only supposed to be used internally, therefore no .strip()s are made.
        """
        if chord_word != '' and chord_word[0].islower():
            res = chord_word[0].upper()
            res += 'm'
            return res
        elif (chord_word == '*'):
            return ''
        else:
            return chord_word
