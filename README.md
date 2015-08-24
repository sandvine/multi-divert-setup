= Create a test network for multi-divert

This script creates 4 virtual machines (client, server, PTS, divert host)
and wires them on a common control bus.
The client and server are wired together through the data interface
of the PTS.
The divert host is wired to the divert port, and, is setup
so that multi-divert works. In particular, the PTS port is set to
trunking (so VLAN tags are maintained). And, the divert host is wired
with two interfaces, on vlan 100, 200, to that same interface.

     ----------------------------------------------[control]
      |     |                |               |
      |     |(1)             |(1)            |(1)
      |  --------         -------         --------
      |  |      |(2)   (3)|     |(4)   (2)|      |
      |  |client|---------| PTS |---------|server|
      |  |      |         |     |         |      |
      |  --------         -------         --------
      |                      |(2,trunk)
      |                      |
      |                    [ovs]
      |                      |
      |                    -----
      |            (2-v100)|  |(3-v200)
      |                  ---------
      |               (1)|       |
      -------------------|divert |
                         |       |
                         ---------

= Usage

run 'install' (it wipes out and reinstalls fresh)

On the divert host, install:

	$ cat /etc/network/interfaces
	# This file describes the network interfaces available on your system
	# and how to activate them. For more information, see interfaces(5).

	# The loopback network interface
	auto lo
	iface lo inet loopback

	# The primary network interface
	auto eth0
	iface eth0 inet dhcp

	auto divert
	iface divert inet manual
	  pre-up brctl addbr divert
	  pre-up brctl addif divert eth1 eth2
	  pre-up ip link set eth1 up
	  pre-up ip link set eth2 up
	  pre-up brctl stp divert off
	  post-down brctl delif divert eth1 eth2
	  post-down brctl delbr divert

	$ sudo ifup -v bridge

On the server, install:

Add this to /etc/network/interfaces:

	auto eth1
	iface eth1 inet static
	  address 10.0.0.1
	  netmask 255.255.255.0

then run 'ifup -v eth1'

	$ cat /etc/init/http-daemon.conf
	description "simple http-daemon"

	start on runlevel [2345]
	stop on runlevel [!2345]

	respawn

	exec /usr/bin/python -m SimpleHTTPServer

On the client, add this to /etc/network/interfaces, then ifup -v eth1

	auto eth1
	iface eth1 inet static
	  address 10.0.0.2
	  netmask 255.255.255.0

Now the client can ping 10.0.0.1, and run
curl -k http://10.0.0.1:8000 to generate a simple http flow.

The divert host bridge should make the full traffic flow. When you
are ready, remove that bridge and replace it with your application.

There is nothing special in the 'trusty.qcow2' or 'pts.qcow2' image
that the script uses.

