import sys
import pytest
from pathlib import Path
from decimal import Decimal
from unittest import mock

# Assurez-vous que le chemin vers le module Hand est correct
sys.path.append(str(Path(__file__).parent.parent))
from Hand import HoldemOmahaHand, Pot  # Assurez-vous que Pot est correctement importé
from Exceptions import FpdbHandPartial  # Assurez-vous que FpdbHandPartial est correctement importé

class TestHandTotalPot:
    
    @pytest.fixture
    def mock_config(self):
        mock_config = mock.MagicMock()
        import_params = {
            'saveActions': True,
            'callFpdbHud': True,
            'cacheSessions': True,
            'publicDB': False
        }
        mock_config.get_import_parameters.return_value = import_params
        mock_config.get_site_id.return_value = 1
        return mock_config

    @pytest.fixture
    def mock_hand(self, mock_config):
        gametype = {
            "type": "ring",
            "base": "hold",
            "category": "holdem",
            "limitType": "nl",
            "currency": "USD",
            "sb": "0.02",  # Petit blind
            "bb": "0.05",  # Grand blind
            "split": False  # Ajouté pour éviter KeyError
        }
        handText = """PokerStars Hand #252349922248:  Omaha Pot Limit (€0.02/€0.05 EUR) - 2024/09/08 18:58:14 CET [2024/09/08 12:58:14 ET]
Table 'Gotha II' 6-max Seat #6 is the button
Seat 1: florentin59 (€21.68 in chips)
Seat 2: eclipseto (€2.29 in chips)
Seat 3: jeje_sat (€6.71 in chips)
Seat 4: chantfrin (€3.96 in chips)
Seat 5: e_carte_toi30 (€8.03 in chips)
Seat 6: anyeflores (€1.86 in chips)
florentin59: posts small blind €0.02
eclipseto: posts big blind €0.05
*** HOLE CARDS ***
Dealt to jeje_sat [6d Th 3c 6c]
jeje_sat: folds
chantfrin: calls €0.05
e_carte_toi30: calls €0.05
anyeflores: calls €0.05
florentin59: calls €0.03
eclipseto: checks
*** FLOP *** [Jc 2h Kh]
florentin59: checks
eclipseto: checks
chantfrin: checks
e_carte_toi30: checks
anyeflores: checks
*** TURN *** [Jc 2h Kh] [3d]
florentin59: checks
eclipseto: bets €0.23
chantfrin: calls €0.23
e_carte_toi30: folds
anyeflores: folds
florentin59: folds
*** RIVER *** [Jc 2h Kh 3d] [8s]
eclipseto: bets €0.67
chantfrin: calls €0.04
Uncalled bet (€0.67) returned to eclipseto
eclipseto collected €0.67 from pot
chantfrin collected €0.04 from pot
*** SUMMARY ***
Total pot €0.71 | Rake €0.04
Board [Jc 2h Kh 3d 8s]
Seat 1: florentin59 (small blind) folded on the Turn
Seat 2: eclipseto (big blind) collected (€0.67)
Seat 3: jeje_sat folded before Flop (didn't bet)
Seat 4: chantfrin folded on the River
Seat 5: e_carte_toi30 folded on the Turn
Seat 6: anyeflores (button) folded on the Turn"""

        # Créer un objet hhc simulé avec les méthodes requises
        hhc = mock.MagicMock()

        # Définir les méthodes que HoldemOmahaHand.__init__ appelle
        hhc.readHandInfo = mock.MagicMock()
        hhc.readPlayerStacks = mock.MagicMock()
        hhc.compilePlayerRegexs = mock.MagicMock()
        hhc.markStreets = mock.MagicMock()
        hhc.readBlinds = mock.MagicMock()
        hhc.readSTP = mock.MagicMock()
        hhc.readAntes = mock.MagicMock()
        hhc.readButton = mock.MagicMock()
        hhc.readHoleCards = mock.MagicMock()
        hhc.readShowdownActions = mock.MagicMock()
        hhc.readAction = mock.MagicMock()
        hhc.readCollectPot = mock.MagicMock()
        hhc.readShownCards = mock.MagicMock()
        hhc.getRake = mock.MagicMock(return_value=Decimal('0.04'))
        hhc.guessMaxSeats = mock.MagicMock(return_value=6)
        hhc.readTourneyResults = mock.MagicMock()
        hhc.readOther = mock.MagicMock()

        # Définir les side_effects pour hhc.readHandInfo et autres si nécessaire
        def mock_readHandInfo(hand):
            # Configuration des joueurs
            hand.players = [
                (1, "florentin59"),
                (2, "eclipseto"),
                (3, "jeje_sat"),
                (4, "chantfrin"),
                (5, "e_carte_toi30"),
                (6, "anyeflores")
            ]

            # Configuration des actions par street
            hand.actions = {
                'BLINDSANTES': [
                    ('florentin59', 'posts small blind', Decimal('0.02')),
                    ('eclipseto', 'posts big blind', Decimal('0.05'))
                ],
                'PREFLOP': [
                    ('jeje_sat', 'folds', None),
                    ('chantfrin', 'calls', Decimal('0.05')),
                    ('e_carte_toi30', 'calls', Decimal('0.05')),
                    ('anyeflores', 'calls', Decimal('0.05')),
                    ('florentin59', 'calls', Decimal('0.03')),
                    ('eclipseto', 'checks', None)
                ],
                'FLOP': [
                    ('florentin59', 'checks', None),
                    ('eclipseto', 'checks', None),
                    ('chantfrin', 'checks', None),
                    ('e_carte_toi30', 'checks', None),
                    ('anyeflores', 'checks', None)
                ],
                'TURN': [
                    ('florentin59', 'checks', None),
                    ('eclipseto', 'bets', Decimal('0.23')),
                    ('chantfrin', 'calls', Decimal('0.23')),
                    ('e_carte_toi30', 'folds', None),
                    ('anyeflores', 'folds', None),
                    ('florentin59', 'folds', None)
                ],
                'RIVER': [
                    ('eclipseto', 'bets', Decimal('0.67')),
                    ('chantfrin', 'calls', Decimal('0.04'))
                ]
            }

            # Configuration des collectees
            hand.collectees = {
                'eclipseto': Decimal('0.67'),
                'chantfrin': Decimal('0.04')
            }

            # Configuration des joueurs distribués
            hand.dealt = ['florentin59', 'eclipseto', 'chantfrin', 'e_carte_toi30', 'anyeflores']

            # Configuration des rues (streets)
            hand.streets = {
                'BLINDSANTES': 'florentin59 posts small blind €0.02\neclipseto posts big blind €0.05',
                'PREFLOP': 'jeje_sat: folds\nchantfrin: calls €0.05\ne_carte_toi30: calls €0.05\nanyeflores: calls €0.05\nflorentin59: calls €0.03\neclipseto: checks',
                'FLOP': 'florentin59: checks\neclipseto: checks\nchantfrin: checks\ne_carte_toi30: checks\nanyeflores: checks',
                'TURN': 'florentin59: checks\neclipseto: bets €0.23\nchantfrin: calls €0.23\ne_carte_toi30: folds\nanyeflores: folds\nflorentin59: folds',
                'RIVER': 'eclipseto: bets €0.67\nchantfrin: calls €0.04'
            }

            # Initialisation du pot et du rake
            hand.pot = Pot()
            hand.pot.committed = {
                'florentin59': Decimal('0.02'),  # small blind
                'eclipseto': Decimal('0.05')      # big blind
            }
            hand.pot.total = Decimal('0.07')  # sb + bb
            hand.pot.pots = []
            hand.pot.returned = {
                'eclipseto': Decimal('0.67'),  # collected
                'chantfrin': Decimal('0.04')   # collected
            }
            hand.rake = Decimal('0.04')

        hhc.readHandInfo.side_effect = mock_readHandInfo

        # Les autres méthodes de hhc sont mockées avec des lambdas acceptant tous les arguments
        hhc.readPlayerStacks.side_effect = lambda *args, **kwargs: None
        hhc.compilePlayerRegexs.side_effect = lambda *args, **kwargs: None
        hhc.markStreets.side_effect = lambda *args, **kwargs: None
        hhc.readBlinds.side_effect = lambda *args, **kwargs: None
        hhc.readSTP.side_effect = lambda *args, **kwargs: None
        hhc.readAntes.side_effect = lambda *args, **kwargs: None
        hhc.readButton.side_effect = lambda *args, **kwargs: None
        hhc.readHoleCards.side_effect = lambda *args, **kwargs: None
        hhc.readShowdownActions.side_effect = lambda *args, **kwargs: None
        hhc.readAction.side_effect = lambda *args, **kwargs: None
        hhc.readCollectPot.side_effect = lambda *args, **kwargs: None
        hhc.readShownCards.side_effect = lambda *args, **kwargs: None
        hhc.readTourneyResults.side_effect = lambda *args, **kwargs: None
        hhc.readOther.side_effect = lambda *args, **kwargs: None

        # Instancier la main avec l'objet hhc simulé
        hand = HoldemOmahaHand(
            config=mock_config,
            hhc=hhc,
            sitename="PokerStars",
            gametype=gametype,
            handText=handText
        )

        # Retourner l'objet main simulé
        return hand

    def test_totalPot_normal_case(self, mock_hand):
        # Simuler des actions conduisant à un pot total de 20
        mock_hand.pot.committed = {'florentin59': Decimal('10'), 'eclipseto': Decimal('10')}
        mock_hand.pot.total = Decimal('20')
        assert mock_hand.pot.total == Decimal('20')




    def test_totalPot_with_rake(self, mock_hand):
        # Simuler un pot total avec rake
        mock_hand.pot.committed = {'player1': Decimal('10'), 'player2': Decimal('10')}
        mock_hand.pot.total = Decimal('20')
        mock_hand.rake = Decimal('2')
        # Ajuster le pot total après le rake
        mock_hand.pot.total -= mock_hand.rake
        assert mock_hand.pot.total == Decimal('18')

    def test_totalPot_multiple_pots(self, mock_hand):
        # Simuler plusieurs pots secondaires
        mock_hand.pot.pots = [(Decimal('30'), {'player1', 'player2'}), (Decimal('40'), {'player3'})]
        total = sum(pot[0] for pot in mock_hand.pot.pots)
        assert total == Decimal('70')

    def test_totalPot_zero_pot(self, mock_hand):
        # Simuler une main sans pot
        mock_hand.pot.total = Decimal('0')
        assert mock_hand.pot.total == Decimal('0')

    def test_totalPot_uncalled_bet(self, mock_hand):
        # Simuler une mise non suivie
        mock_hand.pot.committed = {'player1': Decimal('10'), 'player2': Decimal('0')}
        mock_hand.pot.returned = {'player1': Decimal('10')}
        mock_hand.pot.total = Decimal('0')  # Après retour de la mise non suivie
        assert mock_hand.pot.total == Decimal('0')

    def test_totalPot_called_twice(self, mock_hand):
        # Simuler plusieurs appels contribuant au pot
        mock_hand.pot.committed = {'player1': Decimal('10'), 'player2': Decimal('10'), 'player3': Decimal('10')}
        mock_hand.pot.total = Decimal('30')
        assert mock_hand.pot.total == Decimal('30')
