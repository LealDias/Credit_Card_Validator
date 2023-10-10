from flask import Flask, request, jsonify
import datetime
from flask_cors import CORS  # Import CORS
from flask import Flask, render_template

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS for the entire app

# Define a function to validate the credit card information
def validate_credit_card(card_info):

    count = 0 # Variables to help on decision
    flag = 0
    
    try:
        # Extract card information from the request
        card_number = card_info.get('card_number')
        expiry_month = card_info.get('expiry_month')
        expiry_year = card_info.get('expiry_year')
        cvv = card_info.get('cvv')

        # Check if the expiry date is valid
        current_date = datetime.datetime.now()
        card_expiry_date = datetime.datetime(int(expiry_year), int(expiry_month), 1)
        if card_expiry_date <= current_date:
            count+=1

        # Validate CVV based on card type
        if card_number.startswith("34") or card_number.startswith("37"):
            if len(cvv) != 4:
                count+=1
            flag = 1    

        if flag != 1:
            if len(cvv) != 3:
                count+=1

        card_number = card_number.replace(" ", "")  # Remove spaces
        if not 16 <= len(card_number) <= 19:
            count+=1

        if count >= 1:    
            return {"status": "failure", "message": "Invalid Card"}
        else:
            return {"status": "success", "message": "Valid Card"}


    except Exception as e:
        return {"status": "failure", "message": str(e)}

# Define a route to handle credit card validation requests
@app.route('/validate_credit_card', methods=['POST'])
def validate_credit_card_api():
    try:
        card_info = request.json
        result = validate_credit_card(card_info)
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "failure", "message": str(e)})

# Define a route for the root URL
@app.route('/')
def index():
    # Render an HTML template here or return a simple message
    return render_template('front.html')

if __name__ == '__main__':
    app.run(debug=True)