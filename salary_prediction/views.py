from django.shortcuts import render
from .forms import PredictionForm
from job_offers.views import div_technologies


def salaryprediction(request):

    context = {
        "title": "Salary Prediction",
        'app': 'salary_prediction',
        'page':'prediction'
    }

    offers = []

    if request.method == 'POST':
        form = PredictionForm(request.POST)
        context.update(make_dict_from_form(form))
        print('context: ', context) # temporary for debugging
    else:
        form = PredictionForm()
        context['form'] = form

    return render(request, "salary_prediction/salary_prediction.html", context)

def make_dict_from_form(form):
        prediction_input_data = {}
        prediction_input_data['technologies'] = div_technologies(form['technologies'].value())
        prediction_input_data['experience_level'] = form['experience_level'].value()
        prediction_input_data['location'] = form['location'].value()
        return prediction_input_data