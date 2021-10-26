import socket, os, tqdm

IP = input('IP host> ')
PORT = 7495

BSIZE = 4096
SEP = ':SEP:'

filename = input('Filename> ')
filesize = os.path.getsize(filename)


print(f'Connecting to {IP}:{PORT}')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((IP, PORT))
except Exception as ex:
    print(ex)
    exit()
print('Connected.')

s.send(f'{filename}{SEP}{filesize}'.encode('utf-8'))

resp = s.recv(1024).decode('utf-8')
if resp == 'ok':
    progress = tqdm.tqdm(range(filesize), f'Sending {os.path.basename(filename)}', unit='B', unit_divisor=1024)
    with open(filename, 'rb') as f:
        while True:
            bread = f.read(BSIZE)
            if not bread:
                break
            s.send(bread)
            progress.update(len(bread))

s.close()