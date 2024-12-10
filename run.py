from app import create_app, db

app = create_app('production')

if __name__ == '__main__':
    app.run()