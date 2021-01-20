import socket  
from _thread import *
import threading
from collections import Counter
import time
  

candidate_vs_vote={'Manjunath':0,'Hemanth':0,'Arvind':0,'Gopal':0,'Prakruthi':0,'Veena':0} #globally initialise the dictionary

def threaded(c,name_list,database_list):
        
        enter_name="------------------- Welcome to the Online Voting Portal -----------------\n\nPlease Enter your Username and Password in the format (Usr-Pwd) "
        c.send(enter_name.encode('ascii'))
        f_v=open("Voter_names.txt","a")
        f_c=open("Candidate_names.txt","r")
        
        name = c.recv(1024)
        name=str(name.decode('ascii'))

       
        if name not in database_list:
                wrong="The username or password you entered is incorrect\nPlease Enter your Username and Password once again in the format (Usr-Pwd) "
                c.send(wrong.encode('ascii'))
                name1 = c.recv(1024)
                name1=str(name1.decode('ascii'))
                if name1 not in database_list:
                    closeit="You have exceeded your login limit. Your Vote thus stands cancelled."
                    c.send(closeit.encode('ascii'))    
                else:
                    if name1 not in name_list:
                        name_list.append(name1)
                        f_v.write(name1)
                        f_v.write("\n")
                        enter_vote=("You are allowed to cast your vote only once.\nSelect any one of the candidates mentioned below carefully.\n")
                        c.send(enter_vote.encode('ascii'))

                        all_candidates=""
                        for candidate_name in f_c:
                            all_candidates+=candidate_name
                        c.send(all_candidates.encode('ascii'))
                        
                        vote=c.recv(1024)
                        vote=str(vote.decode('ascii'))
                            
                        if vote in candidate_vs_vote:
                           # print("Checkcounter candidate_vs_vote before{} ".format(candidate_vs_vote[vote]))
                            candidate_vs_vote[vote]+=1
                            #print("Checkcounter candidate_vs_vote after{} ".format(candidate_vs_vote[vote]))
                        else:
                            no_candidate="The candidate of your choice does not exist. Your vote thus stands cancelled."
                            c.send(no_candidate.encode('ascii'))
                    else:
                        enter_vote="Sorry, you have already voted."
                        c.send(enter_vote.encode('ascii'))

        else:    

                if name not in name_list:
                    name_list.append(name)
                    f_v.write(name)
                    f_v.write("\n")
                    enter_vote=("You are allowed to cast your vote only once.\nSelect any one of the candidates mentioned below carefully.\n")
                    c.send(enter_vote.encode('ascii'))

                    all_candidates=""
                    for candidate_name in f_c:
                        all_candidates+=candidate_name
                    c.send(all_candidates.encode('ascii'))
                        
                    vote=c.recv(1024)
                    vote=str(vote.decode('ascii'))
                          
                    if vote in candidate_vs_vote:
                       # print("Checkcounter candidate_vs_vote before{} ".format(candidate_vs_vote[vote]))
                        candidate_vs_vote[vote]+=1
                        #print("Checkcounter candidate_vs_vote after{} ".format(candidate_vs_vote[vote]))
                    else:
                        no_candidate="The candidate of your choice does not exist. Your vote thus stands cancelled."
                        c.send(no_candidate.encode('ascii'))
                else:
                    enter_vote="Sorry, you have already voted."
                    c.send(enter_vote.encode('ascii'))

        f_v.close()
        f_c.close()
        c.close() 
        
def Main(): 
    name_list=[]    #list that holds already voted persons names read from a file
    Votes_buff=[]   #list that holds number of votes that was casted in the previous session of server
    symbol_list=['Tiger', 'Fan', 'Table', 'Book', 'Peacock', 'Vase']

    #creating voters database list
    f_d=open("Voters_database.txt","r")
    database_list=[]    #from database you read the names of eligible candidates
    for data in f_d:
        database_list.append(data)
    database_list=[x[:-1] for x in database_list]

    
    f_vot_rec=open("Votes_Rec.txt","r")    #this is used to keep track of no of votes
    for i in f_vot_rec:
        Votes_buff.append(i.split("\n")[0])    #read votes from file into a buffer
    for key in Votes_buff:
        candidate_vs_vote[key]+=1           #increment the candidates votes depending on the number of occurences of his name in vtes buffer
    
    old_Votes_buff=Votes_buff           #save the initial state of votes before starting this session.needed to find number votes added in this sesion so that so many vtes can be updates
    old_candidate_vs_vote=Counter(old_Votes_buff)
    host = "" 
    port = 2345     #select any port this must be same at the client side
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM) #####
    s.bind((host, port)) 
    #print("socket binded to port", port)
    s.listen(3) 
    #print("socket is listening")

    
    
    #to copy voter names file to num_list from pevious session
    f_v=open("Voter_names.txt","r")
    for i in f_v:
        name_list.append(i)
    name_list = [x[:-1] for x in name_list]

    print("\n")
    cnt=int(input("Enter the number of people voting for this round : "))
    while (cnt>=1):
        c, addr = s.accept()
        #print('Connected to :', addr[0], ':', addr[1])
        #fucntion calling
        threaded(c,name_list,database_list)
        cnt-=1
    yorn=input("Should the final results be declared now? (Y/N) : ")
    if yorn=="Y":
            
        sym_cnt=0
        #to print the results
        print("----------------------------------------------------------------------------------")
        print("                                 RESULTS DECLARED")
        print("----------------------------------------------------------------------------------")
        print("                     -------------------------------------")
        print("                     | Candidate    | Symbol     | Votes |")
        print("                     -------------------------------------")
        for key,val in candidate_vs_vote.items():
            print("                     | {:<12} | {:<7}    |  {:^3}  |".format(key,symbol_list[sym_cnt],val))
            sym_cnt+=1
        print("                     -------------------------------------")    
        print("\n************************** Online Voting Portal Closing **************************\n**************************** Thanks all for voting !! ****************************")
        print("\n The Winner is:{}".format(max(candidate_vs_vote, key=lambda key: candidate_vs_vote[key])))
        s.close()
    else:
        print("The final results will be declared after further rounds.")
        s.close()
            
        
    update_votes=open("Votes_Rec.txt","a")
    for key in candidate_vs_vote:
        counts=candidate_vs_vote[key]-old_candidate_vs_vote[key]
        while(counts>0):
            update_buffer=key
            update_votes.write(update_buffer)
            update_votes.write("\n")
            counts-=1
  
if __name__ == '__main__': 
    Main()
