# MT5 Connection Fix - Error Code -6 Authorization Failed

## Problem Identified

You were experiencing:
1. **Error Code -6: Terminal: Authorization failed**
2. **MT5 terminal disconnecting** every time the bot tried to connect
3. Loss of MT5 terminal connection even when manually logged in

## Root Cause

The issue was in `mt5_connector.py` in how `mt5.initialize()` was being called:

```python
# OLD CODE (PROBLEMATIC):
success = mt5.initialize(
    path=self.path,
    login=self.login,        # ❌ This causes the problem!
    password=self.password,  # ❌ This causes the problem!
    server=self.server,      # ❌ This causes the problem!
    timeout=self.timeout
)
```

**Why this causes disconnection:**
- When you pass `login`, `password`, and `server` to `mt5.initialize()`, it tries to:
  1. Disconnect any existing MT5 connection
  2. Initialize a new connection
  3. Login with the provided credentials

- If MT5 terminal is already running and connected, this causes it to:
  - **Drop the current connection** (your manual login gets disconnected)
  - **Reject the new connection** (Error -6: Authorization failed)
  - Leave you with no connection at all

## The Fix

I've updated `mt5_connector.py` with two key improvements:

### 1. Check for Existing Connection First

Before trying to initialize, the bot now checks if MT5 is already connected to the correct account:

```python
terminal_info = mt5.terminal_info()
if terminal_info is not None:
    account_info = mt5.account_info()
    
    if account_info and account_info.login == self.login and account_info.server == self.server:
        # Already connected to correct account - use it!
        return True, f"Connected as {account_info.login} on {account_info.server}"
```

### 2. Separate Initialize and Login Steps

```python
# NEW CODE (FIXED):
# Step 1: Initialize WITHOUT credentials (doesn't disconnect existing connection)
success = mt5.initialize(path=self.path, timeout=self.timeout)

# Step 2: Then login separately (after initialization succeeds)
if success:
    login_success = mt5.login(self.login, password=self.password, server=self.server)
```

This prevents the bot from forcefully disconnecting an existing MT5 terminal connection.

## What Changed

### Before:
1. Bot calls `mt5.initialize()` with credentials
2. MT5 terminal gets disconnected
3. New connection attempt fails (Error -6)
4. You're left with no connection

### After:
1. Bot checks if MT5 is already connected
2. If connected to correct account → **Reuses existing connection** ✅
3. If not connected → Initializes cleanly without disrupting terminal
4. Then logs in as a separate step
5. Connection succeeds without disruption ✅

## Benefits

1. ✅ **No more disconnections** - If MT5 terminal is already connected, the bot reuses it
2. ✅ **No more Error -6** - Clean initialization process
3. ✅ **Stable connections** - Existing terminal connections are preserved
4. ✅ **Better logging** - Clear messages about what's happening

## How to Use

1. **Option A: Manual MT5 Login (Recommended)**
   - Open MT5 terminal manually
   - Login to your account: `211744072` @ `ExnessKE-MT5Trial9`
   - Run the bot - it will detect and use your existing connection

2. **Option B: Let Bot Connect**
   - Make sure MT5 is closed
   - Start the bot
   - Go to Settings → MT5 Connection → Click CONNECT
   - Bot will initialize and login cleanly

## Testing Steps

### Quick Test (Command Line)

Run the test script to verify the fix:

```bash
python test_connection_fix.py
```

You should see:
```
✅ SUCCESS! Connected as 211744072 on ExnessKE-MT5Trial9
✅ TEST PASSED - Connection fix working correctly!
```

### Full Test (Streamlit App)

1. Close MT5 terminal completely (if running)
2. Run the bot: `streamlit run app.py`
3. Go to Settings → MT5 Connection
4. Click **🔌 CONNECT**
5. You should see:
   ```
   ✅ Connected as 211744072 on ExnessKE-MT5Trial9
   ```

### Test with Running MT5 Terminal

1. Open MT5 terminal manually
2. Login to account: `211744072` @ `ExnessKE-MT5Trial9`
3. Run the bot: `streamlit run app.py`
4. The bot should detect and reuse your existing connection
5. Your MT5 terminal should remain connected (no disconnection!)

## Troubleshooting

If you still see issues:

1. **Ensure AutoTrading is enabled in MT5:**
   - Open MT5 → Tools → Options → Expert Advisors
   - ☑ Enable: "Allow automated trading"
   - ☑ Enable: "Allow DLL imports"

2. **Check MT5 toolbar:**
   - AutoTrading button should be GREEN (enabled)

3. **Close other MT5 connections:**
   - Only one program should connect to MT5 at a time
   - Close any other trading bots or scripts

4. **Run as Administrator:**
   - Right-click MT5 → Run as Administrator
   - Then run the bot

## Files Modified

- ✅ `mt5_connector.py` - Fixed initialization logic (main connector)
- ✅ `src/mt5/connection.py` - Fixed initialization logic (legacy connector)
- ✅ `test_connection_fix.py` - Created test script to verify fix

## Next Steps

Run the bot and test the connection. You should no longer see:
- ❌ Error Code -6
- ❌ MT5 terminal disconnections
- ❌ Connection failures

The bot will now work harmoniously with your MT5 terminal! 🎉
