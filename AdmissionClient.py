import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"


def appilicantDetails(client,connected):
    while connected:
        pgmselection=client.recv(SIZE).decode(FORMAT)
        if(pgmselection=='True'):
            return
            
        else:
            print(f"{pgmselection}")
            response=input('>')
            client.send(response.encode(FORMAT))  
    
def educationDetails(client,connected):
   
    while connected:
        
        pgmselection=client.recv(SIZE).decode(FORMAT)
        if(pgmselection=='True'):
            connected=False
        else:
            print(f"{pgmselection}")
            response=input('>')
            client.send(response.encode(FORMAT))  

    print('hhh')        
    return 

def View(client,connected):
    while connected:
        print(f"Enter the Application id")
        response=input('>')
        client.send(response.encode(FORMAT))
        data=client.recv(SIZE).decode(FORMAT)
        print(f'''
------------------
 PERSONAL DETAILS
------------------
         \n''')
        print(f"{data}")
        data=client.recv(SIZE).decode(FORMAT)
        print(f'''
-------------------
EDUCATIONAL DETAILS
-------------------
         \n''')
        print(f"{data}")
        connected=False
    return

def main():
    # print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")
    client = socket.socket()
    client.connect(ADDR)
    connected = True
    msg = input(">")
    while connected:
       
        client.send(msg.encode(FORMAT))

        if msg == DISCONNECT_MSG:
            connected = False

        elif(msg=='START'):
            msg = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER] {msg}")
            lr=client.recv(SIZE).decode(FORMAT)
            print(f"{lr}")
            response=input('>')
            client.send(response.encode(FORMAT)) 
            if(response=='1'):
                appilicantDetails(client,connected)
                print('k')
                msg=client.recv(SIZE).decode(FORMAT)
                print(msg)
                connected=True
                educationDetails(client,connected)
            else:
                #further with viewing functionality updating any entered data will also be done
                View(client,connected)    
            connected =False
    client.close()            

            
            

if __name__ == "__main__":
    main()