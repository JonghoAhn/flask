from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'gangwon'
def start_new_game():
    return {
        'wallet': 10000,
        'result': "",
        'in_game': True
    }

game_data = start_new_game()

@app.route('/index', methods=['GET', 'POST'])
def index():
    high_score = session.get('high_score', 0)
    if request.method == 'POST':

        return render_template('index.html', wallet=game_data['wallet'],high_score=high_score)
    return render_template('index.html', wallet=game_data['wallet'], high_score=high_score)

@app.route('/')
def instructions():
    return render_template('instructions.html' )

@app.route('/start_game', methods=['POST'])
def start_game():
    global game_data
    game_data = start_new_game()
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    global game_data
    game_data = start_new_game()
    return redirect(url_for('index'))

@app.route('/dice_result', methods=['POST','GET'])
def play_dice():
    dice_result = random.randint(1, 6)
    betting_money = int(request.form.get('amount2'))
    predict_dice = int(request.form.get('bet2'))
    if dice_result == predict_dice:
        result_dice_game = f'축하합니다! 게임결과 {betting_money*2}원 획득하셨습니다.'
    else:      result_dice_game = '아쉽지만 예측에 실패하셨습니다. 다시 도전해보세요.'
    return render_template('dice_result.html', dice_result=dice_result,result_dice_game=result_dice_game)
@app.route('/dice', methods=['POST','GET'])
def dice_game():
    return render_template('dice_game.html')

@app.route('/play', methods=['POST'])
def play():
    global game_data

    if not game_data['in_game']:
        # 게임 종료 상태에서는 index 페이지로 리다이렉트
        return redirect(url_for('index'))

    card = list(range(1, 14))
    ran_num = random.sample(card, 1)[0]

    if ran_num == 7:
        dealer_result = "S"
    elif ran_num < 7:
        dealer_result = "L"
    else:
        dealer_result = "H"

    betting = request.form.get('bet')
    betting_money = int(request.form.get('amount'))
    print(betting_money, type(betting_money))

    if betting_money > game_data['wallet']:
        result = f"배팅할 수 있는 금액이 부족합니다. 현재 자산: {game_data['wallet']}원"
        return render_template('result.html', result=result, wallet=game_data['wallet'])

    if betting != dealer_result:
        game_data['wallet'] -= betting_money
        result = f"당신은 {betting}에 {str(betting_money)}원을 배팅하셨습니다. \n게임 결과는  {dealer_result} 입니다.\n{betting_money}원이 차감됩니다."
    elif betting == dealer_result:
        game_data['wallet'] -= betting_money
        if betting == "S":
            game_data['wallet'] += betting_money * 13
            result = f"당신은 {betting}에 {str(betting_money)}원을 배팅하셨습니다.\n 게임 결과는  {dealer_result} 입니다.\n{betting_money * 13}을 획득하셨습니다."

        else:
            game_data['wallet'] += betting_money * 2
            result = f"당신은 {betting}에 {str(betting_money)}원을 배팅하셨습니다. \n게임 결과는  {dealer_result} 입니다.\n{int(betting_money) * 2}을 획득하셨습니다."

    if game_data['wallet'] <= 0:
        game_data['result'] = result + " 게임을 종료합니다. 파산입니다."
        game_data['in_game'] = False
        # Reset everything and redirect to the index page
        return render_template('result2.html', result=game_data['result'], wallet=0)

    else:
        game_data['result'] = result
        game_data['in_game'] = True

    if game_data['wallet'] > session.get('high_score', 0):
        session['high_score'] = game_data['wallet']

    return render_template('result.html', result=game_data['result'], wallet=game_data['wallet'])

if __name__ == '__main__':
    app.run(debug=True)
