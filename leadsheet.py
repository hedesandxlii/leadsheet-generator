from fpdf import FPDF
from model import *

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
        self.barline_width = 2
        self.staff_height = 25
        self.columns = 4
        self.rows = 8

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

    def calculate_width_for_staff(self, num_bars):
        """ Calculates the maximum width for a staff. """
        num_barlines = num_bars + 1;
        return (self.useable_width - num_barlines * self.barline_width)

    def print_passage(self, passage):
        """ Prints a whole staff to pdf.

        A chord string will be formatted and printed to the pdf.
        staff_string example: 'E C D E' for 4 bars of those chords.
        """
        staff_width = self.calculate_width_for_staff(self.columns)
        print_queue = self.get_print_queue(passage,
                self.calculate_width_for_staff(len(passage.bars)))
        for string, width in print_queue:
            if string == 'newline':
                self.ln(self.staff_height)
            else:
                self._debug_cell(width, string, 'L')


    def get_print_queue(self, passage, useable_width):
        """ Return a list of tuples [('string', width), ...]
        """
        result = []
        outer_barlines = passage.get_outer_barlines()
        num_bars = len(passage.bars)
        num_rows = int(num_bars)/int(self.columns)
        last_line = self.columns % num_bars
        # Every row of bars
        for i in range(self.columns):
            for j in range(num_rows):
                if i+j == 0:
                    result.append( (outer_barlines[0], self.barline_width) )
                elif i+j == num_bars:
                    result.append( (outer_barlines[1], self.barline_width) )
                else:
                    result.append( ('|', self.barline_width) )
                    break


        return result

    def print_barline(self, line, line_break=False):
        """ Prints a barline with width 'self.barline_width' """
        self._font_stack_push(self.notation_font)
        self._debug_cell(self.barline_width, line)
        if line_break:
            self.ln(self.staff_height)
        self._font_stack_pop()

# tmp driver.
if __name__ == "__main__":
    ls = LeadSheet('Macken', 'Galenskaparna')
    ls.add_page()
    ls.print_passage(Repeat('(a F C G a F C G)'))
    ls.add_page()
    ls.output('test.pdf', 'F')
