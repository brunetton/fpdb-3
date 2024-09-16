import pytest
import sys
from decimal import Decimal
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from HandHistoryConverter import HandHistoryConverter
from Hand import Hand, Pot
from Exceptions import FpdbParseError

class MockConfig:
    def __init__(self):
        self.supported_sites = {"PokerStars": 9}
    
    def get_site_id(self, site_name):
        return self.supported_sites.get(site_name, None)

    def get_import_parameters(self):
        return {
            "saveActions": False,
            "callFpdbHud": False,
            "cacheSessions": False,
            "publicDB": False,
            "xloc": None,
            "yloc": None,
            "height": None,
            "width": None
        }

class MockHand(Hand):
    SYMBOL = {'USD': "$", 'EUR': "€", 'T$': "", 'play': ""}
    
    def __init__(self, config):
        self.allStreets = ['BLINDSANTES', 'PREFLOP', 'FLOP', 'TURN', 'RIVER']
        self.actionStreets = ['BLINDSANTES', 'PREFLOP', 'FLOP', 'TURN', 'RIVER']
        self.holeStreets = ['PREFLOP']
        self.discardStreets = ['PREFLOP']
        
        gametype = {
            "type": "ring",
            "category": "holdem",
            "limitType": "nl",
            "currency": "USD"
        }
        
        super().__init__(config, "PokerStars", gametype, "")
        
        self.totalpot = 0
        self.totalcollected = 0
        self.rake = None
        self.roundPenny = False
        self.cashedOut = False
        self.siteId = 9  # Assuming PokerStars
        self.rakes = {}
        self.sb = 0
        self.bb = 0
        self.pot = Pot()
        self.handText = ""
        self.handid = "12345"
        self.startTime = None
        self.sym = self.SYMBOL[self.gametype['currency']]

    def update_currency(self):
        self.sym = self.SYMBOL[self.gametype['currency']]

class MockHandHistoryConverter(HandHistoryConverter):
    def __init__(self, config):
        self.config = config
        self.sitename = "PokerStars"
        self.siteId = 9
        self.in_path = '-'
        self.out_path = '-'

    def readFile(self):
        pass

    def start(self):
        pass

@pytest.fixture
def mock_config():
    return MockConfig()

@pytest.fixture
def hhc(mock_config):
    return MockHandHistoryConverter(mock_config)

def test_getRake_main_pot_only(hhc, mock_config):
    hand = MockHand(mock_config)
    assert hand.gametype['currency'] == 'USD'
    assert hand.sym == '$'
    
    hand.totalpot = Decimal('100')
    hand.totalcollected = Decimal('95')
    hand.pot.pots = [(Decimal('100'), set(['Player1', 'Player2', 'Player3']))]
    
    hhc.getRake(hand)
    
    assert hand.rake == Decimal('5')
    
def test_getRake_no_rake(hhc, mock_config):
    hand = MockHand(mock_config)
    hand.totalpot = Decimal('100')
    hand.totalcollected = Decimal('100')
    hand.pot.pots = [(Decimal('100'), set(['Player1', 'Player2']))]
    
    hhc.getRake(hand)
    
    assert hand.rake == Decimal('0')

def test_getRake_tournament(hhc, mock_config):
    hand = MockHand(mock_config)
    hand.gametype['type'] = 'tour'
    hand.totalpot = Decimal('1000')
    hand.totalcollected = Decimal('950')
    hand.pot.pots = [(Decimal('1000'), set(['Player1', 'Player2', 'Player3', 'Player4']))]
    
    hhc.getRake(hand)
    
    assert hand.rake == Decimal('50')

def test_getRake_cashed_out(hhc, mock_config):
    hand = MockHand(mock_config)
    hand.totalpot = Decimal('100')
    hand.totalcollected = Decimal('80')
    hand.cashedOut = True
    hand.pot.pots = [(Decimal('100'), set(['Player1', 'Player2']))]
    
    hhc.getRake(hand)
    
    assert hand.rake == Decimal('20')

def test_getRake_round_penny(hhc, mock_config):
    hand = MockHand(mock_config)
    hand.totalpot = Decimal('100.02')
    hand.totalcollected = Decimal('100.01')
    hand.roundPenny = True
    hand.pot.pots = [(Decimal('100.02'), set(['Player1', 'Player2']))]
    
    hhc.getRake(hand)
    
    assert hand.rake == Decimal('0.01')

def test_getRake_collected_greater_than_pot(hhc, mock_config):
    hand = MockHand(mock_config)
    hand.totalpot = Decimal('100')
    hand.totalcollected = Decimal('101')
    hand.pot.pots = [(Decimal('100'), set(['Player1', 'Player2']))]
    
    with pytest.raises(FpdbParseError):
        hhc.getRake(hand)

def test_getRake_high_rake(hhc, mock_config):
    hand = MockHand(mock_config)
    hand.totalpot = Decimal('100')
    hand.totalcollected = Decimal('70')
    hand.pot.pots = [(Decimal('100'), set(['Player1', 'Player2']))]
    
    with pytest.raises(FpdbParseError):
        hhc.getRake(hand)

def test_getRake_pokerbros(hhc, mock_config):
    hand = MockHand(mock_config)
    hand.siteId = 29  # Assuming 29 is PokerBros
    hand.totalpot = Decimal('100')
    hand.totalcollected = Decimal('90')
    hand.sb = Decimal('1')
    hand.bb = Decimal('2')
    hand.rakes['rake'] = Decimal('7')
    hand.pot.pots = [(Decimal('100'), set(['Player1', 'Player2']))]
    
    hhc.getRake(hand)
    
    assert hand.rake == Decimal('10')

def test_getRake_fast_fold(hhc, mock_config):
    hand = MockHand(mock_config)
    hand.totalpot = Decimal('100')
    hand.totalcollected = Decimal('75')
    hand.fastFold = True
    hand.pot.pots = [(Decimal('100'), set(['Player1', 'Player2']))]
    
    hhc.getRake(hand)
    
    assert hand.rake == Decimal('25')

def test_getRake_zero_pot(hhc, mock_config):
    hand = MockHand(mock_config)
    hand.totalpot = Decimal('0')
    hand.totalcollected = Decimal('0')
    hand.pot.pots = []
    
    hhc.getRake(hand)
    
    assert hand.rake == Decimal('0')

def test_getRake_negative_rake(hhc, mock_config):
    hand = MockHand(mock_config)
    hand.totalpot = Decimal('100')
    hand.totalcollected = Decimal('102')
    hand.pot.pots = [(Decimal('100'), set(['Player1', 'Player2']))]
    
    with pytest.raises(FpdbParseError):
        hhc.getRake(hand)

def test_getRake_pokerstars_omaha(hhc, mock_config):
    hand = MockHand(mock_config)
    hand.handid = "252349922248"
    hand.gametype['category'] = 'omahahi'
    hand.gametype['limitType'] = 'pl'
    hand.gametype['currency'] = 'EUR'
    hand.update_currency()  # Update the currency symbol
    hand.totalpot = Decimal('0.71')
    hand.totalcollected = Decimal('0.67')
    hand.rake = None
    hand.sb = Decimal('0.02')
    hand.bb = Decimal('0.05')
    hand.pot.pots = [(Decimal('0.71'), set(['florentin59', 'eclipseto', 'chantfrin', 'e_carte_toi30', 'anyeflores']))]
    
    hhc.getRake(hand)
    
    assert hand.rake == Decimal('0.04')
    assert hand.totalpot == Decimal('0.71')
    assert hand.totalcollected == Decimal('0.67')
    assert hand.sym == '€'