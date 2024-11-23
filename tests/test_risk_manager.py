import pytest
from datetime import datetime
from src.agents.risk_management_agent import RiskManagementAgent

@pytest.fixture
def test_config():
    return {
        'max_position_size': 0.1,
        'max_portfolio_var': 0.2,
        'max_drawdown': 0.15,
        'correlation_limit': 0.7,
        'risk_limits': {
            'max_exposure': 1000000,
            'max_leverage': 2.0,
            'account_balance': 100000,
            'available_margin': 100000
        }
    }

@pytest.fixture
def risk_manager(test_config):
    return RiskManagementAgent('test_risk_manager', test_config)

def test_position_risk_calculation(risk_manager):
    """Test calculation of single position risk"""
    position = {
        'entry_price': 100,
        'current_price': 105,
        'size': 1.0,
        'price_history': [98, 99, 100, 102, 105]
    }
    
    risk_metrics = risk_manager.calculate_position_risk(position)
    assert isinstance(risk_metrics, dict)
    assert 'pnl' in risk_metrics
    assert 'volatility' in risk_metrics
    assert risk_metrics['pnl'] == pytest.approx(5.0)

def test_portfolio_risk_calculation(risk_manager):
    """Test calculation of portfolio risk metrics"""
    positions = [
        {
            'id': 'pos1',
            'entry_price': 100,
            'current_price': 105,
            'size': 1.0,
            'price_history': [98, 99, 100, 102, 105]
        },
        {
            'id': 'pos2',
            'entry_price': 50,
            'current_price': 48,
            'size': 2.0,
            'price_history': [50, 49, 48, 47, 48]
        }
    ]
    
    risk_metrics = risk_manager.calculate_portfolio_risk(positions)
    assert isinstance(risk_metrics.total_exposure, float)
    assert isinstance(risk_metrics.volatility, float)
    assert isinstance(risk_metrics.drawdown, float)

def test_trade_validation(risk_manager):
    """Test trade validation logic"""
    valid_trade = {
        'size': 0.05,
        'price': 100
    }
    
    invalid_trade = {
        'size': 0.2,  # Exceeds max_position_size
        'price': 100
    }
    
    is_valid, message = risk_manager.validate_trade(valid_trade)
    assert is_valid
    
    is_valid, message = risk_manager.validate_trade(invalid_trade)
    assert not is_valid
    assert "Position size exceeds limit" in message

def test_risk_score_calculation(risk_manager):
    """Test risk score calculation"""
    risk_score = risk_manager._calculate_risk_score(0.05, 0.1)
    assert 0 <= risk_score <= 1
    assert risk_score == pytest.approx(0.075)
