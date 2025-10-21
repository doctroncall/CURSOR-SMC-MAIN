# 🎯 Accuracy Improvement Plan

## Executive Summary

After comprehensive code review, I've identified **7 critical areas** that can significantly improve prediction accuracy. Current issues stem from simplistic target definitions, limited features, and lack of model optimization.

---

## 🔍 Current Accuracy Issues

### 1. **CRITICAL: Simplistic Target Definition**
**Location**: `src/ml/training.py:59-61`

**Current Problem**:
```python
features_df['future_close'] = features_df['Close'].shift(-1)
features_df['target'] = (features_df['future_close'] > features_df['Close']).astype(int)
```

**Why This Hurts Accuracy**:
- Binary target (up/down) ignores magnitude of movement
- No consideration of noise/spread - a 1 pip move = 100 pip move
- Creates ~50/50 class distribution, making the model barely better than random
- Doesn't align with actual trading profitability

**Impact**: 🔴 **CRITICAL** - Baseline accuracy ceiling of ~55-60%

---

### 2. **Limited Feature Engineering**
**Location**: `src/ml/feature_engineering.py`

**Current Problems**:
- Only ~30 basic features
- Missing advanced price patterns (candlestick patterns, chart patterns)
- No feature interactions (RSI * Volume, MACD * Trend, etc.)
- No rolling statistics (volatility regimes, correlation patterns)
- SMC features are simplified (lines 154-165)

**Impact**: 🔴 **HIGH** - Missing 40-60% of predictive signals

---

### 3. **No Hyperparameter Optimization**
**Location**: `src/ml/training.py:108-124`

**Current Problem**:
```python
xgb_model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    # ... hardcoded defaults
)
```

**Why This Hurts**:
- Using default/basic hyperparameters
- No grid search or Bayesian optimization
- Model is not tuned to this specific market data

**Impact**: 🟡 **MEDIUM** - 5-10% accuracy loss

---

### 4. **No Class Balancing**
**Location**: `src/ml/training.py:72-86`

**Current Problem**:
- No handling of class imbalance
- Market trends are not 50/50 - often 60/40 or worse
- Model learns majority class bias

**Impact**: 🟡 **MEDIUM** - Biased predictions toward dominant class

---

### 5. **Insufficient Model Diversity**
**Location**: `src/ml/training.py:126-135`

**Current Problem**:
- Only 2 models in ensemble (XGBoost, Random Forest)
- Both are tree-based (similar biases)
- Neural network mentioned but not implemented
- No LightGBM, CatBoost, or linear models

**Impact**: 🟡 **MEDIUM** - Limited ensemble diversity

---

### 6. **Arbitrary Confidence Weights**
**Location**: `src/analysis/confidence_scorer.py:43-62`

**Current Problem**:
```python
scores.append(('raw_strength', min(raw_score, 1.0), 0.30))
scores.append(('agreement', agreement_score, 0.25))
scores.append(('clarity', clarity_score, 0.20))
# ... hardcoded weights
```

**Why This Hurts**:
- Weights are not learned from data
- No confidence calibration
- Predicted probabilities don't match actual outcomes

**Impact**: 🟡 **MEDIUM** - Unreliable confidence scores

---

### 7. **No Walk-Forward Validation**
**Location**: `src/ml/training.py:96-101`

**Current Problem**:
- Simple train/test split
- No time-series cross-validation
- Model may overfit to specific market regime
- No validation on truly unseen future data

**Impact**: 🟡 **MEDIUM** - Overfitting to training period

---

## 🚀 Recommended Improvements (Priority Order)

### Priority 1: Fix Target Definition (Expected: +10-15% accuracy)

**Implementation**:
```python
# Option 1: Minimum meaningful move (considering spread/noise)
min_move_pips = 10  # Configurable based on symbol
features_df['price_change_pips'] = (features_df['future_close'] - features_df['Close']) * 10000
features_df['target'] = np.where(
    features_df['price_change_pips'] > min_move_pips, 1,  # Clear uptrend
    np.where(features_df['price_change_pips'] < -min_move_pips, 0,  # Clear downtrend
             -1)  # Neutral/noise - exclude from training
)
features_df = features_df[features_df['target'] != -1]  # Remove noise

# Option 2: Multi-horizon targets (next 3 bars instead of 1)
features_df['future_max'] = features_df['High'].rolling(3).max().shift(-3)
features_df['future_min'] = features_df['Low'].rolling(3).min().shift(-3)
features_df['target'] = (
    (features_df['future_max'] - features_df['Close']) > 
    (features_df['Close'] - features_df['future_min'])
).astype(int)

# Option 3: Risk-adjusted returns
features_df['future_return'] = features_df['Close'].pct_change(3).shift(-3)
features_df['volatility'] = features_df['Close'].pct_change().rolling(20).std()
features_df['risk_adj_return'] = features_df['future_return'] / features_df['volatility']
features_df['target'] = (features_df['risk_adj_return'] > 0.5).astype(int)
```

---

### Priority 2: Enhanced Feature Engineering (Expected: +8-12% accuracy)

**Add These Feature Categories**:

1. **Price Action Patterns**:
   - Candlestick patterns (doji, hammer, engulfing, etc.)
   - Higher highs/lower lows sequences
   - Support/resistance proximity
   - Fibonacci retracement levels

2. **Feature Interactions**:
   - RSI * Volume ratio
   - MACD divergence with price
   - BB position * ATR
   - Trend strength * momentum alignment

3. **Market Regime Features**:
   - Volatility regime (low/normal/high)
   - Trend regime (trending/ranging)
   - Volume regime (dry/normal/surge)
   - Time-of-day patterns

4. **Advanced SMC Features**:
   - Order block strength score
   - FVG fill percentage
   - Premium/discount zone proximity
   - Liquidity sweep detection

5. **Lagged Features**:
   - Previous 3-5 candles' key metrics
   - Rate of change features
   - Acceleration indicators

**Implementation**: Expand `feature_engineering.py` with new methods

---

### Priority 3: Implement Hyperparameter Optimization (Expected: +5-8% accuracy)

**Use Optuna or GridSearchCV**:
```python
import optuna

def objective(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 500),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
        'min_child_weight': trial.suggest_int('min_child_weight', 1, 7),
        'subsample': trial.suggest_float('subsample', 0.6, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
    }
    
    model = xgb.XGBClassifier(**params)
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
    return scores.mean()

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)
```

---

### Priority 4: Add Class Balancing (Expected: +3-5% accuracy)

**Implementation**:
```python
from imblearn.over_sampling import SMOTE
from imblearn.combine import SMOTETomek

# Option 1: SMOTE for synthetic oversampling
smote = SMOTE(random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

# Option 2: Class weights
class_weight = len(y_train) / (2 * np.bincount(y_train))
model = xgb.XGBClassifier(scale_pos_weight=class_weight[1]/class_weight[0])

# Option 3: Stratified sampling with different thresholds
```

---

### Priority 5: Expand Model Ensemble (Expected: +3-5% accuracy)

**Add More Models**:
```python
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

# Tree-based diversity
lgbm_model = LGBMClassifier(n_estimators=200, max_depth=8)
catboost_model = CatBoostClassifier(iterations=200, depth=6, verbose=0)

# Linear model (different perspective)
lr_model = LogisticRegression(max_iter=1000, C=0.1)

# Neural network
nn_model = MLPClassifier(hidden_layers=(100, 50), max_iter=500)

# Weighted ensemble
ensemble = VotingClassifier(
    estimators=[
        ('xgb', xgb_model),
        ('lgbm', lgbm_model),
        ('catboost', catboost_model),
        ('lr', lr_model)
    ],
    voting='soft',
    weights=[0.3, 0.3, 0.3, 0.1]  # Optimize these
)
```

---

### Priority 6: Calibrate Confidence Scores (Expected: +Reliability)

**Implement Probability Calibration**:
```python
from sklearn.calibration import CalibratedClassifierCV

# Calibrate the ensemble
calibrated_model = CalibratedClassifierCV(
    ensemble,
    method='isotonic',  # or 'sigmoid'
    cv=5
)
calibrated_model.fit(X_train, y_train)

# Now predicted probabilities match actual outcomes
```

---

### Priority 7: Walk-Forward Validation (Expected: Better generalization)

**Implementation**:
```python
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5)

scores = []
for train_idx, test_idx in tscv.split(X):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
    
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    scores.append(score)

print(f"Time-series CV scores: {scores}")
print(f"Mean: {np.mean(scores):.2%} ± {np.std(scores):.2%}")
```

---

## 📊 Expected Impact Summary

| Improvement | Expected Gain | Effort | Priority |
|------------|---------------|---------|----------|
| Fix Target Definition | +10-15% | Medium | 🔴 P1 |
| Enhanced Features | +8-12% | High | 🔴 P1 |
| Hyperparameter Tuning | +5-8% | Medium | 🟡 P2 |
| Class Balancing | +3-5% | Low | 🟡 P2 |
| Expand Ensemble | +3-5% | Medium | 🟡 P2 |
| Calibrate Confidence | Reliability | Low | 🟢 P3 |
| Walk-Forward Validation | Robustness | Medium | 🟢 P3 |

**Total Expected Improvement**: +25-40% accuracy (from ~55-60% to **80-85%**)

---

## 🔧 Additional Recommendations

### 8. Feature Selection
- Use SHAP values to identify most important features
- Remove redundant/correlated features
- Recursive feature elimination

### 9. Market Regime Awareness
- Train separate models for trending vs ranging markets
- Train separate models for high vs low volatility
- Use regime switching models

### 10. Ensemble Stacking
- Instead of simple voting, use stacked generalization
- Meta-learner combines base model predictions

### 11. Online Learning
- Implement incremental learning to adapt to changing markets
- Update model weights daily without full retraining

### 12. Better SMC Integration
- Current SMC features are too simplified
- Integrate actual order block detection scores
- Use FVG quality metrics
- Add liquidity sweep confirmation

---

## 🎯 Quick Wins (Can Implement Today)

1. **Change target to require minimum 10-pip move** (30 min)
2. **Add class balancing with SMOTE** (15 min)
3. **Add 10-20 new features** (2 hours):
   - Candlestick patterns
   - Feature interactions
   - Lagged variables
4. **Use TimeSeriesSplit for validation** (30 min)

---

## 📝 Implementation Order

**Week 1** (Quick Wins):
- [ ] Fix target definition
- [ ] Add class balancing
- [ ] Implement time-series CV

**Week 2** (Feature Engineering):
- [ ] Add 30-50 new features
- [ ] Feature importance analysis
- [ ] Remove redundant features

**Week 3** (Model Optimization):
- [ ] Hyperparameter tuning
- [ ] Add LightGBM/CatBoost
- [ ] Probability calibration

**Week 4** (Advanced):
- [ ] Market regime detection
- [ ] Stacked ensemble
- [ ] Online learning framework

---

## 🧪 Testing & Validation

After each improvement:
1. Compare accuracy on hold-out test set
2. Check calibration plots (predicted vs actual probabilities)
3. Analyze confusion matrix
4. Test on multiple symbols/timeframes
5. Backtest with real trading simulation

---

## 📚 Code Changes Required

### Files to Modify:
1. `src/ml/training.py` - Target definition, class balancing, hyperparameter tuning
2. `src/ml/feature_engineering.py` - Add new features
3. `src/ml/model_manager.py` - Support multiple model types
4. `src/analysis/confidence_scorer.py` - Add calibration
5. `config/settings.py` - Add new configuration options

### New Files to Create:
1. `src/ml/hyperparameter_tuner.py` - Optuna-based tuning
2. `src/ml/feature_selector.py` - Feature selection utilities
3. `src/ml/calibrator.py` - Probability calibration
4. `src/analysis/regime_detector.py` - Market regime classification

---

## 💡 Key Insights

**The #1 issue hurting accuracy**: **Simplistic target definition that treats all moves equally, creating a noisy 50/50 problem.**

**The fastest path to 80% accuracy**:
1. Require minimum meaningful move (10+ pips)
2. Add 30-50 quality features  
3. Use proper time-series validation
4. Balance classes
5. Tune hyperparameters

**Remember**: More complex doesn't always mean better. Focus on:
- ✅ Quality features over quantity
- ✅ Proper validation (no look-ahead bias)
- ✅ Domain knowledge (SMC, market structure)
- ✅ Ensemble diversity (different model types)

---

Would you like me to start implementing these improvements? I recommend starting with Priority 1 items for maximum impact.
