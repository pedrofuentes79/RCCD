#!/usr/bin/env python3
from mininet.net import Containernet
from mininet.node import Docker
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
import os

os.system('docker rm -f $(docker ps -aq --filter "name=mn.") 2>/dev/null')

def disable_rstp(sw_name: str) -> str:
    # RSTP en OVS
    return f"ovs-vsctl set bridge {sw_name} rstp_enable=false"

def enable_stp(sw_name: str) -> str:
    # STP 802.1D en OVS
    return f"ovs-vsctl set bridge {sw_name} stp_enable=true"

def set_standalone_mode(sw_name: str) -> str:
    return f"ovs-vsctl set bridge {sw_name} fail_mode=standalone; ovs-ofctl add-flow {sw_name} \"priority=0,actions=NORMAL\""

def main() -> None:
    setLogLevel("error")

    net = Containernet(link=TCLink, controller=None)
    
    setLogLevel("info")

    # Hosts = PCs
    A = net.addHost("A", ip="10.0.0.10/24")
    B = net.addHost("B", ip="10.0.0.11/24")

    # Switches SN
    s1 = net.addSwitch("s1")
    s2 = net.addSwitch("s2")
    s3 = net.addSwitch("s3")
    s4 = net.addSwitch("s4")
    s5 = net.addSwitch("s5")
    s6 = net.addSwitch("s6")
    s7 = net.addSwitch("s7")

    # Links (sin delay por defecto; luego se inyecta por scripts)
    net.addLink(A,  s1)
    net.addLink(s1, s2)
    net.addLink(s1, s3)

    net.addLink(s2, s4)
    net.addLink(s3, s4)

    net.addLink(s2, s5)
    net.addLink(s5, s7)

    net.addLink(s4, s6)
    net.addLink(s6, s7)

    net.addLink(s4, s7)  # enlace directo: fuerza loops STP

    net.addLink(s7, B)

    net.start()

    # Habilitar STP en todos los switches
    for s in [s1, s2, s3, s4, s5, s6, s7]:
        s.cmd(enable_stp(s.name))
        s.cmd(disable_rstp(s.name))
        s.cmd(set_standalone_mode(s.name))

    print("\n[INFO] Topología levantada. STP habilitado en s1..s7.")

    CLI(net)
    net.stop()

if __name__ == "__main__":
    main()
