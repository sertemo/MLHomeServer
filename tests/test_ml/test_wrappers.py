from pathlib import Path

from mlhomeserver.ml.utilities.wrappers import SerializableMixin, DeserializableMixin

def test_save_with_serializablemixin(tmp_path):

    se = SerializableMixin()
    se.value = {"meaning_of_life": 42}

    path_file = tmp_path / "life"
    path_file.mkdir(parents=True, exist_ok=True)

    model_path: Path = path_file / "model.joblib"
    print("Antes de crearlo, existe ?", model_path.exists())

    se.save(model_path)

    assert model_path.exists()


def test_deserializablemixin(tmp_path):

    se = SerializableMixin()
    se.value = {"meaning_of_life": 42}

    path_file = tmp_path / "life"
    path_file.mkdir(parents=True, exist_ok=True)

    model_path: Path = path_file / "model.joblib"
    print("Antes de crearlo, existe ?", model_path.exists())

    se.save(model_path)

    de = DeserializableMixin.load(model_path)

    assert de.value == {"meaning_of_life": 42}