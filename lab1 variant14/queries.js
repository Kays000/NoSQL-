// 1. Получить все документы коллекции
db.tracks.find()

// 2. Найти документ по уникальному идентификатору
db.tracks.find({ trackId: 201 })

// 3. Выполнить поиск по строковому полю
db.tracks.find({ artist: "The Weeknd" })

// 4. Выполнить поиск с $gt или $gte
db.tracks.find({ duration: { $gte: 220 } })

// 5. Выполнить поиск с $lt или $lte
db.tracks.find({ plays: { $lt: 2000000 } })

// 6. Выполнить запрос одновременно по двум условиям
db.tracks.find({ artist: "Linkin Park", duration: { $gt: 200 } })

// 7. Использовать $or
db.tracks.find({ $or: [{ artist: "Queen" }, { plays: { $gte: 3000000 } }] })

// 8. Использовать $in
db.tracks.find({ artist: { $in: ["Queen", "Eagles"] } })

// 9. Выполнить запрос к элементу массива
db.tracks.find({ tags: "rock" })

// 10. Выполнить запрос к полю вложенного документа
db.tracks.find({ "album.year": 2020 })

// 11. Выполнить проекцию
db.tracks.find({}, { title: 1, artist: 1, plays: 1, _id: 0 })

// 12. Выполнить сортировку
db.tracks.find().sort({ plays: -1 })

// 13. Использовать limit()
db.tracks.find().sort({ plays: -1 }).limit(3)

// 14. Изменить одно поле через $set
db.tracks.updateOne({ trackId: 201 }, { $set: { plays: 3600000 } })

// 15. Добавить новый элемент в массив через $push
db.tracks.updateOne({ trackId: 201 }, { $push: { tags: "hit" } })

// 16. Обновить несколько документов через updateMany()
db.tracks.updateMany({ artist: "Linkin Park" }, { $inc: { plays: 50000 } })

// 17. Удалить один документ через deleteOne()
db.tracks.deleteOne({ trackId: 210 })

// 18. Продемонстрировать итоговое содержимое коллекции
db.tracks.find()