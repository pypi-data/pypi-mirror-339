"""Update DNS settings for a deSEC domain."""

import fcntl
import ipaddress
import socket
import struct
from time import sleep

import click
import desec
import ifaddr
import requests
from requests.adapters import HTTPAdapter, Retry

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"], auto_envvar_prefix="DESEC_DYNDNS")


def _get_hardware_address(interface_name: str) -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack("256s", bytes(interface_name, "utf-8")[:15]))
    return ":".join(f"{b:02x}" for b in info[18:24])


def _get_public_ipv4():
    try:
        s = requests.Session()
        s.mount(
            "http://",
            HTTPAdapter(max_retries=Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])),
        )
        response = s.get("https://api.ipify.org/", timeout=5)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        print(f"Error retrieving public IPv4: {e}")
        return None


def _get_public_ipv6(interface_name: str):
    try:
        end_of_mac = _get_hardware_address(interface_name)[-2:]
        adapters = ifaddr.get_adapters()
        for adapter in adapters:
            if adapter.name == interface_name:
                for ip in adapter.ips:
                    address = ipaddress.ip_address(ip.ip[0] if type(ip.ip) is tuple else ip.ip)
                    if address.version == 6 and address.is_global and address.compressed.endswith(end_of_mac):
                        return address.compressed
    except Exception as e:
        print(f"Error retrieving public IPv6: {e}")
    return None


@click.command(context_settings=CONTEXT_SETTINGS, help="Update DNS settings for a deSEC domain")
@click.option("--domain", "-d", required=True, help="The domain to update in")
@click.option("--subdomain", "-s", multiple=True, required=True, help="The subdomain(s) to update")
@click.option("--token", "-t", required=True, help="The token to use for authentication")
@click.option("--interface", "-i", required=True, help="The network interface to use fpr determining the IPv6 address")
@click.option("--update-period", "-p", type=int, default=300, show_default=True, help="The update period in seconds")
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    show_default=True,
    default=False,
    help="Print debug information",
)
def update(domain: str, subdomain: list[str], token: str, interface: str, update_period: int) -> None:
    """Update DNS settings for a deSEC domain."""
    api_client = desec.APIClient(token=token, request_timeout=5, retry_limit=5)
    while True:
        # Get the public IPv4 address
        public_ipv4 = _get_public_ipv4()
        if not public_ipv4:
            print("Failed to retrieve public IPv4 address, skipping update of IPv4.")
        else:
            for subname in subdomain:
                records = api_client.get_records(domain=domain, rtype="A", subname=subname)
                if records:
                    for record in records:
                        foo: list[str] = record["records"]
                        print(foo)
                        if record["records"] != public_ipv4:
                            print(f"Updating IPv4 address for {subname}.{domain} to {public_ipv4}")
                            # api_client.update_record(domain=domain, subname=subname, rtype="A", rrset=public_ipv4)
                        else:
                            print(f"IPv6 address for {subname}.{domain} is already up to date.")
                else:
                    print(f"Creating new IPv4 record for {subname}.{domain} with address {public_ipv4}")
                    # api_client.create_record(domain=domain, subname=subname, rtype="A", rrset=public_ipv4)
                # api_client.update_record(domain=domain, subname=subname, rtype="A", rrset=public_ipv4)

        public_ipv6 = _get_public_ipv6(interface)
        if not public_ipv6:
            print("Failed to retrieve public IPv6 address, skipping update of IPv6.")
        else:
            for subname in subdomain:
                records = api_client.get_records(domain=domain, rtype="AAAA", subname=subname)
                if records:
                    for record in records:
                        foo = record["records"]
                        print(foo)
                        if record["records"] != public_ipv6:
                            print(f"Updating IPv6 address for {subname}.{domain} to {public_ipv6}")
                            # api_client.update_record(domain=domain, subname=subname, rtype="AAAA", rrset=public_ipv4)
                        else:
                            print(f"IPv6 address for {subname}.{domain} is already up to date.")
                else:
                    print(f"Creating new IPv4 record for {subname}.{domain} with address {public_ipv4}")
                    # api_client.create_record(domain=domain, subname=subname, rtype="AAAA", rrset=public_ipv4)
                # api_client.update_record(domain=domain, subname=subname, rtype="AAAA", rrset=public_ipv4)

        # Update the DNS records for each domain
        sleep(update_period)
