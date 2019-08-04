import pytest
from leadsheet import LeadSheet, _parse_chord

@pytest.fixture
def leadsheet():
    """ Setup leadsheet fixture. """
    return LeadSheet("Test fixture", "Artist")

def test_pdf_should_always_be_210mm_in_width(leadsheet):
    assert round(leadsheet.fw) == 210

def test_default_pdf_should_always_have_10mm_margins(leadsheet):
    assert leadsheet.l_margin == 10
    assert leadsheet.t_margin == 10
    assert leadsheet.r_margin == -10


def test_calculate_width_for_staff_defaults_should_be_correct(leadsheet):
    width = leadsheet.calculate_width_for_staff('a b c d')
    #               total   margins barlines
    assert width == (210   - 20     - 2*5)

def test_calculate_width_for_staff_large_margins_should_be_correct():
    ls = LeadSheet("", "", 50, 0, 50)
    width = ls.calculate_width_for_staff('a b c d')
    #               total   margins barlines
    assert width == (210   - 100     - 2*5)

def test_parse_chord_should_parse_minor_chords_correctly(leadsheet):
    assert _parse_chord('c') == 'Cm'
    assert _parse_chord('Cm') == 'Cm'

def test_parse_chord_should_parse_minor_chords_correctly(leadsheet):
    assert _parse_chord('C') == 'C'

def test_parse_chord_should_return_empty_string_is_asterisk_is_passed(leadsheet):
    assert _parse_chord('*') == ''

def test_generate_bar_should_correctly_space_a_simple_bar(leadsheet):
    result = leadsheet.generate_bar('C', 100)
    _, size = result[0]
    assert size == 100

def test_generate_bar_should_correctly_space_a_crowded_bar(leadsheet):
    _, size = leadsheet.generate_bar('c_c_c_c_c', 100)[0]
    assert size == 20

def test_generate_staff_should_correcly_space_bars(leadsheet):
    _, size = leadsheet.generate_staff('C C', 100)[0][0]
    assert size == 50

def test_generate_staff_should_return_empty_list_if_staff_string_is_empty(leadsheet):
    assert leadsheet.generate_staff(' ', 0) == []
