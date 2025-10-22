# 🚀 Anaconda Quick Start Guide

Get your MT5 Sentiment Analysis Bot running with Anaconda in 3 easy steps!

## ⚡ Fast Track Installation

### Step 1: Install Anaconda/Miniconda

**Choose One:**

**Option A: Anaconda (Recommended for beginners)**
- Download: https://www.anaconda.com/download
- Full package with GUI
- Size: ~3GB
- Includes 250+ packages

**Option B: Miniconda (Recommended for advanced users)**
- Download: https://docs.conda.io/en/latest/miniconda.html
- Minimal install
- Size: ~400MB
- Faster, installs only what you need

### Step 2: Run the Launcher

#### Windows Users:
```batch
# Open Anaconda Prompt (or regular cmd)
# Navigate to project folder
cd C:\path\to\mt5-sentiment-bot

# Run launcher
start_bot.bat
```

#### Linux/Mac Users:
```bash
# Open terminal
# Navigate to project folder
cd /path/to/mt5-sentiment-bot

# Run launcher
./start_bot.sh
```

### Step 3: Wait for Setup (First Time Only)

**First run takes 5-15 minutes:**
- ✅ Creates conda environment
- ✅ Installs all packages (including TA-Lib automatically!)
- ✅ Sets up database
- ✅ Launches dashboard

**Subsequent runs: Instant!**

## 📋 What Happens Automatically

✅ Checks if Anaconda/Miniconda is installed  
✅ Creates isolated conda environment (`mt5-sentiment-bot`)  
✅ Installs **TA-Lib automatically** (no manual download!)  
✅ Installs all ML libraries (TensorFlow, XGBoost, etc.)  
✅ Installs Streamlit and dependencies  
✅ Creates data directories  
✅ Initializes SQLite database  
✅ Launches web dashboard at http://localhost:8501  

## 🎯 Why Anaconda?

### Before (Standard Python):
❌ Manual TA-Lib installation (complicated on Windows)  
❌ Dependency conflicts  
❌ Manual wheel downloads  
❌ Compilation errors on Linux  

### Now (Anaconda):
✅ **TA-Lib installs automatically** - no manual steps!  
✅ **No dependency conflicts** - conda resolves automatically  
✅ **Optimized performance** - Intel MKL for faster ML  
✅ **Cross-platform** - works same on Windows/Linux/Mac  
✅ **Reproducible** - exact same environment anywhere  

## ⚙️ First-Time Setup Details

### What You Need:
1. **Anaconda/Miniconda installed**
2. **Internet connection** (for package downloads)
3. **~2GB disk space** (for environment)
4. **5-15 minutes** (first-time setup)

### The Script Does Everything:

1. **Checks conda installation**
   - If missing: Shows download links
   
2. **Creates environment**
   - From `environment.yml` file
   - Includes all dependencies
   
3. **Installs packages**
   - TA-Lib from conda-forge (automatic!)
   - All ML libraries
   - Streamlit framework
   - MetaTrader5 API
   
4. **Verifies installation**
   - Tests TA-Lib import
   - Checks Streamlit
   
5. **Starts the bot**
   - Dashboard at http://localhost:8501

## 🔧 After Installation

### Configure MT5:
1. Dashboard opens automatically
2. Go to **Settings** tab
3. Click **MT5 Connection**
4. Enter your credentials:
   - MT5 Login
   - MT5 Password
   - MT5 Server
5. Click **Connect**

### Run Analysis:
1. Select **Symbol** (e.g., EURUSD)
2. Choose **Timeframe** (e.g., H1)
3. Click **Analyze**
4. View real-time sentiment!

## 🐛 Troubleshooting

### "conda: command not found"

**Solution:**
```bash
# 1. Install Anaconda/Miniconda (see Step 1 above)
# 2. Restart terminal
# 3. If still not found:

# On Windows: Use "Anaconda Prompt" instead of cmd
# On Linux/Mac: Run this then restart terminal:
conda init bash  # or: conda init zsh for Mac
```

### "Failed to create environment"

**Solution:**
```bash
# Update conda first
conda update conda

# Clean cache
conda clean --all

# Try again
./start_bot.sh  # or start_bot.bat on Windows
```

### "TA-Lib import error"

**Solution:**
```bash
# Activate environment
conda activate mt5-sentiment-bot

# Install TA-Lib manually
conda install -c conda-forge ta-lib -y

# Verify
python -c "import talib; print('TA-Lib OK')"
```

### "Environment activation failed"

**Solution:**
```bash
# Initialize conda for your shell
conda init bash  # Linux
conda init zsh   # Mac
conda init cmd.exe  # Windows

# Restart terminal and try again
```

### Still Having Issues?

1. **Check conda version**: `conda --version`
2. **List environments**: `conda env list`
3. **Check logs**: Look in `logs/` folder
4. **See detailed docs**: `ANACONDA_MIGRATION_COMPLETE.md`

## 💡 Useful Commands

```bash
# Check conda is working
conda --version

# List environments
conda env list

# Activate environment manually
conda activate mt5-sentiment-bot

# Deactivate when done
conda deactivate

# Update all packages
conda env update -f environment.yml

# Start fresh (remove and recreate)
conda env remove -n mt5-sentiment-bot
./start_bot.sh  # Creates new environment
```

## 🎊 You're Ready!

Your professional MT5 trading bot is ready with Anaconda!

**To start trading analysis:**
1. Run `start_bot.bat` (Windows) or `./start_bot.sh` (Linux/Mac)
2. Wait for dashboard to open
3. Configure MT5 connection
4. Start analyzing!

## 🌟 Anaconda Benefits

✅ **No more TA-Lib headaches** - Installs automatically!  
✅ **Better performance** - Optimized libraries  
✅ **Fewer conflicts** - Smart dependency resolution  
✅ **Professional** - Industry standard for data science  
✅ **Reproducible** - Same environment everywhere  
✅ **Easy sharing** - Just share environment.yml  

---

**Pro Tips:**
- Use **Anaconda Prompt** on Windows for best results
- Keep conda updated: `conda update conda`
- Clean cache occasionally: `conda clean --all`
- Enable **Multi-Timeframe Analysis** for better signals
- Generate **PDF reports** from dashboard

---

**Built with Anaconda - The Data Science Standard** 🐍📊

*Happy Trading!* 📈
