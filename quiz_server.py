import socket
import random
from threading import Thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address,port))
server.listen()

list_of_clients = []
nicknames = []

questions = [
    "Which is the only city in the World to span 2 continents ? \n a)Cairo b)Panama City c)Istanbul d)Moscow ",
    "What is 'topor' ? \n a)Hibernating b)Hovering c)Hunting d)None of these",
    "Which is the largest bird on Earth ? \n a)Kiwi b)Ostrich c)Falmingo d)Penguin",
    "Who invented the Aeroplane ? \n a)Waterman Brothers b)Thomas Alva Eddisson c)Wright Brothers d)Benjamin Franklin"
]

answers = [
    "c","a","b","c"
]

print("Server has started")

def clientThread(conn):
    score = 0
    conn.send("Welcome to this quiz game!".encode('utf-8'))
    conn.send("You will recive a question. Choose the correct answer from the options provided....")
    conn.send("Good Luck! \n\n".encode('utf-8'))
    index, question, answer = get_random_question_answer(conn)
    while True:
        try:
            message = conn.recv(2048).decode("utf-8")
            if message:
                if message.lower() == answer:
                    score += 1
                    conn.send(f"Bravo ! Your score is {score}\n\n".encode('utf-8'))
                else :
                    conn.send("Incorrect answer ! Better Luck next time !\n\n".encode("utf-8"))
                remove_question(index)
                index,question,answer = get_random_question_answer(conn)
            else : 
                remove_question(conn)
        except:
            continue

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def get_random_question_answer(conn):
    random_index = random.randint(0,len(questions) -1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

while True:
    conn,addr = server.accept()
    conn.send('NICKNAME'.encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')
    list_of_clients.append(conn)
    nicknames.append(nickname)
    print(nickname + "has joined !")
    new_thread = Thread(target=clientThread, args=(conn,nickname))
    new_thread.start()