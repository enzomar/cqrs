from flask import Flask, abort, jsonify
import pymysql
import pymysql.cursors

import sys
import uuid

app = Flask(__name__)


def update_item(uuid, json):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO items (json) VALUES uuid=? WHERE uuid=?", (json, uuid))
    conn.commit()
    conn.close()


def create_empty_item(uuid):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO items (uuid) VALUES uuid=?", (uuid,'{}'))
    item = cur[0]
    conn.commit()
    conn.close()
    return item


def read_from_db(uuid):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT json FROM items WHERE uuid=?", (uuid,))
    item = cur[0]
    conn.close()
    return item


def connect():
    print('connect')
    try:
        conn = pymysql.connect(
            user="cqrs",
            password="123456",
            host="db",
            port=3306,
            database="cqrs"
        )
    except Exception as ex:
        print("Error connecting to MySQL: {0}".format(ex))
        return

    # Get Cursor
    return conn


@app.route('/items/<uuid>', methods=['GET'])
def read(uuid):
    try:
        item = read_from_db(uuid)
    except Exception as ex:
        print(ex)
        abort(404)

    return jsonify(item)


@app.route('/items/<uuid>', methods=['PUT'])
def update(uuid):
    # decode the request
    try:
        jitem = request.get_json()
    except Exception as ex:
        print(ex)
        abort(404)
    try:
        update_item(uuid, jitem)
    except Exception as ex:
        print(ex)
        abort(404)        


@app.route('/items', methods=['POST'])
def create():
    try:    
        new_uuid = uuid.uuid4()
        create_empty_item(new_uuid)
        return new_uuid
    except Exception as ex:
        print(ex)
        try:
            new_uuid = uuid.uuid4()
            create_empty_item(new_uuid)
            return new_uuid
        except Exception as ex:
            print(ex)
    
    abort(404)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
