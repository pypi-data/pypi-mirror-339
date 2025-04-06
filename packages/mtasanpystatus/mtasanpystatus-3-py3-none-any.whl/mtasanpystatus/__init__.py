import socket
from typing import Optional, Tuple

class ServerException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

# Module-level attributes (only keeping what you use)
address: Optional[str] = None
name: Optional[str] = None
port: Optional[int] = None
gamemode: Optional[str] = None
map: Optional[str] = None
version: Optional[str] = None
players: Optional[int] = None
maxplayers: Optional[int] = None
join_link: Optional[str] = None

def _validate_address(addr: str) -> bool:
    try:
        socket.inet_aton(addr)
        return True
    except socket.error:
        return False

def _read_row(response: bytes, start: int) -> Tuple[int, str]:
    """Simplified version without player name parsing"""
    if start >= len(response):
        return start, ""
    
    try:
        length = response[start] - 1
        if length < 0 or start + 1 + length > len(response):
            return start + 1, ""
        
        value = response[start + 1:start + 1 + length]
        return start + 1 + length, value.decode('utf-8', errors='ignore')
    except:
        return start + 1, ""

def _read_socket_data(response: bytes, addr: str, port_num: int):
    global address, name, port, gamemode, map, version, players, maxplayers, join_link
    
    address = addr
    port = port_num
    
    start = 4
    params = ('game', 'port', 'name', 'gamemode', 'map', 'version', 'somewhat', 'players', 'maxplayers')
    values = {}
    
    for param in params:
        start, value = _read_row(response, start)
        values[param] = value

    # Skip unwanted fields (faster processing)
    for _ in range(3):
        start, _ = _read_row(response, start)

    # Only keep the essential fields you use
    name = values['name']
    gamemode = values['gamemode']
    map = values['map']
    version = values['version']
    players = int(values['players']) if values['players'] and values['players'].isdigit() else 0
    maxplayers = int(values['maxplayers']) if values['maxplayers'] and values['maxplayers'].isdigit() else 0
    join_link = f'mtasa://{address}:{port}' if address and port else None

def connect(addr: str, port_num: int = 22003, timeout: float = 0.2):
    """Connect to a MTA:SA server (optimized version)"""
    global address, port
    
    if not _validate_address(addr):
        raise ServerException(f'Invalid server address: {addr}')

    ase_port = port_num + 123
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    
    try:
        sock.connect((addr, ase_port))
        sock.send(b"s")
        response = sock.recv(16384)
        _read_socket_data(response, addr, port_num)
    except socket.error as e:
        raise ServerException(f"Can't connect to server. Original exception: {str(e)}")
    finally:
        sock.close()