from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def voucher():
    return render_template('vouchers.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3480)
    print('Server started on port 3480')
