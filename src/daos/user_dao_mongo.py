"""
User DAO (Data Access Object)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId
from models.user import User


class UserDAOMongo:

    def __init__(self):
        try:
            env_path = ".env"
            load_dotenv(dotenv_path=env_path)

            db_host = os.getenv("MONGODB_HOST")
            db_user = os.getenv("DB_USERNAME")
            db_pass = os.getenv("DB_PASSWORD")

            self.client = MongoClient(
                host=db_host,
                username=db_user,
                password=db_pass,
                authSource="admin"
            )

            self.db = self.client["log430"]
            self.users = self.db["users"]

        except Exception as e:
            print("Erreur : " + str(e))

    def select_all(self):
        """ Select all users from MongoDB """

        documents = self.users.find()

        users = []

        for document in documents:
            user = User(
                str(document["_id"]),
                document["name"],
                document["email"]
            )

            users.append(user)

        return users

    def insert(self, user):
        """ Insert given user into MongoDB """

        document = {
            "name": user.name,
            "email": user.email
        }

        result = self.users.insert_one(document)

        return str(result.inserted_id)

    def update(self, user):
        """ Update given user in MongoDB """

        result = self.users.update_one(
            {"_id": ObjectId(user.id)},
            {
                "$set": {
                    "name": user.name,
                    "email": user.email
                }
            }
        )

        return result.modified_count

    def delete(self, user_id):
        """ Delete user from MongoDB with given user ID """

        result = self.users.delete_one(
            {"_id": ObjectId(user_id)}
        )

        return result.deleted_count

    def delete_all(self):
        """ Delete all users from MongoDB """

        result = self.users.delete_many({})

        return result.deleted_count

    def close(self):
        """ Close MongoDB connection """

        self.client.close()