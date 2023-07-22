import json

from flask import Flask, render_template, request
from flask_cors import CORS
from utils.Accounts_data import GetAccounts,SetAccounts
from utils.get_bililive_api import BiliLive

app = Flask(__name__)
CORS(app)

@app.route('/index')
def index():
    a = GetAccounts()
    return a.rtn_acc()

@app.route('/<path:subpath>', methods=['GET', 'POST'])
def api(subpath):

    if subpath == "up_state":
        b = SetAccounts()
        b.set_state(request.args.get('id'))
        a = GetAccounts()
        return a.rtn_acc()

    if subpath == "ass_info":
        live = BiliLive()
        fans = live.get_fans_sum(**live.conf)
        guard = live.get_guard_sum(**live.conf)
        live.save_guard()
        return {'fans': fans, 'guards': guard}

    if subpath == "edit":
        if request.method == 'GET':
            acc_id = request.args.get('id')
            if id == "null":
                re = {}
            else:
                re = GetAccounts.get_acc_date(acc_id)
            return re
        if request.method == 'POST':
            data = request.get_data().decode('utf-8')
            a = SetAccounts()
            a.up_acc(json.loads(data))
            return {'code': 200}

    if subpath == "del":
        acc_id = request.args.get('id')
        a = SetAccounts()
        a.del_acc(acc_id)
        return {'code': 200}


if __name__ == '__main__':
    app.run()