"""
Feature Engineering
Creates ML features from market data and indicators
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from datetime import datetime

from src.indicators.technical import TechnicalIndicators
from src.indicators.smc import SMCAnalyzer
from src.utils.logger import get_logger

logger = get_logger()


class FeatureEngineer:
    """
    Create ML features from raw market data
    
    Features include:
    - Technical indicators
    - SMC patterns
    - Price patterns
    - Volume patterns
    - Time-based features
    """
    
    def __init__(self):
        """Initialize feature engineer"""
        self.tech_indicators = TechnicalIndicators()
        self.smc_analyzer = SMCAnalyzer()
        self.logger = logger
    
    def create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create all ML features from OHLCV data
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            DataFrame with features
        """
        try:
            self.logger.info("Creating ML features", category="ml_training")
            
            features_df = df.copy()
            
            # Technical indicator features
            features_df = self._add_indicator_features(features_df)
            
            # Price pattern features
            features_df = self._add_price_features(features_df)
            
            # Volume features
            features_df = self._add_volume_features(features_df)
            
            # Time-based features
            features_df = self._add_time_features(features_df)
            
            # SMC features
            features_df = self._add_smc_features(features_df)
            
            # Drop NaN values
            features_df = features_df.dropna()
            
            self.logger.info(f"Created {len(features_df.columns)} features", category="ml_training")
            
            return features_df
            
        except Exception as e:
            self.logger.error(f"Error creating features: {str(e)}", category="ml_training")
            return df
    
    def _add_indicator_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add technical indicator features"""
        # RSI
        df['rsi'] = self.tech_indicators.calculate_rsi(df)
        
        # MACD
        macd = self.tech_indicators.calculate_macd(df)
        df['macd'] = macd['macd']
        df['macd_signal'] = macd['signal']
        df['macd_hist'] = macd['histogram']
        
        # ADX
        adx = self.tech_indicators.calculate_adx(df)
        df['adx'] = adx['adx']
        df['plus_di'] = adx['plus_di']
        df['minus_di'] = adx['minus_di']
        
        # Bollinger Bands
        bb = self.tech_indicators.calculate_bollinger_bands(df)
        df['bb_upper'] = bb['upper']
        df['bb_middle'] = bb['middle']
        df['bb_lower'] = bb['lower']
        df['bb_width'] = (bb['upper'] - bb['lower']) / bb['middle']
        
        # ATR
        df['atr'] = self.tech_indicators.calculate_atr(df)
        df['atr_pct'] = df['atr'] / df['Close']
        
        # Moving averages
        df['ema_20'] = self.tech_indicators.calculate_ema(df, 20)
        df['ema_50'] = self.tech_indicators.calculate_ema(df, 50)
        df['sma_200'] = self.tech_indicators.calculate_sma(df, 200)
        
        # Volume indicators
        df['obv'] = self.tech_indicators.calculate_obv(df)
        df['mfi'] = self.tech_indicators.calculate_mfi(df)
        
        return df
    
    def _add_price_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add price-based features"""
        # Price changes
        df['price_change'] = df['Close'].pct_change()
        df['price_change_5'] = df['Close'].pct_change(periods=5)
        df['price_change_10'] = df['Close'].pct_change(periods=10)
        
        # High-Low range
        df['hl_range'] = (df['High'] - df['Low']) / df['Close']
        
        # Body vs wick
        df['body_size'] = abs(df['Close'] - df['Open']) / df['Close']
        df['upper_wick'] = (df['High'] - df[['Open', 'Close']].max(axis=1)) / df['Close']
        df['lower_wick'] = (df[['Open', 'Close']].min(axis=1) - df['Low']) / df['Close']
        
        # Price position
        df['close_position'] = (df['Close'] - df['Low']) / (df['High'] - df['Low'])
        
        return df
    
    def _add_volume_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add volume-based features"""
        # Volume changes
        df['volume_change'] = df['Volume'].pct_change()
        df['volume_ma_ratio'] = df['Volume'] / df['Volume'].rolling(20).mean()
        
        return df
    
    def _add_time_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add time-based features"""
        df['hour'] = df.index.hour
        df['day_of_week'] = df.index.dayofweek
        df['is_london_session'] = ((df['hour'] >= 8) & (df['hour'] < 17)).astype(int)
        df['is_ny_session'] = ((df['hour'] >= 13) & (df['hour'] < 22)).astype(int)
        
        return df
    
    def _add_smc_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add SMC-based features (simplified for performance)"""
        try:
            # Swing points count (simplified)
            df['recent_highs'] = df['High'].rolling(20).apply(lambda x: (x == x.max()).sum())
            df['recent_lows'] = df['Low'].rolling(20).apply(lambda x: (x == x.min()).sum())
            
            # Trend strength
            df['trend_strength'] = (df['Close'] - df['Close'].shift(20)) / df['Close'].shift(20)
            
        except Exception as e:
            self.logger.warning(f"Error adding SMC features: {str(e)}", category="ml_training")
        
        return df
    
    def get_feature_names(self) -> List[str]:
        """Get list of feature names"""
        return [
            'rsi', 'macd', 'macd_signal', 'macd_hist',
            'adx', 'plus_di', 'minus_di',
            'bb_width', 'atr_pct',
            'ema_20', 'ema_50', 'sma_200',
            'obv', 'mfi',
            'price_change', 'price_change_5', 'price_change_10',
            'hl_range', 'body_size', 'upper_wick', 'lower_wick',
            'close_position',
            'volume_change', 'volume_ma_ratio',
            'hour', 'day_of_week', 'is_london_session', 'is_ny_session',
            'recent_highs', 'recent_lows', 'trend_strength'
        ]


if __name__ == "__main__":
    # Test feature engineering
    print("🔧 Testing Feature Engineer...")
    
    # Create sample data
    dates = pd.date_range(start='2024-01-01', periods=500, freq='1H')
    data = {
        'Open': np.random.uniform(1.08, 1.09, 500),
        'High': np.random.uniform(1.09, 1.10, 500),
        'Low': np.random.uniform(1.07, 1.08, 500),
        'Close': np.random.uniform(1.08, 1.09, 500),
        'Volume': np.random.randint(1000, 10000, 500),
    }
    df = pd.DataFrame(data, index=dates)
    
    engineer = FeatureEngineer()
    
    features_df = engineer.create_features(df)
    
    print(f"✓ Original columns: {len(df.columns)}")
    print(f"✓ Feature columns: {len(features_df.columns)}")
    print(f"✓ Rows after feature engineering: {len(features_df)}")
    print(f"✓ Feature names: {engineer.get_feature_names()}")
    
    print("\n✓ Feature engineer test completed")
