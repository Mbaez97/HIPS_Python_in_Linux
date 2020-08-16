from flask_login import UserMixin

def get_user(user_id):
    url = "/home/marcelojulianbaezferreira/Documentos/HIPS_2020_SO/hips_interfazweb/hips_interfazweb"
    with open(f'{url}/usuario.txt', 'r') as f:
        usuario_file = f.read().replace('\n', '').split(',')
        for user in usuario_file:
            if user == user_id:
                """Aca podes verificar que el segundo dato sea la contraseña """
                usuario=user
                password=usuario_file[usuario_file.index(user) +1]
                return UserModel(UserData(usuario, password))
            else:
                return None



class UserData:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserModel(UserMixin):
    """Modelo de inicio de sesion"""
    def __init__(self, user_data):
        self.id = user_data.username
        self.password = user_data.password

    @staticmethod
    def query(user_id):
        user_doc = get_user(user_id)
        user_data = UserData(
            username=user_doc.id,
            password=user_doc.password
            )

        return UserModel(user_data)