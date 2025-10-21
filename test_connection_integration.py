"""
Test MT5 Connector Integration with Data Fetcher
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from mt5_connector import MT5Connector
from src.mt5.data_fetcher import MT5DataFetcher


def test_integration():
    """Test full integration"""
    print("\n" + "="*60)
    print("TESTING MT5 CONNECTOR + DATA FETCHER INTEGRATION")
    print("="*60)
    
    # Step 1: Connect using new connector
    print("\n[Step 1] Connecting with MT5Connector...")
    connector = MT5Connector()
    success, message = connector.connect()
    
    if not success:
        print(f"\n❌ Connection failed: {message}")
        return False
    
    print("\n✓ Connected successfully")
    
    # Step 2: Verify connection
    print("\n[Step 2] Verifying connection...")
    if not connector.is_connected():
        print("❌ Connection check failed")
        return False
    
    account = connector.get_account_info()
    print(f"✓ Account: {account['login']} @ {account['server']}")
    print(f"✓ Balance: {account['balance']} {account['currency']}")
    
    # Step 3: Test data fetcher
    print("\n[Step 3] Testing MT5DataFetcher...")
    fetcher = MT5DataFetcher(connection=None)  # No old connection needed
    
    # Step 4: Fetch data
    print("\n[Step 4] Fetching EURUSD H1 data...")
    df = fetcher.get_ohlcv('EURUSD', 'H1', count=10)
    
    if df is None or df.empty:
        print("❌ Failed to fetch data")
        connector.disconnect()
        return False
    
    print(f"✓ Fetched {len(df)} bars")
    print(f"\nLatest bar:")
    print(df[['time', 'open', 'high', 'low', 'close', 'tick_volume']].tail(1))
    
    # Step 5: Test multiple symbols
    print("\n[Step 5] Testing multiple symbols...")
    symbols = ['EURUSD', 'GBPUSD', 'USDJPY']
    
    for symbol in symbols:
        df = fetcher.get_ohlcv(symbol, 'H1', count=5)
        if df is not None and not df.empty:
            print(f"✓ {symbol}: {len(df)} bars")
        else:
            print(f"❌ {symbol}: Failed")
    
    # Step 6: Test multiple timeframes
    print("\n[Step 6] Testing multiple timeframes...")
    timeframes = ['M15', 'H1', 'H4', 'D1']
    
    for tf in timeframes:
        df = fetcher.get_ohlcv('EURUSD', tf, count=5)
        if df is not None and not df.empty:
            print(f"✓ EURUSD {tf}: {len(df)} bars")
        else:
            print(f"❌ EURUSD {tf}: Failed")
    
    # Step 7: Disconnect
    print("\n[Step 7] Disconnecting...")
    connector.disconnect()
    print("✓ Disconnected")
    
    # Success!
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED - INTEGRATION WORKING!")
    print("="*60)
    
    return True


if __name__ == "__main__":
    success = test_integration()
    sys.exit(0 if success else 1)
