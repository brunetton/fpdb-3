import sys
import pytest
import re
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from PokerStarsToFpdb import PokerStars


re_WinningRankOne = PokerStars.re_WinningRankOne




def test_re_WinningRankOne():
    text = """jeje_sat wins the tournament and receives €0.75 - congratulations!"""
    match = re_WinningRankOne.search(text)
    assert match is not None
    assert match.group('PNAME') == "jeje_sat"
    assert match.group('AMT') == "0.75"
    



class MockConfig:
    def __init__(self):
        self.site_dict = {"PokerStars": 9}

    def get_import_parameters(self):
        return {
            "changeTimezone": True,
            "recordHudCache": True,
            "allowPartialPhasedRebuy": False,
            "fastStoreHudCache": False,
            "saveActions": False,
            "cacheSessions": False,
            "sessionTimeout": 30,
            "starsArchive": False,
            "ftpArchive": False,
            "testData": False,
            "publicDB": False,
            "callFpdbHud": True,
            "saveStarsHH": False,
            "importFilters": [],
        }

@pytest.fixture
def parser():
    config = MockConfig()
    return PokerStars(config)

def test_re_GameInfo(parser):
    hand = """PokerStars Hand #252348904512:  Omaha Pot Limit (€0.02/€0.05 EUR) - 2024/09/08 18:04:56 CET [2024/09/08 12:04:56 ET]
Table 'Noemi II' 6-max Seat #1 is the button"""
    m = parser.re_GameInfo.search(hand)
    assert m is not None
    assert m.group('HID') == '252348904512'
    assert m.group('GAME') == 'Omaha'
    assert m.group('LIMIT') == 'Pot Limit'
    assert m.group('CURRENCY') == '€'
    assert m.group('SB') == '0.02'
    assert m.group('BB') == '0.05'

def test_re_PlayerInfo(parser):
    hand = "Seat 1: totokex73 (€7.12 in chips)"
    m = parser.re_PlayerInfo.search(hand)
    assert m is not None
    assert m.group('SEAT') == '1'
    assert m.group('PNAME') == 'totokex73'
    assert m.group('CASH') == '7.12'

def test_re_HandInfo(parser):
    hand = "Table 'Noemi II' 6-max Seat #1 is the button"
    m = parser.re_HandInfo.search(hand)
    assert m is not None
    assert m.group('TABLE') == 'Noemi II'
    assert m.group('MAX') == '6'
    assert m.group('BUTTON') == '1'

def test_re_Board(parser):
    board = "[6c 5h Tc Ah 3c]"
    m = parser.re_Board.search(board)
    assert m is not None
    assert m.group('CARDS') == '6c 5h Tc Ah 3c'

def test_re_DateTime(parser):
    date = "2024/09/08 18:04:56"
    m = parser.re_DateTime1.search(date)
    assert m is not None
    assert m.group('Y') == '2024'
    assert m.group('M') == '09'
    assert m.group('D') == '08'
    assert m.group('H') == '18'
    assert m.group('MIN') == '04'
    assert m.group('S') == '56'

def test_re_PostSB(parser):
    action = "florentin59: posts small blind €0.02"
    m = parser.re_PostSB.search(action)
    assert m is not None
    assert m.group('PNAME') == 'florentin59'
    assert m.group('SB') == '0.02'

def test_re_PostBB(parser):
    action = "jeje_sat: posts big blind €0.05"
    m = parser.re_PostBB.search(action)
    assert m is not None
    assert m.group('PNAME') == 'jeje_sat'
    assert m.group('BB') == '0.05'

@pytest.mark.parametrize("action,expected_type", [
    ("florentin59: calls €0.05", ' calls'),
    ("jeje_sat: raises €0.17 to €0.22", ' raises'),
    ("e_carte_toi30: folds", ' folds'),
    ("flavorfla11: checks", ' checks')
])
def test_re_Action(parser, action, expected_type):
    m = parser.re_Action.search(action)
    assert m is not None
    assert m.group('ATYPE') == expected_type

def test_re_ShowdownAction(parser):
    action = "florentin59: shows [Kh 6h Kc Qs] (a full house, Kings full of Tens)"
    m = parser.re_ShowdownAction.search(action)
    assert m is not None
    assert m.group('PNAME') == 'florentin59'
    assert m.group('CARDS') == 'Kh 6h Kc Qs'

def test_re_CollectPot(parser):
    collect = "Seat 2: florentin59 collected (€10.81)"
    m = parser.re_CollectPot.search(collect)
    assert m is not None
    assert m.group('PNAME') == 'florentin59'
    assert m.group('POT') == '10.81'


