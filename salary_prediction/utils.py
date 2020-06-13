from common.utils import div_technologies

def make_dict_from_form(form):
    prediction_input_data = {}
    prediction_input_data['technologies'] = div_technologies(form['technologies'].value())
    prediction_input_data['experience'] = form['experience_level'].value()
    prediction_input_data['city'] = form['location'].value().strip().lower()
    prediction_input_data['b2b'] = form['b2b'].value()
    prediction_input_data['uop'] = form['uop'].value()
    return prediction_input_data