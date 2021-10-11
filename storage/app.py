from flask import Flask, abort, jsonify, request
import pymysql
import pymysql.cursors
import json
import sys
import uuid

app = Flask(__name__)


def update_item(uuid, json):
    conn = connect()
    cur = conn.cursor()
    insert = "UPDATE items SET json = %s WHERE uuid=%s"
    cur.execute(insert, (json,uuid))
    conn.commit()
    conn.close()


def create_empty_item(uuid):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO items (uuid) VALUES (%s)", (uuid))
    conn.commit()
    conn.close()
    return uuid


def read_from_db(uuid):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM items WHERE uuid=%s", (uuid))
        items = cur.fetchall()
        return items[0]
    except Exception as ex:
        print(ex)
    finally:    
        conn.close()



def connect():
    print('connect')
    try:
        conn = pymysql.connect(
            user="cqrs",
            password="123456",
            host="db",
            port=3306,
            database="cqrs",
            cursorclass=pymysql.cursors.DictCursor
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
    print(item)
    return jsonify(item)


@app.route('/items/<uuid>', methods=['PUT'])
def update(uuid):
    # decode the request
    try:
        print(request.data)
        jitem = json.loads(request.data)
        print(jitem)
    except Exception as ex:
        print(ex)
        abort(404)
    try:
        sitem = str(json.dumps(jitem))
        #update_item(uuid, jitem)
        update_item(uuid, sitem)

    except Exception as ex:
        print(ex)
        abort(404)
    return jitem        


@app.route('/items', methods=['POST'])
def create():
    try:    
        new_uuid = str(uuid.uuid4())
        create_empty_item(new_uuid)
        print("new uuid created and added: {0}".format(new_uuid))
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
