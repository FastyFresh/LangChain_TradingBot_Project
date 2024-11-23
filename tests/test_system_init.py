import pytest
from pathlib import Path
import logging
import yaml
from src.system.initialize import SystemInitializer

@pytest.fixture
def test_config_path(tmp_path):
    """Create a temporary test configuration file"""
    config = {
        'environment': 'test',
        'agents': {
            'test_agent_1': {
                'agent_id': 'test_agent_1',
                'agent_type': 'test_trader',
                'risk_limits': {'max_position_size': 0.1},
                'ml_models': ['test_model_1'],
                'strategies': ['test_strategy_1'],
                'update_interval': 60,
                'max_positions': 1,
                'emergency_shutdown_threshold': 0.2
            }
        },
        'models': {
            'test_model_1': {
                'model_id': 'test_model_1',
                'model_type': 'test_lstm',
                'feature_cols': ['price'],
                'target_cols': ['direction'],
                'batch_size': 32,
                'learning_rate': 0.001,
                'training_interval': 3600,
                'validation_split': 0.2,
                'early_stopping_patience': 5
            }
        },
        'risk_limits': {'max_portfolio_var': 0.1},
        'backup_interval': 300,
        'log_level': 'INFO',
        'emergency_contacts': ['test@example.com'],
        'api_keys': {'test_api': 'test_key'},
        'database_url': 'sqlite:///test.db',
        'max_total_exposure': 0.5
    }
    
    config_path = tmp_path / "test_config.yml"
    with open(config_path, 'w') as f:
        yaml.safe_dump(config, f)
    return str(config_path)

@pytest.fixture
def system_initializer(test_config_path):
    """Create a SystemInitializer instance with test configuration"""
    return SystemInitializer(test_config_path)

def test_system_initializer_creation(system_initializer):
    """Test that SystemInitializer is created correctly"""
    assert system_initializer is not None

def test_logging_setup(system_initializer):
    """Test that logging is set up correctly"""
    logger = system_initializer.logger
    assert isinstance(logger, logging.Logger)
    # Remove duplicate handlers if they exist
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    system_initializer._setup_logging()
    assert len(logger.handlers) == 2

def test_model_initialization(caplog):
    """Test model initialization with log capture"""
    with caplog.at_level(logging.INFO):
        initializer = SystemInitializer("config/development.yml")
        initializer._initialize_models()
        assert "Initializing ML models" in caplog.text

def test_full_initialization(caplog):
    """Test full system initialization with log capture"""
    with caplog.at_level(logging.INFO):
        initializer = SystemInitializer("config/development.yml")
        initializer.initialize_system()
        assert "System initialization completed successfully" in caplog.text

def test_system_shutdown(caplog):
    """Test system shutdown with log capture"""
    with caplog.at_level(logging.INFO):
        initializer = SystemInitializer("config/development.yml")
        initializer.shutdown_system()
        assert "Initiating system shutdown" in caplog.text

def test_error_handling(test_config_path):
    """Test error handling with invalid configuration"""
    with pytest.raises(Exception):
        SystemInitializer("nonexistent/config.yml").initialize_system()

def test_integration(caplog):
    """Test full integration of system initialization"""
    with caplog.at_level(logging.INFO):
        initializer = SystemInitializer("config/development.yml")
        try:
            initializer.initialize_system()
            initializer.start_system()
            assert "Starting trading system" in caplog.text
        finally:
            initializer.shutdown_system()
