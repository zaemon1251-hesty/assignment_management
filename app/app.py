import responder
from sqlalchemy.sql import type_api
import service
import json
import asyncio
# config
status = {0:"end",1:"normal",2:"semi",3:"hot"}
api = responder.API()


@api.route('/')
async def index(req, resp):
    user_id = req_user_id(req)
    print("user_id got: %s" % user_id)
    user = service.get_user(id=user_id)
    print("got user///")
    print(user)
    
    job_state = req.params.get('job_state', None)
    if job_state in ['True', True]:
        message = "全てのデータを正常に保存しました"
    elif job_state in ['False', False]:
        message = "なんらかのデータを保存できませんでした"
    elif type(job_state) == str:
        message = job_state
    else:
        message = None
    
    if req.method == 'POST':
        data = await req.media(format="form")
        conditions = {}
        state = int(data['state'])
        conditions['course'] = "%{}%".format(data['course']) if data['course'] != '' else None
        conditions['assignment'] = "%{}%".format(req.form['assignment']) if data['assignment'] != '' else None
        conditions['info'] = "%{}%".format(req.form['info']) if data['info'] != '' else None
        datas = service.get(state=state, user_id=user_id, conditions=conditions, to_dict=True)
    else:
        datas = service.get(user_id=user_id, to_dict=True)
    resp.headers["Content-Type"] = "application/json; charset=UTF-8"
    resp.media = {"data": datas}


@api.route('/add')
async def add(req, resp):
    user_id = req_user_id(req)
    user = service.get_user(id=user_id)
    if not user_id:
        job_state="課題追加はログイン必須です"
    else:
        job_state = "課題を追加します"
    if req.method == 'POST':
        print(req.get_data())
        print(req.form)
        print(req.json)
        try:
            data = await req.media(format="form")
            keywords = data["keywords"].split()
        except:
            keywords = []
    else:
        keywords = []
        
    @api.background.task
    def async_add(user_id, keywords):
        no_problem = service.add(user_id=user_id, keywords=keywords)
        return no_problem
    no_probelm = async_add(user_id, keywords)

    resp.headers["Content-Type"] = "application/json; charset=UTF-8"
    resp.media = {"message" : job_state}


@api.route('/change/{id}/{state}')
def change(req, resp, *, id, state):
    user_id = req_user_id(req)
    no_problem = None
    if req.method == 'GET':
        no_problem = service.changeStatus(state=state, id=int(id), user_id=int(user_id))
    resp.headers["Content-Type"] = "application/json; charset=UTF-8"
    resp.media ={"message":no_problem}


@api.route('/login')
def login(req, resp):
    # id passwd でのログイン処理などの実装もできたらしたい
    name = req.params.get('name', None)
    user  =service.get_user(name=name)
    if user:
        user_id=user.id
    else:
        user_id = -1
    resp.headers["Content-Type"] = "application/json; charset=UTF-8"
    resp.media = {"message": user_id}


@api.route('/user')
async def user(req, resp):
    user_id = req_user_id(req)
    if req.method == 'POST':
        data = await req.media(format="form")
        name = data['name']
        userid = data['moodle_userid']
        passwd = data['moodle_passwd']
        user_id = service.add_user(name, userid, passwd)
    else:
        user = service.get_user(id=user_id)
    resp.headers["Content-Type"] = "application/json; charset=UTF-8"
    resp.media = {"message":user_id}
    

@api.route('/log')
def log(req, resp): 
    resp.headers["Content-Type"] = "text/html; charset=UTF-8"
    resp.media = api.template("log.html")


def req_user_id(req):
    try:
        user_id = int(req.params.get('user_id', -1))
    except:
        user_id = -1
    if user_id == -1:
        user_id = None
    return user_id


if __name__ == '__main__':
    api.run(address='0.0.0.0', port=8889, debug=True)