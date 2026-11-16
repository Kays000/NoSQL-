import os
import random
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "nosql_lab12")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "books")
SEED = int(os.getenv("SEED", 42))
DOC_COUNT = int(os.getenv("DOC_COUNT", 20000))


def main():
    random.seed(SEED)
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
    db = client[DB_NAME]
    coll = db[COLLECTION_NAME]

    # Очистка только учебной коллекции перед генерацией
    coll.drop()

    rows = [
        {
            "categoryId": random.randint(1, 20),
            "publishedYear": random.randint(1990, 2025),
            "title": f"Book {i}",
            "authorId": random.randint(1, 300),
            "pages": random.randint(100, 900),
        }
        for i in range(DOC_COUNT)
    ]

    coll.insert_many(rows)

    server_version = client.server_info().get("version", "unknown")
    total_docs = coll.count_documents({})
    print(f"Версия MongoDB: {server_version}")
    print(f"База данных: {DB_NAME}, коллекция: {COLLECTION_NAME}")
    print(f"Seed: {SEED}, вставлено документов: {total_docs}")


if __name__ == "__main__":
    main()
