# 🔌 MT5 Connection Debugging Guide

## Issue: "MT5 Connection (CRITICAL): Not connected"

This guide helps diagnose and fix MT5 connection issues.

---

## 🔍 Quick Diagnosis

### **Run this command to test:**

```bash
python -c "from src.mt5.connection import MT5Connection; conn = MT5Connection(); conn.connect()"
```

### **Expected Output (Success):**
```
🔄 MT5 Connection Attempt 1/3
   Login: 211744072
   Server: ExnessKE-MT5Trial9
   Path: C:\Program Files\MetaTrader 5\terminal64.exe
   ✓ MetaTrader5 module available
   Using path: C:\Program Files\MetaTrader 5\terminal64.exe
   ✓ MT5 initialized successfully
   🔐 Attempting login...
      Account: 211744072
      Server: ExnessKE-MT5Trial9
   ✓ Logged in successfully
   📊 Verifying account info...
   ✓ Account verified: 211744072 on ExnessKE-MT5Trial9
   ✅ Connection established successfully!
   Account: 211744072
   Server: ExnessKE-MT5Trial9
   Balance: XXXX USD
```

---

## ❌ Common Error Codes

### **Error Code 1: Terminal Not Installed**
```
❌ MT5 initialization failed: Code 1 - Terminal not installed
💡 Tip: MT5 terminal not installed or path incorrect
```

**Solution:**
1. Install MT5 from https://www.metatrader5.com/en/download
2. Verify installation path
3. Update path in config if needed

---

### **Error Code 5: Old Version**
```
❌ MT5 initialization failed: Code 5 - Old client version
💡 Tip: Old MT5 version - update to latest
```

**Solution:**
1. Open MT5 terminal
2. Help → Check for Updates
3. Install latest version
4. Restart bot

---

### **Error Code 10004: No Connection**
```
❌ MT5 login failed: Code 10004 - No connection
💡 Tip: No connection to trade server. Check:
   - Internet connection
   - Server name is correct
   - Firewall not blocking MT5
```

**Solution:**

**Step 1: Check Internet**
```bash
ping google.com
```

**Step 2: Check Server Name**
```python
from config.settings import MT5Config
print(f"Server: {MT5Config.SERVER}")
# Should be: ExnessKE-MT5Trial9
```

**Step 3: Check Firewall**
- Windows Firewall → Allow an app
- Add terminal64.exe
- Allow both Private and Public networks

**Step 4: Test Server Manually**
1. Open MT5 terminal
2. File → Login to Trade Account
3. Enter: 211744072 / dFbKaNLWQ53@9@Z / ExnessKE-MT5Trial9
4. If this fails, server may be down

---

### **Error Code 10013: Invalid Credentials**
```
❌ MT5 login failed: Code 10013 - Invalid account
💡 Tip: Invalid account credentials
```

**Solution:**
1. Verify credentials in config/settings.py:
```python
LOGIN: int = 211744072
PASSWORD: str = "dFbKaNLWQ53@9@Z"
SERVER: str = "ExnessKE-MT5Trial9"
```

2. These are test credentials - if they don't work, the demo account may have expired
3. Create new demo account at broker

---

### **Error Code 10014: Server Not Found**
```
❌ MT5 login failed: Code 10014 - Server not found
💡 Tip: Server not found or unavailable
```

**Solution:**
1. Check server name spelling: `ExnessKE-MT5Trial9`
2. Server may have been renamed by broker
3. Check broker's website for current server names
4. Try alternative servers (ExnessKE-MT5Trial10, etc.)

---

## 🛠️ Step-by-Step Debugging

### **Step 1: Verify Python Package**

```python
python -c "import MetaTrader5; print('✓ Package installed')"
```

If fails:
```bash
pip install MetaTrader5
```

---

### **Step 2: Check Config Loading**

```python
python -c "
from config.settings import MT5Config
print(f'LOGIN: {MT5Config.LOGIN}')
print(f'SERVER: {MT5Config.SERVER}')
print(f'PATH: {MT5Config.PATH}')
"
```

Expected:
```
LOGIN: 211744072
SERVER: ExnessKE-MT5Trial9
PATH: C:\Program Files\MetaTrader 5\terminal64.exe
```

---

### **Step 3: Check MT5 Installation**

**Windows:**
```cmd
dir "C:\Program Files\MetaTrader 5\terminal64.exe"
```

**Common Paths:**
- `C:\Program Files\MetaTrader 5\terminal64.exe` (64-bit)
- `C:\Program Files (x86)\MetaTrader 5\terminal.exe` (32-bit)
- `C:\Users\YourName\AppData\Roaming\MetaQuotes\Terminal\...`

If not found, download from: https://www.metatrader5.com/en/download

---

### **Step 4: Test Manual Connection**

1. Open MT5 terminal manually
2. File → Login to Trade Account
3. Enter test credentials:
   - Login: `211744072`
   - Password: `dFbKaNLWQ53@9@Z`
   - Server: `ExnessKE-MT5Trial9`

If manual connection works but bot doesn't:
- Python version mismatch (need 64-bit Python for 64-bit MT5)
- Permissions issue
- Antivirus blocking

---

### **Step 5: Test Initialize Only**

```python
python -c "
import MetaTrader5 as mt5
result = mt5.initialize()
if result:
    print('✓ Initialize OK')
    print(f'Version: {mt5.version()}')
    mt5.shutdown()
else:
    error = mt5.last_error()
    print(f'✗ Error: {error}')
"
```

---

### **Step 6: Test With Path**

```python
python -c "
import MetaTrader5 as mt5
path = r'C:\Program Files\MetaTrader 5\terminal64.exe'
result = mt5.initialize(path=path)
if result:
    print('✓ Initialize with path OK')
    mt5.shutdown()
else:
    error = mt5.last_error()
    print(f'✗ Error: {error}')
"
```

---

### **Step 7: Full Connection Test**

```python
python -c "
import MetaTrader5 as mt5

# Initialize
if not mt5.initialize():
    print(f'Init failed: {mt5.last_error()}')
    exit()

# Login
if not mt5.login(211744072, password='dFbKaNLWQ53@9@Z', server='ExnessKE-MT5Trial9'):
    print(f'Login failed: {mt5.last_error()}')
    mt5.shutdown()
    exit()

# Get account info
info = mt5.account_info()
if info:
    print(f'✓ Connected: {info.login} on {info.server}')
    print(f'Balance: {info.balance}')
else:
    print('Account info failed')

mt5.shutdown()
"
```

---

## 🔧 Environment-Specific Issues

### **Windows Issues:**

**1. 32-bit vs 64-bit Mismatch**
- 64-bit Python + 32-bit MT5 = Won't work
- 32-bit Python + 64-bit MT5 = Won't work

**Check Python:**
```python
import platform
print(platform.architecture()[0])  # Should match MT5 (64bit or 32bit)
```

**2. User Account Control (UAC)**
- Run CMD/PowerShell as Administrator
- Try running bot with elevated privileges

**3. Antivirus Blocking**
- Add MT5 folder to exceptions
- Add Python to exceptions
- Temporarily disable to test

---

### **Linux/Wine Issues:**

MT5 on Linux requires Wine:
1. Install Wine
2. Install MT5 under Wine
3. Python MetaTrader5 package may have limited support

**Better:** Use Windows or Windows VM for MT5

---

## 📊 Health Check Integration

The bot checks connection status during health checks.

**To see connection status:**
1. Go to **"Health"** tab
2. Click **"Health Check"**
3. Look for MT5 Connection status

**To see detailed logs:**
1. Go to **"Logs & Debug"** tab
2. Click **"Live Logs"**
3. Filter: ERROR
4. Look for MT5 connection errors

---

## 🚨 Emergency Troubleshooting

### **If Nothing Works:**

**1. Reinstall MT5**
```
1. Uninstall MT5
2. Delete: C:\Program Files\MetaTrader 5
3. Download fresh copy
4. Install with default settings
5. Restart computer
```

**2. Reinstall Python Package**
```bash
pip uninstall MetaTrader5
pip install MetaTrader5
```

**3. Create New Demo Account**
```
1. Go to broker website (Exness)
2. Create new demo account
3. Get new credentials
4. Update config/settings.py
```

**4. Check System Requirements**
- Windows 7 or higher (10/11 recommended)
- .NET Framework 4.0 or higher
- Internet connection
- Firewall allows MT5

---

## 📝 Log Examples

### **Successful Connection:**
```
2025-10-21 03:05:00 | INFO | Attempting MT5 connection...
2025-10-21 03:05:01 | INFO | MT5 initialized successfully
2025-10-21 03:05:01 | INFO | Logged in successfully
2025-10-21 03:05:02 | INFO | Account verified: 211744072 on ExnessKE-MT5Trial9
2025-10-21 03:05:02 | INFO | Connection established successfully!
```

### **Failed Connection:**
```
2025-10-21 03:05:00 | INFO | Attempting MT5 connection...
2025-10-21 03:05:01 | ERROR | MT5 initialization failed: Code 10004 - No connection
2025-10-21 03:05:01 | WARNING | Health Issue: MT5 Connection (CRITICAL): Not connected
```

---

## 🆘 Still Not Working?

**Collect this information:**

1. **Python version:**
```bash
python --version
```

2. **MT5 installation:**
```bash
dir "C:\Program Files\MetaTrader 5\terminal64.exe"
```

3. **Package version:**
```bash
pip show MetaTrader5
```

4. **Full error log:**
```bash
# Check logs/mt5_bot_errors.log
```

5. **Connection test output:**
```bash
python -c "from src.mt5.connection import MT5Connection; MT5Connection().connect()"
```

**Then:**
- Check TROUBLESHOOTING.md
- Review log files in logs/ directory
- Verify firewall settings
- Try manual MT5 connection first

---

## ✅ Quick Fixes Summary

| Issue | Quick Fix |
|-------|-----------|
| Package not found | `pip install MetaTrader5` |
| Path incorrect | Update PATH in config/settings.py |
| Credentials wrong | Verify LOGIN/PASSWORD/SERVER |
| Server unavailable | Check internet, firewall |
| Old MT5 version | Update MT5 terminal |
| 32/64 bit mismatch | Match Python and MT5 architecture |
| Firewall blocking | Add MT5 to firewall exceptions |

---

**Last Updated:** 2025-10-21  
**Status:** Enhanced connection diagnostics with detailed error codes
