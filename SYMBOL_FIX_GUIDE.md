# Symbol Selection Fix Guide

## Problem Summary
The MT5 bot was failing to fetch data for GBPUSD with the error:
```
✗ SYMBOL SELECT FAILED - MT5 Error: (-1, 'Terminal: Call failed')
```

This error occurs when:
1. The symbol name doesn't match your broker's naming convention
2. The symbol isn't available in your broker's Market Watch
3. The symbol hasn't been subscribed to in your MT5 terminal

## Changes Made

### 1. Enhanced Data Fetcher (`src/mt5/data_fetcher.py`)

#### Added `find_symbol()` Method
A new intelligent symbol search function that:
- First tries exact match
- Then searches for case-insensitive matches
- Looks for symbols starting with the search term
- Finds symbols containing the search term
- Returns the best match with priority ranking

```python
def find_symbol(self, symbol: str) -> Optional[str]:
    """Find symbol by searching for exact match or similar names"""
    # Returns the correct symbol name or None
```

#### Improved Error Handling in `get_ohlcv()`
The method now:
- Automatically finds the correct symbol name if exact match fails
- Provides detailed debug output showing available symbols
- Suggests alternative symbol names
- Shows available forex symbols when symbol not found

### 2. Symbol Checker Tool (`check_symbols.py`)

Created a diagnostic script that:
- Initializes MT5 and displays connection info
- Searches for GBPUSD and related symbols
- Lists all available forex symbols
- Recommends the best symbol to use
- Attempts to make the symbol visible if needed

## How to Use

### Step 1: Run the Symbol Checker

```bash
python check_symbols.py
```

This will:
1. Connect to MT5
2. Show your broker and account info
3. Search for GBPUSD-related symbols
4. List all available forex symbols
5. Recommend the correct symbol name to use

### Step 2: Update Your Code

If the checker finds a different symbol name (e.g., "GBPUSD.m" or "GBPUSDm"), you have two options:

#### Option A: Update the Symbol List in `app.py`
```python
symbol = st.selectbox(
    "Symbol",
    ["EURUSD", "GBPUSD.m", "USDJPY", "XAUUSD", "BTCUSD"],  # Use correct name
    index=0
)
```

#### Option B: Let the Auto-Detection Work
The improved data fetcher will automatically find the correct symbol name. The debug logs will show:
```
[DEBUG]   Using symbol: GBPUSD.m (instead of GBPUSD)
```

### Step 3: Verify the Fix

1. Start the bot: `streamlit run app.py`
2. Go to Settings → MT5 Connection
3. Connect to MT5
4. Select GBPUSD from the dropdown
5. Click "🔄 Analyze"
6. Check the logs for successful data fetch

## Common Symbol Naming Conventions

Different brokers use different naming conventions:

| Broker Type | Example |
|------------|---------|
| Standard | `GBPUSD` |
| MetaQuotes Demo | `GBPUSD` |
| Some brokers | `GBPUSD.m`, `GBPUSDm` |
| ECN accounts | `GBPUSD.raw`, `GBPUSD.ecn` |
| Others | `GBP/USD`, `GBPUSD.pro` |

## Troubleshooting

### Symbol Still Not Found?

1. **Check Market Watch in MT5**
   - Open MT5 terminal
   - Press Ctrl+M to show Market Watch
   - Right-click → "Symbols"
   - Search for your desired symbol
   - Make sure it's checked (enabled)

2. **Contact Your Broker**
   - Some brokers don't offer certain symbols
   - Ask for the exact symbol names they support
   - Request access to forex symbols if needed

3. **Use the Available Symbols**
   - The checker script lists all available symbols
   - Choose from the visible forex symbols shown
   - Update your bot configuration accordingly

### Error Persists After Symbol Fix?

Check these:
1. **MT5 Connection**: Ensure MT5 is running and connected
2. **Account Type**: Some demo accounts have limited symbols
3. **Broker Access**: Verify you have access to forex symbols
4. **Terminal Settings**: Check if symbols are hidden in MT5 settings

## Debug Output Explanation

When fetching data, you'll see:
```
[DEBUG] get_ohlcv() START - Symbol: GBPUSD, TF: H4, Count: 1000
[DEBUG]   MT5 terminal_info: True
[DEBUG]   Searching for symbols matching 'GBPUSD'...
[DEBUG]   Found 3 matching symbols:
[DEBUG]     - GBPUSD.m
[DEBUG]     - GBPUSDm
[DEBUG]     - GBPUSD_test
[DEBUG]   Using symbol: GBPUSD.m (instead of GBPUSD)
[DEBUG]   ✓ Symbol GBPUSD.m selected
[DEBUG]   ✓ Successfully fetched 1000 rates
```

This shows:
- The search found similar symbols
- It selected the best match
- Data was fetched successfully

## Prevention

To avoid this issue in the future:

1. **Always run `check_symbols.py` first** when setting up on a new broker
2. **Document your broker's symbol names** in your configuration
3. **Test with one symbol** before adding multiple symbols
4. **Keep MT5 Market Watch updated** with symbols you need

## Additional Resources

- [MT5 Symbol Documentation](https://www.mql5.com/en/docs/integration/python_metatrader5/mt5symbolinfo_py)
- [MetaTrader 5 Python Integration](https://www.mql5.com/en/docs/python_metatrader5)

---

**Note**: The enhanced error handling now provides detailed debugging information automatically. If you encounter issues, check the console output for specific guidance on which symbols are available.
