
import pandas as pd
import pytest
from unittest.mock import MagicMock, patch

from mlhomeserver.ml.training.train import Training
from mlhomeserver.exceptions import PreProcessorError, NonValidDataset, NotFoundTrainDFError

def test_trainer_bad_preprocessor_aidtec(trainer_bad_preprocessor):
    with pytest.raises(PreProcessorError):
        trainer_bad_preprocessor.run()

def test_trainer_no_labels_dataframe_aidtec(trainer_bad_preprocessor):
    with patch('mlhomeserver.ml.training.trainer.Trainer._open_dt', return_value=pd.DataFrame()):
        with pytest.raises(NonValidDataset):
            trainer_bad_preprocessor.run()

def test_trainer_dataset_doesnot_exists(trainer_bad_dataframe):
    with pytest.raises(NotFoundTrainDFError):
        trainer_bad_dataframe.run()

def test_train_function_calls_run(mock_trainer):
    trainer_mock = mock_trainer.return_value
    trainer_mock.run.return_value = 'Mocked'

    t = Training()
    t._setup_parser = MagicMock()
    t._setup_parser().parse_args.return_value = MagicMock(desafio='aidtec')

    t.train()

    trainer_mock.run.assert_called_once()



