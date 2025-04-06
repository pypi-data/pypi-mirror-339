from typing import Optional, Union, Dict, Any, Tuple, Callable
import torch
from datasets import Dataset
from transformers import PreTrainedTokenizer
from ..finetune.logger import TrainingLogger
from ..config import DatasetConfig

class DatasetPreprocessor:
    """
    A class for preprocessing datasets for language model training.
    Handles tokenization and formatting of input data.
    """
    
    def __init__(
        self,
        tokenizer: PreTrainedTokenizer,
        logger: TrainingLogger,
        config: Optional[DatasetConfig] = None
    ):
        """
        Initialize the DatasetPreprocessor.
        
        Args:
            tokenizer (PreTrainedTokenizer): Tokenizer to use for preprocessing
            logger (TrainingLogger): Logger instance for logging operations
            config (Optional[DatasetConfig]): Dataset configuration
        """
        self.tokenizer = tokenizer
        self.logger = logger
        self.config = config
        
    def tokenize_dataset(
        self,
        train_dataset: Dataset,
        val_dataset: Optional[Dataset] = None,
        test_dataset: Optional[Dataset] = None,
        config: Optional[DatasetConfig] = None
    ) -> Union[Dataset, Tuple[Dataset, Dataset, Dataset]]:
        """
        Tokenize one or more datasets.
        
        Args:
            train_dataset (Dataset): Training dataset
            val_dataset (Optional[Dataset]): Validation dataset
            test_dataset (Optional[Dataset]): Test dataset
            config (Optional[DatasetConfig]): Dataset configuration
            
        Returns:
            Union[Dataset, Tuple[Dataset, Dataset, Dataset]]: 
                Single tokenized dataset or tuple of tokenized datasets
        """
        try:
            # Use provided config or instance config
            config = config or self.config
            if config is None:
                raise ValueError("DatasetConfig must be provided either during initialization or method call")
                
            self.logger.log_info("Starting dataset tokenization")
            
            def tokenize_function(examples):
                # Tokenize the texts
                tokenized = self.tokenizer(
                    examples[config.text_column],
                    padding="max_length",
                    truncation=True,
                    max_length=config.max_length,
                    return_tensors="pt"
                )
                
                # Add labels if they exist
                if config.label_column in examples:
                    tokenized["labels"] = examples[config.label_column]
                    
                return tokenized
                
            # Tokenize training dataset
            self.logger.log_info("Tokenizing training dataset")
            train_dataset = train_dataset.map(
                tokenize_function,
                batched=True,
                remove_columns=train_dataset.column_names
            )
            
            if val_dataset is None and test_dataset is None:
                return train_dataset
                
            datasets = [train_dataset]
            
            # Tokenize validation dataset if provided
            if val_dataset is not None:
                self.logger.log_info("Tokenizing validation dataset")
                val_dataset = val_dataset.map(
                    tokenize_function,
                    batched=True,
                    remove_columns=val_dataset.column_names
                )
                datasets.append(val_dataset)
                
            # Tokenize test dataset if provided
            if test_dataset is not None:
                self.logger.log_info("Tokenizing test dataset")
                test_dataset = test_dataset.map(
                    tokenize_function,
                    batched=True,
                    remove_columns=test_dataset.column_names
                )
                datasets.append(test_dataset)
                
            self.logger.log_info("Dataset tokenization completed successfully")
            return tuple(datasets)
            
        except Exception as e:
            self.logger.log_error(f"Error in dataset tokenization: {str(e)}")
            raise
            
    def format_dataset(
        self,
        dataset: Dataset,
        config: Optional[DatasetConfig] = None
    ) -> Dataset:
        """
        Format a dataset for training.
        
        Args:
            dataset (Dataset): Dataset to format
            config (Optional[DatasetConfig]): Dataset configuration
            
        Returns:
            Dataset: Formatted dataset
        """
        try:
            # Use provided config or instance config
            config = config or self.config
            if config is None:
                raise ValueError("DatasetConfig must be provided either during initialization or method call")
                
            self.logger.log_info("Formatting dataset")
            
            def format_function(examples):
                # Format the examples according to the model's requirements
                formatted = {
                    "input_ids": examples["input_ids"],
                    "attention_mask": examples["attention_mask"]
                }
                
                if "labels" in examples:
                    formatted["labels"] = examples["labels"]
                    
                return formatted
                
            formatted_dataset = dataset.map(
                format_function,
                batched=True,
                remove_columns=dataset.column_names
            )
            
            self.logger.log_info("Dataset formatting completed successfully")
            return formatted_dataset
            
        except Exception as e:
            self.logger.log_error(f"Error formatting dataset: {str(e)}")
            raise
            
    def apply_custom_preprocessing(
        self,
        dataset: Dataset,
        preprocessing_function: Callable,
        **kwargs
    ) -> Dataset:
        """
        Apply custom preprocessing to dataset.
        
        Args:
            dataset (Dataset): Dataset to preprocess
            preprocessing_function (Callable): Preprocessing function
            **kwargs: Additional preprocessing arguments
            
        Returns:
            Dataset: Preprocessed dataset
        """
        try:
            self.logger.log_info("Applying custom preprocessing")
            processed_dataset = dataset.map(
                preprocessing_function,
                **kwargs
            )
            self.logger.log_info("Successfully applied custom preprocessing")
            return processed_dataset
            
        except Exception as e:
            self.logger.log_error(f"Error in custom preprocessing: {str(e)}")
            raise
            
    def filter_dataset(
        self,
        dataset: Dataset,
        filter_function: Callable,
        **kwargs
    ) -> Dataset:
        """
        Filter dataset based on criteria.
        
        Args:
            dataset (Dataset): Dataset to filter
            filter_function (Callable): Filter function
            **kwargs: Additional filtering arguments
            
        Returns:
            Dataset: Filtered dataset
        """
        try:
            self.logger.log_info("Filtering dataset")
            filtered_dataset = dataset.filter(
                filter_function,
                **kwargs
            )
            self.logger.log_info("Successfully filtered dataset")
            return filtered_dataset
            
        except Exception as e:
            self.logger.log_error(f"Error filtering dataset: {str(e)}")
            raise 