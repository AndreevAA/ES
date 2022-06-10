from flask import Flask

def create_app():

    t_app = Flask(__name__)

    t_app.static_folder = 'static'

    t_app.config['SECRET_KEY'] = 'secret-key-goes-here'
    t_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/[ES][qwerty]'

    # blueprint for auth routes in our app
    from inner_d.auth import Auth
    Auth.register(t_app, route_base='/')

    # blueprint for auth routes in our app
    from inner_d.cabinet import Cabinet
    Cabinet.register(t_app, route_base='/')

    # blueprint for non-auth parts of app
    from main import main as main_blueprint
    t_app.register_blueprint(main_blueprint)

    return t_app


if __name__ == '__main__':
    app = create_app()
    app.run()
