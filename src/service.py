import sys
from datetime import datetime, timezone, timedelta

from sqlalchemy import exc
# セッション変数の取得
from model.setting import session
from sqlalchemy import func, desc, and_
from sqlalchemy.exc import ArgumentError, IntegrityError
# モデルの取得
from model.models import *
from task.task import get_assignments

#config
TZ = timezone(timedelta(hours=+9), 'JST')
THIS_YEAR = datetime.now(TZ).year

def get_user(name=None, id=None):
    if not name and not id:
        return None
    conditions = {'user_name':name, 'user_id':id}
    data = session.query(Users)
    data = add_conditions(data, conditions=conditions)
    return data.first()


def add_user(name, userid, passwd):
    user = session.query(Users).filter(Users.name == name).first()
    if user:
        print("ユーザーが見つかりました。moodleのidとパスワードを変更します。")
        user.moodle_userid = userid
        user.moodle_passwd = passwd
    else:
        print("新規ユーザーを作成します。")
        user = Users(name=name,
                     moodle_userid = userid,
                     moodle_passwd = passwd)
        session.add(user)
    session.commit()
    return user.id


def add(user_id=None, keywords=[]):
    no_problem = True
    if user_id:
        user = session.query(Users).filter(Users.id == user_id).first()
        moodle_userid, moodle_passwd = user.moodle_userid, user.moodle_passwd
    else:
        moodle_userid, moodle_passwd = '', ''
    if keywords == []:
        keywords = [str(THIS_YEAR)]
    else:
        pass
    courses, assignments = get_assignments(moodle_userid, moodle_passwd, keywords=keywords)
    # log
    lectures = []
    works = []
    assignment_ids = []
    user_assigments = []
    # courses
    for lec_id,course in courses.items():
        # Entity検索
        lecture = session.query(Courses).filter(Courses.id == lec_id).first()
        if lecture:
            lecture.title=course['course_title']
            lecture.url=course['course_url']
            # Insert
            try:
                session.commit()
            except:
                no_problem = False
                session.rollback()
        else:
            lecture = Courses(id=lec_id, 
                          title=course['course_title'], 
                          url=course['course_url'])
            lectures.append(lecture)
    session.add_all(lectures)
    
    try:
        session.commit()
    except:
        no_problem = False
        session.rollback()
    # assignments
    for assignment_id,assignment in assignments.items():
        assignment_ids.append(assignment_id)
        # Entity検索
        work = session.query(Assignments).filter(Assignments.id == assignment_id).first()
        if work:
            if work.state <= 0:
                # endした課題は無視
                continue
            work.title=assignment['assignment_title'],
            work.info=assignment['info'], 
            work.url=assignment['assignment_url'], 
            work.course_id=assignment['course_id']
            # Insert
            try:
                session.commit()
            except:
                no_problem = False
                session.rollback()
        else:
            work = Assignments(id=assignment_id, 
                            title=assignment['assignment_title'],
                            state=1,
                            info=assignment['info'], 
                            url=assignment['assignment_url'], 
                            course_id=assignment['course_id'])
            works.append(work)
    session.add_all(works)
    try:
        session.commit()
    except:
        no_problem = False
        session.rollback()    
    # userassignment
    if not user_id:
        # user_idがなかったら終了
        return no_problem
    for assignment_id in assignment_ids:
        user_assigment = session.query(UserAssignment)\
            .filter(UserAssignment.user_id == user_id)\
            .filter(UserAssignment.assignment_id == assignment_id)\
                .first()
        if user_assigment:
            # 無視する
            continue
        else:
            user_assigment = UserAssignment(
                user_id=user_id,
                assignment_id=assignment_id,
                state=1
            )
            user_assigments.append(user_assigment)
    session.add_all(user_assigments)
    try:
        session.commit()
    except:
        no_problem = False
        session.rollback()
    return no_problem


def get(state=1, user_id=None, conditions={}):
    if not user_id:
        data = session.query(Assignments,Courses)\
                .filter(Courses.id == Assignments.course_id)\
                .filter(Assignments.state >= state)
        data = add_conditions(data, conditions=conditions)
        data = data.order_by(desc(Assignments.state)).all()
    else:
        data = session.query(Assignments, Courses, UserAssignment)\
                .filter(UserAssignment.user_id == user_id)\
                .filter(UserAssignment.assignment_id == Assignments.id)\
                .filter(Courses.id == Assignments.course_id)\
                .filter(UserAssignment.state >= state)
        data = add_conditions(data, conditions=conditions)
        data = data.order_by(desc(UserAssignment.state)).all()
    return data


def changeStatus(id, state, user_id=None):
    no_problem =True
    if not user_id:
        assignments = session.query(Assignments).filter(Assignments.id == id).first()
        assignments.state = state
    else:
        user_assignment = session.query(UserAssignment).filter(UserAssignment.id == id).first()
        user_assignment.state = state
    try:
        session.commit()
    except:
        no_problem = False
        session.rollback()
    return no_problem


def add_conditions(q, conditions={}):
    # 動的に条件を追加する
    for key, value in conditions.items():
        if key == "course" and value:
            q = q.filter(Courses.title.like(value))
        elif key == "assignment" and value:
            q = q.filter(Assignments.title.like(value))
        elif key == "info" and value:
            q = q.filter(Assignments.info.like == value)
        elif key == "user_name" and value:
            q = q.filter(Users.name == value)
        elif key == "user_id" and value:
            q = q.filter(Users.id == value)
    return q


def main():
    add_user('zaemon', 'id', 'passwd')
    user_id = get_user(name='zaemon').id
    add(user_id=user_id)
    print(*get(), sep='\n')


if  __name__ == "__main__":
    if len(sys.argv) < 2:
        print("引数が足りません")
        exit()
    f_name = sys.argv[1]
    datas = sys.argv[2:] if len(sys.argv) >= 3 else []
    if f_name == "main":
        main()
    elif f_name == "add":
        courses, assignments = get_assignments()
        add(courses, assignments)
    elif f_name == "get":
        if datas == []:
            print(*get(), sep='\n')
        else:
            try:
                state = int(datas[0])
                user_id = None
            except:
                state = int(datas[0])
                user_id = int(datas[1])
            print(*get(user_id=user_id, state=state), sep='\n')
    elif f_name == "changeStatus":
        if len(sys.argv) <= 4:
            raise ArgumentError("引数が足りません")
        else:
            _id, state = int(datas[0]), int(datas[1]) 
            changeStatus(_id, state)
    else:
        print("正しい関数名を入れてください。\n(関数名: main, add, get, changeStatus)")