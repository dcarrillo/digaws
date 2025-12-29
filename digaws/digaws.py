#!/usr/bin/env python3

import argparse
import ipaddress
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
from dateutil import tz
from requests.exceptions import RequestException

from . import __description__, __version__

AWS_IP_RANGES_URL = "https://ip-ranges.amazonaws.com/ip-ranges.json"
CACHE_DIR = Path(Path.home() / ".digaws")
CACHE_FILE = CACHE_DIR / "ip-ranges.json"
OUTPUT_FIELDS = ["prefix", "region", "service", "network_border_group"]

logger = logging.getLogger()
handler = logging.StreamHandler(sys.stderr)
logger.addHandler(handler)
handler.setFormatter(logging.Formatter("-- %(levelname)s -- %(message)s"))
logger.setLevel(logging.INFO)


def get_aws_ip_ranges() -> dict:
    CACHE_DIR.mkdir(exist_ok=True)

    headers = {}
    try:
        file_time = datetime.fromtimestamp(CACHE_FILE.stat().st_mtime, tz=tz.UTC).strftime(
            "%a, %d %b %Y %H:%M:%S GMT"
        )
        logger.debug(f"cached file modification time: {file_time}")
        headers = {"If-Modified-Since": file_time}
    except FileNotFoundError as e:
        logger.debug(f"Not found: {CACHE_FILE}: {e}")
        pass

    try:
        response = requests.get(url=AWS_IP_RANGES_URL, timeout=5, headers=headers)

        if response.status_code == 304:
            try:
                logger.debug(f"reading cached file {CACHE_FILE}")
                with open(CACHE_FILE) as ip_ranges:
                    return json.load(ip_ranges)
            except (OSError, json.JSONDecodeError) as e:
                logger.debug(f"ERROR reading {CACHE_FILE}: {e}")
                raise CachedFileError(str(e)) from e
        elif response.status_code == 200:
            try:
                with open(CACHE_FILE, "w") as f:
                    f.write(response.text)
            except OSError as e:
                logger.warning(e)

            return response.json()
        else:
            msg = (
                f"Unexpected response from {AWS_IP_RANGES_URL}. Status code: "
                f"{response.status_code}. Content: {response.text}"
            )
            logger.debug(msg)
            raise UnexpectedRequestError(msg)
    except RequestException as e:
        logger.debug(f"ERROR retrieving {AWS_IP_RANGES_URL}: {e}")
        raise e


class CachedFileError(Exception):
    def __init__(self, message: str):
        message = f"Error reading cached ranges {CACHE_FILE}: {message}"
        super().__init__(message)


class UnexpectedRequestError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class DigAWSPrettyPrinter:
    def __init__(self, data: list[dict], output_fields: list[str] | None = None):
        self.data = data
        self.output_fields = output_fields if output_fields is not None else []

    def plain_print(self) -> None:
        for prefix in self.data:
            if "prefix" in self.output_fields:
                try:
                    print(f"Prefix: {prefix['ip_prefix']}")
                except KeyError:
                    print(f"IPv6 Prefix: {prefix['ipv6_prefix']}")
            if "region" in self.output_fields:
                print(f"Region: {prefix['region']}")
            if "service" in self.output_fields:
                print(f"Service: {prefix['service']}")
            if "network_border_group" in self.output_fields:
                print(f"Network border group: {prefix['network_border_group']}")
            print("")

    def json_print(self) -> None:
        data = []
        for prefix in self.data:
            try:
                prefix["ip_prefix"]
                prefix_type = "ip_prefix"
            except KeyError:
                prefix_type = "ipv6_prefix"

            item_dict = {}
            if "prefix" in self.output_fields:
                item_dict.update({prefix_type: str(prefix[prefix_type])})
            if "region" in self.output_fields:
                item_dict.update({"region": prefix["region"]})
            if "service" in self.output_fields:
                item_dict.update({"service": prefix["service"]})
            if "network_border_group" in self.output_fields:
                item_dict.update({"network_border_group": prefix["network_border_group"]})
            data.append(item_dict)

        print(json.dumps(data, indent=2))


class DigAWS:
    def __init__(
        self, *, ip_ranges: dict, output: str = "plain", output_fields: list[str] | None = None
    ):
        self.output = output
        self.output_fields = output_fields if output_fields is not None else []
        self.ip_prefixes = [
            {
                "ip_prefix": ipaddress.IPv4Network(prefix["ip_prefix"]),
                "region": prefix["region"],
                "service": prefix["service"],
                "network_border_group": prefix["network_border_group"],
            }
            for prefix in ip_ranges["prefixes"]
        ]
        self.ipv6_prefixes = [
            {
                "ipv6_prefix": ipaddress.IPv6Network(prefix["ipv6_prefix"]),
                "region": prefix["region"],
                "service": prefix["service"],
                "network_border_group": prefix["network_border_group"],
            }
            for prefix in ip_ranges["ipv6_prefixes"]
        ]

    def lookup(self, address: str) -> DigAWSPrettyPrinter:
        return DigAWSPrettyPrinter(self._lookup_data(address), self.output_fields)

    def _lookup_data(self, address: str) -> list[dict]:
        addr: Any = None
        try:
            addr = ipaddress.IPv4Address(address)
            data = [prefix for prefix in self.ip_prefixes if addr in prefix["ip_prefix"]]
        except ipaddress.AddressValueError:
            try:
                addr = ipaddress.IPv6Address(address)
                data = [prefix for prefix in self.ipv6_prefixes if addr in prefix["ipv6_prefix"]]
            except ipaddress.AddressValueError:
                try:
                    addr = ipaddress.IPv4Network(address)
                    data = [
                        prefix for prefix in self.ip_prefixes if addr.subnet_of(prefix["ip_prefix"])
                    ]
                except (ipaddress.AddressValueError, ValueError):
                    try:
                        addr = ipaddress.IPv6Network(address)
                        data = [
                            prefix
                            for prefix in self.ipv6_prefixes
                            if addr.subnet_of(prefix["ipv6_prefix"])
                        ]
                    except (ipaddress.AddressValueError, ValueError):
                        raise ValueError(f"Wrong IP or CIDR format: {address}") from None

        return data


def arguments_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=True, description=__description__)
    parser.add_argument(
        "--output",
        metavar="<plain|json>",
        choices=["plain", "json"],
        type=str,
        required=False,
        dest="output",
        default="plain",
        help="Formatting style for command output, by default %(default)s",
    )
    parser.add_argument(
        "--output-fields",
        nargs="*",
        choices=OUTPUT_FIELDS,
        required=False,
        dest="output_fields",
        default=OUTPUT_FIELDS,
        help="Print only the given fields",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        required=False,
        default=False,
        dest="debug",
        help="Enable debug",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "addresses",
        nargs="+",
        metavar="<ip address|cidr>",
        type=str,
        help="CIDR or IP (v4 or v6) to look up",
    )

    return parser


def main():
    parser = arguments_parser()
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)

    try:
        ip_ranges = get_aws_ip_ranges()
        dig = DigAWS(ip_ranges=ip_ranges, output_fields=args.output_fields)

        responses = []
        for address in args.addresses:
            responses.append(dig.lookup(address))

        if args.output == "plain":
            for response in responses:
                response.plain_print()
        else:
            if len(responses) == 1:
                responses[0].json_print()
            else:
                joined = []
                for response in responses:
                    joined += response.data

                DigAWSPrettyPrinter(joined, args.output_fields).json_print()
    except (
        RequestException,
        ipaddress.AddressValueError,
        ValueError,
        CachedFileError,
        UnexpectedRequestError,
    ) as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
