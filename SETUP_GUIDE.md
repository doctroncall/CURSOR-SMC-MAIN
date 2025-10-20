# 🚀 MT5 Sentiment Analysis Bot - Setup Guide

Complete installation and configuration guide for the MT5 Sentiment Analysis Bot.

## 📋 Prerequisites

### System Requirements
- **Python**: 3.10 or higher
- **OS**: Windows, Linux, or macOS
- **RAM**: 4GB minimum (8GB recommended)
- **Disk**: 2GB free space
- **MT5**: MetaTrader 5 installed (Windows) or MT5 account access

### Required Software
1. **Python 3.10+** - [Download](https://www.python.org/downloads/)
2. **MetaTrader 5** - [Download](https://www.metatrader5.com/en/download)
3. **Git** - [Download](https://git-scm.com/downloads)

## 🔧 Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/doctroncall/CURSOR-SMC-MAIN.git
cd CURSOR-SMC-MAIN
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

### 3. Install TA-Lib (Required!)

TA-Lib must be installed BEFORE running `pip install -r requirements.txt`.

#### Windows:
1. Download TA-Lib wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
2. Choose the correct version for your Python (e.g., `TA_Lib-0.4.28-cp310-cp310-win_amd64.whl` for Python 3.10)
3. Install:
```bash
pip install path/to/TA_Lib-0.4.XX-cpXX-cpXX-win_amd64.whl
```

#### Linux (Ubuntu/Debian):
```bash
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure --prefix=/usr
make
sudo make install
cd ..
pip install TA-Lib
```

#### macOS:
```bash
brew install ta-lib
pip install TA-Lib
```

### 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
nano .env  # or use your preferred editor
```

**Required Configuration:**

```env
# MT5 Connection (REQUIRED)
MT5_LOGIN=your_account_number
MT5_PASSWORD=your_password
MT5_SERVER=your_broker_server  # e.g., ICMarkets-Demo

# Application Settings
APP_ENV=production
APP_DEBUG=False
LOG_LEVEL=INFO

# Analysis Settings
DEFAULT_SYMBOL=EURUSD
DEFAULT_TIMEFRAMES=M15,H1,H4,D1
UPDATE_FREQUENCY_MINUTES=5

# ML Model Settings
MODEL_VERSION=v1.0.0
AUTO_RETRAIN=True
MIN_CONFIDENCE_THRESHOLD=0.70
```

### 6. Initialize Database

```bash
python -c "from src.database.models import init_database; init_database()"
```

### 7. Test MT5 Connection

```bash
python -c "from src.mt5.connection import MT5Connection; conn = MT5Connection(); conn.connect(); print('✓ Connected!' if conn.is_connected() else '✗ Failed')"
```

## ▶️ Running the Application

### Start the Dashboard

```bash
streamlit run app.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

### First Time Setup

1. **Configure MT5 Connection**:
   - Go to Settings tab → MT5
   - Verify credentials
   - Test connection

2. **Select Symbol and Timeframe**:
   - Use sidebar to select EURUSD (or your preferred symbol)
   - Choose H1 timeframe for primary analysis
   - Enable Multi-Timeframe Analysis for best results

3. **Run First Analysis**:
   - Click "Analyze" button
   - Wait for data fetch and analysis
   - View results in Analysis tab

## 🎯 Usage Guide

### Dashboard Tabs

1. **Analysis** - View sentiment analysis results
2. **Indicators** - Technical indicator details
3. **SMC** - Smart Money Concepts analysis
4. **Health** - System health monitoring
5. **Settings** - Configuration and preferences

### Key Features

- **Real-time Analysis**: Click "Analyze" to get current sentiment
- **Multi-Timeframe**: Enable for confluence analysis across timeframes
- **Auto-Refresh**: Enable for automatic updates
- **Health Monitoring**: Regular system checks
- **Report Generation**: Download PDF reports
- **Alert System**: Configure notifications

## 🔍 Troubleshooting

### Common Issues

#### 1. MT5 Connection Failed
```
Error: MT5 connection failed
```
**Solution:**
- Verify MT5 is running
- Check credentials in .env file
- Ensure server name is correct
- Try `MT5_PATH` if terminal not found

#### 2. TA-Lib Import Error
```
ImportError: DLL load failed while importing _ta_lib
```
**Solution:**
- Reinstall TA-Lib following instructions above
- Ensure correct version for your Python

#### 3. Database Error
```
Error: database is locked
```
**Solution:**
- Close other connections to database
- Restart application
- Check file permissions

#### 4. Missing Dependencies
```
ModuleNotFoundError: No module named 'xxx'
```
**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### Enable Debug Mode

For more detailed error messages:

```env
# In .env file
APP_DEBUG=True
LOG_LEVEL=DEBUG
```

Check logs in `logs/` directory:
- `app.log` - General application logs
- `mt5_connection.log` - MT5 connection logs
- `analysis.log` - Analysis logs
- `errors.log` - Error logs

## 📊 Performance Optimization

### For Better Performance:

1. **Reduce Update Frequency**:
```env
UPDATE_FREQUENCY_MINUTES=15  # Instead of 5
```

2. **Limit Timeframes**:
```env
DEFAULT_TIMEFRAMES=H1,H4  # Instead of M15,H1,H4,D1
```

3. **Adjust Lookback**:
```env
LOOKBACK_BARS=500  # Instead of 1000
```

## 🔐 Security Best Practices

1. **Never commit .env file**:
```bash
# Already in .gitignore
```

2. **Use strong passwords**:
```env
MT5_PASSWORD=strong_secure_password
SECRET_KEY=generate_random_32_char_string
```

3. **Rotate credentials regularly**:
```env
API_KEY_ROTATION_DAYS=90
```

4. **Limit access**:
- Don't expose application to internet
- Use firewall rules
- Run as non-root user

## 📈 Next Steps

After successful setup:

1. **Run Initial Analysis** - Test all functionality
2. **Configure Alerts** - Set up notifications
3. **Generate Report** - Create your first PDF report
4. **Review Logs** - Check for any warnings
5. **Train ML Model** - Let it learn from data (optional)

## 🆘 Getting Help

- **Documentation**: Check README.md
- **Logs**: Review logs/ directory
- **Issues**: Check GitHub issues
- **Testing**: Run diagnostic tests

### Run Diagnostics

```bash
python -c "from src.health.diagnostics import SystemDiagnostics; diag = SystemDiagnostics(); results = diag.run_all_diagnostics(); print(results)"
```

## 🎓 Learning Resources

- **MT5 API**: https://www.mql5.com/en/docs/integration/python_metatrader5
- **Technical Analysis**: Indicator configurations in `config/indicators_config.yaml`
- **SMC Concepts**: SMC parameters in `config/smc_config.yaml`
- **Streamlit**: https://docs.streamlit.io/

## ✅ Verification Checklist

- [ ] Python 3.10+ installed
- [ ] Virtual environment created
- [ ] TA-Lib installed
- [ ] Dependencies installed
- [ ] .env configured
- [ ] MT5 connection successful
- [ ] Database initialized
- [ ] Application starts
- [ ] Dashboard loads
- [ ] First analysis completes

---

**You're all set! 🎉**

Run `streamlit run app.py` and start trading with confidence!
