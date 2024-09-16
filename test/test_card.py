import pytest
import sys
from pathlib import Path
from unittest.mock import Mock

sys.path.append(str(Path(__file__).parent.parent))

from  Card import *

def test_calcStartCards_holdem():
    # Mock 
    mock_hand = Mock()
    mock_hand.gametype = {'category': 'holdem'}
    mock_hand.join_holecards.return_value = [('A', 'h'), ('K', 's')]
    
    result = calcStartCards(mock_hand, 'player1')
    assert result == 156  # Valeur attendue pour AKo

def test_calcStartCards_6_holdem():
    mock_hand = Mock()
    mock_hand.gametype = {'category': '6_holdem'}
    mock_hand.join_holecards.return_value = [('Q', 'd'), ('Q', 'c')]
    
    result = calcStartCards(mock_hand, 'player1')
    expected = twoStartCards(card_map['Q'], 'd', card_map['Q'], 'c')
    assert result == expected, f"Expected {expected}, but got {result}"


def test_calcStartCards_unknown_game():
    mock_hand = Mock()
    mock_hand.gametype = {'category': 'unknown_game'}
    
    result = calcStartCards(mock_hand, 'player1')
    assert result == 170, f"Expected 170, but got {result}"

def test_twoStartCards():
    # Test pair
    result = twoStartCards(4, 'd', 4, 'c')
    assert result == 29
    
    # Test suited
    result = twoStartCards(10, 'h', 12, 'h')
    assert result == 139
    
    # Test unsuited
    result = twoStartCards(6, 's', 9, 'c')
    assert result == 60
    
    # Test invalid cards
    result = twoStartCards(1, 'd', 15, 'h')
    assert result == 170

    # Test invalid value
    result = twoStartCards(5, 'd', 18, 's')
    assert result == 170

def test_decodeStartHandValue():
    # Test holdem game
    assert decodeStartHandValue("holdem", 169) == "AA"
    assert decodeStartHandValue("6_holdem", 166) == "AJs"
    
    # Test razz game
    assert decodeStartHandValue("razz", 260) == '(T2)3'
    assert decodeStartHandValue("27_razz", 200) == '(9A)6'
    
    # Test unknown game
    assert decodeStartHandValue("unknown_game", 123) == "xx"


def test_StartCardRank():
    # Tests that the function returns the correct tuple for idx = 0
    def test_idx_0(self):
        assert StartCardRank(0) == ('22',54,12)

    # Tests that the function returns the correct tuple for idx = 5
    def test_idx_5(self):
        assert StartCardRank(5) == ('72o',169,24)

    # Tests that the function returns the correct tuple for idx = 14
    def test_idx_13(self):
        assert StartCardRank(13) == ('32s',111,8)

    # Tests that the function returns the correct tuple for idx = 15
    def test_idx_14(self):
        assert StartCardRank(14) == ('33',53,12)

    # Tests that the function returns the correct tuple for idx = 170
    def test_idx_169(self):
        assert StartCardRank(171) == ('xx',170,0)
        
def test_encodeRazzStartHand_basic():
    assert encodeRazzStartHand(['3h', '2d', 'As']) == 1  # (32)A
    
def test_encodeRazzStartHand_pair():
    assert encodeRazzStartHand(['4h', '4d', '5s']) == 897  # (44)5

def test_encodeRazzStartHand_higher_first():
    assert encodeRazzStartHand(['7c', '5h', '2d']) == 82  # (75)2

def test_encodeRazzStartHand_broadway():
    assert encodeRazzStartHand(['Kh', 'Qd', 'Js']) == 856  # (KQ)J

def test_encodeRazzStartHand_all_same():
    assert encodeRazzStartHand(['Ah', 'As', 'Ad']) == 1171  # (AA)A

def test_encodeRazzStartHand_invalid_input():
    with pytest.raises(KeyError):
        encodeRazzStartHand(['1h', '2d', '3s'])  # Invalid card '1h'

def test_encodeRazzStartHand_wrong_number_of_cards():
    with pytest.raises(IndexError):
        encodeRazzStartHand(['Ah', '2d'])  # Only 2 cards instead of 3

def test_encodeRazzStartHand_edge_cases():
    assert encodeRazzStartHand(['2h', '3d', '4s']) == 12  # (32)4
    assert encodeRazzStartHand(['Kh', 'Kd', 'Ks']) == 1183  # (KK)K
    
def test_StartCardRank():
    
    assert StartCardRank(0) == ('22', 54, 12), "Test failed for index 0"
    
    
    assert StartCardRank(50) == ('K5o', 126, 24), "Test failed for index 50"
    
    
    assert StartCardRank(168) == ('AA', 1, 12), "Test failed for index 168"
    

    assert StartCardRank(169) == ('xx', 170, 0), "Test failed for index 169"
    

    assert StartCardRank(14) == ('33', 53, 12), "Test failed for pair '33'"
    

    assert StartCardRank(13) == ('32s', 111, 8), "Test failed for suited hand '32s'"
    

    assert StartCardRank(1) == ('32o', 160, 24), "Test failed for offsuit hand '32o'"
    
    
def test_is_suited_true():
    assert is_suited(['Ah', '2h', 'Kc', 'Qd']) == True
    
def test_is_suited_false_all_different():
    assert is_suited(['Ah', '2s', 'Kc', 'Qd']) == False

def test_is_suited_true_three_same():
    assert is_suited(['Ah', '2h', 'Kh', 'Qd']) == True
    
def test_is_suited_true_all_same():
    assert is_suited(['Ah', '2h', 'Kh', 'Qh']) == True
    
def test_is_suited_single_card():
    assert is_suited(['Ah']) == False

def test_is_suited_two_cards_true():
    assert is_suited(['Ah', 'Kh']) == True

def test_is_suited_two_cards_false():
    assert is_suited(['Ah', 'Ks']) == False
    
def test_is_double_suited_4cards_true():
    assert is_double_suited(['Ah', 'Kh', 'Qs', '9s']) == True

def test_is_double_suited_4cards_false():
    assert is_double_suited(['Ah', 'Kh', 'Qs', '9c']) == False
    
def test_is_double_suited_4cards_false():
    assert is_double_suited(['Ah', 'Kh', 'Qh', '9c']) == False
    

def test_is_double_suited_5cards_true():
    assert is_double_suited(['Ah', 'Kh', 'Qh', 'Js', 'Ts']) == True

def test_is_double_suited_5cards_false():
    assert is_double_suited(['Ah', 'Kh', 'Qc', 'Jd', 'Ts']) == False
    
def test_is_suited_5cards_false():
    assert is_suited(['Ah', 'Kh', 'Qc', 'Jd', 'Ts']) == False
    
def test_is_suited_two_cards_true():
    assert is_suited(['Ah', 'Kh']) == True

def test_is_suited_two_cards_false():
    assert is_suited(['Ah', 'Ks']) == False

def test_is_suited_true_three_same():
    assert is_suited(['Ah', '2h', 'Kh', 'Qd']) == True

def test_is_suited_true_all_same():
    assert is_suited(['Ah', '2h', 'Kh', 'Qh']) == True

def test_is_suited_4cards_false():
    assert is_suited(['Ah', 'Ks', 'Qc', '9d']) == False

def test_is_suited_5cards_true():
    assert is_suited(['Ah', 'Kh', 'Qh', 'Jd', 'Ts']) == True

def test_is_suited_5cards_false():
    assert is_suited(['Ah', 'Kh', 'Qc', 'Jd', 'Ts']) == False

def test_is_suited_6cards_true():
    assert is_suited(['Ah', 'Kh', 'Qh', 'Jd', 'Ts', '9c']) == True

def test_is_suited_6cards_false():
    assert is_suited(['Ah', 'Kh', 'Qc', 'Jd', 'Ts', '9c']) == False

def test_is_suited_single_card():
    assert is_suited(['Ah']) == False

def test_is_suited_empty_list():
    assert is_suited([]) == False
    
def test_is_rainbow_true():
    assert is_rainbow(['Ah', '2s', 'Kc', 'Qd']) == True

def test_is_rainbow_false():
    assert is_rainbow(['Ah', '2s', 'Kc', 'Qc']) == False

def test_is_rainbow_less_than_four_cards():
    assert is_rainbow(['Ah', '2s', 'Kc']) == False



def test_is_rainbow_empty_list():
    assert is_rainbow([]) == False

def test_is_rainbow_all_same_suit():
    assert is_rainbow(['Ah', '2h', 'Kh', 'Qh']) == False

def test_is_rainbow_three_different_suits():
    assert is_rainbow(['Ah', '2s', 'Kc', 'Qc']) == False
    


def test_cardFromValueSuit_hearts():
    assert cardFromValueSuit(2, 'h') == 1  # 2h
    assert cardFromValueSuit(14, 'h') == 13  # Ah

def test_cardFromValueSuit_diamonds():
    assert cardFromValueSuit(2, 'd') == 14  # 2d
    assert cardFromValueSuit(14, 'd') == 26  # Ad

def test_cardFromValueSuit_clubs():
    assert cardFromValueSuit(2, 'c') == 27  # 2c
    assert cardFromValueSuit(14, 'c') == 39  # Ac

def test_cardFromValueSuit_spades():
    assert cardFromValueSuit(2, 's') == 40  # 2s
    assert cardFromValueSuit(14, 's') == 52  # As

def test_cardFromValueSuit_invalid_suit():
    assert cardFromValueSuit(2, 'x') == 0
    assert cardFromValueSuit(14, '') == 0

def test_cardFromValueSuit_edge_cases():
    assert cardFromValueSuit(1, 'h') == 0  # Invalid value
    assert cardFromValueSuit(15, 'h') == 14  # Invalid value, but still calculated

def test_cardFromValueSuit_all_hearts():
    for i in range(2, 15):
        assert cardFromValueSuit(i, 'h') == i - 1

def test_cardFromValueSuit_all_suits():
    suits = ['h', 'd', 'c', 's']
    offsets = [-1, 12, 25, 38]
    for suit, offset in zip(suits, offsets):
        for value in range(2, 15):
            assert cardFromValueSuit(value, suit) == value + offset
            

def test_valueSuitFromCard_valid_inputs():
    assert valueSuitFromCard(0) == ''
    assert valueSuitFromCard(12) == 'Kh'
    assert valueSuitFromCard(13) == 'Ah'
    assert valueSuitFromCard(25) == 'Kd'
    assert valueSuitFromCard(26) == 'Ad'


def test_valueSuitFromCard_edge_cases():
    assert valueSuitFromCard(1) == '2h'
    assert valueSuitFromCard(50) == 'Qs'

def test_valueSuitFromCard_invalid_inputs():
    assert valueSuitFromCard(-1) == ''
    assert valueSuitFromCard(53) == ''
    assert valueSuitFromCard(100) == ''

def test_valueSuitFromCard_zero():
    assert valueSuitFromCard(0) == ''


    


def test_encodeCard_valid_inputs():
    assert encodeCard('2h') == 1
    assert encodeCard('Ah') == 13
    assert encodeCard('2d') == 14
    assert encodeCard('Ad') == 26
    assert encodeCard('2c') == 27
    assert encodeCard('Ac') == 39
    assert encodeCard('2s') == 40
    assert encodeCard('As') == 52

def test_encodeCard_lowercase():
    assert encodeCard('ah') == 13
    assert encodeCard('kd') == 25

def test_encodeCard_invalid_inputs():
    assert encodeCard('1h') == 0  # Invalid rank
    assert encodeCard('Ax') == 0  # Invalid suit
    assert encodeCard('') == 0   # Empty string
    assert encodeCard('Hello') == 0  # Random string

def test_encodeCard_edge_cases():
    assert encodeCard('  ') == 0  # Two spaces (defined in encodeCardList)
    assert encodeCard('10h') == 0  # '10' is not a valid rank in this encoding

def test_encodeCard_case_insensitivity():
    assert encodeCard('AH') == encodeCard('Ah')  # Should be case insensitive
    assert encodeCard('AH') == encodeCard('ah')  # Should be case insensitive
    assert encodeCard('2H') == encodeCard('2h')  # Should be case insensitive
    assert encodeCard('Th') == encodeCard('tH')  # Should be case insensitive

def test_encodeCard_all_cards():
    ranks = '23456789TJQKA'
    suits = 'hdcs'
    for i, rank in enumerate(ranks):
        for j, suit in enumerate(suits):
            card = rank + suit
            expected = i + 1 + j * 13
            assert encodeCard(card) == expected

def test_encodeCard_non_string_input():
    assert encodeCard(42) == 0
    assert encodeCard(None) == 0
    assert encodeCard(['A', 'h']) == 0
    
def test_fourStartCards_invalid_input():
    assert fourStartCards(['Ah', 'Kh', 'Qs']) == "Invalid input: You must provide exactly four cards."
    assert fourStartCards(['Ah', 'Kh', 'Qs', 'Jd', 'Td']) == "Invalid input: You must provide exactly four cards."

def test_fourStartCards_suited():
    assert fourStartCards(['Ah', 'Kh', 'Qh', '2d']) == "Suited"
    assert fourStartCards(['As', 'Ks', 'Qs', 'Js']) == "Suited"

def test_fourStartCards_double_suited():
    assert fourStartCards(['Ah', 'Kh', 'Qs', 'Js']) == "Double Suited"
    assert fourStartCards(['Ad', 'Kd', 'Qc', 'Jc']) == "Double Suited"

def test_fourStartCards_rainbow():
    assert fourStartCards(['Ah', 'Kd', 'Qs', 'Jc']) == "Rainbow"
    assert fourStartCards(['2h', '3d', '4s', '5c']) == "Rainbow"





def test_fourStartCards_integration():
    cards = ['Ah', 'Kh', 'Qh', '2d']
    assert fourStartCards(cards) == "Suited"
    assert is_suited(cards) == True
    assert is_double_suited(cards) == False
    assert is_rainbow(cards) == False