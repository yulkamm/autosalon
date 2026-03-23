import os
from app import create_app

# Создаем приложение
application = create_app()  # Важно для uWSGI

# Для локального запуска
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    application.run(host='0.0.0.0', port=port, debug=False)
