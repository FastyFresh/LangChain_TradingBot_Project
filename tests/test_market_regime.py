import pytest
import numpy as np
from datetime import datetime
from src.analysis.market_regime import MarketRegimeDetector

@pytest.fixture
def config():
    return {
        'lookback_period': 20,
        'volatility_threshold': 0.02,
        'trend_strength_threshold': 0.01,
        'volume_ma_period': 14
    }

@pytest.fixture
def detector(config):
    return MarketRegimeDetector(config)

@pytest.fixture
def trending_market_data():
    """Create trending market data"""
    return {
        'price_history': [100 + i for i in range(50)],  # Clear uptrend
        'volume_history': [1000000] * 50
    }

@pytest.fixture
def volatile_market_data():
    """Create volatile market data"""
    np.random.seed(42)
    base = np.array([100] * 50)
    noise = np.random.normal(0, 3, 50)
    return {
        'price_history': (base + noise).tolist(),
        'volume_history': [1000000] * 50
    }

def test_regime_detection_trending(detector, trending_market_data):
    """Test regime detection in trending market"""
    regime = detector.analyze_regime(trending_market_data)
    assert regime.regime == 'trending'
    assert regime.trend_direction == 'bullish'
    assert regime.confidence > 0.5

def test_regime_detection_volatile(detector, volatile_market_data):
    """Test regime detection in volatile market"""
    regime = detector.analyze_regime(volatile_market_data)
    assert regime.regime == 'high_volatility'
    assert regime.rsi_levels == (20, 80)

def test_volume_profile_analysis(detector):
    """Test volume profile analysis"""
    # Create more realistic volume data with clear statistical deviation
    base_volume = 1000000
    normal_volumes = [base_volume + np.random.normal(0, base_volume * 0.1) for _ in range(40)]
    spike_volume = base_volume * 3  # Clear 3x volume spike
    
    market_data = {
        'price_history': [100] * 50,
        'volume_history': normal_volumes + [base_volume] * 9 + [spike_volume]  # End with clear spike
    }
    
    regime = detector.analyze_regime(market_data)
    assert regime.volume_profile == 'high'
    
    # Test low volume scenario
    low_volume = base_volume * 0.3  # Clear volume drop
    market_data['volume_history'] = normal_volumes + [base_volume] * 9 + [low_volume]
    regime = detector.analyze_regime(market_data)
    assert regime.volume_profile == 'low'

def test_rsi_level_adjustment(detector, trending_market_data):
    """Test RSI level adjustment"""
    regime = detector.analyze_regime(trending_market_data)
    # Should have tighter RSI bands in trending market
    assert regime.rsi_levels == (40, 60)

def test_confidence_calculation(detector, trending_market_data, volatile_market_data):
    """Test confidence calculation in different regimes"""
    trending_regime = detector.analyze_regime(trending_market_data)
    volatile_regime = detector.analyze_regime(volatile_market_data)
    
    assert 0 <= trending_regime.confidence <= 1
    assert 0 <= volatile_regime.confidence <= 1
    # Volatile market should have higher confidence due to clearer signals
    assert volatile_regime.confidence > 0.5
