from app import create_app #importamos nuestra propia funcion
app = create_app() #crea la aplicación

if __name__ == "__main__": 
    app.run(debug=True) #inicia el servidor Flask en modo desarrollo (si cambiamos el código, el servidor se reinicia automáticamente y muestra errores)