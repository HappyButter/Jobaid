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

        encoded_data = prepare_and_encode_record(ml_data_dict, features)

        predicted_salary = int(model.predict(encoded_data))
        thousands = str(predicted_salary // 1000)
        rest = str(predicted_salary % 1000)
        rest = '0' + rest if len(rest) < 3 else rest
        context['display_results'] = True
        context['predicted_salary'] = f'~ {thousands} {rest}  PLN'

    else:
        form = PredictionForm()
        context['form'] = form

    return render(request, "salary_prediction/salary_prediction.html", context)