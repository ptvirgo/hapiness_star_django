from django.forms import RadioSelect


class StarSelect(RadioSelect):
    input_type = 'radio'
    template_name = 'django/forms/widgets/radio.html'
    option_template_name = 'happiness_star/widgets/star_radio_option.html'
