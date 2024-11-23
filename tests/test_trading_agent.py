import pytest
from typing import Dict, Any

class ConcreteTestTradingAgent:
    """Concrete implementation for testing"""
    def __init__(self, agent_id: str, config: Dict[str, Any]):
        self.agent_id = agent_id
        self.config = config
        
    async def initialize(self) -> None:
        pass
        
    async def run(self) -> None:
        pass
        
    async def shutdown(self) -> None:
        pass
        
    async def process_message(self, message: Dict[str, Any]) -> None:
        pass

@pytest.fixture
def test_config():
    return {
        'agent_id': 'test_trader_01',
        'default_position_size': 0.1,
        'max_risk': 0.02
    }

@pytest.fixture
def trading_agent(test_config):
    return ConcreteTestTradingAgent("test_trader", test_config)

@pytest.mark.asyncio
async def test_trading_agent_initialization(trading_agent):
    await trading_agent.initialize()
    assert trading_agent.agent_id == "test_trader"
    
@pytest.mark.asyncio
async def test_process_message_risk_update(trading_agent):
    message = {"type": "risk_update", "max_risk": 0.03}
    await trading_agent.process_message(message)
    
@pytest.mark.asyncio
async def test_process_message_strategy_signal(trading_agent):
    message = {"type": "strategy_signal", "signal": 1.0}
    await trading_agent.process_message(message)
