import mysql.connector
from hash import generate_uuid
import time

connection = mysql.connector.connect(
    user="admin",
    password="password",
    host="db",  # if using docker-compose
    # host="127.0.0.1",  # if using local mariadb
    port=3306,
    database="srsdb",
)


def get_all():
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return {"users": users}


def get_one(uuid):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE uuid = %s", (uuid,))
    user = cursor.fetchone()
    return {"user": user}


def post_one(contact):
    values = {"uuid": generate_uuid(contact)}
    if "@" in contact:
        values["email"] = contact
        values["sms"] = None
    else:
        values["sms"] = contact
        values["email"] = None
    values["username"] = None
    values["name"] = None
    current_timestamp = int(time.time())
    values["created"] = current_timestamp
    values["lastseen"] = current_timestamp

    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "INSERT INTO users (uuid, username, name, email, sms, created, lastseen) VALUES (%s, %s, %s, %s, %s, %s, %s)",  # noqa
        (
            values["uuid"],
            values["username"],
            values["name"],
            values["email"],
            values["sms"],
            values["created"],
            values["lastseen"],
        ),
    )
    connection.commit()
    cursor.execute("SELECT * FROM users WHERE uuid = %s", (values["uuid"],))
    user = cursor.fetchone()
    return {"user": user}


def update_one(uuid, update_data: dict):
    update_data_filtered = {
        key: value
        for key, value in update_data.items()
        if key in ["username", "name", "email", "sms"]
    }

    cursor = connection.cursor(dictionary=True)

    update_query = "UPDATE users SET "
    update_values = []

    for key, value in update_data_filtered.items():
        update_query += f"{key} = %s, "
        update_values.append(value)

    update_query += "lastseen = %s"
    update_values.append(int(time.time()))

    update_query += " WHERE uuid = %s"
    update_values.append(uuid)

    cursor.execute(update_query, tuple(update_values))
    connection.commit()

    updated_user = get_one(uuid)
    return {"user": updated_user}


def delete_one(uuid):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("DELETE FROM users WHERE uuid = %s", (uuid,))
    connection.commit()
    if cursor.rowcount:
        return {"status": "success", "deleted_user": uuid}
    else:
        return {"status": "failed"}
