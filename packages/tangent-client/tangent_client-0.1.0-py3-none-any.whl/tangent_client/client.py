"""tangent_client.client."""

import io
import json
import os

import pandas as pd
import requests

TANGENT_API_SERVER = os.getenv("TANGENT_API_SERVER", "https://api.tangent.works/")
TANGENT_LICENSE = os.getenv("TANGENT_LICENSE", "")
TANGENT_API_TIMEOUT = os.getenv("TANGENT_API_TIMEOUT", "90")


class TangentClient:
    """Client for the Tangent API."""

    def __init__(self, server: str = "", token: str = "", timeout: str | int = "") -> None:
        self.server = server or TANGENT_API_SERVER
        self.token = token or TANGENT_LICENSE
        self.timeout = int(timeout or TANGENT_API_TIMEOUT)

        self.auto_forecast = AutoForecastClient(self.server, self.token)
        self.forecasting = ForecastingClient(self.server, self.token)
        self.anomaly_detection = AnomalyDetectionClient(server, token)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} server={self.server} timeout={self.timeout}>"

    def __str__(self) -> str:
        return self.__repr__()


class AutoForecastClient:
    def __init__(self, server: str = "", token: str = "", timeout: str | int = "90") -> None:
        self.server = server or TANGENT_API_SERVER
        self.token = token or TANGENT_LICENSE
        self.timeout = int(timeout) or int(TANGENT_API_TIMEOUT)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} server={self.server} timeout={self.timeout}>"

    def __str__(self) -> str:
        return self.__repr__()

    def run(self, configuration, dataset):
        url = self.server + "/auto-forecast"
        headers = {"Authorization": self.token}
        configuration_file = json.dumps(configuration)
        dataset_file = dataset.to_csv(index=False)
        resp = requests.request(
            method="POST",
            url=url,
            headers=headers,
            files={
                "dataset": ("dataset", dataset_file, "text/csv"),
                "configuration": (
                    "configuration",
                    configuration_file,
                    "application/json",
                ),
            },
            timeout=self.timeout,
        )
        return resp.json()

    def status(self, id):
        url = self.server + f"/auto-forecast/{id}"
        headers = {"Authorization": self.token}
        resp = requests.request(method="GET", url=url, headers=headers, timeout=self.timeout)
        return resp.json()

    def results(self, id):
        url = self.server + f"/auto-forecast/{id}/results"
        headers = {"Authorization": self.token}
        resp = requests.request(method="GET", url=url, headers=headers, timeout=self.timeout)
        return pd.read_csv(io.StringIO(resp.text))


class AnomalyDetectionClient:
    """Client for the Tangent AnomalyDetection API."""

    def __init__(self, server: str = "", token: str = "", timeout: str | int = "90") -> None:
        self.server = server or TANGENT_API_SERVER
        self.token = token or TANGENT_LICENSE
        self.timeout = int(timeout) or int(TANGENT_API_TIMEOUT)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} server={self.server} timeout={self.timeout}>"

    def __str__(self) -> str:
        return self.__repr__()

    def build_model(self, configuration, dataset):
        url = self.server + "/anomaly-detection/build-model"
        headers = {"Authorization": self.token}
        configuration_file = json.dumps(configuration)
        dataset_file = dataset.to_csv(index=False)
        resp = requests.request(
            method="POST",
            url=url,
            headers=headers,
            timeout=self.timeout,
            files={
                "dataset": ("dataset", dataset_file, "text/csv"),
                "configuration": (
                    "configuration",
                    configuration_file,
                    "application/json",
                ),
            },
        )
        return resp.json()

    def detect(self, model, dataset):
        url = self.server + "/anomaly-detection/detect"
        headers = {"Authorization": self.token}
        model_file = json.dumps(model)
        dataset_file = dataset.to_csv(index=False)
        resp = requests.request(
            method="POST",
            url=url,
            headers=headers,
            timeout=self.timeout,
            files={
                "dataset": ("dataset", dataset_file, "text/csv"),
                "model": ("model", model_file, "application/json"),
            },
        )
        return resp.json()

    def status(self, id):
        url = self.server + f"/anomaly-detection/{id}"
        headers = {"Authorization": self.token}
        resp = requests.request(method="GET", url=url, headers=headers, timeout=self.timeout)
        return resp.json()

    def model(self, id):
        url = self.server + f"/anomaly-detection/{id}/model"
        headers = {"Authorization": self.token}
        resp = requests.request(method="GET", url=url, headers=headers, timeout=self.timeout)
        return resp.json()

    def results(self, id):
        url = self.server + f"/anomaly-detection/{id}/results"
        headers = {"Authorization": self.token}
        resp = requests.request(method="GET", url=url, headers=headers, timeout=self.timeout)
        return pd.read_csv(io.StringIO(resp.text))

    def rca(self, configuration, model, dataset):
        url = self.server + "/anomaly-detection/rca"
        headers = {"Authorization": self.token}
        configuration_file = json.dumps(configuration)
        model_file = json.dumps(model)
        dataset_file = dataset.to_csv(index=False)
        resp = requests.request(
            method="POST",
            url=url,
            headers=headers,
            timeout=self.timeout,
            files={
                "configuration": (
                    "configuration",
                    configuration_file,
                    "application/json",
                ),
                "model": ("model", model_file, "application/json"),
                "dataset": ("dataset", dataset_file, "text/csv"),
            },
        )
        return resp.json()

    def rca_results(self, id):
        url = self.server + f"/anomaly-detection/{id}/rca-table"
        headers = {"Authorization": self.token}
        resp = requests.request(method="GET", url=url, headers=headers, timeout=self.timeout)
        rca_json = json.loads(resp.text)
        output = []
        for model_index in rca_json.keys():
            rca_json[model_index]
            rca_df = pd.read_csv(io.StringIO(rca_json[model_index]))
            output.append({model_index: rca_df})
        return output


class ForecastingClient:
    """Client for the Tangent Forecasting API."""

    def __init__(self, server: str = "", token: str = "", timeout: str | int = "90") -> None:
        self.server = server
        self.token = token
        self.timeout = int(timeout) or int(TANGENT_API_TIMEOUT)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} server={self.server} timeout={self.timeout}>"

    def __str__(self) -> str:
        return self.__repr__()

    def build_model(self, configuration, dataset):
        url = self.server + "/forecast/build-model"
        headers = {"Authorization": self.token}
        configuration_file = json.dumps(configuration)
        dataset_file = dataset.to_csv(index=False)
        resp = requests.request(
            method="POST",
            url=url,
            headers=headers,
            timeout=self.timeout,
            files={
                "dataset": ("dataset", dataset_file, "text/csv"),
                "configuration": (
                    "configuration",
                    configuration_file,
                    "application/json",
                ),
            },
        )
        return resp.json()

    def predict(self, configuration, model, dataset):
        url = self.server + "/forecast/predict"
        headers = {"Authorization": self.token}
        configuration_file = json.dumps(configuration)
        model_file = json.dumps(model)
        dataset_file = dataset.to_csv(index=False)
        resp = requests.request(
            method="POST",
            url=url,
            headers=headers,
            timeout=self.timeout,
            files={
                "configuration": (
                    "configuration",
                    configuration_file,
                    "application/json",
                ),
                "model": ("model", model_file, "application/json"),
                "dataset": ("dataset", dataset_file, "text/csv"),
            },
        )
        return resp.json()

    def status(self, id):
        url = self.server + f"/forecast/{id}"
        headers = {"Authorization": self.token}
        resp = requests.request(method="GET", url=url, headers=headers, timeout=self.timeout)
        return resp.json()

    def model(self, id):
        url = self.server + f"/forecast/{id}/model"
        headers = {"Authorization": self.token}
        resp = requests.request(method="GET", url=url, headers=headers, timeout=self.timeout)
        return resp.json()

    def results(self, id):
        url = self.server + f"/forecast/{id}/results"
        headers = {"Authorization": self.token}
        resp = requests.request(method="GET", url=url, headers=headers, timeout=self.timeout)
        return pd.read_csv(io.StringIO(resp.text))

    def rca(self, configuration, model, dataset):
        url = self.server + "/forecast/rca"
        headers = {"Authorization": self.token}
        configuration_file = json.dumps(configuration)
        model_file = json.dumps(model)
        dataset_file = dataset.to_csv(index=False)
        resp = requests.request(
            method="POST",
            url=url,
            headers=headers,
            timeout=self.timeout,
            files={
                "configuration": (
                    "configuration",
                    configuration_file,
                    "application/json",
                ),
                "model": ("model", model_file, "application/json"),
                "dataset": ("dataset", dataset_file, "text/csv"),
            },
        )
        return resp.json()

    def rca_results(self, id):
        url = self.server + f"/forecast/{id}/rca-table"
        headers = {"Authorization": self.token}
        resp = requests.request(method="GET", url=url, headers=headers, timeout=self.timeout)
        rca_json = json.loads(resp.text)
        output = []
        for model_index in rca_json.keys():
            rca_json[model_index]
            rca_df = pd.read_csv(io.StringIO(rca_json[model_index]))
            output.append({model_index: rca_df})
        return output
