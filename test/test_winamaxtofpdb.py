import re
import pytest
import sys 


from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from WinamaxToFpdb import Winamax


re_Identify = Winamax.re_Identify
sym = Winamax.sym
re_HandInfo = Winamax.re_HandInfo
substitutions = Winamax.substitutions
re_HUTP = Winamax.re_HUTP
re_PlayerInfo = Winamax.re_PlayerInfo


def test_re_Identify():
    text = 'Winamax Poker - ESCAPE "Colorado" - HandId: #18876587-492053-1695486636 - Holdem no limit (0.01€/0.02€) - 2023/09/23 16:30:36 UTC'
    match = re_Identify.search(text)
    assert match is not None





def test_re_HUTP():
    text = 'Hold-up to Pot: total 0.20€'
    match = re_HUTP.search(text)
    assert match is not None
    assert match.group('AMOUNT') == '0.20'










def test_re_PlayerInfo():
    text = 'Seat 1: 77boy77 (0.60€)'
    match = re_PlayerInfo.search(text)
    assert match is not None
    assert match.group('SEAT') == '1'
    assert match.group('PNAME') == '77boy77'
    assert match.group('CASH') == '0.60'
