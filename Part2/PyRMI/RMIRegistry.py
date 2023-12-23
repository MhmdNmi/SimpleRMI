import pickle
import socketserver
from RMIconfig import config

class Registry(socketserver.BaseRequestHandler):
    registry_list = dict()

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
    

    def handle(self):
        data = pickle.loads(self.request.recv(4096))

        print(f'\n\tdata: {data}\n')

        try:
            if data['Action'] not in ["ADD", "GET", "DEL"]:
                raise Exception()
        except:
            response = {"error": "Wrong request!"}
            self.request.sendall(pickle.dumps(response))

        if data['Action'] == "ADD":
            if data['Update'] == False and self.registry_list.get(data['object_name'], None) is not None:
                response = {"success": False, "error": "Duplicate name!"}
            else:
                self.registry_list[data['object_name']] = data['address']
                print(f"\n\tNew address added: {self.registry_list[data['object_name']]}\n")
                response = {"success": True}
            self.request.sendall(pickle.dumps(response))

        else:
            if data['Action'] == "GET":
                address = self.registry_list.get(data['object_name'], None)
            if data['Action'] == "DEL":
                address = self.registry_list.pop(data['object_name'], None)
            
            if address is None:
                response = {"success": False, "error": "Name not found!"}
            else:
                response = {"success": True, "address": address}
            
            self.request.sendall(pickle.dumps(response))

if __name__ == "__main__":
    registry_address = (config['REGISTRY_HOST'], config['REGISTRY_PORT'])
    ns = socketserver.TCPServer(registry_address, Registry)

    try:
        print(f"\n\tRegistry is listening on {config['REGISTRY_HOST']}:{config['REGISTRY_PORT']}\n")
        ns.serve_forever()

    except:
        print("\n\tRegistry is down.\n")
        ns.shutdown()