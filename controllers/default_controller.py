import requests

TEXTBOX_SERVER = 'textbox'
TEXTBOX_PORT = 8080
TEXTBOX_ENDPOINT = 'textbox/check'

def analyze_post(body = None):
    # Get the text to analyze
    try:
        text = body['text']
    except:
        return {
            "status" : 400,
            "title" : "Bad Request",
            "detail": "Unable to find \"text\" field to analyze"
        }, 400
    # If is empty, there is nothing to do
    if text == "":
        return {
            "status": 200,
            "sentiment": 0.0
        }, 200
    try:
        #Make the request
        response = requests.post(
            'http://%s:%s/%s' % (TEXTBOX_SERVER, TEXTBOX_PORT, TEXTBOX_ENDPOINT),
            data={'text': text}
        )
        if response.status_code == 200:
            json = response.json()
            # Average all sentences' sentiment
            sentimentList = [ sentence['sentiment'] for sentence in json['sentences'] ]
            sentiment = sum(sentimentList) / float(len(sentimentList))
            # Normalize it to the [ -100 , +100 ] range (textox uses [0,1])
            normalizedSentiment = ( sentiment * 200.0 ) - 100.0
            return {
                "status": 200,
                "sentiment": normalizedSentiment
            }, 200
        else:
            return {
                "status" : response.status_code,
                "title" : "Error while analyzing text with textbox",
                "detail": response.json()
            }, response.status_code
    except:
        return {
            "status" : 500,
            "title" : "Internal server error",
            "detail": "There was an intenal error"
        }, 500
