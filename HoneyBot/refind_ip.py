from socket import gethostbyaddr

if __name__ == '__main__':
    for i in range(116):
        try:
            print(gethostbyaddr('192.168.1.'+str(140 + i)))
            print('next')
        except:
            continue



