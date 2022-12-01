"""
Script copies the input zone file and the necessary configuration file "named.conf"
into an existing or a new Bind container and starts the DNS server on container
port 53, which is mapped to a host port.
"""

#!/usr/bin/env python3

import pathlib
import subprocess
import os


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
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(cur_dir, "zone"), exist_ok=True)
    converted_file = f"{cur_dir}/zone/{zone_file.name}"
    if not os.path.exists(f"{cur_dir}/bind-to-tinydns/bind-to-tinydns"):
        subprocess.run(["make"], cwd=f"{cur_dir}/bind-to-tinydns", check=True)
    if os.path.exists(f"{cur_dir}/bind-to-tinydns/bind-to-tinydns"):
        with open(zone_file, "r") as zone:
            subprocess.run([f"{cur_dir}/bind-to-tinydns/bind-to-tinydns", zone_domain, converted_file, f"{cur_dir}/zone/tmp.txt"], stdin=zone, check=True)
    if restart:
        subprocess.run(['docker', 'container', 'rm', cname, '-f'],
                       stdout=subprocess.PIPE, check=False)
        subprocess.run(['docker', 'run', '-dp', str(port)+':53/udp',
                        '--name=' + cname, 'djbdns' + tag],
                       stdout=subprocess.PIPE, check=False)
    else:
        # Kill the running server instance inside the container
        subprocess.run(
            ['docker', 'exec', cname, 'pkill', 'tinydns'], check=False)
    # Copy the new zone file into the container
    subprocess.run(['docker', 'cp', converted_file, cname +
                    ':/etc/tinydns/root/data'], check=False)
    # Create the Bind-specific configuration file
    # named = f'''
    # options{{
    # recursion no;
    # }};

    # zone "{zone_domain}" {{
    #     type master;
    #     check-names ignore;
    #     file "{"/usr/local/etc/"+ zone_file.name}";
    # }};
    # '''
    # with open('named_'+cname+'.conf', 'w') as file_pointer:
    #     file_pointer.write(named)
    # # Copy the configuration file into the container as "named.conf"
    # subprocess.run(['docker', 'cp', 'named_'+cname+'.conf', cname +
    #                 ':/usr/local/etc/named.conf'], stdout=subprocess.PIPE, check=False)
    # pathlib.Path('named_'+cname+'.conf').unlink()
    # Start the server - When 'named' is run, Bind first reads the "named.conf" file to know
    #                   the settings and where the zone files are
    subprocess.run(['docker', 'exec', "-w", "/etc/tinydns/root", cname, 'tinydns-data'],
                   stdout=subprocess.PIPE, check=False)
    p = subprocess.Popen(['docker', 'exec', cname, "-w", "/etc/tinydns", '/etc/tinydns/run'],
                   stdout=subprocess.PIPE)
