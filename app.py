import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from twilio.rest import Client


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')


# Define Verify_otp() function
@app.route('/login' , methods=['POST'])
def verify_otp():
    username = request.form['username']
    password = request.form['password']
    mobile_number = request.form['number']

    if username == 'verify' and password == '12345':   
        account_sid = 'AC7ac4a37b96a739ae964f4a48b5de0ae8'
        auth_token = '9cfc4984079e59eeb75ffe4ce3cbde35'
        client = Client(account_sid, auth_token)

        verification = client.verify \
            .services('ISdd125a4877f3c15a935c3e62d23b56b4') \
            .verifications \
            .create(to=mobile_number, channel='sms')

        print(verification.status)
        return render_template('otp_verify.html')
    else:
        return render_template('user_error.html')



@app.route('/otp', methods=['POST'])
def get_otp():
    print('processing')

    received_otp = request.form['received_otp']
    mobile_number = request.form['number']

    account_sid = 'AC7ac4a37b96a739ae964f4a48b5de0ae8'
    auth_token = '9cfc4984079e59eeb75ffe4ce3cbde35'
    client = Client(account_sid, auth_token)
                                            
    verification_check = client.verify \
        .services('ISdd125a4877f3c15a935c3e62d23b56b4') \
        .verification_checks \
        .create(to=mobile_number, code=received_otp)
    print(verification_check.status)

    if verification_check.status == "pending":
        return render_template('otp_error.html')

    else:
        return redirect("https://project-c272.onrender.com/")


if __name__ == "__main__":
    app.run()

