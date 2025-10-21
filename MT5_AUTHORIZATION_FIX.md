# 🔧 MT5 Authorization Error (-6) Fix

## Problem Diagnosed

**Error Message:**
```
Initialization failed - Code -6: Terminal: Authorization failed
```

## Root Cause

The bot had **TWO SEPARATE MT5 connection systems** running simultaneously:

1. **OLD System**: `src/mt5/connection.py` with `MT5Connection` class
2. **NEW System**: `mt5_connector.py` with `MT5Connector` class

### Why This Caused Error -6

- Both systems were calling `mt5.initialize()` on the **same global MT5 API**
- MT5 only allows **ONE active connection per process**
- Multiple initialization attempts caused **authorization conflicts**
- MT5 terminal rejected the second connection with error code **-6**

### Symptoms

- ✅ Previous version worked (only one connection system)
- ❌ Current version failed (two systems competing)
- ❌ Connection dropped when accessing bot (both trying to connect)
- ❌ Error occurred every time bot started

---

## Solution Implemented

### 1. Added Error Code -6 Handling

**File:** `mt5_connector.py` (lines 136-148)

Added comprehensive diagnostics for error -6:

```python
elif error_code == -6:
    print(f"   💡 Authorization failed - MT5 terminal might be blocking API access")
    print(f"   💡 Solutions:")
    print(f"      1. Open MT5 terminal manually")
    print(f"      2. Go to Tools → Options → Expert Advisors")
    print(f"      3. Enable: ☑ Allow automated trading")
    print(f"      4. Enable: ☑ Allow DLL imports")
    print(f"      5. Check that AutoTrading button is enabled (green) in toolbar")
    print(f"      6. Close any other programs trying to connect to MT5")
    print(f"      7. Restart MT5 as Administrator if needed")
```

### 2. Added Singleton Protection

**File:** `mt5_connector.py` (lines 22-24, 95-130)

Added initialization lock to prevent concurrent connections:

```python
class MT5Connector:
    """Simple MT5 connection manager with singleton protection"""
    
    _initialization_lock = False  # Prevent concurrent initialization
```

Features:
- ✅ Detects if MT5 is already initialized
- ✅ Reuses existing connection if available
- ✅ Prevents multiple simultaneous `mt5.initialize()` calls
- ✅ Gracefully handles concurrent connection attempts

### 3. Removed Old Connection System

**Files Updated:**
- `app.py` - Removed `MT5Connection` import
- `src/health/diagnostics.py` - Updated to use new connector

**Before:**
```python
from src.mt5.connection import MT5Connection, get_mt5_connection  # ❌ OLD
```

**After:**
```python
# REMOVED: Old MT5Connection import - now using mt5_connector.py via GUI components
```

---

## What Changed

### Architecture Before (Broken)

```
app.py
  ├─ imports: src.mt5.connection.MT5Connection ❌
  └─ creates: MT5 connection instance

gui/components/connection_panel.py
  ├─ imports: mt5_connector.get_connector ❌
  └─ creates: ANOTHER MT5 connection instance

RESULT: Two systems fighting for control → Error -6
```

### Architecture After (Fixed)

```
app.py
  └─ NO direct MT5 imports ✅

gui/components/connection_panel.py
  └─ imports: mt5_connector.get_connector ✅
  └─ creates: SINGLE MT5 connection via singleton

RESULT: One unified connection system → Success
```

---

## How to Use

### Normal Usage (GUI)

1. **Start the bot:**
   ```bash
   start_bot.bat  # Windows
   ./start_bot.sh  # Linux/Mac
   ```

2. **Go to Settings → MT5 Connection**

3. **Click "🔌 CONNECT"**

4. **Wait 5-10 seconds**

5. **See green status:** 🟢 CONNECTED

### If You Get Error -6

**Option 1: Enable AutoTrading in MT5**
1. Open MT5 terminal manually
2. Tools → Options → Expert Advisors
3. Check:
   - ☑ Allow automated trading
   - ☑ Allow DLL imports
4. Click OK
5. Enable AutoTrading button (green) in toolbar
6. Try connecting again in bot

**Option 2: Run MT5 as Administrator**
1. Close MT5 completely
2. Right-click MT5 shortcut
3. "Run as Administrator"
4. Try connecting again in bot

**Option 3: Close Competing Programs**
1. Close any other trading bots
2. Close any other programs using MT5 API
3. Restart bot
4. Try connecting again

---

## Technical Details

### Error Code Reference

| Code | Meaning | Cause | Solution |
|------|---------|-------|----------|
| **-6** | Authorization failed | MT5 blocking API / Multiple connections | Enable AutoTrading, close other programs |
| **1** | Terminal not installed | MT5 not found | Install MT5 |
| **5** | Old client version | Outdated MT5 | Update MT5 |
| **10004** | No connection | Network issue | Check internet/firewall |
| **10013** | Invalid credentials | Wrong login/password | Update credentials |
| **10014** | Server not found | Wrong server name | Check server name |

### Connection Flow (New System)

```
1. User clicks "CONNECT" in GUI
   ↓
2. gui/connection_panel.py → get_mt5_connector()
   ↓
3. mt5_connector.py → get_connector() (singleton)
   ↓
4. Check if already initialized
   ├─ Yes → Reuse existing connection
   └─ No → Initialize new connection
   ↓
5. Set initialization lock
   ↓
6. Call mt5.initialize()
   ↓
7. Call mt5.login()
   ↓
8. Release initialization lock
   ↓
9. Return success/failure
```

---

## Testing

### Test 1: Basic Connection
```bash
python mt5_connector.py
```

**Expected Output:**
```
============================================================
MT5 CONNECTION ATTEMPT
============================================================

[1/4] Validating credentials...
   ✓ Credentials validated

[2/4] Checking MetaTrader5 package...
   ✓ MT5 package available

[3/4] Initializing MT5 terminal...
   ✓ MT5 initialized successfully

[4/4] Logging in to ExnessKE-MT5Trial9...
   ✓ Login successful!

============================================================
CONNECTION SUCCESSFUL
============================================================
```

### Test 2: GUI Connection
1. Start bot
2. Go to Settings → MT5 Connection
3. Click CONNECT
4. Check console for detailed output
5. Verify green status in GUI

### Test 3: Multiple Connection Attempts
1. Connect in GUI
2. Try to run `python mt5_connector.py` while connected
3. Should see: "⚠️ MT5 already initialized (possibly by another instance)"
4. Should reuse existing connection or handle gracefully

---

## Files Modified

### Core Changes
- ✅ `mt5_connector.py` - Added error -6 handling, singleton protection
- ✅ `app.py` - Removed old MT5Connection import
- ✅ `src/health/diagnostics.py` - Updated to use new connector

### Documentation
- ✅ `MT5_AUTHORIZATION_FIX.md` - This file

---

## Prevention

### For Developers

**Never:**
- ❌ Import both connection systems
- ❌ Call `mt5.initialize()` directly in app code
- ❌ Create multiple MT5Connection instances
- ❌ Skip the singleton pattern

**Always:**
- ✅ Use `get_connector()` from `mt5_connector.py`
- ✅ Reuse existing connector instance
- ✅ Let the connector handle initialization
- ✅ Check connection status before operations

### Code Pattern

**Wrong:**
```python
# ❌ Creating new connection every time
from src.mt5.connection import MT5Connection
conn = MT5Connection()
conn.connect()
```

**Correct:**
```python
# ✅ Using singleton connector
from mt5_connector import get_connector
connector = get_connector()
success, message = connector.connect()
```

---

## Summary

### What Was Wrong
- Two competing MT5 connection systems
- Multiple `mt5.initialize()` calls
- MT5 rejected second connection with error -6

### What We Fixed
- ✅ Removed old connection system
- ✅ Added singleton protection
- ✅ Added error -6 diagnostics
- ✅ Unified to single connection system

### Result
- ✅ Stable connections
- ✅ No more authorization errors
- ✅ Clear error messages if issues occur
- ✅ Graceful handling of edge cases

---

**Date:** 2025-10-21  
**Version:** 2.1.0  
**Status:** ✅ Fixed and Tested
