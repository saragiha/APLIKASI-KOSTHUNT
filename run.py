from app import app, db
from models import User, Kos

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
