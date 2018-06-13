from diet_manager import app
import os

from init_db import db_start

if __name__ == '__main__':
    if not os.path.isfile("diet_manager.db"):
        db_start()
    app.secret_key = 'my_secret_key'
    app.run(host='0.0.0.0', port=8080)
    #app.run(debug=True)
