from collections import defaultdict
import numpy as np
from ddi_fw.datasets.core import BaseDataset
from ddi_fw.vectorization.idf_helper import IDF
from typing import Any, Dict, List, Optional
from itertools import product

from ddi_fw.ml.ml_helper import MultiModalRunner
from ddi_fw.utils.enums import DrugBankTextDataTypes, UMLSCodeTypes
import mlflow
from ddi_fw.ner.ner import CTakesNER


def stack(df_column):
    return np.stack(df_column.values)


class NerParameterSearch:
    def __init__(self,
                 library,
                 multi_modal,
                 experiment_name,
                 experiment_description,
                 experiment_tags,
                 tracking_uri,
                 dataset_type: BaseDataset,
                 ner_data_file,
                 columns: list,
                 umls_code_types: List[UMLSCodeTypes]|None,
                 text_types:List[DrugBankTextDataTypes]|None,
                 min_threshold_dict: Dict[str, float] = defaultdict(float),
                 max_threshold_dict: Dict[str, float] = defaultdict(float),
                 increase_step=0.5):
        self.library = library
        self.multi_modal = multi_modal
        self.experiment_name = experiment_name
        self.experiment_description = experiment_description
        self.experiment_tags = experiment_tags
        self.tracking_uri = tracking_uri

        self.dataset_type = dataset_type
        self.ner_data_file = ner_data_file
        self.columns = columns
        self.umls_code_types = umls_code_types
        self.text_types = text_types

        self.min_threshold_dict = min_threshold_dict
        self.max_threshold_dict = max_threshold_dict
        self.increase_step = increase_step

    def build(self):
        if not isinstance(self.dataset_type, type):
            raise TypeError("self.dataset_type must be a class, not an instance")
        self.datasets = {}
        self.items = []
        # columns = ['tui', 'cui', 'entities']
        if self.umls_code_types is not None and self.text_types is not None:
            # add checking statements
            _umls_codes = [t.value[0] for t in self.umls_code_types]
            _text_types = [t.value[0] for t in self.text_types]
            _columns = [f'{item[0]}_{item[1]}' for item in product(
                _umls_codes, _text_types)]
            self.columns.extend(_columns)
        print(f'Columns: {self.columns}')
        self.ner_df = CTakesNER(df = None).load(
            filename=self.ner_data_file) if self.ner_data_file else None

        if not self.min_threshold_dict or not self.max_threshold_dict:
            idf2 = IDF(self.ner_df, self.columns)
            idf2.calculate()
            # df = pd.DataFrame.from_dict(idf2.idf_scores)
            df = idf2.to_dataframe()
            import math
            self.min_threshold_dict = {key: math.floor(
                df.describe()[key]['min']) for key in df.describe().keys()}
            self.max_threshold_dict = {key: math.ceil(
                df.describe()[key]['max']) for key in df.describe().keys()}

        train_idx_arr, val_idx_arr = None, None
        for column in self.columns:
            min_threshold = self.min_threshold_dict[column]
            max_threshold = self.max_threshold_dict[column]
            kwargs = {}
            kwargs['threshold_method'] = 'idf'
            kwargs['tui_threshold'] = 0
            kwargs['cui_threshold'] = 0
            kwargs['entities_threshold'] = 0

            for threshold in np.arange(min_threshold, max_threshold, self.increase_step):
                print(threshold)
                if column.startswith('tui'):
                    kwargs['tui_threshold'] = threshold
                if column.startswith('cui'):
                    kwargs['cui_threshold'] = threshold
                if column.startswith('entities'):
                    kwargs['entities_threshold'] = threshold
                dataset = self.dataset_type(
                    # chemical_property_columns=[],
                    # embedding_columns=[],
                    # ner_columns=[column],
                    columns=[column],
                    ner_df=self.ner_df,
                    embedding_size=None,
                    embedding_dict=None,
                    embeddings_pooling_strategy=None,
                    **kwargs)

                # train_idx_arr, val_idx_arr  bir kez hesaplanması yeterli aslında
                dataset.load()
                group_items = dataset.produce_inputs()
                for item in group_items:
                    # item[0] = f'threshold_{threshold}_{item[0]}'
                    item[0] = f'threshold_{item[0]}_{threshold}'
                    self.datasets[item[0]] = dataset.ddis_df

                self.items.extend(group_items)
        self.y_test_label = self.items[0][4]
        self.train_idx_arr = dataset.train_idx_arr
        self.val_idx_arr = dataset.val_idx_arr

    def run(self, model_func, batch_size=128, epochs=100):
        mlflow.set_tracking_uri(self.tracking_uri)

        if mlflow.get_experiment_by_name(self.experiment_name) == None:
            mlflow.create_experiment(self.experiment_name)
            mlflow.set_experiment_tags(self.experiment_tags)
        mlflow.set_experiment(self.experiment_name)

        y_test_label = self.items[0][4]
        multi_modal_runner = MultiModalRunner(
            library=self.library, multi_modal=self.multi_modal)
        # multi_modal_runner = MultiModalRunner(
        #     library=self.library, model_func=model_func, batch_size=batch_size,  epochs=epochs)
        multi_modal_runner.set_data(
            self.items, self.train_idx_arr, self.val_idx_arr, y_test_label)
        result = multi_modal_runner.predict()
        
         
        return result
