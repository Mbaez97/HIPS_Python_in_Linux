from flask import Flask, render_template, request, session, redirect,url_for,flash
from flask_login import current_user, LoginManager, login_required, login_user, logout_user

#from flask_mysqldb import MySQL


from forms import LoginForm

from models import UserData, UserModel, get_user

from flask_bootstrap import Bootstrap


#semilla = bcrypt.gensalt()

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.secret_key = "secret_key"
login_manager = LoginManager()
login_manager.login_view = '/login'
login_manager.init_app(app)

mensaje_url = "/home/marcelojulianbaezferreira/Documentos/HIPS_2020_SO/returnweb"

@login_manager.user_loader
def load_user(user_id):
    return UserModel.query(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user_doc = get_user(username)

        if user_doc is not None:
            print("hola " + user_doc.password)
            password_from_db = user_doc.password
            if password == password_from_db:
                user_data = UserData(username, password)
                user = UserModel(user_data)
                login_user(user)
                flash('Bienvenido')
                return redirect(url_for('home'))
            else:
                flash('La informacion no coincide')
        else:
                flash('El usuario no existe')

    return render_template('login.html', login_form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Regresa pronto')
    return redirect(url_for('login'))


@app.route('/')
@login_required
def home():
    return render_template('home.html', username=current_user.id)

@app.route('/about')
@login_required
def about():
    return render_template('about.html')

@app.route('/<id>')
def lista_resultado(id):
	if id == 1:
        os.system("python3 /home/marcelojulianbaezferreira/Documentos/HIPS_2020_SO/binariosCMP.py")
        title = request.args.get('titulo')
        with open(f'{mensaje_url}/{id}.txt', 'r') as f:
            data = f.read()
            contx = {
            'titulo': title,
            'data' : data.split('.'),
            }
        return render_template('data_card.html', **contx)
    else:
        pass

    if id == 2:
        os.system("python3 /home/marcelojulianbaezferreira/Documentos/HIPS_2020_SO/comprobar_usuarios_conectados.py")
        title = request.args.get('titulo')
        with open(f'{mensaje_url}/{id}.txt', 'r') as f:
            data = f.read()
            contx = {
            'titulo': title,
            'data' : data.split('.'),
            }
        return render_template('data_card.html', **contx)
    else:
        pass

    if id == 3:
        os.system("python3 /home/marcelojulianbaezferreira/Documentos/HIPS_2020_SO/comprobar_sniffer.py")
        title = request.args.get('titulo')
        with open(f'{mensaje_url}/{id}.txt', 'r') as f:
            data = f.read()
            contx = {
            'titulo': title,
            'data' : data.split('.'),
            }
        return render_template('data_card.html', **contx)
    else:
        pass

    if id == 4:
        os.system("python3 /home/marcelojulianbaezferreira/Documentos/HIPS_2020_SO/acces_logCMP.py")
        os.system("python3 /home/marcelojulianbaezferreira/Documentos/HIPS_2020_SO/comprobar_log_mails.py")
        os.system("python3 /home/marcelojulianbaezferreira/Documentos/HIPS_2020_SO/log_secureCMP.py")
        title = request.args.get('titulo')
        with open(f'{mensaje_url}/{id}.txt', 'r') as f:
            data = f.read()
            contx = {
            'titulo': title,
            'data' : data.split('.'),
            }
        return render_template('data_card.html', **contx)
    else:
        pass

    if id == 5:
        os.system("python3 /home/marcelojulianbaezferreira/Documentos/HIPS_2020_SO/comprobar_cola_mails.py")
        title = request.args.get('titulo')
        with open(f'{mensaje_url}/{id}.txt', 'r') as f:
            data = f.read()
            contx = {
            'titulo': title,
            'data' : data.split('.'),
            }
        return render_template('data_card.html', **contx)
    else:
        pass

    if id == 6:
        os.system("python3 /home/marcelojulianbaezferreira/Documentos/HIPS_2020_SO/comprobar_rendimiento.py")
        title = request.args.get('titulo')
        with open(f'{mensaje_url}/{id}.txt', 'r') as f:
            data = f.read()
            contx = {
            'titulo': title,
            'data' : data.split('.'),
            }
        return render_template('data_card.html', **contx)
    else:
        pass

    if id == 7:
        os.system("python3 /home/marcelojulianbaezferreira/Documentos/HIPS_2020_SO/comprobar_dns.py")
        title = request.args.get('titulo')
        with open(f'{mensaje_url}/{id}.txt', 'r') as f:
            data = f.read()
            contx = {
            'titulo': title,
            'data' : data.split('.'),
            }
        return render_template('data_card.html', **contx)
    else:
        pass

    if id == 8:
        os.system("python3 /home/marcelojulianbaezferreira/Documentos/HIPS_2020_SO/crontabCMP.py")
        title = request.args.get('titulo')
        with open(f'{mensaje_url}/{id}.txt', 'r') as f:
            data = f.read()
            contx = {
            'titulo': title,
            'data' : data.split('.'),
            }
        return render_template('data_card.html', **contx)
    else:
        pass

    if id == 9:
        os.system("python3 /home/marcelojulianbaezferreira/Documentos/HIPS_2020_SO/binariosCMP.py")
        os.system("python3 /home/marcelojulianbaezferreira/Documentos/HIPS_2020_SO/comprobar_usuarios_conectados.py")
        os.system("python3 /home/marcelojulianbaezferreira/Documentos/HIPS_2020_SO/comprobar_sniffer.py")
        os.system("python3 /home/marcelojulianbaezferreira/Documentos/HIPS_2020_SO/acces_logCMP.py")
        os.system("python3 /home/marcelojulianbaezferreira/Documentos/HIPS_2020_SO/comprobar_log_mails.py")
        os.system("python3 /home/marcelojulianbaezferreira/Documentos/HIPS_2020_SO/log_secureCMP.py")
        os.system("python3 /home/marcelojulianbaezferreira/Documentos/HIPS_2020_SO/comprobar_cola_mails.py")
        os.system("python3 /home/marcelojulianbaezferreira/Documentos/HIPS_2020_SO/comprobar_rendimiento.py")
        os.system("python3 /home/marcelojulianbaezferreira/Documentos/HIPS_2020_SO/comprobar_dns.py")
        os.system("python3 /home/marcelojulianbaezferreira/Documentos/HIPS_2020_SO/crontabCMP.py")
        
        title = request.args.get('titulo')
        with open(f'{mensaje_url}/{id}.txt', 'r') as f:
            data = f.read()
            contx = {
            'titulo': title,
            'data' : data.split('.'),
            }
        return render_template('data_card.html', **contx)
    else:
        pass


    #if id == 2:
     #   os.system("python3 /home/marcelojulianbaezferreira/Documentos/HIPS_2020_SO/comprobar_usuarios_conectados.py") 
    
	#mensaje = 'Analisis Completado, si hay problemas en los binarios del sistema el administrador recibira un correo notificando el problema'
    #return redirect(url_for('home'))#render_template('data_card.html', mensaje )

if __name__ == '__main__':
    app.run(debug = True)

