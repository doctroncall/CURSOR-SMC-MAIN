# 🔧 Quick Fix Guide - MT5 Error -6 Resolved

## ⚡ TL;DR - What I Fixed

Your bot was disconnecting MT5 terminal because it called `mt5.initialize()` with login credentials. I fixed it to:
1. Check if MT5 is already connected first
2. Reuse existing connections instead of disrupting them
3. Initialize and login as separate steps (prevents disconnection)

## ✅ Test Right Now

```bash
python test_connection_fix.py
```

Should see: `✅ TEST PASSED - Connection fix working correctly!`

## 🎯 What Changed

| Issue | Fix |
|-------|-----|
| Error -6 Authorization Failed | ✅ Fixed - Smart connection check |
| MT5 terminal disconnects | ✅ Fixed - Reuses existing connection |
| Unstable connections | ✅ Fixed - Clean init process |

## 📁 Files Fixed

- `mt5_connector.py` - Main fix applied
- `src/mt5/connection.py` - Also fixed for consistency
- `test_connection_fix.py` - New test script

## 🚀 Ready to Use!

Your bot will now:
- ✅ Connect without disconnecting MT5 terminal
- ✅ Reuse existing connections when available
- ✅ No more Error -6
- ✅ Stable and reliable connections

---

For detailed technical explanation, see: `MT5_CONNECTION_FIX_SUMMARY.md`  
For complete guide, see: `FIX_APPLIED_README.md`
