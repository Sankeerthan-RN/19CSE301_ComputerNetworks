import socket
import threading
import pandas as pd
import csv

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
WELCOME='''
    --------------------------------------------------
   |     ADMISSION FOR ACADEMIC YEAR 2021-22           |
    --------------------------------------------------      '''

detailslist=['SELECT THE  PROGRAMME\n BTECH-1 \n MTECH-2 ','ENTER THE APPLICANT NAME','Gender','FATHER\'S NAME:','MOTHER\'S NAME','EmailID:','ADDRESS:','DOB','Nationality','True']
edu_details=['Enter your Branch:','12th Standard State:','School Studied:', '12th Result:','True']

WELCOME1='''
----------------
EDUCATION DETAILS
-----------------
'''
LR='''
----------------------------
NEW APPICANT REGISTRATION
ENTER1
ALREADY REGISTERD APPLICANT?
ENTER 2
-----------------------------
'''
#reading csv
df=pd.read_csv('Application.csv')
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)
        if msg == DISCONNECT_MSG:
            connected = False        
        # print(f"[{addr}] {msg}")
        # msg = f"Msg received: {msg}"
        msg = WELCOME
        conn.send(msg.encode(FORMAT))
        msg=LR
        conn.send(msg.encode(FORMAT))
        selected=conn.recv(SIZE).decode(FORMAT)
        print(selected,"----")
        if(selected=='1'):
            details(conn,connected)
            msg = WELCOME1
            conn.send(msg.encode(FORMAT))
            education(conn,connected)
        else:
            View(conn,connected)    
        connected=False

    conn.close()

def View(conn,connected):
    while(connected):


        appid=conn.recv(SIZE).decode(FORMAT)
        df2=pd.read_csv('education.csv')
        df1=pd.read_csv('Application.csv')
        x=df1.loc[df1['AppId']==int((appid))]
        rx=x.to_string(index=False)
        y=df2.loc[df2['App_id']==int((appid))]
        ry=y.to_string(index=False)
        conn.send(rx.encode(FORMAT))
        conn.send(ry.encode(FORMAT))
        connected=False
    return    
        

def education(conn,connected):
    while(connected):
        
        #storing the applicant details in list
        education_info=[]
        #reading the csv to get the number of rows
        df1=pd.read_csv('education.csv')
        df2=pd.read_csv('Application.csv')
        id=df1.iloc[-1:,0:1]
        id=id.to_string(index=False,header=None)
        education_info.append(int(id)+1)

        #reading user input  and storing in list
        for i in range (len(edu_details)) :
            conn.send((edu_details[i].encode(FORMAT)))
            val= conn.recv(SIZE).decode(FORMAT)
            if(i!=len(edu_details)-1):
                education_info.append(str(val))
            
        #writing the row in csv    
        # print(education_info)
        with open('education.csv','a') as f_object:
                writer_object = csv.writer(f_object)
                writer_object.writerow(education_info[:])
               
               
        
       

        connected=False    
    return    

def details(conn,connected):
    while(connected):
        
        #storing the applicant details in list
        applicant_info=[]
        #reading the csv to get the number of rows
        df=pd.read_csv('Application.csv')
       
        row=df.shape[0]
        # print(row)
        applicant_info.append(row+1)

        #reading user input  and storing in list
        for i in range (len(detailslist)) :
            conn.send(detailslist[i].encode(FORMAT))
            if(i!=len(detailslist)-1):
                val= conn.recv(SIZE).decode(FORMAT)
            
            if(i!=0 and i!=len(detailslist)-1):
                applicant_info.append(str(val))
            
        #writing the row in csv    
        # print(applicant_info)
        with open('Application.csv','a') as f_object:
                writer_object = csv.writer(f_object)
                writer_object.writerow(applicant_info)
                f_object.close()
        connected=False    
    return    

  

def main():
    print("[STARTING] Server is starting...")
    server = socket.socket()
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

if __name__ == "__main__":
    main()