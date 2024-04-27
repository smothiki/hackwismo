from flask import Flask, request, jsonify

import google.generativeai as genai
import requests
import re
GOOGLE_API_KEY="AIzaSyCrLKL3IQC904qBREL8qMSws-c2pgvaFiY"

genai.configure(api_key=GOOGLE_API_KEY)
app = Flask(__name__)

@app.route('/query', methods=['POST'])
def process_string():
    # Get the input string from the request
    input_string = request.json.get('query')

    orderPrompt='''
    User provides an order ID in a question. Parse the user query and give me the order number in response.
    The order ID is has 13 Digits. If the query has no order ID . Ask user to provide order ID.
    Provide the order ID in the below format. 
    OrderID:<>
    If order ID is not present. Use the below message as response
    Please provide the 13 Digit order ID
    '''
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])

    response = chat.send_message(orderPrompt +'\n'+ input_string)
    if response.text == "Please provide the 13 Digit order ID":
        return response.text
    
    statusPrompt='''given the following JSON response, draft a customer service chat message with "where is my order" details.
    Make it friendly and "hey dude, I'm a surfer bro" because it's a surf board business.
    In the status please inicude the fullfillment status and the shipping company info if you can find.
    If you are not able to find the status information respond saying "we are working on it. Should receive an update in 2-3 buissiness days"
    JSON:
    '''
    orderID = re.search(r'\d+', response.text).group()
    print(orderID)
    url = "https://eac96d-5e.myshopify.com/admin/api/2024-04/orders/"+orderID+".json"

    payload = {}
    headers = {
    'Content-Type': 'application/json',
    'X-Shopify-Access-Token': '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'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    response = chat.send_message(statusPrompt+'\n'+response.text +'\n'+ "I want the status of the order with order ID "+orderID)
    return response.text

if __name__ == '__main__':
    app.run(debug=True, port=7860)