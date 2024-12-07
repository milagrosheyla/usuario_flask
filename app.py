from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# URL de la API externa para obtener los usuarios
USERS_API_URL = 'https://jsonplaceholder.typicode.com/users'

# Función para obtener los usuarios desde la API
def fetch_users():
    try:
        response = requests.get(USERS_API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except Exception as e:
        print(f"Error al obtener los usuarios: {e}")
        return []

# Ruta principal que renderiza la página HTML
@app.route('/', methods=['GET', 'POST'])
def index():
    user_info = None
    error_message = None

    if request.method == 'POST':
        # Obtención del ID del formulario
        user_id = request.form.get('searchId', type=int)

        if user_id:
            users_data = fetch_users()

            # Buscar el usuario por ID
            user_info = next((user for user in users_data if user['id'] == user_id), None)

            # Si no se encuentra el usuario, mostrar un mensaje de error
            if not user_info:
                error_message = f"Usuario con ID {user_id} no encontrado."

        else:
            error_message = "Por favor, ingresa un ID válido."

    return render_template('user.html', user_info=user_info, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
