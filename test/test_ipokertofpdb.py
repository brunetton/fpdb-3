import sys
import pytest
import re
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from iPokerToFpdb import iPoker


re_PlayerInfo = iPoker.re_PlayerInfo
re_GameInfoTrny = iPoker.re_GameInfoTrny
re_GameInfoTrny2 = iPoker.re_GameInfoTrny2
re_TourNo = iPoker.re_TourNo
re_client = iPoker.re_client
re_MaxSeats = iPoker.re_MaxSeats






def test_re_PlayerInfo2():
    text = '<player bet="20" reg_code="5105918454" win="0" seat="10" dealer="1" rebuy="0" chips="20" name="clement10s" addon="0"/>'
    match = re_PlayerInfo.search(text)
    assert match is not None

def test_re_PlayerInfo7():
    text = '<player bet="100" reg_code="" win="40" seat="3" dealer="0" rebuy="0" chips="1 480" name="pergerd" addon="0"/>'
    match = re_PlayerInfo.search(text)
    assert match is not None
    assert match.group('SEAT') == '3'
    assert match.group('PNAME') == 'pergerd'
    assert match.group('CASH') == '1 480'
    assert match.group('BUTTONPOS') == '0'
    assert match.group('WIN') == '40'
    assert match.group('BET') == '100'

def test_re_PlayerInfo3():
    text='<player bet="100" reg_code="" win="40" seat="3" dealer="0" rebuy="0" chips="1 480" name="pergerd" addon="0"/><player bet="20" reg_code="5105918454" win="0" seat="10" dealer="1" rebuy="0" chips="20" name="clement10s" addon="0"/>'
    m = re_PlayerInfo.finditer(text)
    plist = {}
    for a in m:
        ag = a.groupdict()
        plist[a.group('PNAME')] = [int(a.group('SEAT')), (a.group('CASH')), 
                                        (a.group('WIN')), False]
    assert len(plist) == 2  
    

def test_re_PlayerInfo8():
    text = '<player bet="740" reg_code="" win="1 480" seat="3" dealer="1" rebuy="0" chips="740" name="pergerd" addon="0"/>'
    match = re_PlayerInfo.search(text)
    assert match is not None
    assert match.group('SEAT') == '3'
    assert match.group('PNAME') == 'pergerd'
    assert match.group('CASH') == '740'
    assert match.group('BUTTONPOS') == '1'
    assert match.group('WIN') == '1 480'
    assert match.group('BET') == '740'









def test_re_GameInfoTrny():
    text = """
  <tournamentcode>826763510</tournamentcode>
  <tournamentname>Sit’n’Go Twister 0.20€</tournamentname>
  <rewarddrawn>0,80€</rewarddrawn>
  <place>2</place>
  <buyin>0€ + 0,01€ + 0,19€</buyin>
  <totalbuyin>0,20€</totalbuyin>
  <win>0</win>
"""
    matches = list(re_GameInfoTrny.finditer(text))

    assert matches[0].group('TOURNO') == '826763510'
    assert matches[1].group('NAME') == 'Sit’n’Go Twister 0.20€'
    assert matches[2].group('REWARD') == '0,80€'
    assert matches[3].group('PLACE') == '2'
    assert matches[4].group('BIAMT') == '0€'
    assert matches[4].group('BIRAKE') == '0,01€'
    assert matches[4].group('BIRAKE2') == '0,19€'
    assert matches[5].group('TOTBUYIN') == '0,20€'
    assert matches[6].group('WIN') == '0'


def test_re_GameInfoTrnywin():
    text = """
  <tournamentcode>829730818</tournamentcode>
  <tournamentname>Sit’n’Go Twister 0.20€</tournamentname>
  <rewarddrawn>0,40€</rewarddrawn>
  <place>1</place>
  <buyin>0€ + 0,01€ + 0,19€</buyin>
  <totalbuyin>0,20€</totalbuyin>
  <win>0,40€</win>
"""
    matches = list(re_GameInfoTrny.finditer(text))

    assert matches[0].group('TOURNO') == '829730818'
    assert matches[1].group('NAME') == 'Sit’n’Go Twister 0.20€'
    assert matches[2].group('REWARD') == '0,40€'
    assert matches[3].group('PLACE') == '1'
    assert matches[4].group('BIAMT') == '0€'
    assert matches[4].group('BIRAKE') == '0,01€'
    assert matches[4].group('BIRAKE2') == '0,19€'
    assert matches[5].group('TOTBUYIN') == '0,20€'
    assert matches[6].group('WIN') == '0,40€'


def test_re_GameInfoTrny_red():
    text = """
  <tournamentcode>1061132557</tournamentcode>
  <tournamentname>E10 Freebuy Sat 1x30€</tournamentname>
  <place>N/A</place>
  <buyin>€0 + €0</buyin>
  <totalbuyin>€0</totalbuyin>
  <win>N/A</win>
"""
    matches = list(re_GameInfoTrny2.finditer(text))

    assert matches[0].group('TOURNO') == '1061132557'
    assert matches[1].group('NAME') == 'E10 Freebuy Sat 1x30€'

    assert matches[2].group('PLACE') == 'N/A'
    assert matches[3].group('BIAMT') == '€0'
    assert matches[3].group('BIRAKE') == '€0'

    assert matches[4].group('TOTBUYIN') == '€0'
    assert matches[5].group('WIN') == 'N/A'

def test_re_GameInfoTrny_red():
    text = """
  <tournamentcode>1067382320</tournamentcode>
  <tournamentname>Series Freebuy Sat 1x125€</tournamentname>
  <place>851</place>
  <buyin>€0 + €0</buyin>
  <totalbuyin>€0</totalbuyin>
  <win>0</win>
"""
    matches = list(re_GameInfoTrny2.finditer(text))

    assert matches[0].group('TOURNO') == '1067382320'
    assert matches[1].group('NAME') == 'Series Freebuy Sat 1x125€'

    assert matches[2].group('PLACE') == '851'
    assert matches[3].group('BIAMT') == '€0'
    assert matches[3].group('BIRAKE') == '€0'

    assert matches[4].group('TOTBUYIN') == '€0'
    assert matches[5].group('WIN') == '0'





def test_re_Tourno1():
    text = 'Sit’n’Go Twister 0.20€, 829730819'
    match = re_TourNo.search(text)
    assert match.group('TOURNO') == '829730819'



    


def test_re_cliento1():
    text = '<client_version>23.5.1.13</client_version>'
    match = re_client.search(text)
    assert match.group('CLIENT') == '23.5.1.13'




def test_MaxSeats1():
    text = '<tablesize>6</tablesize>'
    match = re_MaxSeats.search(text)
    assert match.group('SEATS') == '6'