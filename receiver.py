import socket, os, tqdm

IP = input('IP host> ')
PORT = 7495

BSIZE = 4096
SEP = ':SEP:'

#filename = input('Filename> ')
#filesize = os.path.getsize(filename)


print('Starting')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORT))
s.listen(5)
print(f'Listening as {IP}:{PORT}')

client, addr = s.accept()
print(f'{addr} is connected.')

rec = client.recv(1024).decode('utf-8')
fname, fsize = rec.split(SEP)

fname = os.path.basename(fname)
fsize = int(fsize)


pget = input(fname+ '[Y/n]? ')
if pget.lower().startswith('y'):
    client.send('ok'.encode('utf-8'))
    progress = tqdm.tqdm(range(fsize), f'Receiving {fname}', unit='B', unit_divisor=1024)
    with open(fname, 'wb') as f:
        while True:
            bread = client.recv(BSIZE)
            if not bread:
                break
            f.write(bread)
            progress.update(len(bread))


client.close()
s.close()