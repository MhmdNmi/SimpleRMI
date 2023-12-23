import random
import pickle
import socket
import socketserver

class Skeleton(socketserver.BaseRequestHandler):
    object_n = None

    def __init__(self, *args, **kwargs):
        self.object_n_m = self.object_n
        return super().__init__(*args, **kwargs)

    def invoke_method(self, fname, args, kwargs):
        try:
            method = self.object_n_m.__getattribute__(fname)
        except Exception as error:
            return {"error": error}

        try:
            ret = method(*args, **kwargs)
        except TypeError as error:
            if "not callable" in error.args[0]:
                ret = method
            else:
               return {"error": error} 
        except Exception as error:
            return {"error": error}
            
        return ret

    def handle(self):
        try:
            fname, args, kwargs = pickle.loads(self.request.recv(4096))
            ret = self.invoke_method(fname, args, kwargs)
            self.request.sendall(pickle.dumps(ret))
        except Exception as error:
            self.request.sendall(pickle.dumps({"error": error}))



class Server:
    def __init__(self, registry_address, server_address=None):
        if type(server_address) is tuple:
            self.address = server_address
        else:
            self.address = ("localhost", random.randint(49152, 65535))

        self.registry_address = registry_address
    
    def register(self, name, Class_n, update=False):
        self.name = name

        class ClassSkeleton(Skeleton):
            object_n = Class_n()
        self.skeleton = ClassSkeleton

        registry_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        registry_socket.connect(self.registry_address)

        data = pickle.dumps({
            "Action": "ADD",
            "Update": update,
            "object_name": self.name,
            "address": self.address
        })
        registry_socket.sendall(data)

        response = pickle.loads(registry_socket.recv(4096))
        registry_socket.close()

        if "error" not in response:
            print(f"\n\t{self.name} is registered!\n")
        else:
            print(f"\n\t{response['error']}\n")
            raise Exception(response['error'])


    def run(self):
        server = socketserver.TCPServer(self.address, self.skeleton)
        try:
            print(f"\n\tServer is listening on {self.address[0]}:{self.address[1]}\n")
            server.serve_forever()

        except:
            print("\n\tServer is down.\n")
            server.shutdown()    
    
