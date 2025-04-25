from flask import Flask, request, render_template, redirect, url_for, flash
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'olimpiapp_secret_key'  # Necesario para usar flash messages

# Ruta para la página principal - renderiza el formulario
@app.route('/')
def index():
    return render_template('formulario_app.html')

# Ruta para procesar el formulario
@app.route('/procesar_registro', methods=['POST'])
def procesar_registro():
    if request.method == 'POST':
        # Obtenemos los datos del formulario
        datos = {
            # Datos del participante
            'nombre': request.form.get('nombre'),
            'apellidos': request.form.get('apellidos'),
            'fechaNacimiento': request.form.get('fechaNacimiento'),
            
            # Datos del tutor
            'nombre_tutor': request.form.get('nombre_tutor'),
            'apellidos_tutor': request.form.get('apellidos_tutor'),
            'relacion': request.form.get('relacion'),
            'dni_tutor': request.form.get('dni_tutor'),
            'email_tutor': request.form.get('email_tutor'),
            'telefono_tutor': request.form.get('telefono_tutor'),
            
            # Aceptación de términos y consentimiento
            'terminos': 'terminos' in request.form,
            'consentimiento_tutor': 'consentimiento_tutor' in request.form,
            
            # Disciplinas seleccionadas
            'disciplinas': request.form.getlist('disciplinas'),
            
            # Fecha y hora del registro
            'fecha_registro': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Validación de datos
        if len(datos['disciplinas']) > 5:
            flash('Error: Solo se permiten seleccionar hasta 5 disciplinas.')
            return redirect(url_for('index'))
        
        if not datos['terminos'] or not datos['consentimiento_tutor']:
            flash('Error: Debes aceptar los términos y dar consentimiento como tutor legal.')
            return redirect(url_for('index'))
        
        # Guardar los datos en un archivo JSON
        registros_directorio = 'registros'
        if not os.path.exists(registros_directorio):
            os.makedirs(registros_directorio)
        
        # Crear un nombre de archivo único basado en DNI y fecha
        nombre_archivo = f"{registros_directorio}/{datos['dni_tutor']}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
        
        # Guardar los datos en el archivo
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
        
        # Mostrar mensaje de éxito
        flash('¡Registro completado con éxito!')
        return redirect(url_for('confirmacion'))
    
    return redirect(url_for('index'))

# Ruta para la página de confirmación
@app.route('/confirmacion')
def confirmacion():
    return render_template('confirmacion.html')

if __name__ == '__main__':
    app.run(debug=True)