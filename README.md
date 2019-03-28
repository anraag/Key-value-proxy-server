Key-Value Storage System 

Project Description

This project introduces the concept of client/server architecture and caching as discussed in class. Your task is to create a simple web and proxy server that stores and retrieves key-value pairs using socket programming interface. The server only permits commands such as GET PUT and DUMP in the request field followed by the key and value stored. GET returns the value of the key specified, PUT stores the key and a specified value on the server and DUMP lists all of the key value pairs contained in the server. When the client makes a GET request, this request is passed through the proxy server. If the server has made the same request using the same key, the key-value should be retrieved from the proxy server instead of the server. 
