from flask import Flask,render_template,request,redirect,session,url_for
import bcrypt
import os
import json

app = Flask(__name__)

db_file_path = os.path.join(os.path.dirname(__file__),'usres.json')

def load_users():
    with open(db_file_path, 'r')as f:
        return json.load(f)

def save_users(users):
    with open(db_file_path,'w') as f:
        json.dump(users,f,indent=4)


def user_exists(email):
    users = load_users()
    for usre in users['users']:
        if users['email']==email:
            return True
    return False

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login',methods=('GET','POST'))
def login():
    if request.method == 'POST':
        email= request.form['email']
        password= request.form['password'].encode('utf-8')
        usres= load_users()
        for user in usres['usres']:
            if user['email'] == email and bcrypt.checkpw(password,user['password'].encode('utf-8')):
                secion['user']=email
                return redirect(url_for('home'))
            return 'credenciales incorrectas, intente de nuevo'
    return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        email=request.form['email']
        password = request.form['password'].encode('uft-8')
        if user_exists('email'):
            return 'el usario ya exite. porfavor intenta con otro o inicia secion.'
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        new_user = {'email': email, 'password': hashed_password.decode('uft-8')}
        users =load_users()
        users['usres'].append(new_user)
        save_users(users)
        return redirect(url_for('login'))
    return render_template('resgiter.html')


@app.route('/Introduccion')
def introduccion():
    return render_template("introduccion.html")

@app.route('/personajes')
def persoanjes():
    return render_template("personajes.html")

@app.route('/desbloquehables')
def desbloquehables():
    return render_template("desbloquehables.html")

@app.route('/finales')
def finales():
    return render_template("finales.html")

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('/'))

if __name__=='__main__':
    app.secret_key ='supersecredkey'
    app.run(debug=True)