from django.shortcuts import render


def salaryprediction(request):
    context = {
        "title": "Salary Prediction"
    }
    return render(request, "salary_prediction/salary_prediction.html", context)
