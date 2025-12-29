import json
import os

import pytest
import requests

import digaws.digaws as digaws
import tests


class MockGetResponse:
    text = tests.AWS_IP_RANGES
    status_code = 200

    @staticmethod
    def json():
        return json.loads(tests.AWS_IP_RANGES)


def mock_get(*args, **kwargs):
    return MockGetResponse()


@pytest.fixture
def create_cache_dir(fs):
    digaws.CACHE_DIR.mkdir(parents=True)


@pytest.mark.parametrize("fs", [[None, [digaws]]], indirect=True)
def test_get_aws_ip_ranges_cached_valid_file(mocker, fs, create_cache_dir) -> None:
    with open(digaws.CACHE_FILE, "w") as out:
        out.write(tests.AWS_IP_RANGES)

    response = requests.Response
    response.status_code = 304
    mocker.patch("requests.get", return_value=response)

    result = digaws.get_aws_ip_ranges()

    assert result["syncToken"] == "1608245058"


@pytest.mark.parametrize("fs", [[None, [digaws]]], indirect=True)
def test_get_aws_ip_ranges_cached_invalid_file(mocker, fs, create_cache_dir) -> None:
    with open(digaws.CACHE_FILE, "w"):
        pass

    response = requests.Response
    response.status_code = 304
    mocker.patch("requests.get", return_value=response)

    with pytest.raises(digaws.CachedFileError):
        digaws.get_aws_ip_ranges()


@pytest.mark.parametrize("fs", [[None, [digaws]]], indirect=True)
def test_get_aws_ip_ranges_cached_deprecated_file(monkeypatch, fs, create_cache_dir) -> None:
    with open(digaws.CACHE_FILE, "w"):
        pass
    digaws.CACHE_FILE.touch()
    os.utime(digaws.CACHE_FILE, times=(0, 0))

    monkeypatch.setattr(requests, "get", mock_get)
    result = digaws.get_aws_ip_ranges()

    assert result["syncToken"] == "1608245058"


@pytest.mark.parametrize("fs", [[None, [digaws]]], indirect=True)
def test_get_aws_ip_ranges_no_file(monkeypatch, fs, create_cache_dir) -> None:
    monkeypatch.setattr(requests, "get", mock_get)
    result = digaws.get_aws_ip_ranges()

    assert result["syncToken"] == "1608245058"


@pytest.mark.parametrize("fs", [[None, [digaws]]], indirect=True)
def test_get_aws_ip_ranges_invalid_status(mocker, fs, create_cache_dir) -> None:
    response = requests.Response
    response.status_code = 301
    mocker.patch("requests.get", return_value=response)

    with pytest.raises(digaws.UnexpectedRequestError) as e:
        digaws.get_aws_ip_ranges()

    assert str(e.value).startswith("Unexpected response from")
