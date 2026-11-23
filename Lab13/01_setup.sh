#!/bin/bash
# Подставьте пароль локально (не коммитьте его в Git)
docker run -d --name mongo-rbac-lab -p 127.0.0.1:27017:27017 \
 -e MONGO_INITDB_ROOT_USERNAME=labadmin \
 -e MONGO_INITDB_ROOT_PASSWORD=<ЗАДАЙТЕ_ЛОКАЛЬНО> mongo:7

# Вход администратора (пароль вводится интерактивно):
# mongosh --host 127.0.0.1 --authenticationDatabase admin -u labadmin -p
# Затем в сессии: load("02_seed.js"); load("03_roles_users.js")
