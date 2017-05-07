from socket import *
serverName='m-gh.info'
serverPort=12000
clientSocket=socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
sentence=input('Input Lowercase Sentence:')
# clientSocket.send(sentence)
clientSocket.sendto(sentence.encode('utf-8'),(serverName, serverPort))
modifiedSentence=clientSocket.recv(1024)
print ('From Server:',modifiedSentence)
clientSocket.close()

