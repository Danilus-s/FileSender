import socket, os, tqdm
from os.path import exists

IP = input('IP host> ')
PORT = 7495

BSIZE = 4096
SEP = ':SEP:'

#filename = input('Filename> ')
#filesize = os.path.getsize(filename)


print('Starting...')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORT))
s.listen(5)
print(f'Listening as {IP}:{PORT}.')

client, addr = s.accept()
print(f'{addr[0]} is connected.')

rec = client.recv(1024).decode('utf-8')
fname, fsize = rec.split(SEP)

fname = os.path.basename(fname)
fsize = int(fsize)

def stop(send_mess=False):
    if send_mess:
        client.send('stop'.encode('utf-8'))
    client.close()
    s.close()

pget = input('Receive "' + fname + '"? [Y/n] ')
if not pget.lower().startswith('y'):
    stop(True)

if exists(fname):
    pget = input('"'+fname + '" already exists. Overwride? [Y/n] ')
    if not pget.lower().startswith('y'):
        stop(True)
    
client.send('ok'.encode('utf-8'))
progress = tqdm.tqdm(range(fsize), f'Receiving {fname}', unit='B', unit_divisor=1024)
with open(fname, 'wb') as f:
    while True:
        bread = client.recv()
        if not bread:
            break
        f.write(bread)
        progress.update(len(bread))

stop()
