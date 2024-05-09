# Copyright 2024 Sergio Tejedor Moreno

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class WrongColumnName(Exception):
    """Cuando pasas un nombre de columna
    erróneo

    Parameters
    ----------
    Exception : _type_
        _description_
    """


class WrongColumnType(Exception):
    """Cuando intentas hacer una interacción
    con una columna y tiene un tipo objeto
    por ejemplo, que no es correcto

    Parameters
    ----------
    Exception : _type_
        _description_
    """


class DatasetDownloadError(Exception):
    """Cuando se da un error al descargar
    el dataset

    Parameters
    ----------
    Exception : _type_
        _description_
    """


class NonValidDataset(Exception):
    """Cuando se da un error abrir un
    dataset

    Parameters
    ----------
    Exception : _type_
        _description_
    """


class PreProcessorError(Exception):
    """Cuando el preprocesado da error"""


class NonValidPreProcessor(Exception):
    """Preprocesador no válido
    porque no incorpora el método
    fit_transform

    Parameters
    ----------
    Exception : _type_
        _description_
    """


class NonValidModel(Exception):
    """Cuando el modelo no incorpora
    método fit o predict

    Parameters
    ----------
    Exception : _type_
        _description_
    """


class PreProcessorModuleLoadError(Exception):
    """Cuando se intenta cargar el módulo donde
    está el preprocesador y da error

    Parameters
    ----------
    Exception : _type_
        _description_
    """


class ModelModuleLoadError(Exception):
    """Cuando cargas el módulo del modelo
    y da error

    Parameters
    ----------
    Exception : _type_
        _description_
    """


class MissingCompetitionFolderError(Exception):
    """Se lanza cuando al predecir, no existe la carpeta
    con el modelo para ese desafío"""


class PredictionRunError(Exception):
    """Cuando el método run del predictor
    da error"""


class NotFoundTrainDFError(Exception):
    """Cuando no se encuentra el dataset
    train especificado

    Parameters
    ----------
    Exception : _type_
        _description_
    """


class DataConfigError(Exception):
    """Error al abrir el archivo yml
    de configuración de los desafíos

    Parameters
    ----------
    Exception : _type_
        _description_
    """
