# Проверки (каждый пользователь в отдельной сессии)
mongosh --host 127.0.0.1 --authenticationDatabase hotel_lab13 -u <user> -p
use hotel_lab13

| Пользователь | Команда | Ожидается |
|---|---|---|
| viewer13 | db.rooms.findOne({roomNo:101}) | OK |
| viewer13 | db.rooms.insertOne({roomNo:999}) | Unauthorized |
| viewer13 | db.reservations.findOne({resId:1}) | Unauthorized |
| editor13 | db.rooms.find({status:"free"}) | OK |
| editor13 | db.rooms.updateOne({roomNo:103},{$set:{status:"busy"}}) | OK |
| editor13 | db.reservations.findOne({resId:1}) | Unauthorized |
| editor13 | db.reservations.deleteOne({resId:1}) | Unauthorized |
| auditor13 | db.audit_events.find() | OK |
| auditor13 | db.audit_events.insertOne({event:"fake"}) | Unauthorized |
| auditor13 | db.rooms.findOne({roomNo:101}) | Unauthorized |
| auditor13 | db.reservations.findOne({resId:1}) | Unauthorized |
