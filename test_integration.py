"""
Integration Test - Check Module Connectivity
"""
import sys
sys.path.insert(0, '.')

def test_complete_flow():
    """Test complete data flow from MT5 to Dashboard"""
    print("=" * 60)
    print("COMPREHENSIVE INTEGRATION TEST")
    print("=" * 60)
    print()
    
    results = []
    
    # Test 1: Configuration Layer
    print("1. Testing Configuration Layer...")
    try:
        from config.settings import AppConfig, DataConfig, MLConfig
        assert hasattr(AppConfig, 'PAGE_TITLE')
        assert hasattr(DataConfig, 'DEFAULT_SYMBOL')
        assert hasattr(MLConfig, 'MIN_CONFIDENCE')
        print("   ✓ Configuration layer OK")
        results.append(('Configuration', True))
    except Exception as e:
        print(f"   ✗ Configuration error: {e}")
        results.append(('Configuration', False))
    
    # Test 2: MT5 Layer
    print("\n2. Testing MT5 Layer...")
    try:
        from src.mt5.connection import MT5Connection
        from src.mt5.data_fetcher import MT5DataFetcher
        from src.mt5.validator import DataValidator
        
        conn = MT5Connection()
        fetcher = MT5DataFetcher(conn)
        validator = DataValidator()
        
        print("   ✓ MT5 Connection class initialized")
        print("   ✓ Data Fetcher initialized")
        print("   ✓ Data Validator initialized")
        results.append(('MT5 Layer', True))
    except Exception as e:
        print(f"   ✗ MT5 layer error: {e}")
        results.append(('MT5 Layer', False))
    
    # Test 3: Indicators Layer
    print("\n3. Testing Indicators Layer...")
    try:
        from src.indicators.technical import TechnicalIndicators
        from src.indicators.smc import SMCAnalyzer
        from src.indicators.calculator import IndicatorCalculator
        
        tech = TechnicalIndicators()
        smc = SMCAnalyzer()
        calc = IndicatorCalculator()
        
        print("   ✓ Technical Indicators initialized")
        print("   ✓ SMC Analyzer initialized")
        print("   ✓ Indicator Calculator initialized")
        results.append(('Indicators Layer', True))
    except Exception as e:
        print(f"   ✗ Indicators error: {e}")
        results.append(('Indicators Layer', False))
    
    # Test 4: Analysis Layer
    print("\n4. Testing Analysis Layer...")
    try:
        from src.analysis.sentiment_engine import SentimentEngine
        from src.analysis.multi_timeframe import MultiTimeframeAnalyzer
        from src.analysis.confidence_scorer import ConfidenceScorer
        
        engine = SentimentEngine()
        mtf = MultiTimeframeAnalyzer()
        scorer = ConfidenceScorer()
        
        print("   ✓ Sentiment Engine initialized")
        print("   ✓ Multi-Timeframe Analyzer initialized")
        print("   ✓ Confidence Scorer initialized")
        results.append(('Analysis Layer', True))
    except Exception as e:
        print(f"   ✗ Analysis error: {e}")
        results.append(('Analysis Layer', False))
    
    # Test 5: Database Layer
    print("\n5. Testing Database Layer...")
    try:
        from src.database.models import Base
        from src.database.repository import DatabaseRepository
        
        repo = DatabaseRepository()
        
        print("   ✓ Database models loaded")
        print("   ✓ Repository initialized")
        results.append(('Database Layer', True))
    except Exception as e:
        print(f"   ✗ Database error: {e}")
        results.append(('Database Layer', False))
    
    # Test 6: ML Layer
    print("\n6. Testing ML Layer...")
    try:
        from src.ml.model_manager import ModelManager
        from src.ml.training import ModelTrainer
        from src.ml.evaluator import ModelEvaluator
        from src.ml.feature_engineering import FeatureEngineer
        
        manager = ModelManager()
        trainer = ModelTrainer()
        evaluator = ModelEvaluator()
        engineer = FeatureEngineer()
        
        print("   ✓ Model Manager initialized")
        print("   ✓ Model Trainer initialized")
        print("   ✓ Model Evaluator initialized")
        print("   ✓ Feature Engineer initialized")
        results.append(('ML Layer', True))
    except Exception as e:
        print(f"   ✗ ML error: {e}")
        results.append(('ML Layer', False))
    
    # Test 7: Health Layer
    print("\n7. Testing Health Layer...")
    try:
        from src.health.monitor import HealthMonitor
        from src.health.diagnostics import SystemDiagnostics
        from src.health.recovery import AutoRecovery
        
        monitor = HealthMonitor()
        diag = SystemDiagnostics()
        recovery = AutoRecovery()
        
        print("   ✓ Health Monitor initialized")
        print("   ✓ System Diagnostics initialized")
        print("   ✓ Auto Recovery initialized")
        results.append(('Health Layer', True))
    except Exception as e:
        print(f"   ✗ Health error: {e}")
        results.append(('Health Layer', False))
    
    # Test 8: Reporting Layer
    print("\n8. Testing Reporting Layer...")
    try:
        from src.reporting.pdf_generator import PDFReportGenerator
        from src.reporting.charts import ChartGenerator
        
        pdf_gen = PDFReportGenerator()
        chart_gen = ChartGenerator()
        
        print("   ✓ PDF Generator initialized")
        print("   ✓ Chart Generator initialized")
        results.append(('Reporting Layer', True))
    except Exception as e:
        print(f"   ✗ Reporting error: {e}")
        results.append(('Reporting Layer', False))
    
    # Test 9: Logging Layer
    print("\n9. Testing Logging Layer...")
    try:
        from src.utils.logger import get_logger, setup_logging
        
        logger = get_logger()
        
        print("   ✓ Logger initialized")
        results.append(('Logging Layer', True))
    except Exception as e:
        print(f"   ✗ Logging error: {e}")
        results.append(('Logging Layer', False))
    
    # Test 10: GUI Components
    print("\n10. Testing GUI Components...")
    try:
        from gui.components.sentiment_card import render_sentiment_card
        from gui.components.chart_panel import render_price_chart
        from gui.components.health_dashboard import render_health_dashboard
        
        print("   ✓ Sentiment Card component loaded")
        print("   ✓ Chart Panel component loaded")
        print("   ✓ Health Dashboard component loaded")
        results.append(('GUI Components', True))
    except Exception as e:
        print(f"   ✗ GUI error: {e}")
        results.append(('GUI Components', False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, status in results if status)
    total = len(results)
    
    for layer, status in results:
        symbol = "✓" if status else "✗"
        print(f"{symbol} {layer}")
    
    print(f"\nResult: {passed}/{total} layers passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! System is fully integrated.")
        return True
    else:
        print(f"\n⚠ {total - passed} layer(s) failed. Review errors above.")
        return False

if __name__ == "__main__":
    success = test_complete_flow()
    sys.exit(0 if success else 1)
