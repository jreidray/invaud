from webapp import startServer

app = startServer()

if __name__ == '__main__':
    app.config['SECRET_KEY'] = "invaud_key"
    app.run(debug=True)
