from flask import Flask
app = Flask(__name__)
from kafka import KafkaProducer


def fetch_new_uuid()
    try:
        r = requests.post("http://localhost:5001/items")
        if r.status_code == 200:
            return r.json() 
        
    except ex:
        print(ex)
        abort(404)


def push_job(jitem):
    producer = KafkaProducer(bootstrap_servers='queue:19092')
    producer.send('items', jitem)
    



@app.route('/items/', methods=['POST'])
def create(item):

    # decode the request
    try:
        jitem = request.get_json()
    except ex:
        print(ex)
        abort(404)

    # fetch a new id
    new_uuid = fetch_new_uuid() 


    # push the job id plus the requst to the queue
    try:
        jitem = json.dumps({"id": new_uuid, "request":request.get_json()})
        push_job(new_uuid, jitem)
    except ex:
        print(ex)
        abort(404)  



    
    return 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
