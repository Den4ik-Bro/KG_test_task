# KG_test_task

Данный проект можно посмотреть в "боевом" режиме по адресу: https://den90.pythonanywhere.com/


Запуск проекта локально:
  - Создаем директорию под проект, создаем виртуальное окружение и активируем его
  - Клонируем проект командой "git clone https://github.com/Den4ik-BroKG_test_task.git"
  - Устанавливаем зависимости командой pip install -r requirements.txt
  - Выполняем миграции командой "python manage.py migrate" из директории проекта.
  - Создаем супер-пользователя командой python manage.py createsuperuser
  - Запускаем проект командой python manage.py runserver
  
  
Запуск с помощью докера:
  - Создаем директорию под проект, создаем виртуальное окружение и активируем его
  - Клонируем проект командой "git clone https://github.com/Den4ik-BroKG_test_task.git"
  - Выполнить команды "docker-compose build" > "docker_compose up" и проект будет доступен по адресу 127.0.0.1:8000/
