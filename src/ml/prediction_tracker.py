"""
Prediction Tracker
Tracks predictions and actual outcomes for continuous learning
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import pandas as pd

from src.database.repository import DatabaseRepository
from src.utils.logger import get_logger

logger = get_logger()


class PredictionTracker:
    """
    Track predictions and verify against actual outcomes
    
    Features:
    - Store predictions with context
    - Verify predictions after time passes
    - Calculate accuracy metrics
    - Identify when retraining is needed
    - Provide data for continuous learning
    """
    
    def __init__(self, repository: Optional[DatabaseRepository] = None):
        """Initialize prediction tracker"""
        self.repository = repository
        self.logger = get_logger()
    
    def store_prediction(
        self,
        symbol: str,
        timeframe: str,
        sentiment: str,
        confidence: float,
        price_at_prediction: float,
        model_version: str,
        features: Optional[Dict[str, float]] = None
    ) -> int:
        """
        Store a prediction for later verification
        
        Args:
            symbol: Trading symbol
            timeframe: Timeframe
            sentiment: Predicted sentiment (BULLISH/BEARISH/NEUTRAL)
            confidence: Confidence score (0-1)
            price_at_prediction: Price when prediction was made
            model_version: Model version used
            features: Feature values (optional, for analysis)
            
        Returns:
            int: Prediction ID
        """
        if not self.repository:
            self.logger.warning("No repository - prediction not stored", category="ml_training")
            return -1
        
        try:
            prediction = self.repository.create_prediction(
                symbol_name=symbol,
                timeframe=timeframe,
                sentiment=sentiment,
                confidence=confidence,
                price_at_prediction=price_at_prediction,
                model_version=model_version
            )
            
            self.logger.info(
                f"Stored prediction: {symbol} {timeframe} {sentiment} ({confidence:.2%})",
                category="ml_training"
            )
            
            return prediction.id
            
        except Exception as e:
            self.logger.error(f"Error storing prediction: {e}", category="ml_training")
            return -1
    
    def verify_predictions(
        self,
        symbol: str,
        current_price: float,
        lookback_hours: int = 24
    ) -> int:
        """
        Verify unverified predictions for a symbol
        
        Args:
            symbol: Trading symbol
            current_price: Current market price
            lookback_hours: How far back to check predictions
            
        Returns:
            int: Number of predictions verified
        """
        if not self.repository:
            return 0
        
        try:
            # Get unverified predictions older than verification window
            cutoff_time = datetime.now() - timedelta(hours=lookback_hours)
            
            # Get predictions that need verification
            predictions = self.repository.get_predictions(
                symbol_name=symbol,
                is_verified=False,
                limit=100
            )
            
            verified_count = 0
            
            for pred in predictions:
                # Check if enough time has passed
                prediction_age = datetime.now() - pred.timestamp
                
                # Verification window based on timeframe
                verification_hours = self._get_verification_window(pred.timeframe)
                
                if prediction_age.total_seconds() / 3600 < verification_hours:
                    continue  # Not old enough yet
                
                # Determine actual outcome
                price_change = current_price - pred.price_at_prediction
                price_change_pct = (price_change / pred.price_at_prediction) * 100
                
                # Determine if prediction was correct
                actual_outcome = self._determine_outcome(price_change_pct)
                was_correct = (actual_outcome == pred.sentiment)
                
                # Update prediction
                self.repository.verify_prediction(
                    prediction_id=pred.id,
                    actual_outcome=actual_outcome,
                    was_correct=was_correct,
                    price_at_verification=current_price
                )
                
                verified_count += 1
                
                self.logger.info(
                    f"Verified prediction {pred.id}: {pred.sentiment} → {actual_outcome} "
                    f"({'✓' if was_correct else '✗'})",
                    category="ml_training"
                )
            
            if verified_count > 0:
                self.logger.info(
                    f"Verified {verified_count} predictions for {symbol}",
                    category="ml_training"
                )
            
            return verified_count
            
        except Exception as e:
            self.logger.error(f"Error verifying predictions: {e}", category="ml_training")
            return 0
    
    def get_recent_accuracy(
        self,
        symbol: Optional[str] = None,
        days: int = 7
    ) -> Dict[str, Any]:
        """
        Calculate recent prediction accuracy
        
        Args:
            symbol: Symbol to analyze (None for all)
            days: Number of days to look back
            
        Returns:
            Dict with accuracy metrics
        """
        if not self.repository:
            return {'total': 0, 'correct': 0, 'accuracy': 0.0}
        
        try:
            # Get verified predictions from last N days
            since = datetime.now() - timedelta(days=days)
            
            predictions = self.repository.get_predictions(
                symbol_name=symbol,
                is_verified=True,
                limit=1000
            )
            
            # Filter by date
            recent_preds = [p for p in predictions if p.verified_at and p.verified_at >= since]
            
            if not recent_preds:
                return {
                    'total': 0,
                    'correct': 0,
                    'incorrect': 0,
                    'accuracy': 0.0,
                    'by_sentiment': {}
                }
            
            # Calculate metrics
            total = len(recent_preds)
            correct = sum(1 for p in recent_preds if p.was_correct)
            incorrect = total - correct
            accuracy = correct / total if total > 0 else 0.0
            
            # By sentiment
            by_sentiment = {}
            for sentiment in ['BULLISH', 'BEARISH', 'NEUTRAL']:
                sent_preds = [p for p in recent_preds if p.sentiment == sentiment]
                if sent_preds:
                    sent_correct = sum(1 for p in sent_preds if p.was_correct)
                    by_sentiment[sentiment] = {
                        'total': len(sent_preds),
                        'correct': sent_correct,
                        'accuracy': sent_correct / len(sent_preds)
                    }
            
            return {
                'total': total,
                'correct': correct,
                'incorrect': incorrect,
                'accuracy': accuracy,
                'by_sentiment': by_sentiment,
                'period_days': days
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating accuracy: {e}", category="ml_training")
            return {'total': 0, 'correct': 0, 'accuracy': 0.0}
    
    def needs_retraining(
        self,
        min_accuracy: float = 0.70,
        min_predictions: int = 100,
        check_days: int = 7
    ) -> Dict[str, Any]:
        """
        Determine if model needs retraining
        
        Args:
            min_accuracy: Minimum acceptable accuracy
            min_predictions: Minimum predictions before checking
            check_days: Days to check
            
        Returns:
            Dict with retraining recommendation
        """
        accuracy_stats = self.get_recent_accuracy(days=check_days)
        
        needs_retrain = False
        reasons = []
        
        # Check if enough predictions
        if accuracy_stats['total'] < min_predictions:
            needs_retrain = False
            reasons.append(f"Not enough predictions yet ({accuracy_stats['total']}/{min_predictions})")
        
        # Check accuracy
        elif accuracy_stats['accuracy'] < min_accuracy:
            needs_retrain = True
            reasons.append(
                f"Accuracy below threshold ({accuracy_stats['accuracy']:.1%} < {min_accuracy:.1%})"
            )
        
        # Check for data drift (significant new predictions)
        unverified_count = self._get_unverified_count()
        if unverified_count > 200:
            needs_retrain = True
            reasons.append(f"{unverified_count} new predictions available for training")
        
        return {
            'needs_retraining': needs_retrain,
            'reasons': reasons,
            'current_accuracy': accuracy_stats['accuracy'],
            'total_predictions': accuracy_stats['total'],
            'unverified_predictions': unverified_count
        }
    
    def get_training_data_from_predictions(
        self,
        min_predictions: int = 100
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get verified predictions as training data
        
        Args:
            min_predictions: Minimum predictions needed
            
        Returns:
            List of prediction data or None
        """
        if not self.repository:
            return None
        
        try:
            # Get all verified predictions
            predictions = self.repository.get_predictions(
                is_verified=True,
                limit=10000
            )
            
            if len(predictions) < min_predictions:
                self.logger.info(
                    f"Not enough verified predictions for training ({len(predictions)}/{min_predictions})",
                    category="ml_training"
                )
                return None
            
            # Convert to training data format
            training_data = []
            
            for pred in predictions:
                training_data.append({
                    'symbol': pred.symbol_name,
                    'timeframe': pred.timeframe,
                    'timestamp': pred.timestamp,
                    'predicted_sentiment': pred.sentiment,
                    'actual_outcome': pred.actual_outcome,
                    'was_correct': pred.was_correct,
                    'confidence': pred.confidence,
                    'price_at_prediction': pred.price_at_prediction,
                    'price_at_verification': pred.price_at_verification
                })
            
            self.logger.info(
                f"Retrieved {len(training_data)} verified predictions for training",
                category="ml_training"
            )
            
            return training_data
            
        except Exception as e:
            self.logger.error(f"Error getting training data: {e}", category="ml_training")
            return None
    
    def _get_verification_window(self, timeframe: str) -> int:
        """
        Get verification window in hours based on timeframe
        
        Args:
            timeframe: Trading timeframe
            
        Returns:
            int: Hours to wait before verification
        """
        windows = {
            'M1': 0.25,   # 15 minutes
            'M5': 0.5,    # 30 minutes
            'M15': 1,     # 1 hour
            'M30': 2,     # 2 hours
            'H1': 4,      # 4 hours
            'H4': 12,     # 12 hours
            'D1': 24,     # 24 hours
            'W1': 168     # 1 week
        }
        
        return windows.get(timeframe, 4)  # Default 4 hours
    
    def _determine_outcome(self, price_change_pct: float) -> str:
        """
        Determine actual outcome based on price change
        
        Args:
            price_change_pct: Price change percentage
            
        Returns:
            str: BULLISH, BEARISH, or NEUTRAL
        """
        # Use same threshold as training (configurable)
        threshold = 0.05  # 0.05% = ~5 pips for major pairs
        
        if price_change_pct > threshold:
            return 'BULLISH'
        elif price_change_pct < -threshold:
            return 'BEARISH'
        else:
            return 'NEUTRAL'
    
    def _get_unverified_count(self) -> int:
        """Get count of unverified predictions"""
        if not self.repository:
            return 0
        
        try:
            predictions = self.repository.get_predictions(
                is_verified=False,
                limit=10000
            )
            return len(predictions)
        except:
            return 0


if __name__ == "__main__":
    # Test tracker
    print("🔍 Testing Prediction Tracker...")
    
    from src.database.repository import get_repository
    
    tracker = PredictionTracker(repository=get_repository())
    
    # Test storing prediction
    pred_id = tracker.store_prediction(
        symbol="EURUSD",
        timeframe="H1",
        sentiment="BULLISH",
        confidence=0.75,
        price_at_prediction=1.0850,
        model_version="v2.0.0_test"
    )
    
    print(f"✓ Stored prediction ID: {pred_id}")
    
    # Test accuracy calculation
    accuracy = tracker.get_recent_accuracy(days=7)
    print(f"✓ Recent accuracy: {accuracy}")
    
    # Test retraining check
    retrain_check = tracker.needs_retraining()
    print(f"✓ Retraining check: {retrain_check}")
    
    print("\n✓ Prediction tracker test completed")
