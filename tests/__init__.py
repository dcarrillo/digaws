import ipaddress

AWS_IP_RANGES = """
{
  "syncToken": "1608245058",
  "createDate": "2020-12-17-22-44-18",
  "prefixes": [
    {
      "ip_prefix": "52.93.178.234/32",
      "region": "us-west-1",
      "service": "AMAZON",
      "network_border_group": "us-west-1"
    },
    {
      "ip_prefix": "52.94.76.0/22",
      "region": "us-west-2",
      "service": "AMAZON",
      "network_border_group": "us-west-2"
    }
  ],
  "ipv6_prefixes": [
    {
      "ipv6_prefix": "2600:1f00:c000::/40",
      "region": "us-west-1",
      "service": "AMAZON",
      "network_border_group": "us-west-1"
    },
    {
      "ipv6_prefix": "2600:1f01:4874::/47",
      "region": "us-west-2",
      "service": "AMAZON",
      "network_border_group": "us-west-2"
    },
    {
      "ipv6_prefix": "2600:1f14:fff:f800::/53",
      "region": "us-west-2",
      "service": "ROUTE53_HEALTHCHECKS",
      "network_border_group": "us-west-2"
    },
    {
      "ipv6_prefix": "2600:1f14::/35",
      "region": "us-west-2",
      "service": "EC2",
      "network_border_group": "us-west-2"
    }
  ]
}
"""
AWS_IPV4_RANGES_OBJ = [
    {
        "ip_prefix": ipaddress.IPv4Network("52.93.178.234/32"),
        "region": "us-west-1",
        "service": "AMAZON",
        "network_border_group": "us-west-1",
    },
    {
        "ip_prefix": ipaddress.IPv4Network("52.94.76.0/22"),
        "region": "us-west-2",
        "service": "AMAZON",
        "network_border_group": "us-west-2",
    },
]
AWS_IPV6_RANGES_OBJ = [
    {
        "ipv6_prefix": ipaddress.IPv6Network("2600:1f00:c000::/40"),
        "region": "us-west-1",
        "service": "AMAZON",
        "network_border_group": "us-west-1",
    },
    {
        "ipv6_prefix": ipaddress.IPv6Network("2600:1f01:4874::/47"),
        "region": "us-west-2",
        "service": "AMAZON",
        "network_border_group": "us-west-2",
    },
    {
        "ipv6_prefix": ipaddress.IPv6Network("2600:1f14:fff:f800::/53"),
        "region": "us-west-2",
        "service": "ROUTE53_HEALTHCHECKS",
        "network_border_group": "us-west-2",
    },
    {
        "ipv6_prefix": ipaddress.IPv6Network("2600:1f14::/35"),
        "region": "us-west-2",
        "service": "EC2",
        "network_border_group": "us-west-2",
    },
]
LAST_MODIFIED_TIME = "Thu, 17 Dec 2020 23:22:33 GMT"

RESPONSE_PLAIN_PRINT = """Prefix: 52.94.76.0/22
Region: us-west-2
Service: AMAZON
Network border group: us-west-2

"""

RESPONSE_JSON_PRINT = """[
  {
    "ipv6_prefix": "2600:1f14:fff:f800::/53",
    "region": "us-west-2",
    "service": "ROUTE53_HEALTHCHECKS",
    "network_border_group": "us-west-2"
  },
  {
    "ipv6_prefix": "2600:1f14::/35",
    "region": "us-west-2",
    "service": "EC2",
    "network_border_group": "us-west-2"
  }
]
"""

RESPONSE_JSON_FIELDS_PRINT = """[
  {
    "service": "ROUTE53_HEALTHCHECKS",
    "network_border_group": "us-west-2"
  },
  {
    "service": "EC2",
    "network_border_group": "us-west-2"
  }
]
"""

RESPONSE_JSON_JOINED_PRINT = """[
  {
    "ip_prefix": "52.94.76.0/22",
    "region": "us-west-2",
    "service": "AMAZON",
    "network_border_group": "us-west-2"
  },
  {
    "ipv6_prefix": "2600:1f14:fff:f800::/53",
    "region": "us-west-2",
    "service": "ROUTE53_HEALTHCHECKS",
    "network_border_group": "us-west-2"
  },
  {
    "ipv6_prefix": "2600:1f14::/35",
    "region": "us-west-2",
    "service": "EC2",
    "network_border_group": "us-west-2"
  }
]
"""
