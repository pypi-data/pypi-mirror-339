import socket
import pickle
import struct


class NmexecClient:
    def __init__(
        self,
        host: str,
        port: int,
        model_name: str,
        model_kwargs: dict,
    ):
        self.host = host
        self.port = port
        self.model_name = model_name
        self.model_kwargs = model_kwargs
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        conf = {
            "model_name": self.model_name,
            "model_kwargs": self.model_kwargs,
        }
        data = pickle.dumps(conf)
        self.socket.sendall(struct.pack("!I", len(data)))
        self.socket.sendall(data)


    def disconnect(self):
        self.socket.close()


    def exec_data(self, x):
        data = pickle.dumps(x)
        self.socket.sendall(struct.pack("!I", len(data)))
        self.socket.sendall(data)
        rdata = b""
        while len(rdata) < 4:
            rdata += self.socket.recv(4 - len(rdata))
        size = struct.unpack("!I", rdata)[0]
        rdata = b""
        while len(rdata) < size:
            rdata += self.socket.recv(size - len(rdata))
        y = pickle.loads(rdata)

        return y
