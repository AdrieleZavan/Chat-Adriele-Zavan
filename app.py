from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from usuario import Usuario 
from chat import Chat
from contato import Contato


app = Flask(__name__)

app.secret_key = "euamoochoso"

usuario = Usuario()

# Rota para a página inicial
@app.route("/", methods=["GET","POST"])
def cadastro():
    if request.method == 'GET':
        return render_template("cadastro.html")
    else:
        usuario = Usuario()         
        nome = request.form["nome"]
        tel = request.form["telefone"]
        senha = request.form["senha"]

        if usuario.cadastrar(nome, tel, senha) == True:
            print(f"Cadastro efetuado com sucesso! Seja Bem-Vindo!")
        else:
            print("Não foi possível concluir seu cadastro!")
        return render_template("cadastro.html")
    
# @app.route("/cadastrar_via_ajax" , methods = ["POST"])
# def post_cadastro_ajax():
#     #Pegando os dados que foram enviados
#     dados = request.get_json()
#     nome = dados["nome"]
#     telefone = dados["telefone"]
#     senha = dados["senha"]
    
#      usuario = Usuario()  
#      if usuario.cadastrar(nome, tel, senha) == True:
#             return jsonify({'mensagem': Cadastro OK'}), 200
#         else:
#         return jsonify({'mensagem': Erro'}), 500
    
@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login" , methods=["POST"])
def login_post():
    if request.method == "POST":
        telefone = request.form["telefone"]
        senha = request.form["senha"]

        usuario.logar(telefone,senha)

        if usuario.logado:
            session['usuario_logado'] =  {"nome": usuario.nome,
                                            "telefone": usuario.telefone}
            return redirect("/chat")
        else:
            session.clear()
            return "Erro ao logar"
    else:
       return render_template("login.html")

@app.route("/chat")
def pag_chat():
    if "usuario_logado" in session:
        return render_template("chat.html")
    else:
        return redirect("/login")        
    
   
@app.route("/retorna_usuarios")
def retorna_usuarios():
    nome_usuario= session["usuario_logado"]["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]
    chat = Chat(nome_usuario, telefone_usuario)

    contatos = chat.retornar_contatos()
    return jsonify(contatos), 200



@app.route("/get/mensagens/<tel_destinatario>")
def api_get_mensagens(tel_destinatario):
    nome_usuario= session["usuario_logado"]["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]
    chat = Chat(nome_usuario, telefone_usuario)

    destinatario = Contato("", tel_destinatario)

    mensagens = chat.verificar_mensagem(0, destinatario)

    return jsonify(mensagens), 200


@app.route("/enviar_mensagem", methods=["POST"])
def enviar_mensagem():
    if request.method == "POST":
        dados = request.json
        mensagem = dados.get("mensagem")
        tel_destinatario = dados.get("tel_destinatario")
        

        nome_usuario = session["usuario_logado"]["nome"]
        telefone_usuario = session["usuario_logado"]["telefone"]
        chat = Chat(nome_usuario, telefone_usuario)
        tel_destinatario = Contato("", tel_destinatario)
        

        if chat.enviar_mensagem(mensagem, tel_destinatario):
            return jsonify({"mensagem": "Mensagem enviada com sucesso!"}), 200
        else:
            return jsonify({"mensagem": "Erro ao enviar mensagem."}), 500







    
app.run(debug=True)