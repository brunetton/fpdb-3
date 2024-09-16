import pytest
import sys
from unittest.mock import patch, MagicMock
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from OSXTables import Table  # Import the correct module

# Mock config object to be used in tests
class MockConfig:
    pass

def test_get_process_name():
    table = Table(config=MockConfig(), site='Winamax')
    assert table.get_process_name() == 'winamax'

    table.site = 'PokerStars'
    assert table.get_process_name() == 'pokerstars'

    table.site = 'UnknownSite'
    assert table.get_process_name() == ''


@patch.object(Table, 'get_window_titles_via_applescript')
@patch.object(Table, 'get_window_number')
def test_find_table_parameters_winamax_cash(mock_get_window_number, mock_get_windows):
    table = Table(config=MockConfig(), site='Winamax')
    table.search_string = 'WinamaxTable1'
    table.tournament = None

    mock_get_windows.return_value = [
        {
            "proc": "Winamax",
            "pid": 1234,
            "name": "WinamaxTable1 - No Limit Hold'em €0.05/€0.10",
            "size": {"width": 800, "height": 600},
            "position": {"x": 100, "y": 100}
        }
    ]
    mock_get_window_number.return_value = 5678

    assert table.find_table_parameters() == "WinamaxTable1 - No Limit Hold'em €0.05/€0.10"













@patch.object(Table, 'get_window_titles_via_applescript')
@patch.object(Table, 'get_window_number')
def test_find_table_parameters_pokerstars_cash(mock_get_window_number, mock_get_windows):
    table = Table(config=MockConfig(), site='PokerStars')
    table.search_string = 'Ostara III'
    table.tournament = None

    mock_get_windows.return_value = [
        {
            "proc": "PokerStars",
            "pid": 64003,
            "name": "Ostara III - Pot Limit Omaha",
            "size": {"width": 800, "height": 600},
            "position": {"x": 100, "y": 100}
        }
    ]
    mock_get_window_number.return_value = 5678

    assert table.find_table_parameters() == "Ostara III - Pot Limit Omaha"



