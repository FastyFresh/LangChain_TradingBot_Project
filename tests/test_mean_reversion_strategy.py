import pytest
from datetime import datetime
import numpy as np
from src.strategies.mean_reversion_strategy import MeanReversionStrategy
from src.analysis.market_regime import MarketRegime

@pytest.fixture
def config():
    return {
        'strategy_id': 'test_mean_reversion',
        'position_size': 0.1,
        'max_position_size': 0.3,
        'entry_std': 2.0,
        'exit_std': 0.5,
        'lookback_period': 20,
        'min_volume': 1000000,
        'regime_config': {
            'lookback_period': 20,
            'volatility_threshold': 0.02,
            'trend_strength_threshold': 0.01,
            'volume_ma_period': 14
        }
    }

@pytest.fixture
def strategy(config):
    return MeanReversionStrategy(config)

@pytest.fixture
def range_bound_market():
    """Create range-bound market data"""
    np.random.seed(42)
    base = 100
    prices = [base + np.random.normal(0, 1) for _ in range(50)]
    volumes = [1000000 + np.random.normal(0, 100000) for _ in range(50)]
    return {
        'price_history': prices,
        'volume_history': volumes
    }

@pytest.fixture
def trending_market():
    """Create trending market data"""
    prices = [100 + i * 0.5 for i in range(50)]  # Clear uptrend
    volumes = [1000000] * 50
    return {
        'price_history': prices,
        'volume_history': volumes
    }

@pytest.fixture
def volatile_market():
    """Create volatile market data"""
    np.random.seed(42)
    base = 100
    prices = [base + np.random.normal(0, 3) for _ in range(50)]
    volumes = [2000000 + np.random.normal(0, 500000) for _ in range(50)]
    return {
        'price_history': prices,
        'volume_history': volumes
    }

def test_regime_detection(strategy, range_bound_market, trending_market, volatile_market):
    """Test regime detection in different market conditions"""
    # Test range-bound market
    analysis = strategy.analyze_market(range_bound_market)
    assert analysis['regime'].regime == 'range_bound'
    
    # Test trending market
    analysis = strategy.analyze_market(trending_market)
    assert analysis['regime'].regime == 'trending'
    
    # Test volatile market
    analysis = strategy.analyze_market(volatile_market)
    assert analysis['regime'].regime == 'high_volatility'

def test_signal_generation_range_bound(strategy, range_bound_market):
    """Test signal generation in range-bound market"""
    # Modify last price to create clear mean reversion opportunity
    range_bound_market['price_history'][-1] = 105  # Clear deviation
    
    signal = strategy.generate_signal(range_bound_market)
    
    assert signal is not None
    assert signal.direction == 'short'  # Should short when price is above mean
    assert signal.position_size <= strategy.max_position_size
    assert signal.confidence > 0.5

def test_signal_generation_trending(strategy, trending_market):
    """Test signal generation in trending market"""
    # Modify last price to create potential mean reversion signal
    trending_market['price_history'][-1] = 90  # Below trend
    
    signal = strategy.generate_signal(trending_market)
    
    # Should be more cautious or avoid trading against trend
    if signal:
        assert signal.position_size < strategy.base_position_size
        assert signal.confidence < 0.8

def test_position_sizing_volatility(strategy, volatile_market):
    """Test position sizing in volatile market"""
    volatile_market['price_history'][-1] = 110  # Create clear signal
    
    signal = strategy.generate_signal(volatile_market)
    
    assert signal is not None
    # Should reduce position size in volatile markets
    assert signal.position_size < strategy.base_position_size
    assert signal.confidence < 0.8

def test_volume_profile_impact(strategy, range_bound_market):
    """Test impact of volume profile on signals"""
    # Test high volume scenario
    range_bound_market['volume_history'][-1] = 3000000  # High volume
    range_bound_market['price_history'][-1] = 105  # Clear deviation
    
    signal = strategy.generate_signal(range_bound_market)
    
    assert signal is not None
    high_vol_confidence = signal.confidence
    
    # Test low volume scenario
    range_bound_market['volume_history'][-1] = 500000  # Low volume
    signal = strategy.generate_signal(range_bound_market)
    
    assert signal is not None
    assert signal.confidence < high_vol_confidence

def test_stop_loss_adjustment(strategy, volatile_market, range_bound_market):
    """Test stop loss adjustments across regimes"""
    # Test volatile market stop loss
    volatile_market['price_history'][-1] = 110
    volatile_signal = strategy.generate_signal(volatile_market)
    
    # Test range-bound market stop loss
    range_bound_market['price_history'][-1] = 110
    normal_signal = strategy.generate_signal(range_bound_market)
    
    assert volatile_signal is not None and normal_signal is not None
    # Stop loss should be wider in volatile markets
    volatile_stop_distance = abs(volatile_signal.stop_loss - volatile_signal.target_price)
    normal_stop_distance = abs(normal_signal.stop_loss - normal_signal.target_price)
    assert volatile_stop_distance > normal_stop_distance