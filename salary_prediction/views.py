from django.shortcuts import render
from sklearn.ensemble import RandomForestRegressor

from .forms import PredictionForm
from .cleansing import prepare_and_encode_record, initialize_learning
from .utils import make_dict_from_form

model, features = initialize_learning()

def salaryprediction(request):

    context = {
        "title": "Salary Prediction",
        'app': 'salary_prediction',
        'page':'prediction'
    }

    offers = []

    if request.method == 'POST':
        form = PredictionForm(request.POST)
        ml_data_dict = make_dict_from_form(form)

        print('ml data dict: ', ml_data_dict) # temporary for debugging

        encoded_data = prepare_and_encode_record(ml_data_dict, features)
        print('ml data dict Ffsfsdfs:\n', encoded_data)
        predicted_salary = int(model.predict(encoded_data))
        thousands = predicted_salary // 1000
        rest = predicted_salary % 1000
        context['display_results'] = True
        context['predicted_salary'] = f'~ {thousands} {rest}  PLN'

    else:
        form = PredictionForm()
        context['form'] = form

    return render(request, "salary_prediction/salary_prediction.html", context)