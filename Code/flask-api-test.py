from flask import Flask, request, render_template
import time

app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('form.html')


@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    print(processed_text)

    # this is the first time I have used flask so excuse the repeated code

    try:
        int(processed_text)
    except:
        return render_template('errortrap.html')

    if len(processed_text) != 8:
        return render_template('errortrap2.html')

    if processed_text == '22121232':  # put call here
        return render_template('form2.html')

    else:
        return render_template('form3.html')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
