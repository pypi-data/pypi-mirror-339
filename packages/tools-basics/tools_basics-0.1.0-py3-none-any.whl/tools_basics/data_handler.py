from datasets import load_dataset
import pandas as pd
import os

from omegaconf import OmegaConf


class DataHandler:
    """Class to load the IMDB dataset from the Hugging Face datasets library"""
    def __init__(self, conf: OmegaConf) -> None:
        self.conf = conf
        self.dataset = self.conf.dataset
        self.train_path, self.test_path = self.conf.path.train, self.conf.path.test

    def get_data(self, force_reload: bool = False) -> tuple:
        """Return the train and test dataframes"""
        if os.path.exists(self.train_path) and not force_reload:
            print('Loading saved data')
            train_df = pd.read_csv(self.train_path)
            test_df = pd.read_csv(self.test_path)
        else:
            print('Loading data from Hugging Face')
            imdb = load_dataset(self.dataset)
            train_df = pd.DataFrame(imdb['train'])
            test_df = pd.DataFrame(imdb['test'])
        return train_df, test_df
    
    def _save_df(self, df: pd.DataFrame, path: str) -> None:
        """Save the data to a file"""
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            print(f'Creating folder {folder}')
            os.makedirs(folder)
            
        df.to_csv(path, index=False)
    
    def save_data(self, train_df: pd.DataFrame, test_df: pd.DataFrame) -> None:
        """Save the train and test dataframes to CSV"""
        self._save_df(train_df, self.train_path)
        self._save_df(test_df, self.test_path)
