# nets-tcp-framed-race lab

This lab will showcase race conditions and threads.

In the previous lab, the server supported multiple clients via the use of `os.fork()`. However `FramedThreadServer.py` uses threds instead.

This lab implements a threaded version of the file transfer client server. Instead of using mutex which is discontinued in `python3`, the implementation is using threading.Lock(), lock.acquire() and lock.release(). 

Run `fileServer.py` with the following command:

        $ python3 fileServer.py

Run `fileClient.py` for a client to run ( you can use up to ten clients).

        $ python3 fileClient.py

`fileClient.py` creates input file, `input_file.txt`,  generating data to be sent onto the server. Now, the problem to solve is what happens when two file transfers occur at the same time for the same file onto the server. This is solved by creating the same file on the client side, in order for parallelism to be achieved. The server side with the help of the threading starts up a client and acquire() in order to change the state to lock, and while it finishes its execution it saves the input from the client generating an output file with the number of the client. Once the file is saved the release() method is executed in order to change the state to unlock, giving priority to the other client.


## Refrences
* https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
* https://docs.python.org/3/library/threading.html#module-threading
* https://github.com/f18-os/nora-file-transfer-alira33
