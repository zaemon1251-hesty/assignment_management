from flask import Flask, request, render_template, redirect, url_for
import service
# config
status = {0: "end", 1: "normal", 2: "semi", 3: "hot"}
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
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
    return render_template('index.html', datas=datas, user=user, status=status)


@app.route('/add', methods=['GET', 'POST'])
def add():
    user_id = request_user_id(request)
    if request.method == 'POST':
        keywords = request.form['keywords'].split()
    else:
        keywords = []
    no_problem = service.add(user_id=user_id, keywords=keywords)
    return redirect(url_for('index', user_id=user_id))


@app.route('/change/<int:id>/<int:state>', methods=['GET'])
def change(id, state):
    user_id = request_user_id(request)
    if user_id == -1:
        user_id = None
    print("user_id got: %s" % user_id)
    if request.method == 'GET':
        no_problem = service.changeStatus(state=state, id=id, user_id=user_id)
    return redirect(url_for('index', user_id=user_id))


@app.route('/login', methods=['GET'])
def login():
    # id passwd でのログイン処理などの実装もできたらしたい
    name = request.args.get('name')
    user = service.get_user(name=name)
    if user:
        user_id = user.id
    else:
        user_id = -1
    return redirect(url_for('index', user_id=user_id))


@app.route('/user', methods=['GET', 'POST'])
def user():
    user_id = request_user_id(request)
    if request.method == 'POST':
        name = request.form['name']
        userid = request.form['moodle_userid']
        passwd = request.form['moodle_passwd']
        user_id = service.add_user(name, userid, passwd)
        return redirect(url_for('index', user_id=user_id))
    else:
        user = service.get_user(id=user_id)
        return render_template('user.html', user=user)


def request_user_id(request):
    try:
        user_id = int(request.args.get('user_id', -1))
    except BaseException:
        user_id = -1
    if user_id == -1:
        user_id = None
    return user_id


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
