import socket, os
# import thread module 
from _thread import *
import threading 
  
print_lock = threading.Lock()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 50001))
s.listen(10)  # multiple clients

def handle_client(s, addr, i, c):
    while True:
        # No duplicates of same files
        text_file = str(i) + 'saveFile.txt'

        # Receive, output and save file
        with open(text_file, "wb") as fw:
            print("Receiving..")
            while True:
                print('receiving')
                data = c.recv(100)
                if data == b'BEGIN':
                    continue
                elif data == b'ENDED':
                    print('Breaking from file write')
                    break
                else:
                    decoded_data = data.decode("utf-8")
                    if not decoded_data:
                        print_lock.release()
                        print("\nconnection with client " + str(i) + " broken\n")
                        print("  CLIENT " + str(i) + " -> " + decoded_data)
                        break

                    else:
                        print('Received: ', decoded_data)
                        fw.write(data)
                        print('Wrote to file', decoded_data)
                    
            fw.close()
            print("Received..")
            decoded_data = data.decode("utf-8")
            if not decoded_data:
                print("\nconnection with client " + str(i) + " broken\n")
                break
            print("  CLIENT " + str(i) + " -> " + decoded_data)

        # Append and send file
        print('Opening file ', text_file)
        with open(text_file, 'ab+') as fa:
            print('Opened file')
            print("Appending string to file.")
            string = b"Append this to file."
            fa.write(string)
            fa.seek(0, 0)
            print("Sending file.")
            while True:
                data = fa.read(1024)
                c.send(data)
                if not data:
                    break
            fa.close()
            print("Sent file.")
        break

def server():
    i = 1
    while i <= 10:
        c, addr = s.accept()
        print_lock.acquire() 
        print("\nconnection successful with client " +
                str(i) + str(addr) + "\n")
        start_new_thread(handle_client(c, addr, i, c))
        i += 1


server()
s.close()
