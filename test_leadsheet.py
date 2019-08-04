import pytest
from leadsheet import LeadSheet
from model import Bar, Chord, Passage, Repeat

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
    width = leadsheet.calculate_width_for_staff(4)
    #               total   margins barlines
    assert width == (210   - 20     - 2*5)

def test_calculate_width_for_staff_large_margins_should_be_correct():
    ls = LeadSheet("", "", 50, 0, 50)
    width = ls.calculate_width_for_staff(4)
    #               total   margins barlines
    assert width == (210   - 100     - 2*5)

## MODEL
def test_parse_chord_should_parse_minor_chords_correctly():
    assert Chord('c').chord_symbol == 'Cm'
    assert Chord('Cm').chord_symbol == 'Cm'

def test_parse_chord_should_parse_minor_chords_correctly():
    assert Chord('C').chord_symbol == 'C'

def test_parse_chord_should_return_empty_string_is_asterisk_is_passed():
    assert Chord('*').chord_symbol == ''

def test_parse_bar_should_have_correct_length():
    assert len(Bar('C').chords) == 1

def test_long_parse_bar_should_also_have_correct_length():
    assert len(Bar('c_c_c_c_c_c_C').chords) == 7

def test_no_chord_bar_should_have_lenght_1():
    assert len(Bar('*').chords) == 1

def test_empty_string_should_not_be_parsed_as_a_bar():
    assert len(Bar('').chords) == 0

def test_simple_bar_passage_should_be_parsed_correctly():
    assert len(Passage('a b c d').bars) == 4

def test_empty_bar_passage_should_be_parsed_correctly():
    assert len(Passage(' ').bars) == 0

def test_repeat_should_be_able_to_parse_ok_string():
    try:
        Repeat('(a)')
        assert 1
    except ValueError:
        assert 0

def test_repeat_should_be_fail_a_passage_without_parentesis():
    try:
        Repeat('a')
        assert 0
    except ValueError:
        assert 1
