from app import app, db
from time import sleep

if __name__ == "__main__":
    sleep(30)
    db.drop_all()
    db.create_all()
    app.run(host="0.0.0.0", port=5000)
