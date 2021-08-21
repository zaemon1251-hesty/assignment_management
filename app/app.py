import sys
# セッション変数の取得
from model.setting import session
from sqlalchemy import func, desc
from sqlalchemy.exc import ArgumentError, IntegrityError
# モデルの取得
from model.models import *
from task.task import get_assignments

# config
status = {0:"end",1:"normal",2:"semi",3:"hot"}

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


def add(courses, assignments, user_id=None):
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
            lecture.title=course['course_title'], 
            lecture.url=course['course_url']
            # Insert
            try:
                session.add(lecture)
                session.commit()
            except:
                # idが重複するものは無視するだけでいい
                pass
        else:
            lecture = Courses(id=lec_id, 
                          title=course['course_title'], 
                          url=course['course_url'])
            lectures.append(lecture)
    session.add_all(lectures)
    session.commit()
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
                # idが重複するものは無視するだけでいい
                pass
        else:
            work = Assignments(id=assignment_id, 
                           title=assignment['assignment_title'],
                            state=1,
                            info=assignment['info'], 
                            url=assignment['assignment_url'], 
                            course_id=assignment['course_id'])
            works.append(work)
    session.add_all(works)
    session.commit()
    # userassignment
    if not user_id:
        # user_idがなかったら先にリターン
        print("SUCCESS")
        return lectures, works
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
    session.commit()

    print("SUCCESS")
    return lectures, works, user_assigments


def get(request=None, state=1):
    if not request:
        data = session.query(Courses.title, Assignments.title, Assignments.info, Assignments.url, Assignments.state)\
                .filter(Courses.id == Assignments.course_id)\
                .filter(Assignments.state >= state)\
                    .order_by(desc(Assignments.state))\
                        .all()
    else:
        data = []
    return data


def get_with_user(user_id, request=None, state=1):
    if not request:
        data = session.query(Courses.title, Assignments.title, Assignments.info, Assignments.url, UserAssignment.state)\
                .filter(UserAssignment.user_id == user_id)\
                .filter(UserAssignment.assignment_id == Assignments.id)\
                .filter(Courses.id == Assignments.course_id)\
                .filter(UserAssignment.state >= state)\
                    .order_by(desc(UserAssignment.state))\
                        .all()
    else:
        data = []
    return data


def changeStatus(id, state):
    assignments = session.query(Assignments).filter(Assignments.id == id).first()
    assignments.state = state
    session.commit()
    print("SUCCESS")


def changeStatus_with_user(id, state):
    user_assignment = session.query(UserAssignment).filter(UserAssignment.id == id).first()
    user_assignment.state = state
    session.commit()
    print("SUCCESS")


def main():
    pass
    


if  __name__ == "__main__":
    if len(sys.argv) <= 1:
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
                request = None
                state = int(datas[0])
            except:
                request = datas[0]
                state = datas[1]
            print(*get(request=request, state=state), sep='\n')
            
                
    elif f_name == "changeStatus":
        if len(sys.argv) <= 4:
            raise ArgumentError("引数が足りません")
        else:
            _id, state = int(datas[0]), int(datas[1]) 
            changeStatus(_id, state)
    else:
        print("正しい関数名を入れてください。\n(関数名: main, add, get, changeStatus)")