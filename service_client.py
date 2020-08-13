#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
An example for showing clients for DIM servers.

The client will query the values from the two services created in
`service-server.py`, thus it should be run along with that script.

"""

import sys
import time

# Import the pydim module
import pydim

def client_callback1(now):
    """
    Callback function for the service 1.

    Callback functions receive as many arguments as values are returned by the
    service. For example, as the service 1 returns only one string this callback
    function has only one argument.

    """
    print("Client callback function for service 1")
    print("Message received: '%s' (%s)" % (now, type(now)))

def client_callback2(val1, val2):
    """
    Callback function for service 2.

    As the service 2 returned two arguments
    """

    print("Client callback function for service 2")
    print("Values received: %s (%s) and %s (%s)" % (val1, type(val1), val2, type(val2)))

def main():
    """
    A client for subscribing to two DIM services
    """

    # Again, check if a Dim DNS node has been configured.
    # Normally this is done by setting an environment variable named DIM_DNS_NODE
    # with the host name, e.g. 'localhost'.
    #
    if not pydim.dis_get_dns_node():
        print("No Dim DNS node found. Please set the environment variable DIM_DNS_NODE")
        sys.exit(1)

#    pydim.dic_set_dns_node("localhost")
#    dic_node = pydim.dic_get_dns_node()
#    print("dic_node set to ")
#    print(dic_node)
#    dicportsetting = pydim.dic_set_dns_port(8088)
#    if(dicportsetting):
#        print("Client port is set to 8088")

    # The function `dic_info_service` allows to subscribe to a service.
    # The arguments are the following:
    # 1. The name of the service.
    # 2. Service description string
    # 3. Callback function that will be called when the service is
    #    updated.
    res1 = pydim.dic_info_service("example-service-1", "C", client_callback1)
    res2 = pydim.dic_info_service("example-service-2", "D:1;I:1;", client_callback2)

    #res1 = pydim.dic_info_service("example-service-1", client_callback1)
    #res2 = pydim.dic_info_service("example-service-2", client_callback2)

    if not res1 or not res2:
        print("There was an error registering the clients")
        sys.exit(1)

    print("calling example-service-sync that waits 5 seconds to return the number 42")
    res3 = pydim.dic_sync_info_service("example-service-sync",None,5)
    print("example-service-sync returned %s" % str(res3))



    # Wait for updates
    while True:
        tuple_args = ('Test call no. 5')
#        pydim.dic_cmnd_service("int_cmnd",(5,))
        pydim.dic_cmnd_service("int_cmnd",tuple_args,"C")
#        pydim.dic_cmnd_service("string_cmnd",("Hello world !",))
        print("test")
        time.sleep(5)


if __name__=="__main__":
    main()
