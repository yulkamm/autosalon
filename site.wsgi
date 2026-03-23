import sys
import os

# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(__file__))

# Активируем виртуальное окружение (на SprintHost)
activate_this = os.path.expanduser('~/python/bin/activate_this.py')
if os.path.exists(activate_this):
    with open(activate_this) as f:
        exec(f.read(), {'__file__': activate_this})

# Импортируем Flask приложение
# Важно: переменная должна называться application для uWSGI
from wsgi import app as application

# Для совместимости
if __name__ == "__main__":
    application.run()
