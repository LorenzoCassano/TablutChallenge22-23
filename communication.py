import socket
import struct
import json
from utils import converter

class Connector:
    """
    This class has only to send or recive the message from client to server
    """
    
    def __init__(self, name, color, address, sock = None):
        if sock == None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else : 
            self.sock = sock
        self.name = name
        self.color = color
        self.address = address
   
    def connection(self):
        """
        This method connects the client to the server
        """
        if self.color == 'WHITE':
            # Connect the socket to the port where the server is listening
            server_address = (self.address, 5800)
        elif self.color == 'BLACK':
            #  Connect the socket to the port where the server is listening
            server_address = (self.address, 5801)
        else:
            raise Exception("If you play you could only be white or black")
        # Enstablish connection
        self.sock.connect(server_address)

        # Using struct lib in order to represent data as python bytes objects
        # struct.pack(format, val1, val2...) 
        # '>i' means Big Endian(used in network), integer returns a bytes object. 
        self.sock.send(struct.pack('>i', len(self.name)))
        self.sock.send(self.name.encode())
        #print("Sto inviando")

    def recbytes(self, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = b''
        while len(data) < n:
            packet = self.sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data


        # Returning the state as a matrix, who's turn and king_pos
    def get_state(self):
        '''
        Using struct lib in order to represent data as python bytes objects
        struct.pack(format, val1, val2...) 
        '>i' means Big Endian(used in network), integer returns a bytes object. 
        '''
        len_bytes = struct.unpack('>i', self.recbytes(4))[0]
        current_state_server_bytes = self.sock.recv(len_bytes)
        
        # Converting byte into json 
        json_state = json.loads(current_state_server_bytes)
        matrix, king_position = converter(json_state)
        return matrix, king_position
    
    def send_move(self, alpha_move):
        """
        Input: string move: (from, to)
        This method sends the move to a Server in the following template:
            from: letter + number, the letter identifies the column and the number identifies the row
            to: letter + number, same structure
        
        """

        move = json.dumps({
            "from": alpha_move[0], 
            "to" : alpha_move[1],
            "turn" : self.color
        })

        # Using struct lib in order to represent data as python bytes objects
        # struct.pack(format, val1, val2...) 
        # '>i' means Big Endian(used in network), integer returns a bytes object. 
        
        self.sock.send(struct.pack('>i', len(move)))
        self.sock.send(move.encode())
        
    


