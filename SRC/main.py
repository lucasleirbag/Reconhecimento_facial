import cv2
import numpy as np
import os
import sqlite3
from sqlite3 import Error

# Conexão com o banco
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def create_table(conn):
    try:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS usuarios (
                    id integer PRIMARY KEY,
                    nome text NOT NULL,
                    cpf text
                );""")
    except Error as e:
        print(e)

def cadastro(conn, nome, cpf):
    sql = ''' INSERT INTO usuarios(nome,cpf)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (nome, cpf))
    conn.commit()
    return cur.lastrowid

# Reconhecimento facial
def createDir(name, path=''):
    if not os.path.exists(f'{path}/{name}'):  
        os.makedirs(f'{path}/{name}')  

def saveFace(nome):
    global saveface, lastName
    saveface = True  
    createDir('USUARIO')  
    print("CADASTRANDO..")  
    lastName = nome  
    createDir(nome, 'USUARIO')  

def saveImg(img):
    global lastName  
    qtd = os.listdir(f'USUARIO/{lastName}')  
    cv2.imwrite(f'USUARIO/{lastName}/{str(len(qtd))}.jpg', img)  

def trainData():
    global recognizer, trained, persons
    trained = True
    persons = os.listdir('USUARIO')
    ids = []  
    faces = []  
    for i, p in enumerate(persons):  
        i += 1  
        for f in os.listdir(f'USUARIO/{p}'):  
            img = cv2.imread(f'USUARIO/{p}/{f}', 0)  
            faces.append(img) 
            ids.append(i)  
    recognizer.train(faces, np.array(ids))

def check_and_train():
    
    # Verifica se existem dados para treinamento e realiza o treinamento se necessário.
    
    if not os.path.exists('USUARIO') or not os.listdir('USUARIO'):
        print("Nenhum dado de usuário para treinamento.")
        return False

    trainData()
    return True

database = "data/usuarios.db"
conn = create_connection(database)
if conn:
    create_table(conn)
else:
    print("Erro! não foi possível criar a conexão com o banco de dados.")

lastName = ''
saveface = False
savefaceC = 0
trained = False
persons = []

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('SRC/utils/haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
trained = check_and_train()

# threshold de confiança
CONFIDENCE_THRESHOLD = 30

while(True):
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        resize = cv2.resize(roi_gray, (400, 400))

        if trained:
            idf, conf = recognizer.predict(resize)
            if conf < CONFIDENCE_THRESHOLD:
                nameP = persons[idf-1] if idf <= len(persons) else "Desconhecido"
            else:
                nameP = "Desconhecido"

            cv2.putText(frame, nameP, (x+5,y+25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0 if conf < CONFIDENCE_THRESHOLD else 0), 1, cv2.LINE_AA)
        else:
            cv2.putText(frame, 'NAO ENCONTRADO', (10,65), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)

        if saveface:
            savefaceC += 1
            saveImg(resize)
            if savefaceC > 100:
                savefaceC = 0
                saveface = False
                trained = check_and_train()

    cv2.imshow('frame', frame)
    key = cv2.waitKey(10)
    if key == 32:  # Tecla 'espaço'
        nome = input("Digite o nome: ")
        cpf = input("Digite o CPF: ")
        saveFace(nome)
        cadastro(conn, nome, cpf)
    elif key & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()