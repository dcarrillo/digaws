# digaws

The digaws lookup tool displays information for a given IP address (both v4 and v6) or a CIDR, sourced from the AWS official IP ranges.
In order to save bandwidth and time this tool requests the [AWS IP ranges](https://ip-ranges.amazonaws.com/ip-ranges.json) and keeps
a cached version until a new version is published.

[![PyPI version](https://badge.fury.io/py/digaws.svg)](https://pypi.org/project/digaws/)
[![CI](https://github.com/dcarrillo/digaws/workflows/CI/badge.svg)](https://github.com/dcarrillo/digaws/actions)

## Requirements

Python >= 3.8

Tests are verified on Linux, macos and Windows.

## Install

### Using [pipx](https://pypa.github.io/pipx/#install-pipx) (this is the preferred way)

```bash
pipx install digaws
```

### Using pip

```bash
pip install digaws --user
```

## Usage

```text
usage: digaws [-h] [--output <plain|json>] [--output-fields [{prefix,region,service,network_border_group} ...]] [--debug] [--version] <ip address|cidr> [<ip address|cidr> ...]

Look up canonical information for AWS IP addresses and networks

positional arguments:
  <ip address|cidr>     CIDR or IP (v4 or v6) to look up

optional arguments:
  -h, --help            show this help message and exit
  --output <plain|json>
                        Formatting style for command output, by default plain
  --output-fields [{prefix,region,service,network_border_group} ...]
                        Print only the given fields
  --debug               Enable debug
  --version             show program's version number and exit
```

## Examples

- look up an IPv4 address

```text
~ » digaws 52.218.97.130

Prefix: 52.218.0.0/17
Region: eu-west-1
Service: AMAZON
Network border group: eu-west-1

Prefix: 52.218.0.0/17
Region: eu-west-1
Service: S3
Network border group: eu-west-1
```

- look up an IPv6 address

```text
~ » digaws 2600:1f1e:fff:f810:a29b:cb50:2812:e2dc

IPv6 Prefix: 2600:1f1e::/36
Region: sa-east-1
Service: AMAZON
Network border group: sa-east-1

IPv6 Prefix: 2600:1f1e:fff:f800::/53
Region: sa-east-1
Service: ROUTE53_HEALTHCHECKS
Network border group: sa-east-1

IPv6 Prefix: 2600:1f1e::/36
Region: sa-east-1
Service: EC2
Network border group: sa-east-1
```

- look up several addresses and print output as json

```text
~ » digaws 2600:1f14::/36 13.224.119.88 --output json

[
  {
    "ipv6_prefix": "2600:1f14::/35",
    "region": "us-west-2",
    "service": "AMAZON",
    "network_border_group": "us-west-2"
  },
  {
    "ipv6_prefix": "2600:1f14::/35",
    "region": "us-west-2",
    "service": "EC2",
    "network_border_group": "us-west-2"
  },
  {
    "ip_prefix": "13.224.0.0/14",
    "region": "GLOBAL",
    "service": "AMAZON",
    "network_border_group": "GLOBAL"
  },
  {
    "ip_prefix": "13.224.0.0/14",
    "region": "GLOBAL",
    "service": "CLOUDFRONT",
    "network_border_group": "GLOBAL"
  }
]
```

- Choose output fields

```text
~ » digaws 34.255.166.63 --output-fields service

Service: AMAZON

Service: EC2

```
