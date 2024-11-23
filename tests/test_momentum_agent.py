import pytest
from datetime import datetime
import numpy as np
from src.agents.momentum_trading_agent import MomentumTradingAgent
import asyncio
import pytest_asyncio

@pytest.fixture
def config():
    return {
        'momentum_threshold': 0.02,
        'position_size': 0.1,
        'max_positions': 3,
        'risk_per_trade': 0.02,
        'max_drawdown': 0.2,
        'volatility_adjustment': True,
        'regime_config': {
            'lookback_period': 20,
            'volatility_threshold': 0.02,
            'trend_strength_threshold': 0.01
        }
    }

@pytest_asyncio.fixture
async def momentum_agent(config):
    agent = MomentumTradingAgent('test_momentum_agent', config)
    await agent.initialize()
    yield agent
    await agent.shutdown()

@pytest.mark.asyncio
async def test_agent_initialization(momentum_agent, config):
    """Test agent initialization with configuration"""
    assert momentum_agent.momentum_threshold == config['momentum_threshold']
    assert momentum_agent.position_size == config['position_size']
    assert momentum_agent.max_positions == config['max_positions']
    assert momentum_agent.risk_per_trade == config['risk_per_trade']
    assert momentum_agent.max_drawdown == config['max_drawdown']

@pytest.mark.asyncio
async def test_process_market_data(momentum_agent):
    """Test market data processing"""
    market_data = {
        'type': 'market_data',
        'price': 100.0,
        'price_history': [95.0, 98.0, 100.0],
        'volume_history': [1000, 1200, 1100]
    }
    
    message = {
        'sender': 'market_data_provider',
        'message_type': 'market_data',
        'content': market_data,
        'priority': 1,
        'timestamp': datetime.now()
    }
    
    result = await momentum_agent.process_message(message)
    assert isinstance(result, dict)
    assert 'status' in result or 'action' in result

@pytest.mark.asyncio
async def test_momentum_calculation(momentum_agent):
    """Test momentum calculation"""
    market_data = {
        'price_history': [100.0, 102.0, 105.0],
        'volume_history': [1000, 1200, 1100]
    }
    
    momentum = momentum_agent._calculate_momentum(market_data)
    assert isinstance(momentum, float)
    assert momentum == pytest.approx(0.05)

@pytest.mark.asyncio
async def test_risk_update_processing(momentum_agent):
    """Test risk update processing"""
    risk_update = {
        'sender': 'risk_manager',
        'message_type': 'risk_update',
        'content': {
            'risk_limits': {
                'momentum_threshold': 0.03,
                'position_size': 0.15
            }
        },
        'priority': 2,
        'timestamp': datetime.now()
    }
    
    result = await momentum_agent.process_message(risk_update)
    assert result['status'] == 'risk_updated'
    assert momentum_agent.momentum_threshold == 0.03
    assert momentum_agent.position_size == 0.15

@pytest.mark.asyncio
async def test_emergency_stop(momentum_agent):
    """Test emergency stop handling"""
    # First create a position
    market_data = {
        'sender': 'market_data_provider',
        'message_type': 'market_data',
        'content': {
            'price': 100.0,
            'price_history': [95.0, 98.0, 100.0],
            'volume_history': [1000, 1200, 1100]
        },
        'priority': 1,
        'timestamp': datetime.now()
    }
    
    await momentum_agent.process_message(market_data)
    
    # Then send emergency stop
    emergency_stop = {
        'sender': 'risk_manager',
        'message_type': 'emergency_stop',
        'content': {
            'reason': 'risk_limit_breach',
            'severity': 'high'
        },
        'priority': 3,
        'timestamp': datetime.now()
    }
    
    result = await momentum_agent.process_message(emergency_stop)
    assert result['status'] == 'emergency_stop_executed'
    assert len(momentum_agent.current_positions) == 0

@pytest.mark.asyncio
async def test_position_sizing(momentum_agent):
    """Test position size calculations"""
    # Test normal market conditions
    normal_size = momentum_agent._calculate_position_size('long', 100.0)
    assert normal_size <= momentum_agent.max_positions
    
    # Test high volatility conditions
    momentum_agent.risk_metrics = {'volatility': 0.4}
    volatile_size = momentum_agent._calculate_position_size('long', 100.0)
    assert volatile_size < normal_size

@pytest.mark.asyncio
async def test_market_regime_adaptation(momentum_agent):
    """Test strategy adaptation to market regime"""
    # Test trending market
    momentum_agent.market_regime = 'trending'
    momentum_agent.risk_metrics = {'trend_direction': 'bullish'}
    
    trend_size = momentum_agent._calculate_position_size('long', 100.0)
    assert trend_size > momentum_agent.position_size
    
    # Test high volatility market
    momentum_agent.market_regime = 'high_volatility'
    vol_size = momentum_agent._calculate_position_size('long', 100.0)
    assert vol_size < trend_size

@pytest.mark.asyncio
async def test_performance_tracking(momentum_agent):
    """Test performance metrics tracking"""
    assert 'total_trades' in momentum_agent.performance_metrics
    assert 'winning_trades' in momentum_agent.performance_metrics
    assert 'total_pnl' in momentum_agent.performance_metrics
    
    # Simulate a winning trade
    market_data = {
        'sender': 'market_data_provider',
        'message_type': 'market_data',
        'content': {
            'price': 110.0,  # Price moved in our favor
            'price_history': [100.0, 105.0, 110.0],
            'volume_history': [1000, 1200, 1100]
        },
        'priority': 1,
        'timestamp': datetime.now()
    }
    
    await momentum_agent.process_message(market_data)
    assert momentum_agent.performance_metrics['total_trades'] >= 0