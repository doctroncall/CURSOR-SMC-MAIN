# 🐍 MT5 Sentiment Analysis Bot - Anaconda Edition

## ⚡ Ultra-Quick Start

```bash
# 1. Install Anaconda/Miniconda
# 2. Run this:

# Windows:
start_bot.bat

# Linux/Mac:
./start_bot.sh

# 3. Wait 5-15 minutes (first time only)
# 4. Dashboard opens automatically!
```

**That's it!** Everything else is automatic.

---

## 🎯 What Makes This Special

### The TA-Lib Revolution

**Old Way (Standard Python):**
```
Download wheel → Match version → Install → Debug → Fail → Repeat
⏱️ 15-30 minutes of frustration
```

**New Way (Anaconda):**
```
Run start_bot.bat → Wait → Done ✓
⏱️ Automatic installation
```

---

## 🚀 Features

### Technical Analysis
- **15+ Indicators:** RSI, MACD, Bollinger Bands, ADX, Stochastic, etc.
- **TA-Lib Powered:** Professional-grade calculations
- **Multi-Timeframe:** M15, H1, H4, D1 analysis

### Smart Money Concepts
- Order Blocks (Bullish/Bearish/Breaker)
- Fair Value Gaps (FVG)
- Liquidity Pools & Stop Hunts
- Supply & Demand Zones
- Market Structure (BOS, ChOCh)

### Machine Learning
- **4-Model Ensemble:** XGBoost, LightGBM, CatBoost, TensorFlow
- **70+ Features:** Comprehensive market analysis
- **Auto-Retraining:** Daily model updates
- **Calibrated Confidence:** Reliable probability scores

### Market Regime Detection
- Trend identification (uptrend/downtrend/sideways)
- Volatility analysis
- Volume patterns
- Adaptive strategies

### Professional Dashboard
- Real-time Streamlit web interface
- Interactive charts (Plotly)
- Health monitoring
- PDF report generation
- Comprehensive logging

---

## 📦 What's Included

### Conda Environment: `mt5-sentiment-bot`

**Python:** 3.11 (optimized and stable)

**Core (60+ packages):**
```yaml
Technical Analysis:
  ✓ ta-lib (conda-forge - auto-installed!)
  ✓ pandas-ta

Data Science:
  ✓ pandas (Intel MKL optimized)
  ✓ numpy (Intel MKL optimized)
  ✓ scikit-learn

Machine Learning:
  ✓ xgboost
  ✓ lightgbm
  ✓ catboost
  ✓ tensorflow
  ✓ optuna (hyperparameter tuning)
  ✓ shap (model interpretability)
  ✓ imbalanced-learn (SMOTE)

Visualization:
  ✓ streamlit
  ✓ plotly
  ✓ matplotlib
  ✓ seaborn

Database:
  ✓ sqlalchemy
  ✓ alembic

Trading:
  ✓ MetaTrader5 API

And 40+ more...
```

---

## 🎓 Installation

### Prerequisites

**Install Anaconda or Miniconda:**

**Anaconda (Full - Best for Beginners):**
- Download: https://www.anaconda.com/download
- Size: ~3GB
- Includes: GUI + 250+ packages

**Miniconda (Minimal - Best for Advanced):**
- Download: https://docs.conda.io/en/latest/miniconda.html
- Size: ~400MB
- Includes: Just conda + Python

### Setup

**Step 1: Clone/Download Project**
```bash
git clone <your-repo-url>
cd mt5-sentiment-bot
```

**Step 2: Run Launcher**

**Windows:**
```batch
# Open Anaconda Prompt (or cmd if conda is in PATH)
start_bot.bat
```

**Linux/Mac:**
```bash
./start_bot.sh
```

**Step 3: Wait (First Time Only)**

The script automatically:
- ✅ Creates conda environment
- ✅ Installs all 60+ packages
- ✅ Installs TA-Lib (from conda-forge)
- ✅ Sets up database
- ✅ Launches dashboard

**First run:** 5-15 minutes  
**Every run after:** Instant!

**Step 4: Configure MT5**

1. Dashboard opens at http://localhost:8501
2. Go to Settings → MT5 Connection
3. Enter credentials
4. Click Connect

**Step 5: Start Analyzing!**

---

## 📊 Usage

### Basic Analysis

1. **Select Symbol:** EURUSD, GBPUSD, XAUUSD, etc.
2. **Choose Timeframe:** M15, H1, H4, D1
3. **Click "Analyze"**
4. **View Results:**
   - Sentiment (BULLISH/BEARISH/NEUTRAL)
   - Confidence score
   - Contributing factors
   - SMC analysis
   - ML predictions

### Advanced Features

**Multi-Timeframe Analysis:**
- Enable in sidebar
- Select multiple timeframes
- Get timeframe alignment score
- Confluence-based signals

**Market Regime Detection:**
- Automatic trend identification
- Volatility classification
- Volume analysis
- Adaptive recommendations

**ML Model Training:**
- Train custom models
- Hyperparameter tuning
- Feature importance
- Performance metrics

**PDF Reports:**
- Daily summaries
- Performance analytics
- Trade suggestions
- Historical data

---

## 🔧 Commands

### Daily Use

```bash
# Start bot
start_bot.bat  # Windows
./start_bot.sh  # Linux/Mac
```

### Environment Management

```bash
# List environments
conda env list

# Activate manually
conda activate mt5-sentiment-bot

# Deactivate
conda deactivate

# Update packages
conda env update -f environment.yml

# Clean cache
conda clean --all

# Remove and recreate
conda env remove -n mt5-sentiment-bot
./start_bot.sh  # Recreates
```

### Package Management

```bash
# List installed
conda list

# Install package
conda install package-name

# Install from conda-forge
conda install -c conda-forge package-name

# Search packages
conda search package-name

# Update all
conda update --all
```

---

## 🐛 Troubleshooting

### "conda: command not found"

**Windows:**
- Use "Anaconda Prompt" from Start menu
- Or reinstall Anaconda with "Add to PATH"

**Linux/Mac:**
```bash
conda init bash  # or zsh
# Restart terminal
```

### "Failed to create environment"

```bash
conda update conda
conda clean --all
./start_bot.sh  # Try again
```

### "TA-Lib not found"

```bash
conda activate mt5-sentiment-bot
conda install -c conda-forge ta-lib -y
python -c "import talib; print('OK')"
```

### More Help

See `ANACONDA_SETUP_COMPLETE.md` for comprehensive troubleshooting.

---

## 📁 Project Structure

```
mt5-sentiment-bot/
├── environment.yml          # Conda environment spec
├── start_bot.bat           # Windows launcher
├── start_bot.sh            # Linux/Mac launcher
├── app.py                  # Main application
├── config/                 # Configuration
├── src/                    # Source code
│   ├── mt5/               # MT5 integration
│   ├── indicators/        # Technical indicators
│   ├── analysis/          # Sentiment engine
│   ├── ml/                # Machine learning
│   ├── health/            # Monitoring
│   ├── reporting/         # PDF generation
│   └── database/          # Data storage
├── gui/                   # UI components
├── data/                  # Bot data (auto-created)
├── logs/                  # Logs (auto-created)
├── models/                # ML models (auto-created)
└── reports/               # PDF reports (auto-created)
```

---

## 🌟 Why Anaconda?

### Performance

| Operation | Standard Python | Anaconda + MKL |
|-----------|----------------|----------------|
| NumPy matrix ops | 1x | 2-3x faster |
| ML training | 1x | 1.5-2x faster |
| TA-Lib calculations | 1x | Optimized |

### Stability

| Aspect | pip + venv | conda |
|--------|-----------|-------|
| TA-Lib install | Manual (hard) | Auto (easy) |
| Dependency conflicts | Common | Rare |
| Cross-platform | Medium | Excellent |
| Reproducibility | Good | Excellent |

---

## 📚 Documentation

- **START_HERE_ANACONDA.md** - Quick reference
- **ANACONDA_QUICK_START.md** - Detailed quick start  
- **ANACONDA_SETUP_COMPLETE.md** - Full documentation
- **MIGRATION_SUMMARY.md** - What changed
- **README.md** - This file

---

## 🎯 Configuration

### Environment Variables (.env)

```env
# MT5 Connection
MT5_LOGIN=your_account
MT5_PASSWORD=your_password
MT5_SERVER=your_server

# Analysis
DEFAULT_SYMBOL=EURUSD
DEFAULT_TIMEFRAMES=M15,H1,H4,D1

# ML Settings
AUTO_RETRAIN=True
MIN_CONFIDENCE=0.70
```

### Conda Environment (environment.yml)

```yaml
name: mt5-sentiment-bot
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - ta-lib>=0.4.28
  - streamlit>=1.28.0
  # ... 60+ more packages
```

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

---

## 📜 License

MIT License - See LICENSE file

---

## ⚠️ Disclaimer

**Educational purposes only.** Not financial advice. Trading carries risk. Past performance doesn't indicate future results.

---

## 🙏 Acknowledgments

- **Anaconda** - Data science platform
- **MetaTrader 5** - Trading platform API
- **TA-Lib** - Technical analysis library
- **Streamlit** - Web framework
- **SMC Community** - Trading methodology

---

## 📞 Support

**Issues?**
1. Check `logs/` folder
2. Run `conda list` to verify packages
3. See `ANACONDA_SETUP_COMPLETE.md`
4. Update: `conda env update -f environment.yml`

**Resources:**
- Conda Docs: https://docs.conda.io/
- TA-Lib: https://ta-lib.org/
- Streamlit: https://streamlit.io/

---

## 🎉 Success!

You now have a **professional trading bot** powered by:

✅ Anaconda (industry standard)  
✅ Automatic TA-Lib installation  
✅ 60+ optimized packages  
✅ Professional ML pipeline  
✅ Real-time analysis  
✅ Smart Money Concepts  

**Start trading smarter with data-driven insights!** 📊📈

---

**Built with Anaconda 🐍 - The Data Science Standard**

*Professional. Stable. Powerful.*

**Version:** 2.0 (Anaconda Edition)  
**Last Updated:** 2025-10-22
