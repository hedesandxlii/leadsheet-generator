import pytest
from leadsheet import LeadSheet
from model import *

@pytest.fixture(scope='function')
def leadsheet():
    """ Setup leadsheet fixture. """
    return LeadSheet("Test fixture", "Artist")

@pytest.fixture(scope='function')
def minor_chord_lower():
    return Chord('a')

@pytest.fixture(scope='function')
def minor_chord_expl():
    return Chord('a')

@pytest.fixture(scope='function')
def major_chord():
    return Chord('A')

@pytest.fixture(scope='function')
def one_chord_bar():
    return Bar('A')

@pytest.fixture(scope='function')
def four_chord_bar():
    return Bar('A_A_A_A')

@pytest.fixture(scope='function')
def four_bar_passage():
    return Passage('a F C G')

@pytest.fixture(scope='function')
def four_bar_repeat():
    return Repeat('(a F C G)')

@pytest.fixture(scope='function')
def one_bar_repeat():
    return Repeat('(a)')

def test_pdf_should_always_be_210mm_in_width(leadsheet):
    assert round(leadsheet.fw) == 210

def test_default_pdf_should_always_have_10mm_margins(leadsheet):
    assert leadsheet.l_margin == 10
    assert leadsheet.t_margin == 10
    assert leadsheet.r_margin == -10

def test_calculate_width_for_staff_defaults_should_be_correct(leadsheet):
    leadsheet.barline_width = 2
    width = leadsheet.calculate_width_for_staff(4)
    #               total   margins barlines
    assert width == (210   - 20     - 2*5)

def test_calculate_width_for_staff_large_margins_should_be_correct():
    ls = LeadSheet("", "", 50, 0, 50)
    ls.barline_width = 2
    width = ls.calculate_width_for_staff(4)
    #               total   margins barlines
    assert width == (210   - 100     - 2*5)

## MODEL
def test_parse_chord_should_parse_minor_chords_correctly(minor_chord_lower, minor_chord_expl):
    assert minor_chord_lower.chord_symbol == 'Am'
    assert minor_chord_expl.chord_symbol == 'Am'

def test_parse_chord_should_parse_major_chords_correctly(major_chord):
    assert major_chord.chord_symbol == 'A'

def test_parse_chord_should_return_empty_string_is_asterisk_is_passed():
    assert Chord('*').chord_symbol == ''

def test_parse_bar_should_have_correct_length(one_chord_bar):
    assert len(one_chord_bar.chords) == 1

def test_long_parse_bar_should_also_have_correct_length(four_chord_bar):
    assert len(four_chord_bar.chords) == 4

def test_no_chord_bar_should_have_lenght_1():
    assert len(Bar('*').chords) == 1

def test_empty_string_should_not_be_parsed_as_a_bar():
    assert len(Bar('').chords) == 0

def test_simple_bar_passage_should_be_parsed_correctly(four_bar_passage):
    assert len(four_bar_passage.bars) == 4

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

def test_repeat_should_set_bar_properties_correctly(four_bar_repeat):
    assert Bar.BarProperties.REPEAET_BEGIN in four_bar_repeat.bars[0].properties
    assert Bar.BarProperties.REPEAET_END in four_bar_repeat.bars[-1].properties

def test_one_bar_repeat_should_have_both_REPEAT_BEGIN_and_REPEAT_END(one_bar_repeat):
    assert Bar.BarProperties.REPEAET_BEGIN in one_bar_repeat.bars[0].properties
    assert Bar.BarProperties.REPEAET_END in one_bar_repeat.bars[0].properties
