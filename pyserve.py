#!/bin/env python
# -*- coding: UTF-8 -*-
"""
An example for showing how to create a server with DIM.

The server exposes two services that are updated periodically. One of them uses
its function callback to get a string with the current time, the other one
returns a pair of numeric values.

"""

import sys
import time

# Import the pydim module
import pydim
from time import sleep
from datetime import date
#import debug
#import pdb
#from debug import SAY, ERROR, DEBUG
from pydim import dis_update_service, dis_add_service, dic_info_service, dis_start_serving, dis_stop_serving



def service_callback_libo(tag):
    print ("Running callback function for service (libo)")
    now = time.strftime("%X")
    print("Hello! The time is %s" % now)
    return ("hh")

def service_callback(tag):
    """
    Service callbacks are functions (in general, Python callable objects)
    that take one argument: the DIM tag used when the service was added,
    and returns a tuple with the values that corresponds to the service
    parameters definition in DIM.
    """

    print("Running callback function for service 1")

    # Calculate the value
    # This example returns a string with the current time
    now = time.strftime("%X")
    #today = date.today()
    #dd/mm/yy
    #d1=today.strftime("%d/%m/%Y")
   
    # Remember, the callback function must return a tuple
    #print ("Hello! The time is %s" % now,)
    #return ("Hello! The time is ")
    return ("Hello! The time(test) is %s" % now,)
def service_callback2(tag):
    """
    The callback function for the second service.
    """
    # Calculate the value of the server
    # ...
    print("Running callback function for service 2")
    val1 = 3.11
    val2 = 42
    return (val1, val2)

def service_sync_callback(tag):
    print("waiting 5 seconds before returning a value...")
    value = 42
    return(value,)





def main():
    """
    A simple DIM server with two services.
    """
    #Server configuration

    # First of all check if a Dim DNS node has been configured.
    # Normally this is done by setting an environment variable named DIM_DNS_NODE
    # with the host name, e.g. 'localhost'.
    #
    pydim.dis_set_dns_node("localhost")
    
    pydim.dis_set_dns_port(631)

    if not pydim.dis_get_dns_node():
        print("No Dim DNS node found. Please set the environment variable DIM_DNS_NODE")
        sys.exit(1)

    if not pydim.dis_get_dns_port():
        print("No Dim DNS port found. Please set the environment variable DIM_DNS_PORT")
        sys.exit(1)


    print(pydim.dis_get_dns_port())
    print(pydim.dis_get_dns_node())




    # The function dis_add_service is used to register the service in DIM
    # The arguments used are the following:
    #  1. Service name. It must be a unique name within a DNS server.
    #  2. Service description string.
    #  3. A callback function that will be executed for getting the value of
    #     the service.
    #  4. Tag. A parameter to be sent to the callback in order to identify
    #     the service. Normally this parameter is rarely used (but it's still
    #     mandatory, though).
   
    svc = pydim.dis_add_service("example-service-1", "C", service_callback, 0) #original
    # Register another service
    svc2 = pydim.dis_add_service("example-service-2", "D:1;I:1;", service_callback2, 0)

    svc3 = pydim.dis_add_service("example-service-sync","I",service_sync_callback,0)

    # The return value is the service identifier. It can be used to check
    # if the service was registered correctly.
    if not svc or not svc2 or not svc3:
      sys.stderr.write("An error occurred while registering the service\n")
      sys.exit(1)

    print("Services correctly registered")



    # A service must be updated before using it.
    print("Updating the services ...")
    pydim.dis_update_service(svc)
    pydim.dis_update_service(svc2)
    pydim.dis_update_service(svc3)
    print("")

    # Start the DIM server.
    pydim.dis_start_serving("server-name")
    print("Starting the server ...")

    # Initial values for the service 2. Please see below.
    val1 = 3.11
    val2 = 0
    # starting the loop
    while True:
      # Update the services periodically (each 5 seconds)
      time.sleep(5)

      print("")

      # Case 1: When `dis_update_service` is called without arguments the
      # callback function will be executed and its return value
      # will be sent to the clients.
      print("Updating the service 1 with the callback function")
      #update service 1 every 5 seconds
      pydim.dis_update_service(svc)


      # Case 2: When `dis_update_service` is called with arguments, they are
      # sent directly to the clients as the service value, *without* executing the
      # callback function. Please note that the number and the type of the
      # arguments must correspond to the service description.
      #

      # Update the second server each 10 seconds/time interval = 5 seconds
      #
      if val2 % 2:
          print("Updating the service 2 with direct values")
          pydim.dis_update_service(svc2, (val1, val2))

      

      # For the sake of the example, update the values passed to svc2:
      val1 = val1 + 11.30
      val2 = val2 + 1

      


if __name__ == "__main__":
    main()

