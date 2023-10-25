from flask import Flask, request, make_response, jsonify
import pandas as pd
import catboost
import pickle

PORT = 9100

app = Flask(__name__)

categorical_features = [
    'businesstravel',
    'department',
    'educationfield',
    'gender',
    'jobrole',
    'maritalstatus',
    'overtime'
]

numerical_features = [
    'age',
    'dailyrate',
    'distancefromhome',
    'education',
    'environmentsatisfaction',
    'hourlyrate',
    'jobinvolvement',
    'joblevel',
    'jobsatisfaction',
    'monthlyincome',
    'monthlyrate',
    'numcompaniesworked',
    'percentsalaryhike',
    'performancerating',
    'relationshipsatisfaction',
    'stockoptionlevel',
    'totalworkingyears',
    'trainingtimeslastyear',
    'worklifebalance',
    'yearsatcompany',
    'yearsincurrentrole',
    'yearssincelastpromotion',
    'yearswithcurrmanager'
]

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
    params = {key.lower(): value for key, value in params.items()}
    input_data = pd.DataFrame([params])

    with open('catboost_model.pkl', 'rb') as f:
        loaded_catboost_model = pickle.load(f)

    prediction = round(float(loaded_catboost_model.predict_proba(input_data[numerical_features])[0][0]) * 100, 2)
  except Exception as e:
    print(e)
    return createResponse(jsonify(status='error'))
  else:
    return createResponse(jsonify(status='success', value=prediction))

app.run(debug=True, port=PORT)
