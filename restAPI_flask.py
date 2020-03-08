
# from werkzeug.wrappers import Request, Response # for running Flask on Jupyter Lab

from flask import Flask, jsonify, request

from multiprocessing import Value                    #This is Multithreading lib

counter = Value('i', 0)
app = Flask(__name__)

a = []
help_message = """
API Usage:
 
- GET    /api/list
- POST   /api/add data={"key": "value"}
- GET    /api/get/<id>
- PUT    /api/update/<id> data={"key": "value_to_replace"}
- DELETE /api/delete/<id> 

"""


def id_generator():
    '''
    This function that will generate id’s for each document.
    '''
    with counter.get_lock():
        counter.value += 1
        return counter.value

@app.route('/api', methods=['GET'])
def help():
    return help_message

@app.route('/api/list', methods=['GET'])
def list():
    return jsonify(a)

@app.route('/api/add', methods=['POST'])
def index():
    payload = request.json
    print(payload)
    payload['id'] = id_generator()
    a.append(payload)
    return "Created: {} \n".format(payload)

@app.route('/api/get', methods=['GET'])
def get_none():
    return 'ID Required: /api/get/<id> \n'

@app.route('/api/get/<int:_id>', methods=['GET'])
def get(_id):
    for user in a:
        if _id == user['id']:
            selected_user = user
            return jsonify(selected_user)
        else:
            return "Provided ID, Not available!!"

@app.route('/api/update', methods=['PUT'])
def update_none():
    return 'ID and Desired K/V in Payload required: /api/update/<id> -d \'{"name": "john"}\' \n'

'''funtions for updating info'''
@app.route('/api/update/<int:_id>', methods=['PUT'])
def update(_id):

    id_check=[i for i in a if _id == i['id']]
    if len(id_check) == 0:
        print("Not found the ID Given")
        return "The Given ID is not present, Provide the existing one !!!"


    else:
        update_req = request.json
        print(type(update_req))
        # print(list(update_req.keys()))
        key_to_update=[li for li in update_req.keys()]
        print(key_to_update)
        for key in key_to_update:
            print(type(key))
            try:
                next((item for item in a if item['id'] == _id))[key] =  update_req[key]
            except StopIteration as e:
                print(e)
                break
        updated_response=''.join(map(str,[i for i in a if _id == i['id']]))

        return "Updated: {} \n".format(updated_response)


@app.route('/api/delete/<int:_id>', methods=['DELETE'])
def delete(_id):

    id_check=[i for i in a if _id == i['id']]
    if len(id_check) == 0:
        print("Not found the ID Given")
        return "The Given ID is not present to delete, Provide the existing one !!!"

    else:
        try:
            deleted_user = (item for item in a if item['id'] == _id).__next__()

        except StopIteration as e:
            print(e)

        print('*****Deleted User*******')
        print(deleted_user)
        a.remove(deleted_user)
        return "Deleted: {} \n".format(deleted_user)

if __name__ == '__main__':
    app.run(debug=True)

    ##Used below codes for running on Jupyter Notebook
    # from werkzeug.serving import run_simple
    # run_simple('localhost', 9000, app)
