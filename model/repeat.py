from passage import Passage

class Repeat(Passage):
    def __init__(self, repeat_string):
        if repeat_string[0] == '(' and repeat_string[-1] == ')':
            passage_string = repeat_string[1:-1]
            super(Repeat, self).__init__(passage_string)
        else:
            raise ValueError('Repeat string has the wrong format!')

    # override
    def get_outer_barlines(self):
        return ('(', ')')
