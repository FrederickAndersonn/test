#!/usr/bin/env python


from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    # pylint: disable=arguments-differ
    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class NetworkTopo( Topo ):

    # pylint: disable=arguments-differ
    def build( self, **_opts ):

        defaultIPr0 = '10.0.0.100/8'  # IP address for r0-eth1
        defaultIPr1 = '10.0.0.200/8'  # IP address for r1-eth1

        router0 = self.addNode( 'r0', cls=LinuxRouter, ip=defaultIPr0 )
        router1 = self.addNode( 'r1', cls=LinuxRouter, ip=defaultIPr1 )


        s1, s2, s3  = [ self.addSwitch( s ) for s in ( 's1', 's2', 's3' ) ]

        self.addLink( s3, router0, intfName2='r0-eth1',
                      params2={ 'ip' : defaultIPr0 } )

        self.addLink( s3, router1, intfName2='r1-eth1',
                      params2={ 'ip' : defaultIPr1 } )


        self.addLink( s1, router0, intfName2='r0-eth2' )
        self.addLink( s2, router1, intfName2='r1-eth2' )

        h1 = self.addHost( 'h1', ip='128.0.0.1/16' )
        h2 = self.addHost( 'h2', ip='128.0.0.2/16' )

        self.addLink( h1, s1 )
        self.addLink( h2, s1 )

        h3 = self.addHost( 'h3', ip='192.168.0.1/24' )
        h4 = self.addHost( 'h4', ip='192.168.0.2/24' )

        self.addLink( h3, s2 )
        self.addLink( h4, s2 )



def run():
    "LV Netzwerke Heinemann / Linux Static Router Exercise"
    topo = NetworkTopo()
    net = Mininet( topo=topo,
                   waitConnected=True )  # controller is used by s1-s3
    net.start()
    # info( '\n...adding second IP to Router r0 at interface r0-eth2\n' )
    info( net[ 'r0' ].cmd( 'ifconfig r0-eth2 128.0.0.100' ) )
    # info( '...adding second IP to Router r1 at interface r1-eth2\n' )
    info( net[ 'r1' ].cmd( 'ifconfig r1-eth2 192.168.0.100' ) )
    # info( '\n\n' )

    # info( '\n*** Routing Table on Router r0:\n' )
    # info( net[ 'r0' ].cmd( 'route' ) )
    # info( '\n*** Routing Table on Router r1:\n' )
    # info( net[ 'r1' ].cmd( 'route' ) )

    # info( '\n*** Routing Table on Host h1:\n' )
    # info( net[ 'h1' ].cmd( 'route' ) )

    # info( '\n*** Routing Table on Host h2:\n' )
    # info( net[ 'h2' ].cmd( 'route' ) )

    # info( '\n*** Routing Table on Host h3:\n' )
    # info( net[ 'h3' ].cmd( 'route' ) )

    # info( '\n*** Routing Table on Host h4:\n' )
    # info( net[ 'h4' ].cmd( 'route' ) )


    CLI( net )
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
