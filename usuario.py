from conexao import Conexao
from hashlib import sha256

class Usuario:
    def __init__(self):
        self.nome = None
        self.telefone = None
        self.senha = None
        self.logado = False

    def cadastrar(self, nome, telefone, senha):
           # try:
            
                senha= sha256(senha.encode()).hexdigest()
            
                mydb = Conexao.conectar()

                mycursor = mydb.cursor()
                
                sql = "INSERT INTO tb_usuario (nome, tel, senha) VALUES (%s, %s, %s)"
                val = (nome,telefone,senha)
                mycursor.execute(sql, val)

                mydb.commit()
                
                self.nome = nome
                self.telefone = telefone
                self.senha = senha
                self.logado = True

                return True
            #except: return False
            
    
    
    def logar(self, telefone, senha):
        senha= sha256(senha.encode()).hexdigest()
        mydb = Conexao.conectar()

        mycursor = mydb.cursor()
        
        sql = f"SELECT nome, tel, senha FROM tb_usuario WHERE tel = %s and BINARY senha = %s"
        val = (telefone, senha)
        mycursor.execute(sql,val)


        resultado = mycursor.fetchone()

        if  resultado != None:
             self.logado = True
             self.nome = resultado[0]
             self.telefone = resultado[1]
             self.senha = resultado[2]
        else:
             self.logado = False

        return mydb