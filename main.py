from flask import *
from flask import request
from flask import render_template
import hashlib

money_list = [135790, [0, hashlib.sha256('asasas'.encode('UTF-8'))], 1111,
              [123456789, hashlib.sha256('asdfghjkl'.encode('UTF-8'))]]
app = Flask(__name__)


@app.route('/')
def main():
    if request.cookies.get('cardno'):
        cardnoo = {
            'card': money_list[money_list.index(int(make_response(request.cookies.get('cardno')))) + 1][0]
        }
    if request.cookies.get('cardno'):
        return render_template('main.html', **cardnoo)
    else:
        return render_template('main.html')


@app.route('/transfer/', methods=['POST', 'GET'])
def transfer():
    global money_list
    if request.method == 'POST':
        pas = request.form.get('passwd')
        pash = hashlib.sha256(pas.encode('UTF-8'))
        card_n = int(request.form.get('card_from'))
        card_t = int(request.form.get('card_to'))
        pos = int(money_list.index(card_n))
        pos2 = int(money_list.index(card_t))
        if money_list[pos + 1][1].hexdigest() == pash.hexdigest():
            money_list[pos + 1][0] -= int(request.form.get('money'))
            money_list[pos2 + 1][0] += int(request.form.get('money'))
            print(money_list)
    return render_template('site.html')


@app.route('/autorise/', methods=['POST1', 'GET'])
def autorise():
    if request.method == 'POST1':
        pas = request.form.get('passwd')
        pash = hashlib.sha256(pas.encode('UTF-8'))
        card_n = request.form.get('card_from')
        pos = int(money_list.index(card_n))
        if money_list[pos + 1][1].hexdigest() == pash.hexdigest():
            resp = make_response(render_template('autorisation.html'))
            resp.set_cookie('cardno', card_n, max_age=60 * 60 * 24 * 90)
    return render_template('autorisation.html')


if __name__ == '__main__':
    app.run()
