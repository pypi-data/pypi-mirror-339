# Copyright 2023 J.P. Morgan Chase & Co.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
import pathlib
from typing import Tuple

import botocore.response
import pytest

import inference_server
import inference_server.testing


def test_package_has_version():
    assert inference_server.__version__ is not None


@pytest.fixture(autouse=True)
def reset_caches():
    try:
        yield
    finally:
        inference_server._model.cache_clear()


@pytest.fixture
def client():
    return inference_server.testing.client()


@pytest.fixture
def bad_ping():
    class PingPlugin:
        """Plugin which just defines a ping_fun"""

        @staticmethod
        @inference_server.plugin_hook()
        def ping_fn(model):
            """Return False to simulate unhealthy service"""
            return False

    pm = inference_server.testing.plugin_manager()
    pm.register(PingPlugin)
    try:
        yield
    finally:
        pm.unregister(PingPlugin)


@pytest.fixture
def model_using_dir():
    class ModelPlugin:
        """Plugin which just defines a model_fn"""

        @staticmethod
        @inference_server.plugin_hook()
        def model_fn(model_dir: str):
            """Model function for testing we are passing a custom directory"""
            assert model_dir != "/opt/ml/model"
            return lambda data: data

    pm = inference_server.testing.plugin_manager()
    pm.register(ModelPlugin)
    try:
        yield
    finally:
        pm.unregister(ModelPlugin)


def test_version():
    """Test that the package has a version"""
    assert inference_server.__version__ is not None


def test_ping(client):
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.data == b""


def test_ping_unhealthy(client, bad_ping):
    response = client.get("/ping")
    assert response.status_code == 503
    assert response.data == b""


def test_warmup():
    assert inference_server.warmup() is None


def test_path_not_found(client):
    response = client.get("/this-endpoint-does-not-exist")
    assert response.status_code == 404


def test_invocations():
    """Test the default plugin (which passes through any input bytes) using low-level testing.post_invocations"""
    data = b"What's the shipping forecast for tomorrow"
    response = inference_server.testing.post_invocations(data=data, headers={"Accept": "application/octet-stream"})
    assert response.data == data
    assert response.headers["Content-Type"] == "application/octet-stream"


def test_invocations_custom_model_dir(model_using_dir):
    """Test the default plugin (which passes through any input bytes) using low-level testing.post_invocations"""
    data = b"What's the shipping forecast for tomorrow"
    model_dir = pathlib.Path(__file__).parent

    response = inference_server.testing.post_invocations(
        data=data, model_dir=model_dir, headers={"Accept": "application/octet-stream"}
    )
    assert response.data == data


def test_prediction_custom_serializer():
    """Test the default plugin again, now using high-level testing.predict"""

    class Serializer:
        @property
        def CONTENT_TYPE(self) -> str:
            return "application/octet-stream"

        def serialize(self, data: str) -> bytes:
            return data.encode()  # Simple str to bytes serializer

    class Deserializer:
        @property
        def ACCEPT(self) -> Tuple[str]:
            return ("application/octet-stream",)

        def deserialize(self, stream: botocore.response.StreamingBody, content_type: str) -> str:
            assert content_type in self.ACCEPT
            return stream.read().decode()  # Simple bytes to str deserializer

    input_data = "What's the shipping forecast for tomorrow"  # Simply pass a string
    prediction = inference_server.testing.predict(
        data=input_data,
        serializer=Serializer(),
        deserializer=Deserializer(),
    )
    assert prediction == input_data  # Receive a string


def test_prediction_no_serializer():
    input_data = b"What's the shipping forecast for tomorrow"
    prediction = inference_server.testing.predict(input_data)  # No serializer should be bytes pass through again
    assert prediction == input_data


def test_prediction_model_dir(model_using_dir):
    input_data = b"What's the shipping forecast for tomorrow"
    model_dir = pathlib.Path(__file__).parent

    prediction = inference_server.testing.predict(input_data, model_dir=model_dir)
    assert prediction == input_data


def test_execution_parameters(client):
    response = client.get("/execution-parameters")
    assert response.data == b'{"BatchStrategy":"MultiRecord","MaxConcurrentTransforms":1,"MaxPayloadInMB":6}'


def test_default_plugin_registered():
    assert inference_server.testing.plugin_is_registered(inference_server.default_plugin)


def test_invalid_hookimpl_fn():
    assert not inference_server.testing.hookimpl_is_valid(lambda x: x)


def test_default_model_fn_hook_is_valid():
    assert inference_server.testing.hookimpl_is_valid(inference_server.default_plugin.model_fn)


def test_default_input_fn_hook_is_valid():
    assert inference_server.testing.hookimpl_is_valid(inference_server.default_plugin.input_fn)


def test_default_predict_fn_hook_is_valid():
    assert inference_server.testing.hookimpl_is_valid(inference_server.default_plugin.predict_fn)


def test_default_output_fn_hook_is_valid():
    assert inference_server.testing.hookimpl_is_valid(inference_server.default_plugin.output_fn)


def test_default_batch_strategy_hook_is_valid():
    assert inference_server.testing.hookimpl_is_valid(inference_server.default_plugin.batch_strategy)


def test_default_max_concurrent_transforms_hook_is_valid():
    assert inference_server.testing.hookimpl_is_valid(inference_server.default_plugin.max_concurrent_transforms)


def test_default_max_payload_in_mb_hook_is_valid():
    assert inference_server.testing.hookimpl_is_valid(inference_server.default_plugin.max_payload_in_mb)
