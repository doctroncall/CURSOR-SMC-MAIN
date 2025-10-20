# 🔑 Test Credentials - Pre-configured

## ✅ Hardcoded Testing Credentials

The bot now comes with **dummy testing credentials already configured** for immediate testing!

### 📋 Pre-configured Values:

```
MT5_LOGIN=211744072
MT5_PASSWORD=dFbKaNLWQ53@9@Z
MT5_SERVER=ExnessKE-MT5Trial9
MT5_PATH=C:\Program Files\MetaTrader 5\terminal64.exe
MT5_TIMEOUT=60000
```

---

## 🚀 Quick Start - No Configuration Needed!

### **Option 1: Just Run It!** (Easiest)

```bash
# Windows users:
start_bot.bat

# Linux/Mac users:
./start_bot.sh
```

**That's it!** The bot will use the pre-configured dummy credentials automatically.

---

## 🔧 How It Works

### **1. Hardcoded in `config/settings.py`:**

```python
class MT5Config:
    """MT5 Connection Configuration"""
    # Hardcoded dummy credentials for testing
    LOGIN: int = int(os.getenv("MT5_LOGIN", "211744072"))
    PASSWORD: str = os.getenv("MT5_PASSWORD", "dFbKaNLWQ53@9@Z")
    SERVER: str = os.getenv("MT5_SERVER", "ExnessKE-MT5Trial9")
    PATH: Optional[str] = os.getenv("MT5_PATH", r"C:\Program Files\MetaTrader 5\terminal64.exe")
```

- If `.env` file exists → uses those values
- If `.env` doesn't exist → uses hardcoded defaults
- **Result:** Works out of the box! 📦

---

## 🔄 Override If Needed

### **Want to use your own credentials?**

Create a `.env` file:

```bash
# Copy the example
cp .env.example .env

# Edit with your credentials
nano .env  # or use any text editor
```

Then modify the values:
```
MT5_LOGIN=your_account_number
MT5_PASSWORD=your_password
MT5_SERVER=your_broker_server
```

---

## ✅ Testing the Configuration

### **1. Verify Credentials Loaded:**

```bash
python -c "from config.settings import MT5Config; print(f'Login: {MT5Config.LOGIN}'); print(f'Server: {MT5Config.SERVER}')"
```

**Expected Output:**
```
Login: 211744072
Server: ExnessKE-MT5Trial9
```

### **2. Test MT5 Connection:**

```python
from src.mt5.connection import MT5Connection

conn = MT5Connection()
if conn.connect():
    print("✅ Connected to MT5 successfully!")
    print(f"   Account: {conn.account_info['login']}")
    print(f"   Server: {conn.account_info['server']}")
    conn.disconnect()
else:
    print("❌ Connection failed")
```

---

## 📝 Important Notes

### ✅ **Safe to Share**
- These are **dummy testing credentials**
- Not real trading accounts
- Safe to commit to Git
- Safe to share publicly

### ⚠️ **For Production:**
- Use real credentials in `.env` file
- Keep `.env` in `.gitignore` (already configured)
- Never commit real credentials to Git

### 🔒 **Security:**
- The `.env` file is ignored by Git
- Only `.env.example` is tracked
- Hardcoded values are dummy/testing only

---

## 🎯 Benefits

✅ **Instant Testing** - No setup required  
✅ **Zero Configuration** - Works immediately  
✅ **Flexible** - Easy to override when needed  
✅ **Secure** - Real credentials stay in `.env`  
✅ **Beginner-Friendly** - Just download and run  

---

## 🆘 Troubleshooting

### **Issue: "Invalid credentials"**

**Solution:**
1. Check if MT5 is installed at `C:\Program Files\MetaTrader 5\`
2. Ensure you have MT5 Trial account access
3. Verify the server is accessible

### **Issue: "Connection timeout"**

**Solution:**
1. Check internet connection
2. Verify firewall isn't blocking MT5
3. Try increasing timeout in config

### **Issue: "Server not found"**

**Solution:**
1. Check server name is correct: `ExnessKE-MT5Trial9`
2. Ensure you're using an Exness trial account
3. Contact broker for correct server name

---

## 📞 Need Help?

- Check `SETUP_GUIDE.md` for detailed setup
- Review `ARCHITECTURE_REVIEW.md` for technical details
- Open an issue on GitHub

---

**Last Updated:** 2025-10-20  
**Status:** ✅ Ready for Immediate Testing
