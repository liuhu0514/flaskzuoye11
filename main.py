from flask import Flask, render_template, request, redirect, make_response
import datetime
from orm import ormmanage

app = Flask(__name__)
app.debug = True
app.send_file_max_age_default = datetime.timedelta(seconds=1)


@app.route('/')
def index():
    user = None
    userid = request.cookies.get('uid')
    user = ormmanage.queryUname(userid)
    return render_template('index.html', userinfo=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', b='')
    elif request.method == 'POST':
        uname = request.form['username']
        upwd = request.form['password']
        r = ormmanage.insertUser(uname, upwd)
        if r == 'empty':
            return render_template('register.html', b='用户名和密码都不能为空，请重新输入')
        elif r == 'success':
            return redirect('/login')
        else:
            return render_template('register.html', b='你输入的用户名已经存在注册失败，请重新注册！')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', a='')
    elif request.method == 'POST':
        uname = request.form['username']
        upwd = request.form['password']
        r = ormmanage.checkUser(uname, upwd)
        if r == 'fail':
            return render_template('login.html', a="用户名或者密码错误，登录失败")
        else:
            res = make_response(redirect('/list'))
            res.set_cookie('uid', str(r), expires=datetime.datetime.now() + datetime.timedelta(days=7))
            return res


@app.route('/list', methods=['GET', 'POST'])
def list():
    if request.method == 'GET':
        userid = request.cookies.get('uid')
        uname = ormmanage.queryUname(userid)
        ps = ormmanage.obtainProject(userid)
        return render_template('list.html', ps=ps, userinfo=uname)
    elif request.method == 'POST':
        search = request.form['search']
        userid = request.cookies.get('uid')
        uname = ormmanage.queryUname(userid)
        ps = ormmanage.search(search, userid)
        if ps == 'fail':
            userid = request.cookies.get('uid')
            uname = ormmanage.queryUname(userid)
            ps = ormmanage.obtainProject(userid)
            return render_template('list.html', ps=ps, userinfo=uname, content=search)
        elif ps == 'kong':
            userid = request.cookies.get('uid')
            uname = ormmanage.queryUname(userid)
            ps = ormmanage.obtainProject(userid)
            return render_template('list.html', ps=ps, userinfo=uname, tips='！没有找到你所要查找的文章！请换个搜索试试', content=search)
        else:
            return render_template('list.html', sps=ps, userinfo=uname, content=search)


@app.route('/detail/<pid>')
def detail(pid):
    userid = request.cookies.get('uid')
    uname = ormmanage.queryUname(userid)
    p = ormmanage.qureyPdetails(pid)
    return render_template('detail.html', userinfo=uname, nr=p.pdetails, pname=p.pname, p=p)


@app.route('/quit')
def quit():
    res = make_response(redirect('/'))
    res.delete_cookie('uid')
    return res


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        userid = request.cookies.get('uid')
        uname = ormmanage.queryUname(userid)
        return render_template('add.html', userinfo=uname)
    elif request.method == 'POST':
        userid = request.cookies.get('uid')
        uname = ormmanage.queryUname(userid)
        pnam = request.form['pname']
        pdetails = request.form['pdetails']
        r = ormmanage.addProject(pnam, pdetails, userid)
        if r == 'success':
            return render_template('add.html', userinfo=uname, tips='添加成功！')
        else:
            return render_template('add.html', userinfo=uname, tips='添加失败，您可能没有填写项目名称，请仔细检查')


@app.route('/delete/<pid>')
def delete(pid):
    r = ormmanage.delete(pid)
    if r == 'success':
        userid = request.cookies.get('uid')
        uname = ormmanage.queryUname(userid)
        ps = ormmanage.obtainProject(userid)
        return render_template('list.html', ps=ps, userinfo=uname, tips='删除成功！')

    else:
        userid = request.cookies.get('uid')
        uname = ormmanage.queryUname(userid)
        ps = ormmanage.obtainProject(userid)
        return render_template('list.html', ps=ps, userinfo=uname, tips='删除失败！')


@app.route('/modify/<pid>', methods=['GET', 'POST'])
def modify(pid):
    if request.method == 'GET':
        userid = request.cookies.get('uid')
        uname = ormmanage.queryUname(userid)
        p = ormmanage.qureyPdetails(pid)
        return render_template('modify.html', userinfo=uname, p=p)
    elif request.method == 'POST':
        pname = request.form['pname']
        if not pname:
            userid = request.cookies.get('uid')
            uname = ormmanage.queryUname(userid)
            p = ormmanage.qureyPdetails(pid)
            return render_template('modify.html', userinfo=uname, p=p, tips='项目名不能为空！')

        else:
            pdetails = request.form['pdetails']
            r = ormmanage.modify(pid, pname, pdetails)
            if r == 'success':
                userid = request.cookies.get('uid')
                uname = ormmanage.queryUname(userid)
                p = ormmanage.qureyPdetails(pid)
                return render_template('modify.html', userinfo=uname, p=p, tips='修改成功！')
            else:
                userid = request.cookies.get('uid')
                uname = ormmanage.queryUname(userid)
                p = ormmanage.qureyPdetails(pid)
                return render_template('modify.html', userinfo=uname, p=p, tips='修改失败！')


if __name__ == '__main__':
    app.run()
