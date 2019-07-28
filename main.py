from app import app
from auth.auth_bp import auth
import view

app.register_blueprint(auth, url_prefix='/auth')

if __name__ == '__main__':
	app.run()
