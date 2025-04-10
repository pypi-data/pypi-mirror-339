"""tangent_client."""

# from tangent_client.anomaly_detection.api import AnomalyDetectionAPI
# from tangent_client.forecasting.api import ForecastingAPI
# from tangent_client.insights.insights import Insights
# from tangent_client.julia_core.connector import JuliaConnector
# from tangent_client.utils.license import TangentLicense
# from tangent_client.utils.spark import (
#     SparkParallelProcessingApi as SparkParallelProcessing,
# )

from tangent_client.client import TangentClient

from ._version import (
    __description__,
    __metadata__,
    __url__,
    __version__,
)

__all__ = [
    "TangentClient",
    "__description__",
    "__metadata__",
    "__url__",
    "__version__",
]


import tangent_client.logging as tc_logging

# setup the logging according to our logging.yaml
tc_logging.initialize()


# class TangentWorks:
#     """
#     Main TangentWorks class wrapping all underlying funcionality.

#     The main entry point for interacting with the Tangent Works library, providing access to

#     forecasting, anomaly detection, insights, license and parellel processing in spark.

#     Attributes:
#         - forecasting (ForecastingAPI):
#             Provides methods for forecasting operations such as model building,
#             predictions, root cause analysis (RCA), and automatic forecasting.

#             Available Methods:
#                 - build_model:
#                     Builds a forecasting model using the provided configuration and dataset.
#                 - predict:
#                     Generates predictions using the given configuration, dataset, and forecasting model.
#                 - rca:
#                     Performs root cause analysis (RCA) to identify potential causes
#                     of anomalies or variations.
#                 - auto_forecast:
#                     Automatically builds a forecasting model and generates predictions in a single step.

#         - anomaly_detection (AnomalyDetectionAPI):
#             Provides methods for anomaly detection, including model building,
#             anomaly detection, and root cause analysis (RCA).

#             Available Methods:
#                 - build_model:
#                     Builds an anomaly detection model using the provided configuration and dataset.
#                 - detect:
#                     Detects anomalies in the provided dataset using
#                     the specified anomaly detection model.
#                 - rca:
#                     Performs root cause analysis (RCA) to identify potential causes
#                     of anomalies in the dataset.

#         - insights (Insights):
#             Provides methods for generating insights and interpreting results.

#             Available Methods:
#                 - properties:
#                     Retrieves and processes the variable properties of the given model,
#                     sorted by importance.
#                 - features:
#                     Extracts and processes the features used in the given model.

#         - license (TangentLicense):
#             Provides methods for working with the Tangent License.

#             Available Methods:
#                 - get_token:
#                     Retrieves the Tangent License token from the environment.
#                 - decode_token:
#                     Decodes the Tangent License token.
#                 - validate_json:
#                     Validates the Tangent License token JSON.
#                 - validate_license:
#                     Validates the Tangent License token.

#         - spark_parallel_processing (SparkParallelProcessing):
#             Provides methods for parallel processing in Spark.

#             Available Methods:
#                 - parallelize:
#                     Parallelizes the given dataset in Spark.
#                 - map:
#                     Maps a function to the given dataset in Spark.
#                 - reduce:
#                     Reduces the given dataset

#     Example Usage:
#         ```python
#         from tangent_works import TangentWorks

#         # Initialize TangentWorks
#         tw = TangentWorks()

#         # Use the ForecastingAPI
#         model = tw.forecasting.build_model(configuration=config, dataset=data)
#         predictions = tw.forecasting.predict(configuration=config, dataset=data, model=model)

#         # Use the AnomalyDetectionAPI
#         anomaly_model = tw.anomaly_detection.build_model(configuration=config, dataset=data)
#         anomalies = tw.anomaly_detection.detect(dataset=data, model=anomaly_model)

#         # Use the Insights API
#         insights = tw.insights.properties(model=model)
#         features = tw.insights.features(model=model)
#         ```

#     """

#     def __init__(self) -> None:
#         self._connector = JuliaConnector()
#         self.forecasting = ForecastingAPI(connector=self._connector)
#         self.anomaly_detection = AnomalyDetectionAPI(connector=self._connector)
#         self.insights = Insights()
#         self.license = TangentLicense()
#         self.spark_parallel_processing = SparkParallelProcessing(app_name="TangentWorks")

#     def __repr__(self) -> str:
#         return f"<{self.__class__.__name__}>"

#     def __str__(self) -> str:
#         return self.__repr__()
