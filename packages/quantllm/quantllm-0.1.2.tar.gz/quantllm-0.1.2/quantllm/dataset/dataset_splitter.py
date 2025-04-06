from typing import Tuple, Optional, Union, Dict, Any
import numpy as np
from datasets import Dataset, DatasetDict
from ..finetune.logger import TrainingLogger

class DatasetSplitter:
    """
    A class for splitting datasets into training, validation, and test sets.
    Supports both single datasets and DatasetDict objects.
    """
    
    def __init__(self, logger: TrainingLogger):
        """
        Initialize the DatasetSplitter.
        
        Args:
            logger (TrainingLogger): Logger instance for logging operations
        """
        self.logger = logger
        
    def train_val_test_split(
        self,
        dataset: Union[Dataset, DatasetDict],
        train_size: float = 0.8,
        val_size: float = 0.1,
        test_size: float = 0.1,
        shuffle: bool = True,
        seed: Optional[int] = None,
        **kwargs
    ) -> Tuple[Dataset, Dataset, Dataset]:
        """
        Split a dataset into training, validation, and test sets.
        
        Args:
            dataset (Union[Dataset, DatasetDict]): The dataset to split
            train_size (float): Proportion of the dataset to include in the train split
            val_size (float): Proportion of the dataset to include in the validation split
            test_size (float): Proportion of the dataset to include in the test split
            shuffle (bool): Whether to shuffle the data before splitting
            seed (Optional[int]): Random seed for reproducibility
            **kwargs: Additional arguments to pass to the split function
            
        Returns:
            Tuple[Dataset, Dataset, Dataset]: Training, validation, and test datasets
            
        Raises:
            ValueError: If the split sizes don't sum to 1 or if the dataset is empty
            TypeError: If the dataset type is not supported
        """
        try:
            # Validate split sizes
            total_size = train_size + val_size + test_size
            if not np.isclose(total_size, 1.0):
                raise ValueError(f"Split sizes must sum to 1.0, got {total_size}")
                
            # Handle DatasetDict
            if isinstance(dataset, DatasetDict):
                self.logger.log_info("Processing DatasetDict object")
                if "train" in dataset and "test" in dataset:
                    # If dataset already has train/test splits, use them
                    train_dataset = dataset["train"]
                    test_dataset = dataset["test"]
                    
                    # If validation split exists, use it; otherwise split from train
                    if "validation" in dataset:
                        val_dataset = dataset["validation"]
                    else:
                        val_size_relative = val_size / (train_size + val_size)
                        train_dataset, val_dataset = train_dataset.train_test_split(
                            test_size=val_size_relative,
                            shuffle=shuffle,
                            seed=seed,
                            **kwargs
                        ).values()
                        
                elif "train" in dataset:
                    # If only train split exists, split it into train/val/test
                    train_dataset = dataset["train"]
                    val_size_relative = val_size / (1 - test_size)
                    train_dataset, val_dataset = train_dataset.train_test_split(
                        test_size=val_size_relative,
                        shuffle=shuffle,
                        seed=seed,
                        **kwargs
                    ).values()
                    test_dataset = None
                else:
                    raise ValueError("DatasetDict must contain at least a 'train' split")
                    
            # Handle single Dataset
            elif isinstance(dataset, Dataset):
                self.logger.log_info("Processing single Dataset object")
                if len(dataset) == 0:
                    raise ValueError("Cannot split an empty dataset")
                    
                # First split into train and temp (val + test)
                temp_size = val_size + test_size
                train_dataset, temp_dataset = dataset.train_test_split(
                    test_size=temp_size,
                    shuffle=shuffle,
                    seed=seed,
                    **kwargs
                ).values()
                
                # Then split temp into val and test
                val_size_relative = val_size / temp_size
                val_dataset, test_dataset = temp_dataset.train_test_split(
                    test_size=val_size_relative,
                    shuffle=shuffle,
                    seed=seed,
                    **kwargs
                ).values()
                
            else:
                raise TypeError(f"Unsupported dataset type: {type(dataset)}")
                
            self.logger.log_info(
                f"Dataset split successfully. Sizes: "
                f"Train: {len(train_dataset)}, "
                f"Val: {len(val_dataset)}, "
                f"Test: {len(test_dataset)}"
            )
            
            return train_dataset, val_dataset, test_dataset
            
        except Exception as e:
            self.logger.log_error(f"Error splitting dataset: {str(e)}")
            raise
            
    def train_test_split(
        self,
        dataset: Union[Dataset, DatasetDict],
        test_size: float = 0.2,
        shuffle: bool = True,
        seed: Optional[int] = None,
        **kwargs
    ) -> Tuple[Dataset, Dataset]:
        """
        Split a dataset into training and test sets.
        
        Args:
            dataset (Union[Dataset, DatasetDict]): The dataset to split
            test_size (float): Proportion of the dataset to include in the test split
            shuffle (bool): Whether to shuffle the data before splitting
            seed (Optional[int]): Random seed for reproducibility
            **kwargs: Additional arguments to pass to the split function
            
        Returns:
            Tuple[Dataset, Dataset]: Training and test datasets
        """
        try:
            # Handle DatasetDict
            if isinstance(dataset, DatasetDict):
                if "train" in dataset and "test" in dataset:
                    return dataset["train"], dataset["test"]
                elif "train" in dataset:
                    return dataset["train"].train_test_split(
                        test_size=test_size,
                        shuffle=shuffle,
                        seed=seed,
                        **kwargs
                    ).values()
                else:
                    raise ValueError("DatasetDict must contain at least a 'train' split")
                    
            # Handle single Dataset
            elif isinstance(dataset, Dataset):
                if len(dataset) == 0:
                    raise ValueError("Cannot split an empty dataset")
                return dataset.train_test_split(
                    test_size=test_size,
                    shuffle=shuffle,
                    seed=seed,
                    **kwargs
                ).values()
                
            else:
                raise TypeError(f"Unsupported dataset type: {type(dataset)}")
                
        except Exception as e:
            self.logger.log_error(f"Error in train_test_split: {str(e)}")
            raise
            
    def k_fold_split(
        self,
        dataset: Dataset,
        n_splits: int = 5,
        shuffle: bool = True,
        seed: int = 42,
        **kwargs
    ) -> list:
        """
        Split dataset into k folds.
        
        Args:
            dataset (Dataset): Dataset to split
            n_splits (int): Number of folds
            shuffle (bool): Whether to shuffle
            seed (int): Random seed
            **kwargs: Additional splitting arguments
            
        Returns:
            list: List of (train, test) dataset tuples
        """
        try:
            self.logger.log_info(f"Splitting dataset into {n_splits} folds")
            
            # Convert to pandas for k-fold split
            df = dataset.to_pandas()
            
            from sklearn.model_selection import KFold
            kf = KFold(n_splits=n_splits, shuffle=shuffle, random_state=seed)
            
            folds = []
            for train_idx, test_idx in kf.split(df):
                train_df = df.iloc[train_idx]
                test_df = df.iloc[test_idx]
                
                train_dataset = Dataset.from_pandas(train_df, **kwargs)
                test_dataset = Dataset.from_pandas(test_df, **kwargs)
                
                folds.append((train_dataset, test_dataset))
                
            self.logger.log_info("Successfully created k-fold splits")
            return folds
            
        except Exception as e:
            self.logger.log_error(f"Error creating k-fold splits: {str(e)}")
            raise 