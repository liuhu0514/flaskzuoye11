from orm import model
from sqlalchemy import create_engine
engine = create_engine("mysql+mysqlconnector://root:123456@localhost/flaskdb",
                                    encoding='utf8', echo=True)
from sqlalchemy.orm import sessionmaker
session = sessionmaker(bind=engine)()


def checkUser(username, password):
    """
    登录验证
    :param username: 用户输入的登录用户名
    :param password: 用户输入的登录密码
    :return: 返回登录结果
    """
    try:
        uname = session.query(model.User).all()
        for i in uname:
            if i.username == username and i.password == password:
                return i.id
        else:
            return 'fail'
    except:
        return 'fail'


def insertUser(username, password):
    """
    注册验证
    :param username: 用户输入的用户名
    :param password: 用户输入的密码
    :return: 返回注册结果
    """
    n_list = []
    try:
        if username and password:
            uname = session.query(model.User.username).all()
            for i in uname:
                n_list += [i.username]
            if username in n_list:
                return 'fail'
            else:
                session.add(model.User(username=username, password=password))
                session.commit()
                session.close()
                return 'success'
        else:
            return 'empty'

    except:
        return 'fail'


def obtainProject(id):
    """
    获取指定用户所有项目
    :param id: 用户id
    :return: 返回查询到的该用户所有项目
    """
    try:
        ps = session.query(model.Project).filter(model.Project.uid == int(id)).all()
        return ps
    except:
        return 'fail'


def queryUname(id):
    """
    获取用户名
    :param id: 用户id
    :return: 返回用户名
    """
    try:
        u = session.query(model.User).filter(model.User.id == int(id)).first()
        return u.username

    except Exception as e:
        return 'fail'


def qureyPdetails(pid):
    """
    获取指定项目的详情
    :param pid: 项目id
    :return: 返回指定项目
    """
    p = session.query(model.Project).filter(model.Project.id == int(pid)).first()
    return p


def addProject(pname, pdetails, uid):
    """
    添加项目
    :param pname: 项目名称
    :param pdetails: 项目详情
    :param uid: 用户id
    :return: 返回添加结果
    """
    try:
        if pname:
            session.add(model.Project(pname=pname, pdetails=pdetails, uid=int(uid)))

            session.commit()
            session.close()
            return 'success'
        else:
            return "kongname"
    except Exception as e:
        return "fail"


def delete(pid):
    try:
        session.query(model.Project).filter(model.Project.id == int(pid)).delete()
        session.commit()
        session.close()
        return 'success'
    except:
        return 'fail'


def modify(pid, pname, pdetails):
    try:
        session.query(model.Project).filter(model.Project.id == int(pid)).update({model.Project.pname: pname,
                                                                                  model.Project.pdetails: pdetails})
        session.commit()
        session.close()
        return 'success'
    except:
        return 'fail'


def search(search, uid):
    try:

        ps = session.query(model.Project).filter(model.Project.uid == int(uid),
                                             model.Project.pname.like('%'+search+'%')).all()
        if ps:
            return ps
        else:
            return 'kong'
    except:
        return 'fail'
