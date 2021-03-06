"""A proxy server that forwards requests from one port to another server.

To run this using Python 2.7:

% python proxy.py

It listens on a port (`LISTENING_PORT`, below) and forwards commands to the
server. The server is at `SERVER_ADDRESS`:`SERVER_PORT` below.
"""

# This code uses Python 2.7. These imports make the 2.7 code feel a lot closer
# to Python 3. (They're also good changes to the language!)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import socket
import library

# Where to find the server. This assumes it's running on the same machine
# as the proxy, but on a different port.
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 7777

# The port that the proxy server is going to occupy. This could be the same
# as SERVER_PORT, but then you couldn't run the proxy and the server on the
# same machine.
LISTENING_PORT = 8888

# Cache values retrieved from the server for this long.
MAX_CACHE_AGE_SEC = 60.0  # 1 minute


def ForwardCommandToServer(command, server_addr, server_port):
  """Opens a TCP socket to the server, sends a command, and returns response.

  Args:
    command: A single line string command with no newlines in it.
    server_addr: A string with the name of the server to forward requests to.
    server_port: An int from 0 to 2^16 with the port the server is listening on.
  Returns:
    A single line string response with no newlines.
  """

  # Execute the command based on the first word in the command line.
  #open a socket to connect to the server and send the command to it, then, close the client socket.
  client_sock = library.CreateClientSocket(server_addr, server_port)
  client_sock.sendall(command)
  data = client_sock.recv(1024)
  client_sock.close()
  return data
  ###################################################
  #TODO: Implement Function: WiP
  ###################################################

'''
def CheckCachedResponse(command_line, cache):
  cmd, name, text = library.ParseCommand(command_line)

  # Update the cache for PUT commands but also pass the traffic to the server.
  if cmd == "PUT":
    return ForwardCommandToServer(command_line, SERVER_ADDRESS, SERVER_PORT)

  ##########################
  #TODO: Implement section
  ##########################
  elif cmd == "GET":
    if name in cache.Keys():
      cache.StoreValue(name, cache.GetValue(name), 1)
      return cache.GetValue(name)
    else:
      data = ForwardCommandToServer(command_line, SERVER_ADDRESS, SERVER_PORT)
      cache.StoreValue(name, data, 1)
      return data

  # GET commands can be cached.

  ############################
  #TODO: Implement section
  ############################

  '''


def ProxyClientCommand(sock, server_addr, server_port, cache):
  """Receives a command from a client and forwards it to a server:port.

  A single command is read from `sock`. That command is passed to the specified
  `server`:`port`. The response from the server is then passed back through
  `sock`.

  Args:
    sock: A TCP socket that connects to the client.
    server_addr: A string with the name of the server to forward requests to.
    server_port: An int from 0 to 2^16 with the port the server is listening on.
    cache: A KeyValueStore object that maintains a temorary cache.
    max_age_in_sec: float. Cached values older than this are re-retrieved from
      the server.
  """
  command_line = library.ReadCommand(sock)
  cmd, name, text = library.ParseCommand(command_line)

  # Update the cache for PUT commands but also pass the traffic to the server.
  if cmd == "PUT" or cmd == "DUMP":
    if cmd == "PUT":
      #if the given key is already in proxy server cache but the value is updated in the server database, 
      # we want to have the value corresponding to the key updated in the proxy server cache too.
      if name in cache.Keys():
        cache.StoreValue(name, text + "\n", 1)
    #pass the traffic to the server
    return ForwardCommandToServer(command_line, server_addr, server_port)
    

  ##########################
  #TODO: Implement section
  ##########################

  elif cmd == "GET":
    if name in cache.Keys():
      # check if the given key has not crossed maximum cache age
      if cache.GetValue(name, MAX_CACHE_AGE_SEC) != None:
        data = cache.GetValue(name, MAX_CACHE_AGE_SEC)
        #since we used GET on a key that is already in the proxy server cache, 
        # its "time accessed" should be changed to the current time.
        cache.StoreValue(name, data, 1)
        return data
      else:
        data = ForwardCommandToServer(command_line, server_addr, server_port)
        #if the given key is not in proxy server cache  but is past the maximum cache age, 
        # we update the proxy cache to change the time accessed to the current time.
        cache.StoreValue(name, data, 1)
        return data
    else:
      #if the key is not in the proxy cache, we retrieve the value from the server
      data = ForwardCommandToServer(command_line, server_addr, server_port)
      cache.StoreValue(name, data, 1)
      return data
  
  ###########################################
  #TODO: Implement ProxyClientCommand
  ###########################################




def main():
  # Listen on a specified port...
  #wait for a keyboard interrupt to end the while loop and close the server socket
  try:
    server_sock = library.CreateServerSocket(LISTENING_PORT)
    cache = library.KeyValueStore()
    # Accept incoming commands indefinitely.
    while True:
      # Wait until a client connects and then get a socket that connects to the
      # client.
      client_sock, (address, port) = library.ConnectClientToServer(server_sock)
      print('Received connection from %s:%d' % (address, port))
      response = ProxyClientCommand(client_sock, SERVER_ADDRESS, SERVER_PORT,
                        cache)
      client_sock.sendall(response)
      
      client_sock.close()
  except KeyboardInterrupt:
    server_sock.close()
  #################################
  #TODO: Close socket's connection
  #################################


main()
