from fpdf import FPDF

class LeadSheet(FPDF):

    # Member functions
    def __init__( self, title, artist,
                    margin_left=10, margin_top=10, margin_right=10,
                    barline_width=2 ):
        """ Sets initial values, making generation more managable. """
        super(LeadSheet, self).__init__('P', 'mm', 'A4')
        # Meta data
        self.set_title(title)
        self.artist = artist

        # Fonts
        self.add_font(family='HedesandNotation', fname=r'./fonts/hedesandnotation.ttf', uni=True)
        self.add_font(family='CaviarDreams', fname=r'./fonts/CaviarDreams.ttf', uni=True)
        self.notation_font = ('HedesandNotation', '', 7)
        self.chord_font = ('CaviarDreams', '', 30)
        self.header_font = ('Courier', 'I', 12)
        self.font_stack = []
        self._font_stack_push(self.chord_font)

        # Size and dimensions
        self.set_margins(margin_left, margin_top, -margin_right)
        self.useable_width = round(self.fw) - margin_left - margin_right
        self.barline_width = 3
        self.staff_height = 25

    def _font_stack_push(self, font_tuple):
        """ Sets current font to font_tuple.

        Pushes a font tuple (family, style, size) to the font_stack and sets it as
        the current font. Make sure to _font_stack_pop() when done.
        """
        self.font_stack.append(font_tuple)
        self.set_font(font_tuple[0], font_tuple[1], font_tuple[2])

    def _font_stack_pop(self):
        """ Restores the current font to to the previous used one.

        Pops a font tuple (family, style, size) from the font_stack and sets the
        previous font as the  current font.
        """
        if len(self.font_stack) > 0:
            self.font_stack.pop()
            last_font = self.font_stack[len(self.font_stack)-1]
            self.set_font(last_font[0], last_font[1], last_font[2])

    # Overrides
    def header(self):
        if self.page_no() == 1:
            self._print_frontpage_header()
        else:
            self._font_stack_push(self.header_font)
            self._cell(w=self.useable_width/2, txt=self.title, align='L')
            self._cell(w=self.useable_width/2, txt=self.artist, align='R')
            self._font_stack_pop()

    # Helpers
    def _debug_cell(self, w = 0, txt = '', align = 'L'):
        self.cell(w=w, h=self.staff_height, txt=txt, border=1, align=align)


    def _cell(self, w = 0, txt = '', align = 'L'):
        self.cell(w=w, h=self.staff_height, txt=txt, align=align)

#== Printing =======================================================================

    def _print_frontpage_header(self):
        # Song title
        self._font_stack_push(('Courier', 'U', 20))
        self._cell(10)
        self._cell(w=0, txt=self.title, align='L')
        self._font_stack_pop()
        self.ln(10)
        # Artist
        self._font_stack_push(('Courier', '', 15))
        self._cell(15)
        self._cell(w=0, txt=self.artist, align='L')
        self._font_stack_pop()
        self.ln(30)

    def calculate_width_for_staff(self, staff_string):
        """ Calculates the maximum width for a staff. """
        num_bars = len(staff_string.split())
        num_barlines = num_bars + 1;
        return (self.useable_width - num_barlines * self.barline_width)

    def print_staff(self, staff_string):
        """ Prints a whole staff to pdf.

        A chord string will be formatted and printed to the pdf.
        staff_string example: 'E C D E' for 4 bars of those chords.
        """
        staff_width = self.calculate_width_for_staff(staff_string)

        for bar in self.generate_staff(staff_string, staff_width):
            self.print_barline()
            for (chord_string, width) in bar:
                    self._debug_cell(width, chord_string, 'L')

        self.print_barline(True)


    def print_barline(self, line_break=False):
        """ Prints a barline with width 'self.barline_width' """
        self._font_stack_push(self.notation_font)
        self._debug_cell(self.barline_width, '|')
        if line_break:
            self.ln(self.staff_height)
        self._font_stack_pop()


#== Model ==========================================================================

    def generate_staff(self, staff_string, staff_width):
        """ Generates a staff containing a defined number of bars.

        Bars are told aside from eachother by a space (' ')
        Returns a list of list of tuples ready for printing
        Tuple format: ('<chord_string>', sub_cell_width)
        """
        result = []
        bar_strings = staff_string.strip().split()

        for bar_string in bar_strings:
            result.append( self.generate_bar(bar_string, staff_width/len(bar_strings)))

        return result

    def generate_bar(self, bar_string, cell_width):
        """ Generates a single bar, which can contain more than one chord.

        Multiple chords per bar is supported using '_'.
        Empty bars are supported with asterisk (*).
        Returns a list of tuples of ('<chord_string>', sub_cell_width)
        """
        result = []
        chord_strings_in_bar = bar_string.split('_')
        sub_cell_width = cell_width / len(chord_strings_in_bar)

        for chord_string in chord_strings_in_bar:
            parsed_chord = _parse_chord(chord_string) # parses chord
            result.append((parsed_chord, sub_cell_width))

        return result


# Non-memeber functions
def _parse_chord(chord_word):
    """ Used to parse a single word containing a 'chord' - if necessary.

    As of 2019-08-03 only supports major (A -> A) and minor (Am, a -> Am)
    This is only supposed to be used internally, therefore no .strip()s are made.
    """
    # Todo implement parser-like thingy for more complicated things.
    if chord_word != '' and chord_word[0].islower():
        res = chord_word[0].upper()
        res += 'm'
        return res
    elif (chord_word == '*'):
        return ''
    else:
        return chord_word


# tmp driver.
if __name__ == "__main__":
    ls = LeadSheet('Macken', 'Galenskaparna')
    ls.add_page()
    ls.print_staff('a F C G')
    ls.print_staff('a F C G')
    ls.print_staff('a F C G')
    ls.print_staff('a F C G')
    ls.print_staff('a F C G')
    ls.add_page()
    ls.output('test.pdf', 'F')
