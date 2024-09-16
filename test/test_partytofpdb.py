import re
import pytest
import sys 


from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from PartyPokerToFpdb import PartyPoker

# Récupérer les regex depuis la classe Cake
re_GameInfo = PartyPoker.re_GameInfo

def test_re_GameInfo():
    text = """
                ***** Hand History for Game 23913549618 *****
                €2 EUR PL Omaha - Monday, September 25, 20:28:14 CEST 2023
                Table Besançon (Real Money)
                """
    match = re_GameInfo.search(text)
    assert match is not None
    assert match.group('HID') == '23913549618'
    assert match.group('CURRENCY') == '€'
    assert match.group('GAME') == 'Omaha'
