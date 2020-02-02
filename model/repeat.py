from .passage import Passage
from .bar import Bar

class Repeat(Passage):
    def __init__(self, repeat_string):
        if repeat_string[0] == '(' and repeat_string[-1] == ')':
            passage_string = repeat_string[1:-1]
            super(Repeat, self).__init__(passage_string)
            # Set properties of starting and ending bars to be repeats.
            self.bars[0].properties.append(Bar.BarProperties.REPEAET_BEGIN)
            self.bars[-1].properties.append(Bar.BarProperties.REPEAET_END)
        else:
            raise ValueError('Repeat string has the wrong format!')
