"""
Continuous Learning Module
Automatically improves model based on prediction results
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import pandas as pd

from src.ml.model_manager import ModelManager
from src.ml.prediction_tracker import PredictionTracker
from src.database.repository import DatabaseRepository
from src.utils.logger import get_logger
from config.settings import MLConfig

logger = get_logger()


class ContinuousLearner:
    """
    Continuous learning system
    
    Features:
    - Monitors prediction accuracy
    - Triggers retraining when needed
    - Incorporates new verified predictions
    - Maintains performance over time
    """
    
    def __init__(self, repository: Optional[DatabaseRepository] = None):
        """Initialize continuous learner"""
        self.repository = repository
        self.tracker = PredictionTracker(repository=repository)
        self.manager = ModelManager(repository=repository)
        self.logger = get_logger()
    
    def should_retrain(self) -> Dict[str, Any]:
        """
        Check if model should be retrained
        
        Returns:
            Dict with decision and reasoning
        """
        # Check tracker recommendation
        tracker_check = self.tracker.needs_retraining(
            min_accuracy=MLConfig.MIN_CONFIDENCE,
            min_predictions=100,
            check_days=7
        )
        
        # Check time since last training
        last_training_time = self._get_last_training_time()
        days_since_training = (datetime.now() - last_training_time).days if last_training_time else 999
        
        should_retrain = False
        reasons = tracker_check['reasons'].copy()
        
        # Time-based retraining (daily recommended)
        if days_since_training >= 1:
            should_retrain = True
            reasons.append(f"Last training was {days_since_training} days ago")
        
        # Accuracy-based retraining
        if tracker_check['needs_retraining']:
            should_retrain = True
        
        return {
            'should_retrain': should_retrain,
            'reasons': reasons,
            'current_accuracy': tracker_check['current_accuracy'],
            'days_since_training': days_since_training,
            'new_predictions': tracker_check['unverified_predictions']
        }
    
    def execute_retraining(
        self,
        symbol: str = "EURUSD",
        timeframe: str = "H1",
        num_bars: int = 2000,
        use_tuning: bool = False
    ) -> Dict[str, Any]:
        """
        Execute automatic retraining
        
        Args:
            symbol: Symbol to train on
            timeframe: Timeframe
            num_bars: Number of bars
            use_tuning: Whether to use hyperparameter tuning
            
        Returns:
            Dict with retraining results
        """
        try:
            self.logger.info("Starting automatic retraining", category="ml_training")
            
            # Fetch fresh data
            from src.mt5.data_fetcher import MT5DataFetcher
            
            fetcher = MT5DataFetcher(connection=None)
            df = fetcher.get_ohlcv(symbol, timeframe, count=num_bars)
            
            if df is None or df.empty:
                self.logger.error("Failed to fetch data for retraining", category="ml_training")
                return {'success': False, 'error': 'Data fetch failed'}
            
            # Train new model
            version = f"v2.0.0_auto_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            result = self.manager.train_new_model(
                df=df,
                version=version,
                tune_hyperparameters=use_tuning,
                select_features=True,
                calibrate_probabilities=True,
                n_features=50
            )
            
            # Store retraining record
            self._store_retraining_record(
                version=version,
                accuracy=result['test_accuracy'],
                trigger='automatic'
            )
            
            self.logger.info(
                f"Automatic retraining complete: {version} ({result['test_accuracy']:.2%} accuracy)",
                category="ml_training"
            )
            
            return {
                'success': True,
                'version': version,
                'accuracy': result['test_accuracy'],
                'cv_score': result['cv_mean'],
                'improvement': self._calculate_improvement(result['test_accuracy'])
            }
            
        except Exception as e:
            self.logger.error(f"Automatic retraining failed: {e}", category="ml_training")
            return {'success': False, 'error': str(e)}
    
    def check_and_retrain(self) -> Optional[Dict[str, Any]]:
        """
        Check if retraining is needed and execute if so
        
        Returns:
            Dict with results if retraining occurred, None otherwise
        """
        decision = self.should_retrain()
        
        if not decision['should_retrain']:
            self.logger.info("Retraining not needed yet", category="ml_training")
            return None
        
        self.logger.info(
            f"Retraining triggered. Reasons: {', '.join(decision['reasons'])}",
            category="ml_training"
        )
        
        # Execute retraining
        result = self.execute_retraining()
        
        return {
            'decision': decision,
            'result': result
        }
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """
        Get continuous learning statistics
        
        Returns:
            Dict with learning stats
        """
        try:
            # Recent accuracy
            accuracy_7d = self.tracker.get_recent_accuracy(days=7)
            accuracy_30d = self.tracker.get_recent_accuracy(days=30)
            
            # Last training info
            last_training = self._get_last_training_time()
            
            # Model versions
            models = self.manager.list_models()
            
            return {
                'accuracy_7d': accuracy_7d['accuracy'],
                'accuracy_30d': accuracy_30d['accuracy'],
                'predictions_7d': accuracy_7d['total'],
                'predictions_30d': accuracy_30d['total'],
                'last_training': last_training,
                'days_since_training': (datetime.now() - last_training).days if last_training else None,
                'model_versions': len(models),
                'latest_version': models[0] if models else None,
                'auto_retrain_enabled': True
            }
            
        except Exception as e:
            self.logger.error(f"Error getting learning stats: {e}", category="ml_training")
            return {}
    
    def _get_last_training_time(self) -> Optional[datetime]:
        """Get timestamp of last training"""
        try:
            from config.settings import MODELS_DIR
            
            # Get most recent model
            models = self.manager.list_models()
            
            if not models:
                return None
            
            latest_version = models[0]
            metadata_path = MODELS_DIR / f"metadata_{latest_version}.json"
            
            if metadata_path.exists():
                import json
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                    
                    training_date_str = metadata.get('training_date')
                    if training_date_str:
                        # Parse datetime string
                        return datetime.fromisoformat(training_date_str.replace('Z', '+00:00'))
            
            # Fallback to file modification time
            model_path = MODELS_DIR / f"model_{latest_version}.joblib"
            if model_path.exists():
                return datetime.fromtimestamp(model_path.stat().st_mtime)
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting last training time: {e}", category="ml_training")
            return None
    
    def _calculate_improvement(self, new_accuracy: float) -> Optional[float]:
        """Calculate improvement over previous model"""
        try:
            models = self.manager.list_models()
            
            if len(models) < 2:
                return None
            
            # Get previous model accuracy
            prev_version = models[1]
            metadata_path = MODELS_DIR / f"metadata_{prev_version}.json"
            
            if metadata_path.exists():
                import json
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                    prev_accuracy = metadata.get('test_accuracy', 0)
                    
                    return new_accuracy - prev_accuracy
            
            return None
            
        except:
            return None
    
    def _store_retraining_record(self, version: str, accuracy: float, trigger: str):
        """Store record of retraining event"""
        try:
            from config.settings import MODELS_DIR
            import json
            
            record_path = MODELS_DIR / "retraining_history.json"
            
            # Load existing history
            history = []
            if record_path.exists():
                with open(record_path, 'r') as f:
                    history = json.load(f)
            
            # Add new record
            history.append({
                'timestamp': datetime.now().isoformat(),
                'version': version,
                'accuracy': float(accuracy),
                'trigger': trigger
            })
            
            # Save
            with open(record_path, 'w') as f:
                json.dump(history, f, indent=2)
            
        except Exception as e:
            self.logger.error(f"Error storing retraining record: {e}", category="ml_training")


if __name__ == "__main__":
    # Test continuous learner
    print("🧠 Testing Continuous Learner...")
    
    from src.database.repository import get_repository
    
    learner = ContinuousLearner(repository=get_repository())
    
    # Test retraining decision
    decision = learner.should_retrain()
    print(f"✓ Should retrain: {decision}")
    
    # Test stats
    stats = learner.get_learning_stats()
    print(f"✓ Learning stats: {stats}")
    
    print("\n✓ Continuous learner test completed")
