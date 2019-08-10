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
