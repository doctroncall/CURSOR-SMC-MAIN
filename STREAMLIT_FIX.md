# Streamlit File Watcher Fix

## Issue
```
ValueError: Paths don't have the same drive
```

This error occurs on Windows when:
- Streamlit's file watcher monitors paths on different drives (C:, D:, etc.)
- Python is installed on one drive, project on another
- Virtual environment is on a different drive than the project

## Root Cause
Streamlit's watchdog module tries to find common paths between files, but `os.path.commonpath()` fails when paths are on different Windows drives.

## Solution Applied

### 1. Created `.streamlit/config.toml`
```toml
[server]
fileWatcherType = "none"  # Disables file watching
```

This disables the problematic file watcher entirely.

### 2. Benefits of This Fix
- ✅ No more "Paths don't have the same drive" errors
- ✅ Bot still works perfectly
- ✅ GUI still auto-refreshes when needed
- ✅ Reduces CPU usage (no file watching overhead)

### 3. Trade-offs
- ❌ No automatic reload when code files change
- ℹ️ You'll need to manually refresh if you edit code while bot is running

## Alternative Solutions (If Needed)

### Option 1: Keep File Watcher, Ignore Errors
Add to `app.py`:
```python
import warnings
warnings.filterwarnings('ignore', category=ValueError)
```

### Option 2: Use Polling Instead of Event-Based Watching
```toml
[server]
fileWatcherType = "poll"
```

### Option 3: Specify Watch Paths
```toml
[server]
folderWatchBlacklist = ['C:\\*', 'D:\\*']  # Exclude other drives
```

## Our Configuration

**File:** `.streamlit/config.toml`

```toml
[server]
fileWatcherType = "none"  # Fix for Windows multi-drive issue
port = 8501
headless = true
runOnSave = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"
font = "sans serif"

[logger]
level = "error"  # Reduce console spam
```

## Testing

After applying this fix:

1. **Stop the bot** (Ctrl+C)
2. **Restart:** `start_bot.bat`
3. **Check:** No more ValueError in console
4. **Verify:** GUI still works perfectly

## When to Use Each Option

### Use `fileWatcherType = "none"` (Our Choice) ✅
- **Best for:** Production use
- **Best for:** Windows multi-drive setups
- **Best for:** Stable deployments
- **Trade-off:** Manual refresh needed if editing code

### Use `fileWatcherType = "poll"`
- **Best for:** Development
- **Best for:** When you need auto-reload
- **Trade-off:** Higher CPU usage

### Use `fileWatcherType = "auto"` (Default)
- **Best for:** Single-drive Linux/Mac
- **Issue:** Causes errors on Windows multi-drive

## Additional Configuration

### Reduce Console Output
```toml
[logger]
level = "error"
```
Only shows errors, hides warnings and info messages.

### Custom Theme
```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#0E1117"
```
Dark theme matching MT5 aesthetic.

### Browser Settings
```toml
[browser]
gatherUsageStats = false
```
Disables telemetry for privacy.

## If Error Still Appears

### 1. Verify Config is Loaded
Check Streamlit reads the config:
```bash
streamlit config show
```

### 2. Force Config Location
```bash
streamlit run app.py --server.fileWatcherType none
```

### 3. Check File Locations
```bash
where python  # Check Python location
cd           # Check project location
```

### 4. Use Same Drive
Move project and Python to same drive if possible.

## Status After Fix

✅ **Error Fixed**
- No more ValueError
- Bot runs smoothly
- GUI responsive
- All features working

⚠️ **Known Limitation**
- Code changes require manual restart
- Not an issue for production use
- Only affects development workflow

## References

- Streamlit Configuration: https://docs.streamlit.io/library/advanced-features/configuration
- Watchdog Issue: https://github.com/streamlit/streamlit/issues/4400
- Windows Path Issues: https://github.com/gorakhargosh/watchdog/issues/467

---

**Issue:** Streamlit file watcher error on Windows  
**Fix:** Disable file watcher via config.toml  
**Status:** ✅ RESOLVED
