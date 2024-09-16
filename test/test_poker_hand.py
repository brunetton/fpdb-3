# test_poker_hand.py
import sys
from pathlib import Path
import pytest
from decimal import Decimal
from unittest.mock import MagicMock

sys.path.append(str(Path(__file__).parent.parent))
# Importation des classes nécessaires depuis le script principal
from Hand import Pot, Hand, HoldemOmahaHand, DrawHand, StudHand

# Simulation de la classe Configuration si elle n'est pas disponible
class Configuration:
    def __init__(self):
        self.currency = 'USD'
        self.supportedGames = {
            'holdem': {'base': 'hold', 'category': 'holdem'}
        }

    def get_import_parameters(self):
        return {
            'saveActions': True,
            'callFpdbHud': False,
            'cacheSessions': False,
            'publicDB': False
        }

    def get_site_parameters(self, sitename):
        return {
            'timezone': 'ET',
            'currency': 'USD'
        }

    def get_site_id(self, sitename):
        return 1  # Retourne un ID factice

# Tests pour la classe Pot
def test_pot_initialization():
    pot = Pot()
    assert pot.total is None
    assert pot.sym == '$'
    assert pot.committed == {}
    assert pot.common == {}
    assert pot.antes == {}
    assert pot.contenders == set()
    assert pot.pots == []

def test_pot_add_player():
    pot = Pot()
    pot.addPlayer('Player1')
    assert pot.committed['Player1'] == Decimal(0)
    assert pot.common['Player1'] == Decimal(0)
    assert pot.antes['Player1'] == Decimal(0)

def test_pot_add_money():
    pot = Pot()
    pot.addPlayer('Player1')
    pot.addMoney('Player1', Decimal('10'))
    assert pot.committed['Player1'] == Decimal('10')
    assert 'Player1' in pot.contenders

def test_pot_add_fold():
    pot = Pot()
    pot.addPlayer('Player1')
    pot.addFold('Player1')
    assert 'Player1' not in pot.contenders

def test_pot_end_calculation():
    pot = Pot()
    pot.addPlayer('Player1')
    pot.addPlayer('Player2')
    pot.addMoney('Player1', Decimal('50'))
    pot.addMoney('Player2', Decimal('100'))
    pot.end()
    assert pot.total == Decimal('100')
    assert pot.returned == {'Player2': Decimal('50')}



def test_pot_with_equal_bets():
    """Test with two players who bet the same amount."""
    pot = Pot()
    pot.addPlayer('Player1')
    pot.addPlayer('Player2')
    pot.addMoney('Player1', Decimal('100'))
    pot.addMoney('Player2', Decimal('100'))
    pot.end()
    assert pot.total == Decimal('200')
    assert pot.pots == [(Decimal('200'), {'Player1', 'Player2'})]
    assert pot.returned == {}

def test_pot_with_one_fold():
    """Test avec trois joueurs, un se couche après avoir misé."""
    pot = Pot()
    pot.addPlayer('Player1')
    pot.addPlayer('Player2')
    pot.addPlayer('Player3')
    pot.addMoney('Player1', Decimal('50'))
    pot.addMoney('Player2', Decimal('50'))
    pot.addMoney('Player3', Decimal('50'))
    pot.addFold('Player3')  # Player3 se couche après avoir misé
    pot.end()
    assert pot.total == Decimal('150')
    assert pot.pots == [(Decimal('150'), {'Player1', 'Player2', 'Player3'})]


def test_pot_with_all_in():
    """Test with a player going all-in with less chips."""
    pot = Pot()
    pot.addPlayer('Player1')
    pot.addPlayer('Player2')
    pot.addPlayer('Player3')
    # Player3 goes all-in with 50
    pot.addMoney('Player1', Decimal('100'))
    pot.addMoney('Player2', Decimal('100'))
    pot.addMoney('Player3', Decimal('50'))
    pot.end()
    assert pot.total == Decimal('250')
    assert pot.pots == [
        (Decimal('150'), {'Player1', 'Player2', 'Player3'}),  # Main pot
        (Decimal('100'), {'Player1', 'Player2'})             # Side pot
    ]
    assert pot.returned == {}

def test_pot_with_multiple_side_pots():
    """Test avec plusieurs joueurs allant all-in à différents montants."""
    pot = Pot()
    pot.addPlayer('Player1')
    pot.addPlayer('Player2')
    pot.addPlayer('Player3')
    pot.addPlayer('Player4')
    # Player1 all-in avec 50
    # Player2 all-in avec 100
    # Player3 mise 150
    # Player4 mise 200
    pot.addMoney('Player1', Decimal('50'))
    pot.addMoney('Player2', Decimal('100'))
    pot.addMoney('Player3', Decimal('150'))
    pot.addMoney('Player4', Decimal('200'))
    pot.end()
    assert pot.total == Decimal('450')
    assert pot.pots == [
        (Decimal('200'), {'Player1', 'Player2', 'Player3', 'Player4'}),  # Pot principal
        (Decimal('150'), {'Player2', 'Player3', 'Player4'}),             # Pot secondaire 1
        (Decimal('100'), {'Player3', 'Player4'}),                        # Pot secondaire 2 (corrigé)
        (Decimal('50'), {'Player4'})                                     # Pot secondaire 3
    ]
    assert pot.returned == {'Player4': Decimal('50')}

def test_pot_with_no_bets():
    """Test when all players fold without placing any bets."""
    pot = Pot()
    pot.addPlayer('Player1')
    pot.addPlayer('Player2')
    pot.addFold('Player1')
    pot.addFold('Player2')
    pot.end()
    assert pot.total == Decimal('0')
    assert pot.pots == []
    assert pot.returned == {}

def test_pot_with_antes():
    """Test with players posting antes."""
    pot = Pot()
    pot.addPlayer('Player1')
    pot.addPlayer('Player2')
    pot.antes['Player1'] = Decimal('10')
    pot.antes['Player2'] = Decimal('10')
    pot.common['Player1'] = Decimal('10')
    pot.common['Player2'] = Decimal('10')
    pot.addMoney('Player1', Decimal('100'))
    pot.addMoney('Player2', Decimal('100'))
    pot.end()
    assert pot.total == Decimal('220')  # 10+10 antes + 100+100 bets
    assert pot.pots == [
        (Decimal('20'), {'Player1', 'Player2'}),  # Ante pot
        (Decimal('200'), {'Player1', 'Player2'})  # Main pot
    ]
    assert pot.returned == {}


def test_pot_with_uneven_antes():
    """Test when players post different ante amounts (e.g., one is all-in)."""
    pot = Pot()
    pot.addPlayer('Player1')
    pot.addPlayer('Player2')
    pot.antes['Player1'] = Decimal('10')
    pot.antes['Player2'] = Decimal('5')  # Player2 couldn't cover full ante
    pot.common['Player1'] = Decimal('10')
    pot.common['Player2'] = Decimal('5')
    pot.addMoney('Player1', Decimal('100'))
    pot.addMoney('Player2', Decimal('50'))
    pot.end()
    assert pot.total == Decimal('115')
    assert pot.pots == [
        (Decimal('10'), {'Player1', 'Player2'}),   # Ante pot
        (Decimal('5'), {'Player1'}),               # Ante side pot
        (Decimal('100'), {'Player1', 'Player2'}),  # Main pot
        (Decimal('50'), {'Player1'})               # Side pot
    ]
    assert pot.returned == {'Player1': Decimal('50')}


def test_pot_with_player_zero_bet():
    """Test when a player has zero bet (e.g., sits out or disconnects)."""
    pot = Pot()
    pot.addPlayer('Player1')
    pot.addPlayer('Player2')
    pot.addPlayer('Player3')
    pot.addMoney('Player1', Decimal('100'))
    pot.addMoney('Player2', Decimal('100'))
    # Player3 does not bet
    pot.end()
    assert pot.total == Decimal('200')
    assert pot.pots == [(Decimal('200'), {'Player1', 'Player2'})]
    assert pot.returned == {}


def test_pot_with_uncalled_bet():
    """Test when a player bets and everyone else folds."""
    pot = Pot()
    pot.addPlayer('Player1')
    pot.addPlayer('Player2')
    pot.addMoney('Player1', Decimal('50'))
    pot.addFold('Player2')
    pot.end()
    # Since Player2 folded, Player1 should win the pot
    assert pot.total == Decimal('0')
    assert pot.pots == [(Decimal('50'), {'Player1'})]
    assert pot.returned == {'Player1': Decimal('50')}
    

def test_pot_with_all_folds():
    """Test when all but one player folds before any bets are made."""
    pot = Pot()
    pot.addPlayer('Player1')
    pot.addPlayer('Player2')
    pot.addPlayer('Player3')
    pot.addFold('Player2')
    pot.addFold('Player3')
    pot.end()
    # Player1 wins by default
    assert pot.total == Decimal('0')
    assert pot.pots == []
    assert pot.returned == {}


def test_pot_no_antes():
    pot = Pot()
    pot.addPlayer('Player1')
    pot.addPlayer('Player2')
    pot.addMoney('Player1', Decimal('50'))
    pot.addMoney('Player2', Decimal('50'))
    pot.end()
    assert pot.total == Decimal('100')
    assert pot.pots == [(Decimal('100'), {'Player1', 'Player2'})]




def test_pot_multiple_main_pots_single_ante():
    pot = Pot()
    pot.addPlayer('Player1')
    pot.addPlayer('Player2')
    pot.addPlayer('Player3')
    pot.antes['Player1'] = Decimal('10')
    pot.antes['Player2'] = Decimal('10')
    pot.antes['Player3'] = Decimal('10')
    pot.common['Player1'] = Decimal('10')
    pot.common['Player2'] = Decimal('10')
    pot.common['Player3'] = Decimal('10')
    pot.addMoney('Player1', Decimal('100'))
    pot.addMoney('Player2', Decimal('50'))
    pot.addMoney('Player3', Decimal('25'))
    pot.end()
    assert pot.total == Decimal('155')
    assert pot.returned == {'Player1': Decimal('50')}
    

def test_pot_with_returned_bets():
    pot = Pot()
    pot.addPlayer('Player1')
    pot.addPlayer('Player2')
    pot.addMoney('Player1', Decimal('100'))
    pot.addMoney('Player2', Decimal('50'))
    pot.addFold('Player2')
    pot.end()
    assert pot.total == Decimal('50')
    assert pot.returned == {'Player1': Decimal('100')}
 
    
def test_pot_all_fold_no_bets():
    pot = Pot()
    pot.addPlayer('Player1')
    pot.addPlayer('Player2')
    pot.addFold('Player1')
    pot.addFold('Player2')
    pot.end()
    assert pot.total == Decimal('0')
    assert pot.pots == []   
    
    
def test_pot_antes_no_bets():
    pot = Pot()
    pot.addPlayer('Player1')
    pot.addPlayer('Player2')
    pot.antes['Player1'] = Decimal('10')
    pot.antes['Player2'] = Decimal('10')
    pot.common['Player1'] = Decimal('10')
    pot.common['Player2'] = Decimal('10')
    pot.end()
    assert pot.total == Decimal('20')
    assert pot.pots == [(Decimal('20'), {'Player1', 'Player2'})]


# # Tests pour la classe Hand
# def test_hand_initialization():
#     config = Configuration()
#     hand = Hand(config, 'PokerStars', {}, '')
#     assert hand.sitename == 'PokerStars'
#     assert hand.players == []
#     assert hand.actions == {'BLINDSANTES': [], 'PREFLOP': [], 'FLOP': [], 'TURN': [], 'RIVER': []}

# def test_hand_add_player():
#     config = Configuration()
#     hand = Hand(config, 'PokerStars', {}, '')
#     hand.addPlayer(1, 'Player1', '100')
#     assert hand.players == [[1, 'Player1', '100', None, None]]
#     assert hand.stacks['Player1'] == Decimal('100')

# def test_hand_add_blind():
#     config = Configuration()
#     hand = Hand(config, 'PokerStars', {'sb': '0.5', 'bb': '1'}, '')
#     hand.addPlayer(1, 'Player1', '100')
#     hand.addBlind('Player1', 'small blind', '0.5')
#     assert hand.stacks['Player1'] == Decimal('99.5')
#     assert hand.actions['BLINDSANTES'] == [('Player1', 'small blind', Decimal('0.5'), False)]

# def test_hand_add_bet():
#     config = Configuration()
#     hand = Hand(config, 'PokerStars', {}, '')
#     hand.addPlayer(1, 'Player1', '100')
#     hand.addBet('PREFLOP', 'Player1', '10')
#     assert hand.stacks['Player1'] == Decimal('90')
#     assert hand.actions['PREFLOP'] == [('Player1', 'bets', Decimal('10'), False)]
#     assert hand.lastBet['PREFLOP'] == Decimal('10')

# def test_hand_total_pot():
#     config = Configuration()
#     hand = Hand(config, 'PokerStars', {}, '')
#     hand.pot = Pot()
#     hand.pot.addPlayer('Player1')
#     hand.pot.addPlayer('Player2')
#     hand.pot.addMoney('Player1', Decimal('50'))
#     hand.pot.addMoney('Player2', Decimal('100'))
#     hand.totalPot()
#     assert hand.totalpot == Decimal('150')

# # Tests pour la classe HoldemOmahaHand
# def test_holdem_hand_initialization():
#     config = Configuration()
#     hhc = MagicMock()
#     gametype = {'base': 'hold', 'category': 'holdem', 'sb': '0.5', 'bb': '1', 'type': 'ring'}
#     handText = ''
#     hand = HoldemOmahaHand(config, hhc, 'PokerStars', gametype, handText, builtFrom='DB')
#     assert hand.sb == '0.5'
#     assert hand.bb == '1'
#     assert hand.allStreets == ['BLINDSANTES', 'PREFLOP', 'FLOP', 'TURN', 'RIVER']

# # Tests pour la classe DrawHand
# def test_draw_hand_initialization():
#     config = Configuration()
#     hhc = MagicMock()
#     gametype = {'base': 'draw', 'category': 'fivedraw', 'sb': '0.5', 'bb': '1', 'type': 'ring'}
#     handText = ''
#     hand = DrawHand(config, hhc, 'PokerStars', gametype, handText, builtFrom='DB')
#     assert hand.sb == '0.5'
#     assert hand.bb == '1'
#     assert 'DRAWONE' in hand.allStreets

# # Tests pour la classe StudHand
# def test_stud_hand_initialization():
#     config = Configuration()
#     hhc = MagicMock()
#     gametype = {'base': 'stud', 'category': 'studhi', 'sb': '0.5', 'bb': '1', 'type': 'ring'}
#     handText = ''
#     hand = StudHand(config, hhc, 'PokerStars', gametype, handText, builtFrom='DB')
#     assert hand.sb == '0.5'
#     assert hand.bb == '1'
#     assert 'THIRD' in hand.allStreets

# # Test de l'ajout et de l'évaluation des actions dans une main de Hold'em
# def test_holdem_hand_actions():
#     config = Configuration()
#     hand = HoldemOmahaHand(config, None, 'PokerStars', {'base': 'hold', 'category': 'holdem'}, '')
#     hand.addPlayer(1, 'Player1', '100')
#     hand.addPlayer(2, 'Player2', '100')
#     hand.addBlind('Player1', 'small blind', '0.5')
#     hand.addBlind('Player2', 'big blind', '1')
#     hand.addCall('PREFLOP', 'Player1', '0.5')
#     hand.addBet('PREFLOP', 'Player2', '2')
#     hand.totalPot()
#     assert hand.totalpot == Decimal('4')
#     assert hand.stacks['Player1'] == Decimal('99')
#     assert hand.stacks['Player2'] == Decimal('97')

# # Test de l'ajout et de l'évaluation des actions dans une main de Stud
# def test_stud_hand_actions():
#     config = Configuration()
#     hand = StudHand(config, None, 'PokerStars', {'base': 'stud', 'category': 'studhi'}, '')
#     hand.addPlayer(1, 'Player1', '100')
#     hand.addPlayer(2, 'Player2', '100')
#     hand.addAnte('Player1', '1')
#     hand.addAnte('Player2', '1')
#     hand.addBringIn('Player1', '2')
#     hand.addRaiseTo('THIRD', 'Player2', '4')
#     hand.totalPot()
#     assert hand.totalpot == Decimal('8')
#     assert hand.stacks['Player1'] == Decimal('97')
#     assert hand.stacks['Player2'] == Decimal('95')

# # Test de la gestion des pots avec des mises non appelées
# def test_pot_uncalled_bets():
#     pot = Pot()
#     pot.addPlayer('Player1')
#     pot.addPlayer('Player2')
#     pot.addPlayer('Player3')
#     pot.addMoney('Player1', Decimal('100'))
#     pot.addMoney('Player2', Decimal('50'))
#     pot.addMoney('Player3', Decimal('50'))
#     pot.addFold('Player2')
#     pot.addFold('Player3')
#     pot.end()
#     assert pot.total == Decimal('200')
#     assert pot.returned['Player1'] == Decimal('50')

# # Test de la méthode addHoleCards pour HoldemOmahaHand
# def test_holdem_add_holecards():
#     config = Configuration()
#     hand = HoldemOmahaHand(config, None, 'PokerStars', {'base': 'hold', 'category': 'holdem'}, '')
#     hand.hero = 'Hero'
#     hand.addPlayer(1, 'Hero', '100')
#     hand.addHoleCards('PREFLOP', 'Hero', closed=['Ah', 'Kh'])
#     assert hand.holecards['PREFLOP']['Hero'] == [[], ['Ah', 'Kh']]

# # Test de la méthode addShownCards pour HoldemOmahaHand
# def test_holdem_add_showncards():
#     config = Configuration()
#     hand = HoldemOmahaHand(config, None, 'PokerStars', {'base': 'hold', 'category': 'holdem'}, '')
#     hand.addPlayer(1, 'Player1', '100')
#     hand.addShownCards(['Ah', 'Kh'], 'Player1', shown=True)
#     assert hand.holecards['PREFLOP']['Player1'] == [[], ['Ah', 'Kh']]
#     assert 'Player1' in hand.shown

# # Test de la méthode addDiscard pour DrawHand
# def test_draw_hand_add_discard():
#     config = Configuration()
#     hand = DrawHand(config, None, 'PokerStars', {'base': 'draw', 'category': 'fivedraw'}, '')
#     hand.addPlayer(1, 'Player1', '100')
#     hand.addDiscard('DRAWONE', 'Player1', 2, ['As', 'Ks'])
#     assert hand.actions['DRAWONE'] == [('Player1', 'discards', Decimal(2), ['As', 'Ks'])]

# # Test de la méthode writeHand pour HoldemOmahaHand
# def test_holdem_write_hand():
#     config = Configuration()
#     hand = HoldemOmahaHand(config, None, 'PokerStars', {'base': 'hold', 'category': 'holdem', 'sb': '0.5', 'bb': '1', 'currency': 'USD'}, '')
#     hand.handid = '123456789'
#     hand.tablename = 'Test Table'
#     hand.startTime = '2021/01/01 12:00:00 ET'
#     hand.addPlayer(1, 'Hero', '100')
#     hand.addHoleCards('PREFLOP', 'Hero', closed=['Ah', 'Kh'])
#     hand.actions['PREFLOP'] = [('Hero', 'calls', Decimal('1'), False)]
#     hand.pot = Pot()
#     hand.pot.addPlayer('Hero')
#     hand.pot.addMoney('Hero', Decimal('1'))
#     hand.pot.total = Decimal('2')
#     hand.rake = Decimal('0.1')
#     hand.totalpot = Decimal('2')
#     from io import StringIO
#     output = StringIO()
#     hand.writeHand(output)
#     hand_history = output.getvalue()
#     assert 'PokerStars Game #123456789' in hand_history
#     assert 'Dealt to Hero [Ah Kh]' in hand_history
