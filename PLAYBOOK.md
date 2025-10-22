## COS 460/540 - Computer Networks
# Project 2: HTTP Server

# Irenya Cai

This project is written in Python on Window.

## How to compile

This project does not required complie, but you need to install Python to run it.

## How to run

Run this project by open the terminal or command prompt. Then, naviagte to the directory containing the server.py file, which mine is Project2_Server.py. Also, make sure that there is a www folder with the file project you want to run. After the naviagtion, run the server by using "python Project2_Server.py --port 1010 --root ./www" which --port specifies the port number (1010 is defualt) and --root is the document root folder (./www is default). 

Open another command prompt and using curl to access the server, "curl -v http://localhost:1010/index.html," Which "-v" will shows the headers and the body. 

To visit on a browser, type in "http://localhost:1010/index.html" in the search bar.

## My experience with this project

My experience with this project is it taught me how the simple HTTP works and how to handle TCP sockets with the threads. I learned how to parse HTTP requests and extract the request line into 3 parts (GET method, path, HTTP version), to built the responses of HTTP method with the status codes. I know how to get the full file path on the server from the root and how to read the file's contents now. Also, I leanred how to use MIME type to serve text and binary files, and handling multiple clients using threads. Lastly, I learned some error handling for invalild requests or missing files.
