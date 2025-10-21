"""
Comprehensive Module Integration Test
Tests all module connections and data flow
"""
import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def print_test(name, passed, details=""):
    """Print test result"""
    status = f"{GREEN}✓{RESET}" if passed else f"{RED}✗{RESET}"
    print(f"{status} {name}")
    if details:
        print(f"  {details}")

def test_mt5_connector():
    """Test 1: MT5 Connector"""
    print(f"\n{'='*60}")
    print("TEST 1: MT5 Connector")
    print(f"{'='*60}")
    
    try:
        from mt5_connector import MT5Connector, get_connector
        
        connector = MT5Connector()
        print_test("MT5Connector class import", True)
        
        # Test connection
        success, message = connector.connect()
        print_test("MT5 connection", success, message)
        
        if success:
            # Test status
            status = connector.get_status()
            print_test("Get status", status['connected'])
            
            # Test account info
            account = connector.get_account_info()
            print_test("Get account info", account is not None, 
                      f"Account: {account['login']}" if account else "")
            
            connector.disconnect()
            return True
        return False
        
    except Exception as e:
        print_test("MT5Connector", False, str(e))
        return False

def test_data_fetcher(connector):
    """Test 2: Data Fetcher"""
    print(f"\n{'='*60}")
    print("TEST 2: Data Fetcher")
    print(f"{'='*60}")
    
    try:
        from src.mt5.data_fetcher import MT5DataFetcher
        
        # Reconnect for test
        if not connector.is_connected():
            connector.connect()
        
        # Create fetcher
        fetcher = MT5DataFetcher(connection=None)
        print_test("MT5DataFetcher init", True)
        
        # Test symbol info
        symbol_info = fetcher.get_symbol_info('EURUSD')
        print_test("Get symbol info", symbol_info is not None,
                  f"Spread: {symbol_info['spread']}" if symbol_info else "")
        
        # Test OHLCV fetch
        df = fetcher.get_ohlcv('EURUSD', 'H1', count=10)
        print_test("Fetch OHLCV data", df is not None and not df.empty,
                  f"Fetched {len(df)} bars" if df is not None else "")
        
        if df is not None and not df.empty:
            # Test data structure
            required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            has_cols = all(col in df.columns for col in required_cols)
            print_test("Data structure valid", has_cols,
                      f"Columns: {list(df.columns)}")
            return df
        
        return None
        
    except Exception as e:
        print_test("Data Fetcher", False, str(e))
        return None

def test_technical_indicators(df):
    """Test 3: Technical Indicators"""
    print(f"\n{'='*60}")
    print("TEST 3: Technical Indicators")
    print(f"{'='*60}")
    
    try:
        from src.indicators.technical import TechnicalIndicators
        
        tech = TechnicalIndicators()
        print_test("TechnicalIndicators init", True)
        
        # Test RSI
        rsi = tech.calculate_rsi(df)
        print_test("Calculate RSI", rsi is not None and not rsi.empty,
                  f"Latest RSI: {rsi.iloc[-1]:.2f}" if rsi is not None else "")
        
        # Test MACD
        macd = tech.calculate_macd(df)
        print_test("Calculate MACD", macd is not None)
        
        # Test all indicators
        all_indicators = tech.calculate_all_indicators(df)
        print_test("Calculate all indicators", bool(all_indicators),
                  f"Generated {len(all_indicators)} indicator groups")
        
        return all_indicators
        
    except Exception as e:
        print_test("Technical Indicators", False, str(e))
        return None

def test_smc_analyzer(df):
    """Test 4: SMC Analyzer"""
    print(f"\n{'='*60}")
    print("TEST 4: SMC Analyzer")
    print(f"{'='*60}")
    
    try:
        from src.indicators.smc import SMCAnalyzer
        
        smc = SMCAnalyzer()
        print_test("SMCAnalyzer init", True)
        
        # Test market structure
        structure = smc.detect_market_structure(df)
        print_test("Detect market structure", structure is not None,
                  f"Trend: {structure.get('trend')}" if structure else "")
        
        # Test order blocks
        order_blocks = smc.detect_order_blocks(df)
        print_test("Detect order blocks", order_blocks is not None,
                  f"Found {len(order_blocks)} order blocks")
        
        # Test FVGs
        fvgs = smc.detect_fvg(df)
        print_test("Detect FVGs", fvgs is not None,
                  f"Found {len(fvgs)} FVGs")
        
        # Test complete analysis
        analysis = smc.analyze(df, 'EURUSD')
        print_test("Complete SMC analysis", analysis is not None)
        
        return analysis
        
    except Exception as e:
        print_test("SMC Analyzer", False, str(e))
        return None

def test_sentiment_engine(df):
    """Test 5: Sentiment Engine"""
    print(f"\n{'='*60}")
    print("TEST 5: Sentiment Engine")
    print(f"{'='*60}")
    
    try:
        from src.analysis.sentiment_engine import SentimentEngine
        
        engine = SentimentEngine()
        print_test("SentimentEngine init", True)
        
        # Test sentiment analysis
        result = engine.analyze_sentiment(df, 'EURUSD', 'H1')
        print_test("Analyze sentiment", result is not None)
        
        if result:
            print_test("Sentiment generated", 'sentiment' in result,
                      f"Sentiment: {result.get('sentiment')}")
            print_test("Confidence calculated", 'confidence' in result,
                      f"Confidence: {result.get('confidence', 0)*100:.1f}%")
            print_test("Risk level assessed", 'risk_level' in result,
                      f"Risk: {result.get('risk_level')}")
            return result
        
        return None
        
    except Exception as e:
        print_test("Sentiment Engine", False, str(e))
        return None

def test_multi_timeframe(connector):
    """Test 6: Multi-Timeframe Analyzer"""
    print(f"\n{'='*60}")
    print("TEST 6: Multi-Timeframe Analyzer")
    print(f"{'='*60}")
    
    try:
        from src.analysis.multi_timeframe import MultiTimeframeAnalyzer
        from src.mt5.data_fetcher import MT5DataFetcher
        
        mtf = MultiTimeframeAnalyzer()
        print_test("MultiTimeframeAnalyzer init", True)
        
        # Fetch data for multiple timeframes
        fetcher = MT5DataFetcher(connection=None)
        data_dict = {}
        timeframes = ['M15', 'H1', 'H4']
        
        for tf in timeframes:
            df = fetcher.get_ohlcv('EURUSD', tf, count=100)
            if df is not None:
                data_dict[tf] = df
        
        print_test("Fetch multi-timeframe data", len(data_dict) > 0,
                  f"Fetched {len(data_dict)} timeframes")
        
        if data_dict:
            # Test MTF analysis
            result = mtf.analyze_multiple_timeframes(data_dict, 'EURUSD')
            print_test("Multi-timeframe analysis", result is not None)
            
            if result:
                print_test("Alignment calculated", 'alignment' in result)
                print_test("Dominant sentiment", 'dominant_sentiment' in result)
                return result
        
        return None
        
    except Exception as e:
        print_test("Multi-Timeframe Analyzer", False, str(e))
        return None

def test_database_repository():
    """Test 7: Database Repository"""
    print(f"\n{'='*60}")
    print("TEST 7: Database Repository")
    print(f"{'='*60}")
    
    try:
        from src.database.repository import DatabaseRepository, get_repository
        
        repo = get_repository()
        print_test("DatabaseRepository init", True)
        
        # Test symbol operations
        symbol = repo.get_or_create_symbol('EURUSD')
        print_test("Get/create symbol", symbol is not None,
                  f"Symbol ID: {symbol.id}" if symbol else "")
        
        # Test get symbols
        symbols = repo.get_all_symbols()
        print_test("Get all symbols", symbols is not None,
                  f"Found {len(symbols)} symbols")
        
        # Test predictions (may be empty)
        predictions = repo.get_predictions(limit=5)
        print_test("Get predictions", predictions is not None,
                  f"Found {len(predictions)} predictions")
        
        return repo
        
    except Exception as e:
        print_test("Database Repository", False, str(e))
        return None

def test_ml_pipeline():
    """Test 8: ML Pipeline"""
    print(f"\n{'='*60}")
    print("TEST 8: ML Pipeline")
    print(f"{'='*60}")
    
    try:
        from src.ml.feature_engineering import FeatureEngineer
        from src.ml.model_manager import ModelManager
        
        engineer = FeatureEngineer()
        print_test("FeatureEngineer init", True)
        
        manager = ModelManager()
        print_test("ModelManager init", True)
        
        # Check for existing models
        models = manager.list_models()
        print_test("List models", models is not None,
                  f"Found {len(models)} models" if models else "No models yet")
        
        return True
        
    except Exception as e:
        print_test("ML Pipeline", False, str(e))
        return False

def test_health_monitor():
    """Test 9: Health Monitor"""
    print(f"\n{'='*60}")
    print("TEST 9: Health Monitor")
    print(f"{'='*60}")
    
    try:
        from src.health.monitor import HealthMonitor
        
        monitor = HealthMonitor()
        print_test("HealthMonitor init", True)
        
        # Test system resources
        resources = monitor.check_system_resources()
        print_test("Check system resources", resources is not None,
                  f"Status: {resources.get('status')}")
        
        # Test comprehensive health check
        health = monitor.perform_health_check()
        print_test("Comprehensive health check", health is not None,
                  f"Status: {health.get('overall_status')}")
        
        if health:
            issues = health.get('issues', [])
            print_test("Issues detected", True,
                      f"{len(issues)} issues found")
        
        return health
        
    except Exception as e:
        print_test("Health Monitor", False, str(e))
        return None

def test_logger():
    """Test 10: Logger"""
    print(f"\n{'='*60}")
    print("TEST 10: Logger")
    print(f"{'='*60}")
    
    try:
        from src.utils.logger import get_logger, setup_logging
        
        logger = get_logger()
        print_test("Get logger", logger is not None)
        
        # Test logging
        logger.info("Integration test message")
        print_test("Log info message", True)
        
        logger.debug("Debug test message")
        print_test("Log debug message", True)
        
        return True
        
    except Exception as e:
        print_test("Logger", False, str(e))
        return False

def test_gui_components():
    """Test 11: GUI Components"""
    print(f"\n{'='*60}")
    print("TEST 11: GUI Components")
    print(f"{'='*60}")
    
    try:
        from gui.components.connection_panel import get_mt5_connector
        from gui.components.live_logs import log_to_console, add_activity
        
        print_test("Import connection_panel", True)
        print_test("Import live_logs", True)
        
        # These work without Streamlit running
        connector = get_mt5_connector()
        print_test("Get MT5 connector from GUI", connector is not None)
        
        return True
        
    except Exception as e:
        print_test("GUI Components", False, str(e))
        return False

def main():
    """Run all tests"""
    print(f"\n{'='*60}")
    print("COMPREHENSIVE MODULE INTEGRATION TEST")
    print(f"{'='*60}")
    print("Testing all module connections and data flow...")
    
    results = {}
    
    # Test 1: MT5 Connector
    connector_ok = test_mt5_connector()
    results['MT5 Connector'] = connector_ok
    
    if not connector_ok:
        print(f"\n{RED}❌ MT5 Connector failed - cannot continue{RESET}")
        return False
    
    # Reconnect for remaining tests
    from mt5_connector import get_connector
    connector = get_connector()
    connector.connect()
    
    # Test 2: Data Fetcher
    df = test_data_fetcher(connector)
    results['Data Fetcher'] = df is not None
    
    if df is not None:
        # Test 3: Technical Indicators
        indicators = test_technical_indicators(df)
        results['Technical Indicators'] = indicators is not None
        
        # Test 4: SMC Analyzer
        smc_result = test_smc_analyzer(df)
        results['SMC Analyzer'] = smc_result is not None
        
        # Test 5: Sentiment Engine
        sentiment = test_sentiment_engine(df)
        results['Sentiment Engine'] = sentiment is not None
    else:
        results['Technical Indicators'] = False
        results['SMC Analyzer'] = False
        results['Sentiment Engine'] = False
    
    # Test 6: Multi-Timeframe
    mtf_result = test_multi_timeframe(connector)
    results['Multi-Timeframe'] = mtf_result is not None
    
    # Test 7: Database
    repo = test_database_repository()
    results['Database'] = repo is not None
    
    # Test 8: ML Pipeline
    ml_ok = test_ml_pipeline()
    results['ML Pipeline'] = ml_ok
    
    # Test 9: Health Monitor
    health = test_health_monitor()
    results['Health Monitor'] = health is not None
    
    # Test 10: Logger
    logger_ok = test_logger()
    results['Logger'] = logger_ok
    
    # Test 11: GUI Components
    gui_ok = test_gui_components()
    results['GUI Components'] = gui_ok
    
    # Disconnect
    connector.disconnect()
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for module, status in results.items():
        symbol = f"{GREEN}✓{RESET}" if status else f"{RED}✗{RESET}"
        print(f"{symbol} {module}")
    
    print(f"\n{passed}/{total} modules passed")
    
    if passed == total:
        print(f"\n{GREEN}{'='*60}")
        print("🎉 ALL TESTS PASSED - ALL MODULES CONNECTED!")
        print(f"{'='*60}{RESET}\n")
        return True
    else:
        print(f"\n{YELLOW}{'='*60}")
        print(f"⚠️  {total - passed} module(s) failed")
        print(f"{'='*60}{RESET}\n")
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
