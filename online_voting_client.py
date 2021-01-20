import socket 
    
def Main():  
    host = '2409:4073:2086:292e:347e:d8c:b91:4666'
    #host='127.0.0.1'
    port = 2345
    s = socket.socket(socket.AF_INET6,socket.SOCK_STREAM) 
    s.connect((host,port)) 
    
    # print the statement sent by server to name themselves
    recv1 = s.recv(1024)
    print("\n")
    print(str(recv1.decode('ascii')))

    # enter user name and send it to server
    data1=input() 
    s.send(data1.encode('ascii'))

    # print the statement sent by server to whom to vote
    recv2=s.recv(1024) # recevives enter_vote from server
    print("\n")
    print(str(recv2.decode('ascii')))

    # check if user is already there 
    if str(recv2.decode('ascii'))=="Sorry, you have already voted.":
        s.close()
    elif str(recv2.decode('ascii'))=="The username or password you entered is incorrect\nPlease Enter your Username and Password once again in the format (Usr-Pwd) ":
        datan=input() 
        s.send(datan.encode('ascii'))
        
        recva=s.recv(1024)
        print(str(recva.decode('ascii')))
        if str(recva.decode('ascii'))=="You have exceeded your login limit. Your Vote thus stands cancelled.":
            s.close()
        elif str(recva.decode('ascii'))=="Sorry, you have already voted.":
            s.close()
        else:
            # to print list of candidates
            recv3=s.recv(1024)
            print(str(recv3.decode('ascii')))

            # enter user wished candidate name
            data2=input() 
            s.send(data2.encode('ascii'))

            # if user enters non existant candidate name        
            recv4=s.recv(1024)
            print("\n")
            print(str(recv4.decode('ascii')))
            if str(recv4.decode('ascii'))=="The candidate of your choice does not exist. Your vote thus stands cancelled.":
                s.close

        
        #s.close()        
    else:
        # to print list of candidates
        recv3=s.recv(1024)
        print(str(recv3.decode('ascii')))

        # enter user wished candidate name
        data2=input() 
        s.send(data2.encode('ascii'))

        # if user enters non existant candidate name        
        recv4=s.recv(1024)
        print("\n")
        print(str(recv4.decode('ascii')))
        if str(recv4.decode('ascii'))=="The candidate of your choice does not exist. Your vote thus stands cancelled.":
            s.close
    print("\n")
    print("Thank you for participating in the Online-Voting session.\nHave a happy and safe day !!")
    s.close() 
  
if __name__ == '__main__': 
    Main()




