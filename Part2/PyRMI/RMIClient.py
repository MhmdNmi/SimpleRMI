import socket
import pickle

class Stub:
    def __init__(self, registry_address, object_name):
        self.registry_address = registry_address
        self.object_name = object_name

        message = {
                    "Action": "GET",
                    "object_name": self.object_name
                }

        ret = self.transfer_data(self.registry_address, message)
        if ret['success'] == True:
            self.object_address = ret['address']
        else:
            raise Exception(ret["error"])

    def __getattr__(self, key):
        def f(*args, **kwargs):
            return self.transfer_data(self.object_address, (key, args, kwargs))
        return f

    def transfer_data(self, address, message):
        tmp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tmp_socket.settimeout(5)
        tmp_socket.connect(address)
        tmp_socket.sendall(pickle.dumps(message))
        result = tmp_socket.recv(4096)
        return pickle.loads(result)
