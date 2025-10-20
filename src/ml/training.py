"""
Model Trainer
Trains ML models for sentiment prediction
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
from typing import Dict, Any, Tuple
import time
from datetime import datetime

from .feature_engineering import FeatureEngineer
from config.settings import MLConfig
from src.utils.logger import get_logger

logger = get_logger()


class ModelTrainer:
    """
    Train ML models for sentiment prediction
    
    Uses ensemble approach:
    - XGBoost
    - Random Forest
    - Voting classifier
    """
    
    def __init__(self):
        """Initialize trainer"""
        self.feature_engineer = FeatureEngineer()
        self.config = MLConfig
        self.logger = logger
        self.scaler = StandardScaler()
    
    def prepare_training_data(
        self,
        df: pd.DataFrame,
        target_col: str = 'target'
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Prepare data for training
        
        Args:
            df: DataFrame with OHLCV data
            target_col: Name of target column
            
        Returns:
            Tuple of (features_df, target_series)
        """
        # Create features
        features_df = self.feature_engineer.create_features(df)
        
        # Create target (future price movement)
        if target_col not in features_df.columns:
            # Create target based on future price movement
            features_df['future_close'] = features_df['Close'].shift(-1)
            features_df['target'] = (features_df['future_close'] > features_df['Close']).astype(int)
            features_df = features_df.dropna()
            target_col = 'target'
        
        # Split features and target
        feature_cols = self.feature_engineer.get_feature_names()
        X = features_df[feature_cols]
        y = features_df[target_col]
        
        return X, y
    
    def train_model(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        model_version: str = None
    ) -> Dict[str, Any]:
        """
        Train ensemble model
        
        Args:
            X: Feature DataFrame
            y: Target Series
            model_version: Model version string
            
        Returns:
            Dict with trained model and metrics
        """
        try:
            start_time = time.time()
            model_version = model_version or self.config.MODEL_VERSION
            
            self.logger.info(f"Training model {model_version}", category="ml_training")
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y,
                test_size=self.config.TEST_SIZE,
                random_state=self.config.RANDOM_STATE,
                stratify=y
            )
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train XGBoost
            xgb_model = xgb.XGBClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=self.config.RANDOM_STATE,
                n_jobs=-1
            )
            xgb_model.fit(X_train_scaled, y_train)
            
            # Train Random Forest
            rf_model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=self.config.RANDOM_STATE,
                n_jobs=-1
            )
            rf_model.fit(X_train_scaled, y_train)
            
            # Create ensemble
            ensemble = VotingClassifier(
                estimators=[
                    ('xgb', xgb_model),
                    ('rf', rf_model)
                ],
                voting='soft',
                weights=[self.config.XGBOOST_WEIGHT, self.config.RANDOM_FOREST_WEIGHT]
            )
            ensemble.fit(X_train_scaled, y_train)
            
            # Evaluate
            train_score = ensemble.score(X_train_scaled, y_train)
            test_score = ensemble.score(X_test_scaled, y_test)
            
            # Cross-validation
            cv_scores = cross_val_score(
                ensemble, X_train_scaled, y_train,
                cv=self.config.CV_FOLDS,
                scoring='accuracy'
            )
            
            duration = time.time() - start_time
            
            # Feature importance (from XGBoost)
            feature_importance = dict(zip(
                X.columns,
                xgb_model.feature_importances_
            ))
            
            result = {
                'model': ensemble,
                'scaler': self.scaler,
                'version': model_version,
                'train_accuracy': train_score,
                'test_accuracy': test_score,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std(),
                'feature_importance': feature_importance,
                'training_samples': len(X_train),
                'training_duration': duration,
                'training_date': datetime.now()
            }
            
            self.logger.log_ml_training(
                model_version,
                len(X_train),
                test_score,
                duration
            )
            
            self.logger.info(
                f"Model trained: {test_score:.2%} accuracy in {duration:.2f}s",
                category="ml_training"
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error training model: {str(e)}", category="ml_training")
            raise


if __name__ == "__main__":
    # Test model trainer
    print("🎓 Testing Model Trainer...")
    
    # Create sample data with target
    dates = pd.date_range(start='2024-01-01', periods=1000, freq='1H')
    trend = np.linspace(1.08, 1.10, 1000) + np.random.normal(0, 0.001, 1000)
    
    data = {
        'Open': trend - np.random.uniform(0, 0.001, 1000),
        'High': trend + np.random.uniform(0, 0.002, 1000),
        'Low': trend - np.random.uniform(0, 0.002, 1000),
        'Close': trend,
        'Volume': np.random.randint(1000, 10000, 1000),
    }
    df = pd.DataFrame(data, index=dates)
    
    trainer = ModelTrainer()
    
    # Prepare data
    X, y = trainer.prepare_training_data(df)
    print(f"✓ Prepared data: {len(X)} samples, {len(X.columns)} features")
    
    # Train model
    result = trainer.train_model(X, y, "v1.0.0-test")
    print(f"✓ Model trained:")
    print(f"   Train accuracy: {result['train_accuracy']:.2%}")
    print(f"   Test accuracy: {result['test_accuracy']:.2%}")
    print(f"   CV mean: {result['cv_mean']:.2%} ± {result['cv_std']:.2%}")
    print(f"   Duration: {result['training_duration']:.2f}s")
    
    print("\n✓ Model trainer test completed")
