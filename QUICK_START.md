# 🚀 Quick Start Guide

Get your MT5 Sentiment Analysis Bot running in 3 easy steps!

## ⚡ Fast Track Installation (Python-Based)

Your bot runs on **Python** for maximum stability and reliability!

### Windows Users:

1. **Download the project**
2. **Double-click `start_bot.bat`**
3. **Follow the prompts**

That's it! The enhanced Python script handles everything automatically.

### Linux/Mac Users:

1. **Download the project**
2. **Run in terminal:**
   ```bash
   ./start_bot.sh
   ```
3. **Follow the prompts**

The script automatically validates your Python version and sets up everything!

## 📋 What the Enhanced Python Launcher Does Automatically:

✅ Validates Python version (3.10+ required)  
✅ Checks Python installation path  
✅ Creates isolated virtual environment  
✅ Upgrades pip to latest version  
✅ Installs all dependencies with progress tracking  
✅ Creates required directories (data, logs, models, reports)  
✅ Initializes SQLite database  
✅ Starts the Streamlit dashboard  
✅ Provides detailed error messages if issues occur  

## ⚙️ First-Time Setup (One-Time Only):

### 1. Install TA-Lib (Required!)

**Windows:**
- Download from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
- Choose your Python version
- Install: `pip install TA_Lib-0.4.XX-cpXX-cpXX-win_amd64.whl`

**Mac:**
```bash
brew install ta-lib
```

**Linux:**
```bash
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure --prefix=/usr
make
sudo make install
```

### 2. Configure MT5 Credentials

When prompted, edit the `.env` file with your MT5 details:

```env
MT5_LOGIN=your_account_number
MT5_PASSWORD=your_password
MT5_SERVER=your_broker_server
```

Save and close the file.

### 3. Run the Bot

**Windows:** Double-click `start_bot.bat`  
**Linux/Mac:** Run `./start_bot.sh`

## 🎯 Using the Bot:

1. **Dashboard opens automatically** in your browser
2. **Select symbol** (e.g., EURUSD) from sidebar
3. **Choose timeframe** (e.g., H1)
4. **Click "Analyze"** button
5. **View results** in real-time!

## 🔧 Troubleshooting:

### "Python not found" or "Python version too old"
- Install Python 3.10+ from python.org (3.11 recommended)
- **Windows**: Make sure to check "Add Python to PATH" during installation
- **Linux**: `sudo apt-get install python3 python3-pip python3-venv`
- **macOS**: `brew install python3`
- Restart your terminal/command prompt after installation

### "TA-Lib import error"
- Follow TA-Lib installation instructions above
- **Windows**: Download the wheel file matching your Python version
- Restart the launcher script after installation

### "Failed to create virtual environment"
- **Linux**: Install venv: `sudo apt-get install python3-venv`
- Ensure you have write permissions in the project directory
- Check available disk space

### "MT5 connection failed"
- Check credentials in `.env` file
- Ensure MT5 terminal is running (Windows only)
- Verify server name is correct
- Go to Settings → MT5 Connection in the dashboard

### "Streamlit exited with error"
- Check the `logs/` folder for detailed error messages
- Ensure all dependencies installed correctly
- Try deleting `venv` folder and running the start script again

## 📚 Need More Help?

- **Detailed setup:** See `SETUP_GUIDE.md`
- **Troubleshooting:** Check the `logs/` folder
- **Configuration:** See `config/` folder

## 🎊 You're Ready!

Your professional MT5 trading bot is ready to use. Happy trading! 📈

---

**Pro Tips:**
- Enable "Multi-Timeframe Analysis" for better signals
- Check "Health" tab to monitor system status
- Generate PDF reports from the dashboard
- Configure alerts in Settings tab
