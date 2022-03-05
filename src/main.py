from fastapi import FastAPI, HTTPException, status
import json

from src.interface.controller import api_router
import service
# config
app = FastAPI(__name__)

app.include_router(api_router, prefix="/api")


@app.get(
    "/",
    status_code=status.HTTP_200_OK
)
async def healthz():
    return json.dumps({"message": "I am Zaemon."})


@app.route('/', methods=['GET', 'POST'])
def _index():
    user_id = request_user_id(request)
    print("user_id got: %s" % user_id)
    user = service.get_user(id=user_id)
    print("got user///")
    print(user)
    if request.method == 'POST':
        conditions = {}
        state = int(request.form['state'])
        conditions['course'] = "%{}%".format(
            request.form['course']) if request.form['course'] != '' else None
        conditions['assignment'] = "%{}%".format(
            request.form['assignment']) if request.form['assignment'] != '' else None
        conditions['info'] = "%{}%".format(
            request.form['info']) if request.form['info'] != '' else None
        datas = service.get(state=state, user_id=user_id,
                            conditions=conditions)
    else:
        datas = service.get(user_id=user_id)


@app.route('/add', methods=['GET', 'POST'])
def add():
    user_id = request_user_id(request)
    if request.method == 'POST':
        keywords = request.form['keywords'].split()
    else:
        keywords = []
    no_problem = service.add(user_id=user_id, keywords=keywords)


@app.route('/change/<int:id>/<int:state>', methods=['GET'])
def change(id, state):
    user_id = request_user_id(request)
    if user_id == -1:
        user_id = None
    print("user_id got: %s" % user_id)
    if request.method == 'GET':
        no_problem = service.changeStatus(state=state, id=id, user_id=user_id)


@app.route('/login', methods=['GET'])
def login():
    # id passwd でのログイン処理などの実装もできたらしたい
    name = request.args.get('name')
    user = service.get_user(name=name)
    if user:
        user_id = user.id
    else:
        user_id = -1


@app.route('/user', methods=['GET', 'POST'])
def user():
    user_id = request_user_id(request)
    if request.method == 'POST':
        name = request.form['name']
        userid = request.form['moodle_userid']
        passwd = request.form['moodle_passwd']
        user_id = service.add_user(name, userid, passwd)
    else:
        user = service.get_user(id=user_id)


def request_user_id(request):
    try:
        user_id = int(request.args.get('user_id', -1))
    except BaseException:
        user_id = -1
    if user_id == -1:
        user_id = None


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
