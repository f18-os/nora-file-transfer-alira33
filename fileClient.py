import socket
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 50001))

text_file = 'input_file.txt'
f= open("input_file.txt","w+")
for i in range(100000):
    f.write("This is line %d\r\n"%(i+1))

if os.path.isfile(text_file) and os.stat(text_file).st_size != 0:
    # Send file
    with open(text_file, 'rb') as fs:
        # Using with, no file close is necessary,
        # with automatically handles file close
        s.send(b'BEGIN')
        while True:
            data = fs.read(1024)
            print('Sending data', data.decode('utf-8'))
            s.send(data)
            print('Sent data', data.decode('utf-8'))
            if not data:
                print("No data to read")
                done = False
                print('Breaking from sending data')
                break
        s.send(b'ENDED')
        fs.close()

    # Receive file
    print("Receiving..")
    with open(text_file, 'wb') as fw:
        while True:
            data = s.recv(1024)
            if not data:
                break
            fw.write(data)
        fw.close()
    print("Received..")

    s.close()
else:
    print("File does not exist or empty!")
