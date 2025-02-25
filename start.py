from webapp import startServer
from os import getenv
from dotenv import load_dotenv

load_dotenv()
app = startServer(
    rootDir = getenv('ROOT_DIR'),
    dataDir = getenv('DATA_DIR'),
    SECRET_KEY = getenv('SECRET_KEY'),
    username = getenv('USERNAME'),
    password = getenv('PASSWORD')
)

if __name__ == '__main__':
    app.run(debug=True)
