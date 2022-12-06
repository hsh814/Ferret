#!/usr/bin/env python3

import os
import pathlib
import subprocess
from typing import List

def converter(orig_lines:List[str]):
    result=[]
    for line in orig_lines:
        if 'IN SOA' in line:
            tokens=line.strip().split()
            new_line=f'@ {tokens[1]} SOA ( . meilof@{tokens[0][:-1]} 2002052301 {tokens[7]} {tokens[8]} {tokens[9]} {tokens[10]} )\n'
            result.append(new_line)
        elif 'IN NS' in line:
            tokens=line.strip().split()
            new_line=f'{tokens[0]} NS {tokens[4]}\n'
            result.append(new_line)
        elif 'IN CNAME' in line:
            tokens=line.strip().split()
            new_line=f'{tokens[0]} CNAME {tokens[4]}\n'
            result.append(new_line)
        elif 'IN DNAME' in line:
            tokens=line.strip().split()
            new_line=f'{tokens[0]} DNAME {tokens[4]}\n'
            result.append(new_line)

        else: raise ValueError(f'Unknown line: {line}')

    return result

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
                        '--name=' + cname, 'posadis' + tag],
                        stdout=subprocess.PIPE, check=False)
    else:
        # Kill the running server instance inside the container
        subprocess.run(
            ['docker', 'exec', cname, 'pkill', 'posadis'], check=False)

    # Convert default input to posadis format
    file_name=f'db.{zone_domain[:-1]}'
    subprocess.run(['cp','-rf','Implementations/Posadis/posadisrc',f'Implementations/Posadis/rc_{cname}'],stdout=subprocess.PIPE, check=False)
    with open(f'Implementations/Posadis/rc_{cname}', 'r') as file_pointer:
        orig_lines=file_pointer.readlines()
        new_lines=orig_lines.copy()
        for i,line in enumerate(orig_lines):
            if line.startswith('ZoneFile'):
                new_lines[i]=f'ZoneFile "{file_name}"\n'
    with open(f'Implementations/Posadis/rc_{cname}', 'w') as file_pointer:
        file_pointer.writelines(new_lines)
    
    subprocess.run(['cp','-rf',zone_file,'Implementations/Posadis/'],stdout=subprocess.PIPE, check=False)
    # with open(zone_file, 'r') as file_pointer:
    #     orig_lines=file_pointer.readlines()
    #     new_lines=converter(orig_lines)
    # with open(f'Implementations/Posadis/{zone_file.name}', 'w') as file_pointer:
    #     file_pointer.writelines(new_lines)

    # Copy the new zone file into the container
    subprocess.run(['docker', 'cp', f'Implementations/Posadis/{zone_file.name}', cname +
                    f':/etc/posadis/db.{zone_domain[:-1]}'], stdout=subprocess.PIPE, check=False)
    subprocess.run(['docker', 'cp', f'Implementations/Posadis/rc_{cname}', cname +
                    ':/etc/posadisrc'], stdout=subprocess.PIPE, check=False)

    # Start the server
    subprocess.run(['docker', 'exec', '-d', cname, 'posadis'],
                   stdout=subprocess.PIPE, check=False)