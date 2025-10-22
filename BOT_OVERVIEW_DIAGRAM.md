# 🎯 SMC Bot - Complete Architecture Overview

## 📋 Table of Contents
1. [System Architecture](#system-architecture)
2. [Component Hierarchy](#component-hierarchy)
3. [Data Flow](#data-flow)
4. [Launch Workflow](#launch-workflow)
5. [Technology Stack](#technology-stack)
6. [Directory Structure](#directory-structure)

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         SMC TRADING BOT                                 │
│                    (MT5 Sentiment Analysis Bot)                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
         ┌──────────▼──────────┐       ┌───────────▼──────────┐
         │  CONDA SMC.BAT      │       │   STREAMLIT GUI      │
         │  (Orchestrator)     │       │   (app.py)           │
         │                     │       │                      │
         │ • Checks Conda      │       │ • User Interface     │
         │ • Creates Env       │       │ • Dashboard          │
         │ • Installs Deps     │       │ • Real-time Updates  │
         │ • Launches Bot      │       │ • 9 Tabs             │
         └──────────┬──────────┘       └───────────┬──────────┘
                    │                              │
                    └──────────┬───────────────────┘
                               │
        ┌──────────────────────┴──────────────────────┐
        │                                             │
┌───────▼────────┐                          ┌────────▼─────────┐
│  CONDA ENV     │                          │   CORE MODULES   │
│  "smc bot"     │                          │                  │
│                │                          │  (Python 3.11)   │
│ • Python 3.11  │                          └────────┬─────────┘
│ • 60+ Packages │                                   │
│ • TA-Lib       │                 ┌─────────────────┴─────────────────┐
│ • ML Libraries │                 │                                   │
└────────────────┘          ┌──────▼──────┐                   ┌────────▼────────┐
                            │   MT5 Core  │                   │  Analysis Core  │
                            └──────┬──────┘                   └────────┬────────┘
                                   │                                   │
                    ┌──────────────┴──────────────┐       ┌────────────┴────────────┐
                    │                             │       │                         │
            ┌───────▼────────┐          ┌────────▼──────┐ │              ┌──────────▼─────────┐
            │  Connection    │          │ Data Fetcher  │ │              │  Sentiment Engine  │
            │  • Initialize  │          │ • OHLCV       │ │              │  • Technical       │
            │  • Validate    │          │ • Multi-TF    │ │              │  • SMC             │
            │  • Monitor     │          │ • Symbols     │ │              │  • ML Predictions  │
            └────────────────┘          └───────────────┘ │              └────────────────────┘
                                                           │
                                                  ┌────────▼──────────┐
                                                  │ Multi-Timeframe   │
                                                  │ • M15, H1, H4, D1 │
                                                  │ • Alignment Score │
                                                  │ • Dominant Signal │
                                                  └───────────────────┘
```

---

## 🧩 Component Hierarchy

```
app.py (Main Application)
│
├── 📊 GUI Components (gui/components/)
│   │
│   ├── connection_panel.py       → MT5 Connection Management
│   ├── sentiment_card.py          → Sentiment Display
│   ├── chart_panel.py             → Price Charts & Indicators
│   ├── health_dashboard.py        → System Health Monitor
│   ├── metrics_panel.py           → Performance Metrics
│   ├── ml_training_panel.py       → ML Model Training (NEW v2.0)
│   ├── regime_panel.py            → Market Regime Detection (NEW v2.0)
│   ├── settings_panel.py          → Configuration Settings
│   └── live_logs.py               → Real-time Logging
│
├── 🔧 Core Modules (src/)
│   │
│   ├── mt5/
│   │   ├── connection.py          → MT5 Connection Handler
│   │   ├── data_fetcher.py        → Market Data Retrieval
│   │   └── validator.py           → Data Validation
│   │
│   ├── analysis/
│   │   ├── sentiment_engine.py    → Main Analysis Engine
│   │   ├── multi_timeframe.py     → MTF Analysis
│   │   ├── regime_detector.py     → Market Regime (NEW v2.0)
│   │   └── confidence_scorer.py   → Confidence Calculation
│   │
│   ├── indicators/
│   │   ├── technical.py           → RSI, MACD, EMA, etc.
│   │   ├── smc.py                 → Smart Money Concepts
│   │   └── calculator.py          → Indicator Engine
│   │
│   ├── ml/
│   │   ├── training.py            → Model Training (NEW v2.0)
│   │   ├── model_manager.py       → Model Lifecycle
│   │   ├── feature_engineering.py → 70+ Features (NEW v2.0)
│   │   ├── evaluator.py           → Performance Evaluation
│   │   ├── calibrator.py          → Probability Calibration
│   │   └── hyperparameter_tuner.py→ Optuna Tuning (NEW v2.0)
│   │
│   ├── database/
│   │   ├── models.py              → SQLAlchemy Models
│   │   └── repository.py          → Data Access Layer
│   │
│   ├── health/
│   │   ├── monitor.py             → Health Monitoring
│   │   ├── diagnostics.py         → System Diagnostics
│   │   └── recovery.py            → Auto-Recovery
│   │
│   ├── reporting/
│   │   ├── pdf_generator.py       → PDF Reports
│   │   └── charts.py              → Chart Generation
│   │
│   └── utils/
│       └── logger.py              → Logging System
│
└── ⚙️ Configuration (config/)
    ├── settings.py                → App Configuration
    ├── indicators_config.yaml     → Indicator Settings
    └── smc_config.yaml            → SMC Parameters
```

---

## 🔄 Data Flow

```
┌─────────────┐
│   USER      │
│  (Browser)  │
└──────┬──────┘
       │ Clicks "Analyze"
       │
┌──────▼──────────────────────────────────────────────────────────┐
│                    STREAMLIT GUI (app.py)                       │
│                                                                  │
│  Tab 1: Analysis  │ Tab 2: Indicators │ Tab 3: Metrics │ ...   │
└──────┬──────────────────────────────────────────────────────────┘
       │
       │ 1. Check Connection
       ▼
┌─────────────────────┐
│  MT5 Connection     │ ◄─── Validates credentials
│  (connection.py)    │      Checks terminal status
└──────┬──────────────┘
       │ Connected ✓
       │
       │ 2. Fetch Data
       ▼
┌─────────────────────┐
│  MT5 Data Fetcher   │ ◄─── Retrieves OHLCV
│  (data_fetcher.py)  │      Multi-timeframe support
└──────┬──────────────┘      1000 bars per timeframe
       │
       │ OHLCV DataFrame(s)
       ▼
┌─────────────────────────────────────────────────────────────────┐
│              TECHNICAL INDICATOR CALCULATION                     │
│                   (indicators/calculator.py)                     │
│                                                                  │
│  RSI │ MACD │ EMA │ Bollinger │ ATR │ Stochastic │ Volume │... │
└──────┬──────────────────────────────────────────────────────────┘
       │
       │ Enriched DataFrame
       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SMC ANALYSIS                                  │
│                  (indicators/smc.py)                             │
│                                                                  │
│  Order Blocks │ Fair Value Gaps │ Liquidity Zones │ BOS │ CHoCH│
└──────┬──────────────────────────────────────────────────────────┘
       │
       │ SMC Signals
       ▼
┌─────────────────────────────────────────────────────────────────┐
│                SENTIMENT ENGINE / ML PREDICTION                  │
│              (analysis/sentiment_engine.py)                      │
│                                                                  │
│  • Combines Technical + SMC signals                             │
│  • ML Model Predictions (XGBoost, LightGBM, CatBoost, RF)       │
│  • Confidence Scoring                                            │
│  • Risk Assessment                                               │
└──────┬──────────────────────────────────────────────────────────┘
       │
       │ Sentiment Result
       ▼
┌─────────────────────────────────────────────────────────────────┐
│           MULTI-TIMEFRAME AGGREGATION (Optional)                │
│              (analysis/multi_timeframe.py)                       │
│                                                                  │
│  M15 ──┐                                                         │
│  H1  ──┼──► Alignment Score ──► Dominant Sentiment              │
│  H4  ──┤                                                         │
│  D1  ──┘                                                         │
└──────┬──────────────────────────────────────────────────────────┘
       │
       │ Final Analysis Result
       ▼
┌─────────────────────┐         ┌──────────────────┐
│   DATABASE SAVE     │         │  DISPLAY TO USER │
│  (repository.py)    │         │   (GUI Cards)    │
│                     │         │                  │
│ • Prediction        │         │ • Sentiment Card │
│ • Confidence        │         │ • Charts         │
│ • Timestamp         │         │ • Factors        │
│ • Actual Outcome    │         │ • Insights       │
└─────────────────────┘         └──────────────────┘
```

---

## 🚀 Launch Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                  USER DOUBLE-CLICKS                              │
│                   "conda smc.bat"                                │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │  [1/5] Check Conda Installed   │
        │  ✓ Verify conda is in PATH     │
        └────────────┬───────────────────┘
                     │
                     ▼
        ┌────────────────────────────────┐
        │ [2/5] Check Environment Exists │
        │                                │
        │ conda env list | find "smc bot"│
        └────────┬───────────────────────┘
                 │
         ┌───────┴───────┐
         │               │
    NOT FOUND         FOUND
         │               │
         ▼               │
┌─────────────────┐      │
│ Create New Env  │      │
│                 │      │
│ conda env       │      │
│  create -f      │      │
│  environment.yml│      │
│  -n "smc bot"   │      │
│                 │      │
│ (5-15 minutes)  │      │
└────────┬────────┘      │
         │               │
         └───────┬───────┘
                 │
                 ▼
        ┌────────────────────────────────┐
        │ [3/5] Activate Environment     │
        │                                │
        │ conda activate "smc bot"       │
        └────────────┬───────────────────┘
                     │
                     ▼
        ┌────────────────────────────────┐
        │ [4/5] Verify Dependencies      │
        │                                │
        │ Check:                         │
        │  ✓ streamlit                   │
        │  ✓ talib                       │
        │  ✓ MetaTrader5                 │
        │                                │
        │ Install missing if needed      │
        └────────────┬───────────────────┘
                     │
                     ▼
        ┌────────────────────────────────┐
        │ Create Directories             │
        │                                │
        │  • data/                       │
        │  • logs/                       │
        │  • models/                     │
        │  • reports/                    │
        └────────────┬───────────────────┘
                     │
                     ▼
        ┌────────────────────────────────┐
        │ [5/5] Launch Bot               │
        │                                │
        │ streamlit run app.py           │
        │   --server.headless=true       │
        │   --server.port=8501           │
        └────────────┬───────────────────┘
                     │
                     ▼
        ┌────────────────────────────────┐
        │   BROWSER OPENS AUTOMATICALLY  │
        │                                │
        │   http://localhost:8501        │
        │                                │
        │   ┌──────────────────────┐     │
        │   │  SMC BOT DASHBOARD  │     │
        │   │                      │     │
        │   │  Ready for Trading!  │     │
        │   └──────────────────────┘     │
        └────────────────────────────────┘
```

---

## 🛠️ Technology Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                        TECHNOLOGY LAYERS                         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      DEPLOYMENT LAYER                            │
│  • Anaconda/Miniconda (Environment Manager)                     │
│  • Windows Batch Scripting (Orchestration)                      │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                      FRONTEND LAYER                              │
│  • Streamlit 1.28+ (Web Framework)                              │
│  • Plotly 5.17+ (Interactive Charts)                            │
│  • Matplotlib 3.8+ (Static Plots)                               │
│  • Custom CSS (Styling)                                          │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                     BUSINESS LOGIC LAYER                         │
│  • Python 3.11                                                   │
│  • Pandas 2.1+ (Data Manipulation)                              │
│  • NumPy 1.24+ (Numerical Computing)                            │
│  • TA-Lib 0.4.28+ (Technical Indicators)                        │
│  • pandas-ta 0.3.14+ (Additional Indicators)                    │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                    MACHINE LEARNING LAYER                        │
│  • XGBoost 2.0+ (Gradient Boosting)                             │
│  • LightGBM 4.0+ (Fast Boosting)                                │
│  • CatBoost 1.2+ (Categorical Boosting)                         │
│  • Scikit-learn 1.3+ (Random Forest, Preprocessing)             │
│  • TensorFlow 2.14+ (Deep Learning - Optional)                  │
│  • Optuna 3.4+ (Hyperparameter Tuning)                          │
│  • SHAP 0.43+ (Model Explainability)                            │
│  • imbalanced-learn 0.11+ (SMOTE)                               │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                      DATA ACCESS LAYER                           │
│  • MetaTrader5 5.0.45+ (Broker Integration)                     │
│  • SQLAlchemy 2.0+ (ORM)                                        │
│  • SQLite (Database)                                             │
│  • Alembic 1.12+ (Migrations)                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                    INFRASTRUCTURE LAYER                          │
│  • Loguru 0.7+ (Logging)                                        │
│  • psutil 5.9+ (System Monitoring)                              │
│  • python-dotenv 1.0+ (Config Management)                       │
│  • pytest 7.4+ (Testing)                                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Directory Structure

```
📦 SMC Bot Root
│
├── 📄 conda smc.bat              ← MAIN ORCHESTRATOR (NEW!)
├── 📄 environment.yml            ← Conda environment definition
├── 📄 requirements.txt           ← Pip fallback
├── 📄 app.py                     ← Main Streamlit application
│
├── 📂 config/                    ← Configuration files
│   ├── settings.py               ← App settings
│   ├── indicators_config.yaml    ← Indicator parameters
│   └── smc_config.yaml           ← SMC parameters
│
├── 📂 gui/                       ← GUI components
│   └── components/
│       ├── connection_panel.py   ← MT5 connection UI
│       ├── sentiment_card.py     ← Sentiment display
│       ├── chart_panel.py        ← Charts
│       ├── health_dashboard.py   ← Health monitor
│       ├── metrics_panel.py      ← Metrics display
│       ├── ml_training_panel.py  ← ML training UI (NEW v2.0)
│       ├── regime_panel.py       ← Regime detection UI (NEW v2.0)
│       ├── settings_panel.py     ← Settings UI
│       └── live_logs.py          ← Logging UI
│
├── 📂 src/                       ← Source code
│   ├── mt5/                      ← MT5 integration
│   │   ├── connection.py
│   │   ├── data_fetcher.py
│   │   └── validator.py
│   │
│   ├── analysis/                 ← Analysis engines
│   │   ├── sentiment_engine.py
│   │   ├── multi_timeframe.py
│   │   ├── regime_detector.py    (NEW v2.0)
│   │   └── confidence_scorer.py
│   │
│   ├── indicators/               ← Indicators
│   │   ├── technical.py
│   │   ├── smc.py
│   │   └── calculator.py
│   │
│   ├── ml/                       ← Machine Learning
│   │   ├── training.py           (NEW v2.0)
│   │   ├── model_manager.py
│   │   ├── feature_engineering.py (NEW v2.0)
│   │   ├── evaluator.py
│   │   ├── calibrator.py
│   │   ├── hyperparameter_tuner.py (NEW v2.0)
│   │   └── feature_selector.py
│   │
│   ├── database/                 ← Data persistence
│   │   ├── models.py
│   │   └── repository.py
│   │
│   ├── health/                   ← Monitoring
│   │   ├── monitor.py
│   │   ├── diagnostics.py
│   │   └── recovery.py
│   │
│   ├── reporting/                ← Reports
│   │   ├── pdf_generator.py
│   │   └── charts.py
│   │
│   └── utils/                    ← Utilities
│       └── logger.py
│
├── 📂 data/                      ← Database & cache (auto-created)
│   └── mt5_sentiment.db
│
├── 📂 logs/                      ← Log files (auto-created)
│   ├── app.log
│   ├── mt5.log
│   └── analysis.log
│
├── 📂 models/                    ← ML models (auto-created)
│   ├── xgboost_model.pkl
│   ├── lightgbm_model.pkl
│   ├── catboost_model.pkl
│   └── rf_model.pkl
│
└── 📂 reports/                   ← PDF reports (auto-created)
    └── EURUSD_20231022_120000.pdf
```

---

## 🎯 Key Features Summary

### 📊 **9 Dashboard Tabs**
1. **Analysis** - Main sentiment analysis
2. **Indicators** - Technical indicator charts
3. **Metrics** - Performance tracking
4. **SMC** - Smart Money Concepts analysis
5. **Market Regime** - Regime detection (NEW v2.0)
6. **ML Training** - Train models with 70+ features (NEW v2.0)
7. **Health** - System diagnostics
8. **Settings** - Configuration
9. **Logs & Debug** - Real-time logging

### 🤖 **ML Capabilities**
- 4-model ensemble (XGBoost, LightGBM, CatBoost, Random Forest)
- 70+ engineered features
- SMOTE balancing
- Hyperparameter tuning with Optuna
- Probability calibration
- 10+ pip meaningful targets

### 📈 **Analysis Features**
- Multi-timeframe analysis (M15, H1, H4, D1)
- 15+ technical indicators
- Smart Money Concepts (Order Blocks, FVG, Liquidity)
- Market regime detection (Trending, Ranging, Volatile)
- Confidence scoring
- Risk assessment

### 🔌 **MT5 Integration**
- Auto-connect to MetaTrader 5
- Real-time data fetching
- Multiple symbols support
- Multi-timeframe data
- Connection health monitoring

---

## 🎬 Usage Flow

```
1. USER:     Double-click "conda smc.bat"
             ↓
2. SCRIPT:   Creates/activates "smc bot" environment
             Installs all dependencies
             ↓
3. BOT:      Launches Streamlit dashboard
             Opens browser automatically
             ↓
4. USER:     Configure MT5 connection (Settings tab)
             Click "Connect" button
             ↓
5. USER:     Select symbol & timeframe
             Click "Analyze" button
             ↓
6. BOT:      Fetches data → Calculates indicators → Runs ML
             Displays sentiment + confidence + insights
             ↓
7. USER:     Reviews analysis, charts, and recommendations
             Optionally trains new models (ML Training tab)
             Generates PDF reports
```

---

## 🔧 Maintenance & Updates

```
Update Environment:
conda env update -f environment.yml -n "smc bot" --prune

Retrain Models:
Go to "ML Training" tab → Configure → Click "Train Models"

Export Reports:
Analysis tab → Click "Generate Report" → Download PDF

View Logs:
Logs & Debug tab → Select log file → Download
```

---

**Created:** 2025-10-22  
**Environment:** Anaconda (smc bot)  
**Launch:** `conda smc.bat`  
**Dashboard:** http://localhost:8501
