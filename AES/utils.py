# PYTHON3 'BYTES' FUNCTIONS
def bytes_to_string(bytes_data):
    return bytes_data.decode()  # default utf-8
 
def string_to_bytes(string_data):
    return string_data.encode()  # default utf-8