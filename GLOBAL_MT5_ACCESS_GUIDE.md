# 🌐 Global MT5 Access Guide

> NOTE: The legacy `mt5_connector.py` has been removed. The application now uses `src/mt5/connection.py` (`MT5Connection`) everywhere. Replace any references to `mt5_connector` with `get_mt5_connection()` and pass the connection to components that need it.

## How MT5 Connection Works in This App

### Overview

The app now uses a single connection manager: `src/mt5/connection.py` (`MT5Connection`). Connect via the GUI and the MetaTrader5 library is initialized for use by all components through the managed connection.

---

## 🔑 Key Concept: Global Initialization

`MT5Connection.connect()` initializes the MetaTrader5 Python library and establishes an authenticated session.

```python
from src.mt5.connection import MT5Connection
conn = MT5Connection()
conn.connect()
```

### What This Means

Once connected, **ANY** Python code in the app can use MT5:

```python
# In data_fetcher.py
import MetaTrader5 as mt5
rates = mt5.copy_rates_from_pos("EURUSD", mt5.TIMEFRAME_H1, 0, 100)  # ✅ Works!

# In sentiment_engine.py (if needed)
import MetaTrader5 as mt5
symbol_info = mt5.symbol_info("EURUSD")  # ✅ Works!

# In health_monitor.py
import MetaTrader5 as mt5
terminal_info = mt5.terminal_info()  # ✅ Works!
```

---

## 🏗️ Architecture

### Connection Flow

```
User clicks "CONNECT" in GUI
       ↓
gui/connection_panel.py
       ↓
get_mt5_connector() → Returns MT5Connector instance
       ↓
connector.connect() → Calls mt5.initialize() GLOBALLY
       ↓
MT5 library is now initialized for ENTIRE Python process
       ↓
ALL components can now use: import MetaTrader5 as mt5
```

### Component Access Pattern

```python
# ✅ Recommended pattern
from src.mt5.connection import get_mt5_connection
from src.mt5.data_fetcher import MT5DataFetcher

conn = get_mt5_connection()
conn.connect()
fetcher = MT5DataFetcher(connection=conn)
df = fetcher.get_ohlcv("EURUSD", "H1", count=100)
```

---

## 📦 Component Integration

### 1. Data Fetcher

**File:** `src/mt5/data_fetcher.py`

```python
class MT5DataFetcher:
    def __init__(self, connection: Optional[MT5Connection] = None):
        """
        Args:
            connection: MT5Connection instance (optional)
                       If None, uses GLOBAL MT5 API (recommended)
        """
        self.connection = connection  # None = use global API
```

**Usage:**
```python
# ✅ Recommended: Use global API
fetcher = MT5DataFetcher(connection=None)

# ❌ Old way: Pass connection object (no longer needed)
fetcher = MT5DataFetcher(connection=conn_obj)
```

### 2. Sentiment Engine

**File:** `src/analysis/sentiment_engine.py`

Doesn't need MT5 access directly - works with DataFrames:

```python
engine = SentimentEngine()
result = engine.analyze_sentiment(df, "EURUSD", "H1")
```

### 3. Health Monitor

**File:** `src/health/monitor.py`

Uses connector to check connection:

```python
from mt5_connector import get_connector

connector = get_connector()
if connector.is_connected():
    # Check health
    pass
```

---

## 🛠️ Helper Functions

### Check if MT5 is Available

```python
from mt5_connector import is_mt5_available

if is_mt5_available():
    print("MT5 is ready to use!")
else:
    print("MT5 not connected")
```

### Get Account Info

```python
from mt5_connector import get_mt5_account_info

account = get_mt5_account_info()
if account:
    print(f"Balance: {account['balance']} {account['currency']}")
```

### Ensure Connection

```python
from mt5_connector import ensure_mt5_connection

success, message = ensure_mt5_connection()
if success:
    # Proceed with MT5 operations
    import MetaTrader5 as mt5
    rates = mt5.copy_rates_from_pos(...)
```

---

## 📋 Usage Examples

### Example 1: Fetching Data

```python
# In analysis tab or any component:

# Step 1: Ensure connected
from mt5_connector import get_connector
connector = get_connector()

if not connector.is_connected():
    success, message = connector.connect()
    if not success:
        print(f"Connection failed: {message}")
        return

# Step 2: Use global MT5 API via data fetcher
from src.mt5.data_fetcher import MT5DataFetcher

fetcher = MT5DataFetcher(connection=None)  # Uses global API
df = fetcher.get_ohlcv("EURUSD", "H1", count=100)

if df is not None:
    print(f"Fetched {len(df)} bars")
```

### Example 2: Direct MT5 Usage

```python
# Anywhere in the app after connection:

import MetaTrader5 as mt5

# Get symbol info
symbol_info = mt5.symbol_info("EURUSD")
print(f"Bid: {symbol_info.bid}, Ask: {symbol_info.ask}")

# Get current tick
tick = mt5.symbol_info_tick("GBPUSD")
print(f"Last price: {tick.last}")

# Copy rates
rates = mt5.copy_rates_from_pos("EURUSD", mt5.TIMEFRAME_M15, 0, 50)
print(f"Fetched {len(rates)} bars")
```

### Example 3: In Streamlit App

```python
# In app.py or any tab:

import streamlit as st
from mt5_connector import get_connector
from src.mt5.data_fetcher import MT5DataFetcher

# Initialize connector in session state
if 'mt5_connector' not in st.session_state:
    st.session_state.mt5_connector = get_connector()

connector = st.session_state.mt5_connector

# Check connection
if not connector.is_connected():
    st.error("MT5 not connected. Go to Settings → MT5 Connection")
    return

# Use global MT5 API
fetcher = MT5DataFetcher(connection=None)
df = fetcher.get_ohlcv("EURUSD", "H1", count=100)

st.write(df)
```

---

## ✅ Best Practices

### Do's ✅

1. **Always use `get_connector()` for connection management**
   ```python
   from mt5_connector import get_connector
   connector = get_connector()
   ```

2. **Pass `connection=None` to MT5DataFetcher**
   ```python
   fetcher = MT5DataFetcher(connection=None)  # Uses global API
   ```

3. **Check connection before operations**
   ```python
   if connector.is_connected():
       # Safe to use MT5
   ```

4. **Import MT5 directly when needed**
   ```python
   import MetaTrader5 as mt5
   # After connector.connect(), this works everywhere
   ```

### Don'ts ❌

1. **Don't create multiple connections**
   ```python
   # ❌ BAD
   from src.mt5.connection import MT5Connection
   conn1 = MT5Connection()
   conn2 = MT5Connection()  # Causes conflicts!
   ```

2. **Don't call mt5.initialize() directly**
   ```python
   # ❌ BAD
   import MetaTrader5 as mt5
   mt5.initialize()  # Let connector handle this
   ```

3. **Don't pass old connection objects**
   ```python
   # ❌ OLD WAY
   from src.mt5.connection import MT5Connection
   conn = MT5Connection()
   fetcher = MT5DataFetcher(connection=conn)
   
   # ✅ NEW WAY
   fetcher = MT5DataFetcher(connection=None)
   ```

---

## 🔍 Troubleshooting

### Problem: "MT5 functions return None"

**Cause:** MT5 not initialized globally

**Solution:**
```python
from mt5_connector import get_connector
connector = get_connector()
success, message = connector.connect()
```

### Problem: "Authorization failed (-6)"

**Cause:** Multiple initialization attempts or MT5 settings

**Solution:**
1. Enable AutoTrading in MT5 terminal
2. Close other programs using MT5
3. Restart MT5 as Administrator

### Problem: "Component can't access MT5"

**Cause:** Component might be trying to use old connection pattern

**Solution:**
```python
# Change from:
fetcher = MT5DataFetcher(connection=old_conn)  # ❌

# To:
fetcher = MT5DataFetcher(connection=None)  # ✅
```

---

## 🧪 Testing Global Access

### Test Script

Run this to verify global access:

```python
# test_global_access.py
from mt5_connector import get_connector, is_mt5_available
import MetaTrader5 as mt5

# Connect
connector = get_connector()
success, message = connector.connect()

if not success:
    print(f"Failed: {message}")
    exit(1)

# Test global access
print("Testing global MT5 access...")

# 1. Terminal info
terminal = mt5.terminal_info()
print(f"✅ Terminal: {terminal.name if terminal else 'N/A'}")

# 2. Account info  
account = mt5.account_info()
print(f"✅ Account: {account.login if account else 'N/A'}")

# 3. Symbol info
symbol = mt5.symbol_info("EURUSD")
print(f"✅ Symbol: Bid={symbol.bid if symbol else 'N/A'}")

# 4. Rates
rates = mt5.copy_rates_from_pos("EURUSD", mt5.TIMEFRAME_H1, 0, 10)
print(f"✅ Rates: {len(rates) if rates is not None else 0} bars")

print("\n✅ All components have global MT5 access!")

connector.disconnect()
```

---

## 📊 Comparison: Old vs New

### Old System (Removed)

```python
# ❌ OLD: Required passing connection object

from src.mt5.connection import MT5Connection
conn = MT5Connection()
conn.connect()

# Every component needed connection object
fetcher = MT5DataFetcher(connection=conn)
engine = SentimentEngine(connection=conn)
monitor = HealthMonitor(connection=conn)
```

**Problems:**
- Connection object passed everywhere
- Multiple instances caused conflicts
- Complex dependency management
- Error-prone

### New System (Current)

```python
# ✅ NEW: Global initialization

from mt5_connector import get_connector

# Connect once
connector = get_connector()
connector.connect()  # Initializes MT5 globally

# All components use global API
fetcher = MT5DataFetcher(connection=None)
engine = SentimentEngine()  # No connection needed
monitor = HealthMonitor()   # Uses global API

# Or use MT5 directly
import MetaTrader5 as mt5
rates = mt5.copy_rates_from_pos(...)  # Works!
```

**Benefits:**
- ✅ Simple and clean
- ✅ No connection passing
- ✅ One source of truth
- ✅ No conflicts
- ✅ Easy to use

---

## 🎯 Summary

### Key Points

1. **`mt5_connector.py` initializes MT5 GLOBALLY**
   - One call to `connector.connect()`
   - Entire app can use MT5

2. **Components use global API**
   - No need to pass connection objects
   - Just `import MetaTrader5 as mt5`

3. **Simplified architecture**
   - Removed old `MT5Connection` class
   - Single connector via `get_connector()`

4. **Full app access**
   - Data fetcher: `MT5DataFetcher(connection=None)`
   - Direct usage: `mt5.copy_rates_from_pos(...)`
   - Anywhere: `mt5.account_info()`, `mt5.symbol_info()`

### The Connection is Global ✅

```
mt5_connector.connect()
        ↓
   MT5 Initialized GLOBALLY
        ↓
┌───────┴────────┬─────────┬──────────┐
│                │         │          │
Data Fetcher   GUI    Analyzers   Health Monitor
     ↓            ↓         ↓          ↓
   All can use import MetaTrader5 as mt5
```

---

**Date:** 2025-10-21  
**Version:** 2.1.0  
**Status:** ✅ Production Ready
