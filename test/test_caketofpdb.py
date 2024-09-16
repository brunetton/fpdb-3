import re
import pytest
import sys 

from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from CakeToFpdb import Cake


re_PlayerInfo = Cake.re_PlayerInfo
re_PlayerInfo2 = Cake.re_PlayerInfo  
re_GameInfo = Cake.re_GameInfo


def test_re_PlayerInfo2():
    text = 'Seat 1: joker7 (1 200 in chips) '
    match = re_PlayerInfo.search(text)
    assert match is not None
    assert match.group('SEAT') == '1'
    assert match.group('PNAME') == 'joker7'
    assert match.group('CASH') == '1 200'

def test_re_PlayerInfo3():
    text = 'Seat 1: joker7 (1 200 in chips) '
    match = re_PlayerInfo2.search(text)
    assert match is not None
    assert match.group('SEAT') == '1'
    assert match.group('PNAME') == 'joker7'
    assert match.group('CASH') == '1 200'



def test_re_GameInfo3():
    text = "Hand#710910543B500014 - Freeroll to GOLD CHIPS T17122229 -- FREEROLL -- $0 + $0 -- 9 Max -- Table 4 -- 0/10/20 NL Hold'em -- 2023/09/22 - 17:35:27"
    match = re_GameInfo.search(text)
    assert match is not None
    assert match.group('HID') == '710910543B500014'
    assert match.group('TABLE') == 'Freeroll to GOLD CHIPS'
    assert match.group('DATETIME') == '2023/09/22 - 17:35:27'
    assert match.group('TABLENO') == '4'
    assert match.group('BUYIN') == '$0 + $0'
    assert match.group('TMAX') == '9'
    assert match.group('BIAMT') == '$0'
    assert match.group('BIRAKE') == '$0'
    assert match.group('ANTESB') == '0'
    assert match.group('SBBB') == '10'
    assert match.group('BB') == '20'
    assert match.group('LIMIT') == 'NL'
    assert match.group('GAME') == 'Hold\'em'


