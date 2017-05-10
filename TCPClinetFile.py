from socket import *
serverName='m-gh.info'
serverPort=12001
clientSocket=socket(AF_INET,SOCK_STREAM)

fileName=input("Please Insert Name Of Your Text File:")
# try:
file=open(fileName+".txt","rb")
l=file.read()
clientSocket.connect((serverName,serverPort))
print(l)
clientSocket.sendall(l)
file.close()
# except:
# print("\n\n\nSomething Goes Wrong. Please Try Again!\n\n")
# exit()

# clientSocket.sendto(bytes([num_lines]),(serverName, serverPort))#Saying Number Of Lines To Server
# for line in myFile:
#     clientSocket.sendto(line.encode('utf-8'),(serverName, serverPort))
modifiedSentence=clientSocket.recv(1024)
print ('From Server:',modifiedSentence)
clientSocket.close()