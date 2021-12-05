# **Лабораторна робота №5**
---
## Послідовність виконання лабораторної роботи:
#### 1. Для ознайомляння з `docker-compose` звернувся до документації.
Щоб встановити `docker-compose` використав команди:
```text
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
#### 2. Ознайомився з бібліотекою `Flask`, яку найчастіше використовують для створення простих веб-сайтів на Python.
#### 3. Моє завдання: за допомогою Docker автоматизувати розгортання веб сайту з усіма супутніми процесами. Зроблю я це двома методами: 
* за допомогою `Makefile`;
* за допомогою `docker-compose.yaml`.

#### 4. Першим розгляну метод з `Makefile`, але спочатку створю робочий проект.
#### 5. Створив папку `my_app` в якій буде знаходитись мій проект. Створив папку `tests` де будуть тести на перевірку працездатності мого проекту. Скопіював файли `my_app/templates/index.html`, `my_app/app.py `, `my_app/requirements.txt`, `tests/conftest.py`, `tests/requirements.txt`, `tests/test_app.py` з репозиторію викладача у відповідні папки мого репозеторію. Ознайомився із вмістом кожного з файлів. Звернув увагу на файл requirements.txt у папці проекту та тестах. Даний файл буде мітити залежності для мого проекту він містить назви бібліотек які імпортуються.
#### 6. Я спробував чи проект є працездатним перейшовши у папку `my_app` та після ініціалізації середовища виконав команди записані нижче:
```text
sudo pipenv --python 3.8
sudo pipenv install -r requirements.txt
sudo pipenv run python app.py
```
1. Так само я ініціалузував середовище для тестів у іншій вкладці шелу та запустив їх командою `sudo pipenv run pytest test_app.py --url http://localhost:5000` але спочатку треба перейти в папку `tests`:
    ```text
    19:41:27 l1@l1:~/TPIS/IK_31/lab5/tests (master) $ sudo pipenv run pytest test_app.py --url http://localhost:5000
    [sudo] password for pavlovulchak: 
    ============================= test session starts ==============================
    platform linux -- Python 3.9.5, pytest-6.2.5, py-1.11.0, pluggy-1.0.0
    rootdir: /home/l1/TPIS/IK_31/lab5/tests
    collected 4 items                                                              
    
    test_app.py ..FF                                                         [100%]
    
    =================================== FAILURES ===================================
    __________________________________ test_logs ___________________________________
    url = 'http://localhost:5000'
    
        def test_logs(url):
            response = requests.get(url + '/logs')
    >       assert 'My Hostname is:' in response.text, 'Logs do not have Hostname'
    E       AssertionError: Logs do not have Hostname
    E       assert 'My Hostname is:' in '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"\n  "http://www.w3.org/TR/html4/loose.dtd">\n<html>\n  ...en(\'logs/app.log\', \'r\') as log:\nFileNotFoundError: [Errno 2] No such file or directory: \'logs/app.log\'\n\n-->\n'
    E        +  where '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"\n  "http://www.w3.org/TR/html4/loose.dtd">\n<html>\n  ...en(\'logs/app.log\', \'r\') as log:\nFileNotFoundError: [Errno 2] No such file or directory: \'logs/app.log\'\n\n-->\n' = <Response [500]>.text
    
    test_app.py:27: AssertionError
    ________________________________ test_main_page ________________________________
    
    url = 'http://localhost:5000'
    
        def test_main_page(url):
            response = requests.get(url)
    >       assert 'You are at main page.' in response.text, 'Main page without text'
    E       AssertionError: Main page without text
    E       assert 'You are at main page.' in '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"\n  "http://www.w3.org/TR/html4/loose.dtd">\n<html>\n  ...)\nredis.exceptions.ConnectionError: Error -3 connecting to redis:6379. Temporary failure in name resolution.\n\n-->\n'
    E        +  where '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"\n  "http://www.w3.org/TR/html4/loose.dtd">\n<html>\n  ...)\nredis.exceptions.ConnectionError: Error -3 connecting to redis:6379. Temporary failure in name resolution.\n\n-->\n' = <Response [500]>.text
    
    test_app.py:32: AssertionError
    =========================== short test summary info ============================
    FAILED test_app.py::test_logs - AssertionError: Logs do not have Hostname
    FAILED test_app.py::test_main_page - AssertionError: Main page without text
    ========================= 2 failed, 2 passed in 0.48s ==========================
    20:59:26 l1@l1:~/TPIS/IK_31/lab5/tests (master) $ 
    ```
2. Звернув увагу, що в мене автоматично створюються файли `Pipfile` та `Pipfile.lock`, а також на хост машині буде створена папка `.venv`. Після зупинки проекту видалив їх.
3. Перевірив роботу сайту перейшовши головну сторінку. Сайт не працює бо на відсутній `redis`.

#### 7. Видалив файли які постворювались після тестового запуску. Щоб моє середовище було чистим, все буде створюватись і виконуватись всередині Docker. Створив два файла `Dockerfile.app`, `Dockerfile.tests` та `Makefile` який допоможе автоматизувати процес розгортання.
#### 8. Скопіював вміст файлів `Dockerfile.app`, `Dockerfile.tests` та `Makefile` з репозиторію викладача та ознайомився із вмістом `Dockerfile` та `Makefile` та його директивами. 
Вміст файла `Dockerfile.app`:
```text
FROM python:3.8-slim
LABEL author="P"
# оновлюємо систему та встановлюємо потрібні пакети
RUN apt-get update \
    && apt-get upgrade -y\
    && apt-get install git -y\
    && pip install pipenv
WORKDIR /app
# Копіюємо файл із списком пакетів які нам потрібно інсталювати
COPY my_app/requirements.txt ./
RUN pipenv install -r requirements.txt
# Копіюємо наш додаток
COPY my_app/ ./
# Створюємо папку для логів
RUN mkdir logs
EXPOSE 5000
ENTRYPOINT pipenv run python app.py
```
Вміст файла `Dockerfile.tests`:
```text
FROM python:3.8-slim
LABEL author="P"
# оновлюємо систему та встановлюємо потрібні пакети
RUN apt-get update \
    && apt-get upgrade -y\
    && apt-get install git -y\
    && pip install pipenv
WORKDIR /tests
# Копіюємо файл із списком пакетів які нам потрібно інсталювати
COPY tests/requirements.txt ./
RUN pipenv install -r requirements.txt
# Копіюємо нашого проекту
COPY tests/ ./
ENTRYPOINT pipenv run pytest test_app.py --url http://app:5000
```
Вміст файла `Makefile`:
```text
STATES := app tests
REPO := kekeroni1337/lab4
.PHONY: $(STATES)
$(STATES):
	@docker build -f Dockerfile.$(@) -t $(REPO):$(@) .
run:
	@docker network create --driver=bridge appnet \
	&& docker run --rm --name redis --net=appnet -d redis \
	&& docker run --rm --name app --net=appnet -p 5000:5000 -d $(REPO):app
test-app:
	@docker run --rm -it --name test --net=appnet $(REPO):tests
	
docker-prune:
	@docker rm $$(docker ps -a -q) --force || true \
	&& docker container prune --force \
	&& docker volume prune --force \
	&& docker network prune --force \
	&& docker image prune --force
```
Дерективи `app` та `tests`:
Створення імеджів для сайту та тесту відповідно.
Деректива `run`:
Запускає сторінку сайту.
Деректива `test-app`:
Запуск тесту сторінки.
Деректива `docker-prune`:
Очищення іміджів, контейнера і інших файлів без тегів.
#### 9. Для початку, використовуючи команду `sudo make app` створіть Docker імеджі для додатку та для тестів `sudo make tests`. Теги для цих імеджів є з моїм Docker Hub репозиторієм. Запустив додаток командою `sudo make run` та перейшовши в іншу вкладку шелу запустіть тести командою `sudo make test-app`.
Запуск сайту
```text
01:06:01 l1@l1:~/TPIS/IK_31/lab5 (master) $ sudo make run
[sudo] password for l1: 
5a59f988768827aa44e7b5e9904e4f3d2692ffd1bf8c78e262fd16d87790717b
Unable to find image 'redis:latest' locally
latest: Pulling from library/redis
eff15d958d66: Pull complete 
1aca8391092b: Pull complete 
06e460b3ba1b: Pull complete 
def49df025c0: Pull complete 
646c72a19e83: Pull complete 
db2c789841df: Pull complete 
Digest: sha256:619af14d3a95c30759a1978da1b2ce375504f1af70ff9eea2a8e35febc45d747
Status: Downloaded newer image for redis:latest
5d3c4e343ac11e52d0e53cc314d99b224a14dfc0d0361ee3c24b2c55e5f0e903
3e719efd34012a377571a3207e660531d1f6b18164e7bbb5bc144b847787c476
```
Проходження тесту:
```text
01:00:51 l1@l1:~/TPIS/IK_31/lab5 (master) $ sudo make test-app
Warning: Your Pipfile requires python_version 3.9, but you are using 3.8.12 (/root/.local/share/v/t/bin/python).
  $ pipenv --rm and rebuilding the virtual environment may resolve the issue.
  $ pipenv check will surely fail.
============================= test session starts ==============================
platform linux -- Python 3.8.12, pytest-6.2.5, py-1.11.0, pluggy-1.0.0
rootdir: /tests
collected 4 items                                                              
test_app.py ....                                                         [100%]
============================== 4 passed in 0.24s ===============================
01:10:04 l1@l1:~/TPIS/IK_31/lab5 (master) $ 
```
#### 10. Зупинив проект натиснувши Ctrl+C та почистив всі ресурси `Docker` за допомогою `make`.
```text
01:31:51 l1@l1:~/TPIS/IK_31/lab5 (master) $ sudo make docker-prune
[sudo] password for l1: 
3e719efd3401
5d3c4e343ac1
3044d4300891
ab8221ccae28
8afa1cc22d03
7d38d9594c2e
3282dc276687
bfd0bd0bcee8
Total reclaimed space: 0B
Deleted Volumes:
7f09c2bd964c9c17e7a1433e63435de02a2215081acba88d51167ef905e54265
Total reclaimed space: 0B
Deleted Networks:
appnet
Total reclaimed space: 0B
01:35:49 l1@l1:~/TPIS/IK_31/lab5 (master) $ 
```

#### 11. Створив директиву `docker-push` в Makefile для завантаження створених імеджів у мій Docker Hub репозиторій.
Деректива `docker-push`:
```text
docker-push:
	@docker login \
	&& docker push $(REPO):app \
	&& docker push $(REPO):tests
```

#### 12. Видалив створені та закачані імеджі. Команда `docker images` виводить пусті рядки. Створив директиву в Makefile яка автоматизує процес видалення моїх імеджів.
Деректива `images-delete`:
```text
images-delete:
	@docker rmi $$(docker images -q)
```
Запуск:
```text
00:34:18 l1@l1:~/TPIS/IK_31/lab5 (master) $ sudo docker images
REPOSITORY          TAG        IMAGE ID       CREATED       SIZE
kekeroni1337/lab4   tests      3fcb8b169ee7   2 hours ago   305MB
kekeroni1337/lab4   app        8bb22e6efdd4   2 hours ago   302MB
python              3.8-slim   214d62795dbb   3 weeks ago   122MB
00:37:59 l1@l1:~/TPIS/IK_31/lab5 (master) $ sudo make images-delete
Untagged: kekeroni1337/lab4:tests
Untagged: kekeroni1337/lab4@sha256:8967bd6199d707ece3dd7257f64dc10d884f56a60a21facfabee2745b992e451
Deleted: sha256:3fcb8b169ee7d43497e7578ef1b54b7a885f0991bc06205aa89fd41460a032ce
Deleted: sha256:d19690ae4af92a372aa3ea2374015cf6e4f5ea270a956b4d0c6e5cb7ce0f56d2
Deleted: sha256:4c1dbe3aa9b78a457c273addf25e7312c2232631e0162a85ac291fc1ffb7783e
Deleted: sha256:2dab9b49224a5c4123a79c2cf57578e3e3068cb3b573eb074535647e8a63b313
Deleted: sha256:cf571657e58c56b1557cf758fc7a63e5b33fc4f51e6a9dfe96eb30376e7c6218
Deleted: sha256:8228f73aba7460fd05c71bffe514068ebc8371ae77a504b4b44fd77db82ce76e
Deleted: sha256:7b4599904f43cdf61d90298254322765bc377f33baba6860c8152dd5a659e600
Deleted: sha256:93f97cc1f62267a62d575e00c27d9e490469b732db80c8a1ec9f92b36e4c0462
Deleted: sha256:564ffb6f18c61d4be3c691a680511ce142fb5915f6e121c8ff40a86a6f07f74d
Untagged: kekeroni1337/lab4:app
Untagged: kekeroni1337/lab4@sha256:c5dae1dffdc7fba23ffa264b01ec51a38dba6c9231ba79ca7b2896aeff171cab
Deleted: sha256:8bb22e6efdd40579c284ab3cacb26db27f36bd646e45c1a1adf54f073868b515
Deleted: sha256:c63c9477ac96b5026caa3fd5d823a1e894a39cf54bc5b9b7be20ecc1c7d6aca1
Deleted: sha256:6b981e317a46c0ed57785ff76d9b0e69eb81324bc0d73b342ce747f6c0334b83
Deleted: sha256:199dad3209712100c5279a0e5524a4fa22672b443561b47fe19265f8229b9ce5
Deleted: sha256:2117171fae144d30276d9651cd0020c21948eee9db29712208475d8e864fb58e
Deleted: sha256:88617aa53853ebb2bd1edd5482ee7356bec0fe86c5fdb6afdffddd8d812c341e
Deleted: sha256:e789488bdc2984e2799bea9aba070310652a4dbab5ba9128caeff21aed3a24f4
Deleted: sha256:9b8e653a26cad3da2c324ef4947d8cfb6fe0eddba31907a6813c0da869ec0bb4
Deleted: sha256:614592d489c65ea3c1716036d3a6ffb9aeafb38c321870b27887b972979a9737
Deleted: sha256:8793abab2d3c14c056c2795b8685f0f00308d3faed709953e526236ef16777e2
Deleted: sha256:01a2bcebf413d400b535c49c3af50b118f5a9331be4534c46c24bdd42a895e25
Deleted: sha256:10e80a5d8c50e73f69a96207e755af6a5f2d12046ce363379dc0cc3a1a3c4fc0
Deleted: sha256:737d053c98166e4949f26b6be47c451e0eea04633bb1a048820e1915e2581774
Deleted: sha256:7a1cefb2540611b408fa6afbb5e932546e7c524b77ab3ae97f347787ade231f2
Deleted: sha256:80bf47bd9ea86287c4544159538a1e85bbf33ada8024351b6ee0e017f25bfff3
Untagged: python:3.8-slim
Untagged: python@sha256:d31a1beb6ccddbf5b5c72904853f5c2c4d1f49bb8186b623db0b80f8c37b5899
Deleted: sha256:214d62795dbbd487ac169bb05c944ca76c11c7b5b5f0277509747824db906992
Deleted: sha256:2072f4f0804d38c63805f550eac93e494b408ad8982e27a464fecb7d5e5cda58
Deleted: sha256:a766fa6d3c77dd3b9ced55be33949a1e74b10a612020e1811e8b01cd914fe0db
Deleted: sha256:9dcdcbc891c78c6c76cf09888373a78f9aafc223bfc0325ddff8a83e3b7bbe0a
Deleted: sha256:e3b8dc3b414c4a2cedba49b7442af204935d902b3338dbebdd1267c36fcc219d
Deleted: sha256:e8b689711f21f9301c40bf2131ce1a1905c3aa09def1de5ec43cf0adf652576e
00:38:28 l1@l1:~/TPIS/IK_31/lab5 (master) $ sudo docker images
REPOSITORY   TAG       IMAGE ID   CREATED   SIZE
00:38:44 l1@l1:~/TPIS/IK_31/lab5 (master) $ 
```

#### 13. Перейшов до іншого варіанту з використанням `docker-compose.yaml`. Для цього створив даний файл у кореновій папці проекту та заповнив вмістом з прикладу. Проект який я буду розгортити за цим варіантом трохи відрізняється від першого тим що у нього зявляється дві мережі: приватна і публічна.
Файл `docker-compose.yaml`:
```text
version: '3.8'
services:
  hits:
    build:
      context: .
      dockerfile: Dockerfile.app
    image: pavlovulchak/lab4:compose-app
    container_name: app
    depends_on:
      - redis
    networks:
      - public
      - secret
    ports:
      - 80:5000
    volumes:
      - hits-logs:/hits/logs
  tests:
    build:
      context: .
      dockerfile: Dockerfile.tests
    image: pavlovulchak/lab4:compose-tests
    container_name: tests
    depends_on:
      - hits
    networks:
      - public
  redis:
    image: redis:alpine
    container_name: redis
    volumes:
      - redis-data:/data
    networks:
      - secret
volumes:
  redis-data:
    driver: local
  hits-logs:
    driver: local
networks:
  secret:
    driver: bridge
  public:
    driver: bridge
```

#### 14. Перевірив чи `Docker-compose` встановлений та працює у моїй системі, а далі просто запускаю `docker-compose`:
```text
docker-compose --version
sudo docker-compose -p lab5 up
```
```text
09:25:32 l1@l1:~/TPIS/IK_31/lab5 (master) $ docker-compose --version
docker-compose version 1.29.2, build 5becea4c
09:33:50 l1@l1:~/TPIS/IK_31/lab5 (master) $
```

#### 15. Перевірив чи працює веб-сайт. Дана сторінка відображається за адресою `http://172.19.0.2:5000/`

#### 16. Перевірив чи компоуз створив докер імеджі. Всі теги коректні і назва репозиторія вказана коректно:
```text
10:01:08 l1@l1:~/TPIS/IK_31/lab5 (master) $ sudo docker images
[sudo] password for l1: 
REPOSITORY          TAG             IMAGE ID       CREATED          SIZE
kekeroni1337/lab4   compose-tests   9db98127b13e   20 minutes ago   301MB
kekeroni1337/lab4   compose-app     94499c320c52   22 minutes ago   299MB
python              3.8-slim        64458f531a7e   6 days ago       122MB
redis               alpine          5c08f13a2b92   10 days ago      32.4MB
10:01:47 l1@l1:~/TPIS/IK_31/lab5 (master) $ 
```

#### 17. Зупинив проект натиснувши `Ctrl+C` і почистітив ресурси створені компоуз командою `docker-compose down`.

#### 18. Завантажив створені імеджі до Docker Hub репозиторію за допомого команди `sudo docker-compose push`.

#### 19. Що на Вашу думку краще використовувати `Makefile` чи `docker-compose.yaml`? - На мою думку `Makefile` більш інтуїтивно зрозумілий, адже можна в ньому побачити які команди запускаються.

#### 20. (Завдання) Оскільки Ви навчились створювати docker-compose.yaml у цій лабораторній то потрібно:
- Cтворив `docker-compose.yaml` для лабораторної №4. Компоуз повинен створити два імеджі для `Django` сайту та моніторингу, а також їх успішно запустити.
Файлик `docker-compose.yaml`:
```text
version: '3.8'
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    image: kekeroni1337/lab4:compose-jango
    container_name: django
    networks:
      - public
    ports:
      - 8000:8000
  monitoring:
    build:
      context: .
      dockerfile: Dockerfile.site
    image: kekeroni1337/lab4:compose-monitoring
    container_name: monitoring
    network_mode: host
networks:
  public:
    driver: bridge
```
#### 21. Після успішного виконання роботи я відредагував свій `README.md` у цьому репозиторію та створив pull request.
