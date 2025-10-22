# 🔌 MT5 Connection Guide

## New Simplified Connection System

The MT5 connection has been completely refactored for simplicity and control.

---

## 🎯 **Quick Start**

### **Step 1: Start the Bot**
```bash
start_bot.bat  # Windows
./start_bot.sh  # Linux/Mac
```

### **Step 2: Connect to MT5**
1. Click **"Settings"** tab (6th tab)
2. Click **"MT5 Connection"** sub-tab (first one)
3. Click the big **🔌 CONNECT** button
4. Wait 5-10 seconds
5. See green **🟢 CONNECTED** status

### **Step 3: Start Analyzing**
1. Go to **"Analysis"** tab
2. Select symbol and timeframe
3. Click **"🔄 Analyze"**

**That's it!** ✅

---

## 🔍 **New Architecture**

### Connection Module

Use `src/mt5/connection.py` (`MT5Connection`) as the single source of truth.

Standalone test:
```bash
python -c "from src.mt5.connection import MT5Connection as C; c=C(); print('Connecting...'); c.connect(); print('OK'); c.disconnect()"
```

**Expected output:**
```
============================================================
MT5 CONNECTION ATTEMPT
============================================================

[1/4] Validating credentials...
   Login: 211744072
   Server: ExnessKE-MT5Trial9
   Path: C:\Program Files\MetaTrader 5\terminal64.exe
   ✓ Credentials validated

[2/4] Checking MetaTrader5 package...
   ✓ MT5 package available (Build 3960)

[3/4] Initializing MT5 terminal...
   Trying path: C:\Program Files\MetaTrader 5\terminal64.exe
   ✓ MT5 initialized successfully

[4/4] Logging in to ExnessKE-MT5Trial9...
   ✓ Login successful!

============================================================
CONNECTION SUCCESSFUL
============================================================
Account: 211744072
Server: ExnessKE-MT5Trial9
Name: Demo Account
Balance: 10000.00 USD
Leverage: 1:100
Company: Exness
============================================================
```

---

## 🎨 **GUI Components**

### **1. Connection Status Widget** (Top of every page)

**When Connected:**
```
🟢 MT5 Connected: 211744072 @ ExnessKE-MT5Trial9
```

**When Disconnected:**
```
🔴 MT5 Disconnected - Go to Settings → Connection    [Connect]
```

---

### **2. Connection Panel** (Settings → MT5 Connection)

**Status Display:**
```
┌─────────────────────────────────────────────┐
│ 🟢 CONNECTED                     Uptime     │
│                                  15m        │
│ Account: 211744072                          │
│ Server: ExnessKE-MT5Trial9                  │
│ Balance: 10000.00 USD                       │
│ Company: Exness                             │
│ Connected for: 0h 15m                       │
└─────────────────────────────────────────────┘
```

**Connection Details:**
```
Login: 211744072               Password: ************
Server: ExnessKE-MT5Trial9     Path: C:\Program Files\MetaTr...
```

**Control Buttons:**
```
┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐
│ 🔌 CONNECT   │ │ ⛔ DISCONNECT │ │ 🔄 Check Status      │
│  (Primary)   │ │  (Secondary)  │ │                      │
└──────────────┘ └──────────────┘ └──────────────────────┘
```

---

## 🔧 **How It Works**

### **Connection Process**

**When you click CONNECT:**

1. **Validates credentials**
   - Checks LOGIN is set
   - Checks PASSWORD is set
   - Checks SERVER is set

2. **Checks MT5 package**
   - Verifies MetaTrader5 Python package installed
   - Shows build version

3. **Initializes MT5 terminal**
   - Tries configured path
   - Falls back to common paths if needed
   - Searches for MT5 installation

4. **Logs in to server**
   - Connects to ExnessKE-MT5Trial9
   - Uses credentials: 211744072 / dFbKaNLWQ53@9@Z
   - Retrieves account info

5. **Displays success**
   - Shows green status
   - Displays account details
   - Enables analysis

---

### **Connection State**

**Stored in Streamlit session state:**
```python
st.session_state.mt5_connection
```

**Persists across:**
- Tab changes
- Page refreshes (within same session)
- Multiple analyses

**Does NOT persist across:**
- Browser refresh
- App restart
- New browser session

---

## 🎮 **Controls**

### **CONNECT Button**
- **When to use:** First time or after disconnect
- **Color:** Blue (primary)
- **Time:** 5-10 seconds
- **Effect:** Establishes MT5 connection
- **Disabled:** When already connected

### **DISCONNECT Button**
- **When to use:** End of session, troubleshooting
- **Color:** Gray (secondary)
- **Time:** Instant
- **Effect:** Closes MT5 connection
- **Disabled:** When not connected

### **Check Status Button**
- **When to use:** Verify connection, refresh display
- **Color:** Gray
- **Time:** Instant
- **Effect:** Updates status display

---

## ❌ **Error Handling**

### **Analysis Without Connection**

**What you'll see:**
```
❌ MT5 not connected. Please connect in Settings → MT5 Connection
```

**Solution:**
1. Go to Settings tab
2. Click MT5 Connection
3. Click CONNECT

---

### **Connection Failures**

**Error Code 1: Terminal Not Installed**
```
❌ Initialization failed - Code 1: Terminal not installed
💡 MT5 not installed or wrong path
```

**Solution:** Install MT5 from https://www.metatrader5.com/en/download

---

**Error Code 5: Old Version**
```
❌ Initialization failed - Code 5: Old client version
💡 Old MT5 version - please update
```

**Solution:** Update MT5 to latest version

---

**Error Code -6: Authorization Failed**
```
❌ Initialization failed - Code -6: Terminal: Authorization failed
💡 Authorization failed - MT5 terminal might be blocking API access
```

**Solution:**
1. Open MT5 terminal manually
2. Go to **Tools → Options → Expert Advisors**
3. Enable: ☑ **Allow automated trading**
4. Enable: ☑ **Allow DLL imports**
5. Check that **AutoTrading button** is enabled (green) in toolbar
6. Close any other programs trying to connect to MT5
7. Restart MT5 as Administrator if needed

**Common Causes:**
- AutoTrading disabled in MT5 settings
- DLL imports not allowed
- Another program already connected to MT5
- MT5 terminal security settings too restrictive

---

**Error Code 10004: No Connection**
```
❌ Login failed - Code 10004: No connection
💡 No connection to server - check internet/firewall
```

**Solution:**
1. Check internet connection
2. Verify firewall not blocking MT5
3. Try manual connection in MT5 terminal

---

**Error Code 10013: Invalid Credentials**
```
❌ Login failed - Code 10013: Invalid account
💡 Invalid credentials or account expired
```

**Solution:**
- Test credentials may have expired
- Create new demo account at broker
- Update your environment variables (.env) consumed by `config/settings.py`

---

**Error Code 10014: Server Not Found**
```
❌ Login failed - Code 10014: Server not found
💡 Server 'ExnessKE-MT5Trial9' not found
```

**Solution:**
- Check server name spelling
- Server may have been renamed
- Try alternative server name

---

## 🔄 **Connection Lifecycle**

```
[App Start]
     ↓
[Disconnected] ─────────────────┐
     ↓                          │
[User clicks CONNECT]           │
     ↓                          │
[Validation]                    │
     ↓                          │
[Initialize MT5]                │
     ↓                          │
[Login]                         │
     ↓                          │
[Connected] ←───────────────────┤
     ↓                          │
[User analyses data]            │
     ↓                          │
[User clicks DISCONNECT] ───────┘
     ↓
[Disconnected]
```

---

## 💡 **Best Practices**

### **Do:**
✅ Connect once at start of session  
✅ Leave connected during analysis  
✅ Check status if unsure  
✅ Disconnect when finished  
✅ Reconnect if connection drops  

### **Don't:**
❌ Disconnect/reconnect repeatedly  
❌ Try to analyze while disconnected  
❌ Ignore connection errors  
❌ Modify credentials while connected  

---

## 🧪 **Testing Connection**

### **Test 1: Standalone Test**
```bash
python -c "from src.mt5.connection import MT5Connection as C; c=C(); c.connect(); print(c.get_account_info()); c.disconnect()"
```
**Should show:** Account info and a clean disconnect

---

### **Test 2: GUI Test**
1. Start bot
2. Go to Settings → MT5 Connection
3. Click CONNECT
4. Check console output
5. Verify green status

---

### **Test 3: Analysis Test**
1. Ensure connected (green status)
2. Go to Analysis tab
3. Click Analyze
4. Should fetch data successfully

---

## 📊 **Status Indicators**

| Indicator | Meaning | Action |
|-----------|---------|--------|
| 🟢 CONNECTED | Active connection | Can analyze |
| 🔴 DISCONNECTED | No connection | Click CONNECT |
| ⏱️ Uptime: 15m | Connection duration | - |
| ⚠️ Last error: ... | Previous failure | Check error message |

---

## 🛠️ **Troubleshooting**

### **Connection Button Does Nothing**
1. Check console for errors
2. Check Logs & Debug tab
3. Verify MT5 installed
4. Run standalone test

### **Connection Drops During Analysis**
1. Check internet connection
2. Verify MT5 terminal running
3. Check firewall settings
4. Reconnect using CONNECT button

### **"Not Connected" After Clicking CONNECT**
1. Wait full 10 seconds
2. Check error message displayed
3. See console output for details
4. Follow error-specific guidance

---

## 📖 **Code Examples**

### **Using Connection in Code**

```python
from src.mt5.connection import get_mt5_connection

conn = get_mt5_connection()
conn.connect()
if conn.is_connected():
    info = conn.get_account_info()
    print(f"Balance: {info['balance']}")
conn.disconnect()
```

---

### **Using in GUI Components**

```python
from gui.components.connection_panel import get_mt5_connector

conn = get_mt5_connector()
if conn.is_connected():
    # Do analysis
    pass
else:
    st.error("Please connect first")
```

---

## 🎯 **Summary**

**New system is:**
- ✅ Simpler - One module, clear flow
- ✅ Explicit - User controls connection
- ✅ Visible - Status always shown
- ✅ Testable - Standalone operation
- ✅ Debuggable - Detailed output

**Old system was:**
- ❌ Complex - Multiple classes
- ❌ Hidden - Auto-connect attempts
- ❌ Confusing - Unclear status
- ❌ Integrated - Hard to test
- ❌ Opaque - Limited feedback

---

**Last Updated:** 2025-10-21  
**Version:** 2.0.0 (Refactored)  
**Status:** ✅ Production Ready
