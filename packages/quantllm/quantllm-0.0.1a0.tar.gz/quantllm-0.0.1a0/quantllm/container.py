from typing import Dict, Any, Type, Optional
from .model import ModelLoader
from .data import DatasetProcessor
from .trainer import FineTuningTrainer, ModelEvaluator, TrainingLogger
from .hub import HubManager, CheckpointManager
from .config import ModelConfig, DatasetConfig, TrainingConfig, EvaluationConfig

class Container:
    """Dependency Injection Container for QuantLLM."""
    
    def __init__(self):
        self._instances: Dict[Type, Any] = {}
        self._configs: Dict[str, Any] = {}
        
    def register_config(self, name: str, config: Any) -> None:
        """Register a configuration instance."""
        self._configs[name] = config
        
    def get_config(self, name: str) -> Any:
        """Get a configuration instance."""
        if name not in self._configs:
            raise KeyError(f"Configuration {name} not registered")
        return self._configs[name]
        
    def get_model_loader(self) -> ModelLoader:
        """Get or create ModelLoader instance."""
        if ModelLoader not in self._instances:
            model_config = self.get_config("model")
            self._instances[ModelLoader] = ModelLoader(model_config)
        return self._instances[ModelLoader]
        
    def get_dataset_processor(self) -> DatasetProcessor:
        """Get or create DatasetProcessor instance."""
        if DatasetProcessor not in self._instances:
            dataset_config = self.get_config("dataset")
            self._instances[DatasetProcessor] = DatasetProcessor(dataset_config)
        return self._instances[DatasetProcessor]
        
    def get_trainer(self, model, tokenizer, dataset) -> FineTuningTrainer:
        """Create new FineTuningTrainer instance."""
        training_config = self.get_config("training")
        return FineTuningTrainer(training_config, model, tokenizer, dataset)
        
    def get_evaluator(self, model, tokenizer) -> ModelEvaluator:
        """Create new ModelEvaluator instance."""
        eval_config = self.get_config("evaluation")
        return ModelEvaluator(model, tokenizer, eval_config)
        
    def get_logger(self) -> TrainingLogger:
        """Get or create TrainingLogger instance."""
        if TrainingLogger not in self._instances:
            training_config = self.get_config("training")
            self._instances[TrainingLogger] = TrainingLogger(
                log_dir=training_config.output_dir,
                use_wandb=training_config.use_wandb,
                wandb_config=training_config.wandb_config
            )
        return self._instances[TrainingLogger]
        
    def get_hub_manager(self) -> Optional[HubManager]:
        """Get or create HubManager instance if hub pushing is enabled."""
        if HubManager not in self._instances:
            model_config = self.get_config("model")
            if model_config.push_to_hub:
                self._instances[HubManager] = HubManager(
                    model_id=model_config.model_name,
                    token=model_config.hub_token,
                    organization=model_config.hub_organization
                )
        return self._instances.get(HubManager)