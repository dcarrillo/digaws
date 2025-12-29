import json
import sys

import pytest

import digaws.digaws as digaws
import tests
from digaws import __description__, __version__


@pytest.fixture
def test_dig():
    return digaws.DigAWS(
        ip_ranges=json.loads(tests.AWS_IP_RANGES), output_fields=digaws.OUTPUT_FIELDS
    )


def test_cli(capsys):
    sys.argv = ["digaws", "-h"]
    try:
        digaws.main()
    except SystemExit as e:
        out, _ = capsys.readouterr()
        assert __description__ in out
        assert e.code == 0


def test_cli_version(capsys, mocker):
    sys.argv = ["digaws", "--version"]
    try:
        digaws.main()
    except SystemExit as e:
        out, _ = capsys.readouterr()
        assert out == f"digaws {__version__}\n"
        assert e.code == 0


def test_cli_invocation(capsys, mocker):
    sys.argv = [
        "digaws",
        "52.94.76.0/22",
        "2600:1f14:fff:f810:a1c1:f507:a2d1:2dd8",
        "--output",
        "json",
    ]
    mocker.patch("digaws.digaws.get_aws_ip_ranges", return_value=json.loads(tests.AWS_IP_RANGES))
    digaws.main()
    out, _ = capsys.readouterr()

    assert out == tests.RESPONSE_JSON_JOINED_PRINT


def test_cli_output_plain_fields_invocation(capsys, mocker):
    sys.argv = [
        "digaws",
        "52.94.76.0/22",
        "--output=plain",
        "--output-fields",
        "region",
    ]
    mocker.patch("digaws.digaws.get_aws_ip_ranges", return_value=json.loads(tests.AWS_IP_RANGES))
    digaws.main()
    out, _ = capsys.readouterr()

    assert out == "Region: us-west-2\n\n"


def test_cli_output_json_fields_invocation(capsys, mocker):
    sys.argv = [
        "digaws",
        "2600:1f14:fff:f810:a1c1:f507:a2d1:2dd8",
        "--output=json",
        "--output-fields",
        "service",
        "network_border_group",
    ]
    mocker.patch("digaws.digaws.get_aws_ip_ranges", return_value=json.loads(tests.AWS_IP_RANGES))
    digaws.main()
    out, _ = capsys.readouterr()

    assert out == tests.RESPONSE_JSON_FIELDS_PRINT


def test_dig_aws_construct(test_dig):
    assert test_dig.ip_prefixes == tests.AWS_IPV4_RANGES_OBJ
    assert test_dig.ipv6_prefixes == tests.AWS_IPV6_RANGES_OBJ


def test_lookup(test_dig):
    assert str(test_dig._lookup_data("52.94.76.1")[0]["ip_prefix"]) == "52.94.76.0/22"
    assert str(test_dig._lookup_data("52.94.76.0/24")[0]["ip_prefix"]) == "52.94.76.0/22"

    ipv6_addr = "2600:1f14:fff:f810:a1c1:f507:a2d1:2dd8"
    assert str(test_dig._lookup_data(ipv6_addr)[0]["ipv6_prefix"]) == "2600:1f14:fff:f800::/53"
    assert str(test_dig._lookup_data(ipv6_addr)[1]["ipv6_prefix"]) == "2600:1f14::/35"
    assert str(test_dig._lookup_data("2600:1f14::/36")[0]["ipv6_prefix"]) == "2600:1f14::/35"

    with pytest.raises(ValueError) as e:
        test_dig.lookup("what are you talking about")
    assert str(e.value).startswith("Wrong IP or CIDR format")


def test_response_plain_print(test_dig, capsys):
    test_dig.lookup("52.94.76.0/22").plain_print()
    out, _ = capsys.readouterr()

    assert out == tests.RESPONSE_PLAIN_PRINT


def test_response_json_print(test_dig, capsys):
    test_dig.lookup("2600:1f14:fff:f810:a1c1:f507:a2d1:2dd8").json_print()
    out, _ = capsys.readouterr()

    assert out == tests.RESPONSE_JSON_PRINT
