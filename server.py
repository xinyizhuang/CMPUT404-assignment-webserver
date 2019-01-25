#  coding: utf-8 

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Xinyi Zhuang
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/



#  coding: utf-8 
import socketserver, os, sys
#import SocketServer, os.path, inspect

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Justin Wong
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        
        method = self.data.split()[0].decode()
        
        if method == "GET" :
            
            filename = self.data.split()[1].decode()  #/index.html
            directory = sys.path[0] + "/www"
            filepath = directory + filename            
            
            #check file exist or not
            if os.path.isfile(filepath):
                # html/css extension
                extension = filename.split('.')[1]
                if extension in ("html", "css") :
                    status = "HTTP/1.1 200 OK\r\nContent-Type: text/%s\r\n\r\n%s" %(extension, open(filepath).read())
                else:
                    status = "HTTP/1.1 404 Not Found\r\nContent-Thpe: text/plain\r\n\r\n%s" %"HTTP/1.1 404 Not Found"
   
            #check the directory
            elif os.path.isdir(filepath) or os.path.isdir(filepath+'/'):    
                if os.path.isfile(filepath + "index.html"):
                    status = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n%s" %open(filepath + "index.html").read()
                #redirect and return 301 status code
                elif os.path.isfile(filepath + "/index.html"):
                    status = "HTTP/1.1 301 Permanently moved\r\nContent-Type: text/html\r\nLocation: %s/\r\n\r\n" %filename
                    
                else:
                    status = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\n%s" %"HTTP/1.1 404 Not Found"
            else:
                status = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\n%s" %"HTTP/1.1 404 Not Found"
        else:
            #cannot handle (POST/PUT/DELETE)
            status = "HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/html\r\n\r\n%s" %"HTTP/1.1 405 Method Not Allowed"
         
        self.request.sendall(status.encode())  

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

