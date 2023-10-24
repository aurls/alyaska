from flask import Flask, request, make_response, jsonify

PORT = 9100

app = Flask(__name__)

def createResponse(data):
  response = make_response(data)

  response.headers['X-Frame-Options'] = 'DENY'
  response.headers['X-XSS-Protection'] = '1; mode=block'
  response.headers['X-Content-Type-Options'] = 'nosniff'
  response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
  response.headers['Set-Cookie'] = 'SameSite=Strict; Secure; HttpOnly'
  response.headers['X-Powered-By'] = 'alyaska'
  response.headers['Server'] = 'alyaska'

  return response

@app.route('/api/v1/attrition', methods=['POST'])
def hello():
  try:
    params = request.json.get('params')

    # run model here like getPrediction(params)
    prediction = 666

  except:
    return createResponse(jsonify(status='error'))

  else:
    return createResponse(jsonify(status='success', value=prediction))

app.run(debug=True, port=PORT)
