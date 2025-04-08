import os

def clear_console():
    command = 'cls' if os.name in ('nt', 'dos') else 'clear'
    os.system(command)