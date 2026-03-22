from app import create_app

app = create_app()

if __name__ == '__main__':
    # Note: Use a production WSGI server like Gunicorn
    # gunicorn --bind 0.0.0.0:8000 run:app
    app.run(debug=True, port=8000)
