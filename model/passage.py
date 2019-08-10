from bar import Bar

class Passage(object):
    """ Describes a sequence of bars. """
    def __init__(self, passage_string):
        self.bars = self._parse_passage(passage_string)

    def _parse_passage(self, passage_string):
        result = []
        for bar_string in passage_string.split():
            result.append(Bar(bar_string))

        return result
