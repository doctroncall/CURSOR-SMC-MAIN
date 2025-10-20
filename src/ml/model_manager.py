"""
Model Manager
Manages ML model lifecycle, storage, and deployment
"""
import joblib
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from .training import ModelTrainer
from .evaluator import ModelEvaluator
from config.settings import MLConfig, MODELS_DIR
from src.database.repository import DatabaseRepository
from src.utils.logger import get_logger

logger = get_logger()


class ModelManager:
    """
    Manage ML model lifecycle
    
    Features:
    - Model training and retraining
    - Model storage and loading
    - Version management
    - Performance tracking
    - Model deployment
    """
    
    def __init__(self, repository: Optional[DatabaseRepository] = None):
        """Initialize model manager"""
        self.trainer = ModelTrainer()
        self.evaluator = ModelEvaluator()
        self.repository = repository
        self.config = MLConfig
        self.logger = logger
        
        # Ensure models directory exists
        MODELS_DIR.mkdir(exist_ok=True)
        
        self.active_model = None
        self.active_scaler = None
    
    def train_new_model(
        self,
        df,
        version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Train a new model
        
        Args:
            df: Training data DataFrame
            version: Model version string
            
        Returns:
            Dict with training results
        """
        try:
            version = version or self._generate_version()
            
            self.logger.info(f"Training new model {version}", category="ml_training")
            
            # Prepare data
            X, y = self.trainer.prepare_training_data(df)
            
            # Train model
            result = self.trainer.train_model(X, y, version)
            
            # Save model
            self.save_model(
                result['model'],
                result['scaler'],
                version,
                result
            )
            
            # Save to database if repository provided
            if self.repository:
                self._save_to_database(result)
            
            self.logger.info(f"Model {version} trained and saved", category="ml_training")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error training new model: {str(e)}", category="ml_training")
            raise
    
    def save_model(
        self,
        model,
        scaler,
        version: str,
        metadata: Dict[str, Any]
    ) -> bool:
        """Save model to disk"""
        try:
            # Save model
            model_path = MODELS_DIR / f"model_{version}.joblib"
            joblib.dump(model, model_path)
            
            # Save scaler
            scaler_path = MODELS_DIR / f"scaler_{version}.joblib"
            joblib.dump(scaler, scaler_path)
            
            # Save metadata
            metadata_path = MODELS_DIR / f"metadata_{version}.json"
            
            # Convert datetime to string
            meta_dict = {
                k: str(v) if isinstance(v, datetime) else v
                for k, v in metadata.items()
                if k not in ['model', 'scaler']  # Exclude model objects
            }
            
            with open(metadata_path, 'w') as f:
                json.dump(meta_dict, f, indent=2)
            
            self.logger.info(f"Model {version} saved to {model_path}", category="ml_training")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving model: {str(e)}", category="ml_training")
            return False
    
    def load_model(self, version: str) -> bool:
        """Load model from disk"""
        try:
            model_path = MODELS_DIR / f"model_{version}.joblib"
            scaler_path = MODELS_DIR / f"scaler_{version}.joblib"
            
            if not model_path.exists() or not scaler_path.exists():
                self.logger.warning(f"Model {version} not found", category="ml_training")
                return False
            
            self.active_model = joblib.load(model_path)
            self.active_scaler = joblib.load(scaler_path)
            
            self.logger.info(f"Model {version} loaded successfully", category="ml_training")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading model: {str(e)}", category="ml_training")
            return False
    
    def predict(self, X, return_proba: bool = False):
        """Make prediction with active model"""
        if self.active_model is None:
            raise ValueError("No active model loaded")
        
        X_scaled = self.active_scaler.transform(X)
        
        if return_proba:
            return self.active_model.predict_proba(X_scaled)
        else:
            return self.active_model.predict(X_scaled)
    
    def _generate_version(self) -> str:
        """Generate version string"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"v_{timestamp}"
    
    def _save_to_database(self, result: Dict[str, Any]):
        """Save model metadata to database"""
        if not self.repository:
            return
        
        try:
            # Convert feature importance to JSON string
            feature_importance_json = json.dumps(result.get('feature_importance', {}))
            
            self.repository.create_model_version(
                version=result['version'],
                model_type='ensemble',
                training_date=result['training_date'],
                training_samples=result['training_samples'],
                training_duration_seconds=result['training_duration'],
                train_accuracy=result['train_accuracy'],
                test_accuracy=result['test_accuracy'],
                validation_accuracy=result.get('cv_mean', 0.0),
                feature_importance=feature_importance_json,
                is_active=True
            )
            
        except Exception as e:
            self.logger.error(f"Error saving to database: {str(e)}", category="ml_training")
    
    def list_models(self) -> list:
        """List all saved models"""
        model_files = list(MODELS_DIR.glob("model_*.joblib"))
        versions = [f.stem.replace("model_", "") for f in model_files]
        return sorted(versions, reverse=True)


if __name__ == "__main__":
    # Test model manager
    print("🎯 Testing Model Manager...")
    
    manager = ModelManager()
    
    # List models
    models = manager.list_models()
    print(f"✓ Found {len(models)} saved models")
    
    print("\n✓ Model manager test completed")
