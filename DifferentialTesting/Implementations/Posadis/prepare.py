#!/usr/bin/env python3

import pathlib
import subprocess


def run(zone_file: pathlib.Path, zone_domain: str, cname: str, port: int, restart: bool, tag: str) -> None:
    """
    :param zone_file: Path to the Bind-style zone file
    :param zone_domain: The domain name of the zone
    :param cname: Container name
    :param port: The host port which is mapped to the port 53 of the container
    :param restart: Whether to load the input zone file in a new container
                        or reuse the existing container
    :param tag: The image tag to be used if restarting the container
    """
    if restart:
        subprocess.run(['docker', 'container', 'rm', cname, '-f'],
                        stdout=subprocess.PIPE, check=False)
        subprocess.run(['docker', 'run', '-dp', str(port)+':53/udp',
                        '--name=' + cname, 'bind' + tag],
                        stdout=subprocess.PIPE, check=False)
    else:
        # Kill the running server instance inside the container
        subprocess.run(
            ['docker', 'exec', cname, 'pkill', 'posadis'], check=False)
    # Copy the new zone file into the container
    subprocess.run(['docker', 'cp', str(zone_file), cname +
                    f':/etc/posadis/{zone_domain}.prm'], stdout=subprocess.PIPE, check=False)

    # Start the server
    subprocess.run(['docker', 'exec', '-d', cname, 'posadis'],
                   stdout=subprocess.PIPE, check=False)