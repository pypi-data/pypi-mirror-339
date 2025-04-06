from datasets import Dataset
from typing import Optional, Dict, Any, Callable
from transformers import PreTrainedTokenizer
from ..trainer.logger import TrainingLogger

class DatasetPreprocessor:
    def __init__(self, tokenizer, logger=None):
        self.tokenizer = tokenizer
        self.logger = logger or TrainingLogger()
        
    def validate_datasets(self, datasets):
        """Validate input datasets."""
        for dataset in datasets:
            if dataset is not None and not isinstance(dataset, Dataset):
                raise ValueError(f"Expected Dataset object, got {type(dataset)}")
                
    def tokenize_dataset(
        self,
        train_dataset,
        val_dataset=None,
        test_dataset=None,
        max_length: int = 512,
        text_column: str = "text",
        label_column: str = None,
        batch_size: int = 1000
    ):
        """Tokenize datasets with batching and error handling."""
        try:
            # Validate inputs
            self.validate_datasets([train_dataset, val_dataset, test_dataset])
            
            if not text_column in train_dataset.column_names:
                raise ValueError(f"Text column '{text_column}' not found in dataset")
                
            if label_column and not label_column in train_dataset.column_names:
                raise ValueError(f"Label column '{label_column}' not found in dataset")
                
            def tokenize_batch(examples):
                texts = examples[text_column]
                if not isinstance(texts, list):
                    texts = [texts]
                    
                # Handle empty or invalid texts
                texts = [str(text).strip() if text else "" for text in texts]
                
                try:
                    tokenized = self.tokenizer(
                        texts,
                        padding=True,
                        truncation=True,
                        max_length=max_length,
                        return_tensors="pt"
                    )
                except Exception as e:
                    self.logger.log_warning(f"Error tokenizing batch: {str(e)}")
                    # Return empty tensors with correct shape for failed tokenization
                    return {
                        "input_ids": [[self.tokenizer.pad_token_id] * max_length] * len(texts),
                        "attention_mask": [[0] * max_length] * len(texts)
                    }
                
                result = {
                    "input_ids": tokenized["input_ids"],
                    "attention_mask": tokenized["attention_mask"]
                }
                
                if label_column:
                    result["labels"] = examples[label_column]
                    
                return result
                
            # Process datasets
            train_dataset = train_dataset.map(
                tokenize_batch,
                batched=True,
                batch_size=batch_size,
                remove_columns=train_dataset.column_names
            )
            
            if val_dataset is not None:
                val_dataset = val_dataset.map(
                    tokenize_batch,
                    batched=True,
                    batch_size=batch_size,
                    remove_columns=val_dataset.column_names
                )
                
            if test_dataset is not None:
                test_dataset = test_dataset.map(
                    tokenize_batch,
                    batched=True,
                    batch_size=batch_size,
                    remove_columns=test_dataset.column_names
                )
                
            self.logger.log_info("Successfully tokenized all datasets")
            return train_dataset, val_dataset, test_dataset
            
        except Exception as e:
            self.logger.log_error(f"Error tokenizing dataset: {str(e)}")
            raise
            
    def preprocess_text(self, dataset, text_column: str, processors: list = None):
        """Apply text preprocessing steps."""
        try:
            if processors is None:
                processors = [
                    str.lower,
                    str.strip
                ]
                
            def process_text(example):
                text = example[text_column]
                for processor in processors:
                    text = processor(text)
                example[text_column] = text
                return example
                
            dataset = dataset.map(process_text)
            return dataset
            
        except Exception as e:
            self.logger.log_error(f"Error preprocessing text: {str(e)}")
            raise