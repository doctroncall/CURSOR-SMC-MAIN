# 📋 GUI Live Logging System - User Guide

## Overview

The MT5 Sentiment Bot now features a **comprehensive real-time logging and debug system** built directly into the GUI. You can see exactly what's happening at every step!

---

## 🎯 New Tab: "Logs & Debug"

### **Location:**
Click the **"📋 Logs & Debug"** tab (7th tab in the dashboard)

### **4 Sub-Tabs:**

---

## 1. 📋 **Live Logs**

### **What it shows:**
- Real-time log entries from `logs/mt5_bot.log`
- Color-coded by severity level
- Formatted with timestamps and emoji indicators

### **Features:**

#### **Filter Controls:**
```
Filter Level: [ALL, DEBUG, INFO, WARNING, ERROR, CRITICAL]
Show Lines: [25, 50, 100, 200, 500]
Auto-scroll to bottom: ☑
🔄 Refresh button
```

#### **Log Stats:**
- **Total Lines:** Count of logs displayed
- **Errors/Critical:** Number of serious issues
- **Warnings:** Number of warnings

#### **Color Coding:**
| Level | Color | Emoji | Example |
|-------|-------|-------|---------|
| DEBUG | Gray | 🔍 | `🔍 DEBUG Not connected, attempting...` |
| INFO | Blue | ℹ️ | `ℹ️ INFO MT5 connected successfully` |
| WARNING | Yellow | ⚠️ | `⚠️ WARNING Low data freshness` |
| ERROR | Red | ❌ | `❌ ERROR Failed to fetch data` |
| CRITICAL | Dark Red | 🔥 | `🔥 CRITICAL Connection failed` |

### **Example Display:**
```
2025-10-21 02:48:35 ℹ️ INFO Initializing bot components
2025-10-21 02:48:36 ℹ️ INFO Components initialized successfully
2025-10-21 02:48:37 🔍 DEBUG Attempting MT5 connection...
2025-10-21 02:48:38 ✅ INFO MT5 connected - Account 211744072
2025-10-21 02:48:39 📊 INFO Fetching data for EURUSD
2025-10-21 02:48:40 ⚠️ WARNING High CPU usage: 85.2%
```

---

## 2. 🔧 **Module Status**

### **What it shows:**
Real-time status of all 7 core modules

### **Modules Tracked:**

| Module | What It Does |
|--------|--------------|
| **MT5 Connection** | Connection to MetaTrader 5 |
| **Data Fetcher** | Fetching OHLCV data |
| **Indicators** | Calculating technical indicators |
| **SMC Analyzer** | Smart Money Concepts analysis |
| **Sentiment Engine** | Sentiment calculation |
| **Database** | Data persistence |
| **Health Monitor** | System health checks |

### **Status Indicators:**

| Symbol | Status | Meaning |
|--------|--------|---------|
| ⚪ | Idle | Not active yet |
| 🔵 | Running | Currently executing |
| 🟢 | Success | Completed successfully |
| 🟡 | Warning | Completed with warnings |
| 🔴 | Error | Failed with error |

### **Example Display:**
```
🟢 MT5 Connection
Status: success
Last Action: Connected successfully
Time: 14:32:15

🔵 Data Fetcher
Status: running
Last Action: Fetching data for EURUSD...
Time: 14:32:18

🟢 Sentiment Engine
Status: success
Last Action: Analysis complete: BULLISH
Time: 14:32:25
```

### **How to Use:**
1. Run an analysis
2. Watch module status change in real-time
3. Click **"🔄 Refresh Module Status"** for updates
4. Identify which module is stuck or failing

---

## 3. 📡 **Activity Feed**

### **What it shows:**
A timeline of recent bot actions (last 20 activities)

### **Activity Types:**

| Icon | Type | Examples |
|------|------|----------|
| 🔍 | Analysis | "Analysis started" |
| ✅ | Success | "Connected to MT5 - Account 211744072" |
| 📊 | Data | "Fetched 1000 bars across 4 timeframe(s)" |
| 🎯 | Result | "Sentiment: BULLISH (78% confidence)" |
| ❌ | Error | "Data fetch failed" |
| ⚠️ | Warning | "Low data quality detected" |

### **Color Coding:**
- **Blue (Info):** General information
- **Green (Success):** Successful operations
- **Yellow (Warning):** Warnings
- **Red (Error):** Errors

### **Example Feed:**
```
14:32:15 🔍 Analysis started
14:32:16 ✅ Connected to MT5 - Account 211744072
14:32:18 📊 Fetched 1000 bars across 1 timeframe(s)
14:32:25 🎯 Sentiment: BULLISH (78.5% confidence)
14:32:26 ℹ️ Analysis complete
```

### **Controls:**
- **🔄 Refresh Activity:** Update the feed
- **🗑️ Clear Activity:** Clear all entries

---

## 4. 🐛 **Debug Console**

### **What it shows:**
Detailed execution log with timestamps

### **Features:**

#### **Verbose Mode:**
- ☑ **Verbose Mode** - Shows detailed debug information
- Includes step-by-step execution flow
- Shows internal module operations

#### **Console Output:**
```
[2025-10-21 14:32:15.234] [INFO] === Starting Analysis ===
[2025-10-21 14:32:15.456] [INFO] Attempting MT5 connection...
[2025-10-21 14:32:16.123] [DEBUG] Not connected, attempting to connect...
[2025-10-21 14:32:16.789] [INFO] MT5 connected successfully - Account: 211744072
[2025-10-21 14:32:17.012] [INFO] Fetching data for EURUSD
[2025-10-21 14:32:17.234] [DEBUG] Single timeframe: H1
[2025-10-21 14:32:18.567] [INFO] Data fetched successfully: 1000 total bars
[2025-10-21 14:32:18.890] [INFO] Starting sentiment analysis for H1...
[2025-10-21 14:32:19.123] [DEBUG] Running technical indicators on 1000 bars...
[2025-10-21 14:32:25.456] [INFO] Analysis complete: BULLISH with 78.5% confidence
[2025-10-21 14:32:25.678] [INFO] === Analysis Complete ===
```

#### **Test Buttons:**
- **📝 Add Test Log** - Add test INFO message
- **⚠️ Add Test Warning** - Add test WARNING message

#### **Clear Console:**
- **🗑️ Clear Console** - Remove all console entries

---

## 📊 How It All Works Together

### **Scenario: Running an Analysis**

#### **Step 1: Click "Analyze"**

**Module Status shows:**
```
🔵 MT5 Connection - Running: Connecting to MT5...
```

**Activity Feed shows:**
```
14:32:15 🔍 Analysis started
```

**Debug Console shows:**
```
[2025-10-21 14:32:15.234] [INFO] === Starting Analysis ===
[2025-10-21 14:32:15.456] [INFO] Attempting MT5 connection...
```

**Live Logs shows:**
```
2025-10-21 14:32:15 ℹ️ INFO Starting analysis...
2025-10-21 14:32:15 🔍 DEBUG Attempting MT5 connection...
```

---

#### **Step 2: Connection Established**

**Module Status updates:**
```
🟢 MT5 Connection - Success: Connected successfully
🔵 Data Fetcher - Running: Fetching data for EURUSD...
```

**Activity Feed adds:**
```
14:32:16 ✅ Connected to MT5 - Account 211744072
```

**Debug Console adds:**
```
[2025-10-21 14:32:16.789] [INFO] MT5 connected successfully - Account: 211744072
[2025-10-21 14:32:17.012] [INFO] Fetching data for EURUSD
```

---

#### **Step 3: Data Fetched**

**Module Status updates:**
```
🟢 Data Fetcher - Success: Fetched 1000 bars
🔵 Sentiment Engine - Running: Analyzing H1...
```

**Activity Feed adds:**
```
14:32:18 📊 Fetched 1000 bars across 1 timeframe(s)
```

---

#### **Step 4: Analysis Complete**

**Module Status updates:**
```
🟢 Sentiment Engine - Success: Analysis complete: BULLISH
```

**Activity Feed adds:**
```
14:32:25 🎯 Sentiment: BULLISH (78.5% confidence)
```

**Debug Console shows:**
```
[2025-10-21 14:32:25.456] [INFO] Analysis complete: BULLISH with 78.5% confidence
[2025-10-21 14:32:25.678] [INFO] === Analysis Complete ===
```

---

## 🔍 Troubleshooting with Logs

### **Issue: Analysis Fails**

#### **Check Module Status:**
```
🔴 MT5 Connection - Error: Failed to connect
❌ Last Action: Error: Code 10004
```
**Diagnosis:** MT5 connection problem

#### **Check Activity Feed:**
```
14:32:15 🔍 Analysis started
14:32:16 ❌ MT5 connection failed: Code 10004
```
**Diagnosis:** Connection error code 10004

#### **Check Debug Console:**
```
[2025-10-21 14:32:16.123] [ERROR] MT5 initialization failed: Code 10004
[2025-10-21 14:32:16.234] [ERROR] Failed to connect after 3 attempts
```
**Diagnosis:** Detailed error with attempt count

#### **Check Live Logs:**
```
2025-10-21 14:32:16 ❌ ERROR MT5 initialization failed: Code 10004
2025-10-21 14:32:16 🔥 CRITICAL Connection failed after 3 attempts
```
**Diagnosis:** Critical failure, see TROUBLESHOOTING.md

---

## 💡 Best Practices

### **1. Monitor During First Run**
- Keep **"Logs & Debug"** tab open
- Watch **Module Status** for stuck modules
- Check **Activity Feed** for progress

### **2. Use Filters Effectively**
- Set **Live Logs** to `ERROR` when troubleshooting
- Use `DEBUG` for detailed analysis
- Use `ALL` for complete picture

### **3. Check Activity Feed First**
- Quickest way to see what happened
- Shows high-level flow
- Easy to spot failures

### **4. Use Debug Console for Details**
- Enable **Verbose Mode** for troubleshooting
- Shows exact execution flow
- Includes timestamps for timing issues

### **5. Module Status for Quick Health Check**
- See all modules at a glance
- Identify which module is stuck
- Check timestamps for hung processes

---

## 🎨 UI Screenshots

### **Module Status:**
```
┌─────────────────────────────────────┐
│ 🟢 MT5 Connection                   │
│ Status: success                     │
│ Last Action: Connected successfully │
│ Time: 14:32:16                      │
├─────────────────────────────────────┤
│ 🔵 Data Fetcher                     │
│ Status: running                     │
│ Last Action: Fetching EURUSD...     │
│ Time: 14:32:18                      │
└─────────────────────────────────────┘
```

### **Activity Feed:**
```
┌─────────────────────────────────────┐
│ 14:32:15 🔍 Analysis started        │
├─────────────────────────────────────┤
│ 14:32:16 ✅ Connected to MT5        │
├─────────────────────────────────────┤
│ 14:32:18 📊 Fetched 1000 bars       │
├─────────────────────────────────────┤
│ 14:32:25 🎯 BULLISH (78% conf)      │
└─────────────────────────────────────┘
```

---

## ⚙️ Configuration

### **Auto-Refresh:**
- **Live Logs:** Optional auto-refresh every 5 seconds
- **Module Status:** Manual refresh button
- **Activity Feed:** Real-time updates during operations

### **Line Limits:**
- **Live Logs:** 25-500 lines
- **Activity Feed:** Last 20 activities
- **Debug Console:** Last 500 lines

### **Storage:**
- All data stored in Streamlit session state
- Cleared on app restart
- No persistent storage

---

## 🚀 Quick Start Guide

### **1. Start the Bot:**
```bash
start_bot.bat  # Windows
./start_bot.sh  # Linux/Mac
```

### **2. Open Logs Tab:**
- Click **"📋 Logs & Debug"** tab

### **3. Run Analysis:**
- Go to **"Analysis"** tab
- Click **"🔄 Analyze"**
- Return to **"Logs & Debug"**

### **4. Watch in Real-Time:**
- **Module Status:** See progress
- **Activity Feed:** See actions
- **Debug Console:** See details
- **Live Logs:** See full logs

---

## 📞 Support

If logs show issues:
1. Check **Module Status** for failed modules
2. Look at **Activity Feed** for error messages
3. Review **Debug Console** for detailed errors
4. Search **Live Logs** for ERROR/CRITICAL
5. See `TROUBLESHOOTING.md` for solutions

---

**Last Updated:** 2025-10-21  
**Version:** 2.0.0  
**Status:** ✅ Production Ready with Full Logging
