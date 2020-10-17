import socket


if __name__ == "__main__":
    s = socket.socket()
    s.connect(('localhost', 8000))
    guess = 50
    while True:
        data = s.recv(11)
        resp = data.decode("utf-8")
        print(resp)
        if resp == 'correct':
            s.close()
            exit(1)
        elif resp == 'less':
            guess = guess - 1
        elif resp == 'more':
            guess = guess + 1
        s.send(bytes(str(guess), "utf-8"))



