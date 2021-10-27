from flask import *
from flask import request
from flask import render_template
from flask import make_response
import hashlib

money_list = [135790, [0, hashlib.sha256('asasas'.encode('UTF-8'))], 1111,
              [123456789, hashlib.sha256('asdfghjkl'.encode('UTF-8'))]]
app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/transfer/', methods=['POST', 'GET'])
def transfer():
    global money_list
    if request.method == 'POST':
        pas = request.form.get('passwd')
        pash = hashlib.sha256(pas.encode('UTF-8'))
        del pas
        card_n = int(request.form.get('card_from'))
        card_t = int(request.form.get('card_to'))
        pos = int(money_list.index(card_n))
        pos2 = int(money_list.index(card_t))
        if money_list[pos + 1][1].hexdigest() == pash.hexdigest():
            money_list[pos + 1][0] -= int(request.form.get('money'))
            money_list[pos2 + 1][0] += int(request.form.get('money'))
            print(money_list)
    return render_template('site.html')


@app.route('/user/')
def autorise2():
    return "У вас {} пуджи.".format(money_list[int(money_list.index(int(request.cookies.get('cardno')))) + 1][0])


@app.route('/user/<int:user_id>/')
def user(user_id):
    if not request.cookies.get('cardno'):
        res = make_response("Перезагрузите сайт, пожалуйста.")
        res.set_cookie('cardno', str(user_id), max_age=60 * 60 * 24 * 365 * 2)
        return res


if __name__ == '__main__':
    app.run()
