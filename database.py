import mysql.connector
from hash import generate_uuid
import time


def connect():
    return mysql.connector.connect(
        user="admin",
        password="password",
        host="127.0.0.1",
        port=3306,
        database="srsdb",
    )


def get_all():
    query = "SELECT * FROM users"
    cursor = None
    try:
        connection = connect()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        users = cursor.fetchall()
        return {"users": users}
    finally:
        cursor.close() if cursor else None
        connection.close() if connection else None


def get_one(uuid):
    query = "SELECT * FROM users WHERE uuid = %s"
    cursor = None
    try:
        connection = connect()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, (uuid,))
        user = cursor.fetchone()
        return {"user": user}
    finally:
        cursor.close() if cursor else None
        connection.close() if connection else None


def post_one(contact):
    insert_query = (
        "INSERT INTO users (uuid, username, name, email, sms, created, lastseen) "  # noqa
        "VALUES (%(uuid)s, %(username)s, %(name)s, %(email)s, %(sms)s, %(created)s, %(lastseen)s)"  # noqa
    )

    values = {
        "uuid": generate_uuid(contact),
        "username": None,
        "name": None,
        "email": contact if "@" in contact else None,
        "sms": contact if "@" not in contact else None,
        "created": int(time.time()),
        "lastseen": int(time.time()),
    }
    cursor = None
    try:
        connection = connect()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(insert_query, values)
        connection.commit()

        select_query = "SELECT * FROM users WHERE uuid = %s"
        cursor.execute(select_query, [values["uuid"]])
        user = cursor.fetchone()

        return {"user": user}

    finally:
        cursor.close() if cursor else None
        connection.close() if connection else None


def update_one(uuid, update_data: dict):
    update_query = "UPDATE users SET "
    update_values = {}

    for key, value in update_data.items():
        if key in ["username", "name", "email", "sms"]:
            update_query += f"{key} = %({key})s, "
            update_values[key] = value

    update_query += "lastseen = %(lastseen)s"
    update_values["lastseen"] = int(time.time())

    update_query += " WHERE uuid = %(uuid)s"
    update_values["uuid"] = uuid

    cursor = None

    try:
        connection = connect()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(update_query, update_values)
        connection.commit()

        updated_user = get_one(uuid)
        return {"user": updated_user}
    finally:
        cursor.close() if cursor else None
        connection.close() if connection else None


def delete_one(uuid):
    cursor = None
    try:
        connection = connect()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("DELETE FROM users WHERE uuid = %s", (uuid,))
        connection.commit()

        return (
            {"status": "success", "deleted_user": uuid}
            if cursor.rowcount
            else {"status": "failed"}
        )

    finally:
        cursor.close() if cursor else None
        connection.close() if connection else None
