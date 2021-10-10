from flask import Flask
app = Flask(__name__)


@app.route('/items/<uuid>', methods=['GET'])
def read(uuid):
    try:
        # try to find the item with id 'uuid' in the cache
        redis_instance = redis.Redis(host='localhost', port=6379, db=0)
        # Return the value at key name, 
        # or None if the key doesn’t exist
        item = json.dump(r.get(uuid))
        # if not found checke in the main storage and 
        # set the value in the cache eventually
        if not item:
            r = requests.get("http://localhost:5001/items/"+str(uuid))
            if r.status_code == 200:
                item = r.json()
            redis_instance.set(uuid,item)

    except ex:
        item = None
        print(ex)
    
    if not item:
        abort(404)
    
    return json.dump(item)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
