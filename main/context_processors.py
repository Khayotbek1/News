from .models import Category  
import requests
import datetime

def get_weather(request):
    data = requests.get('https://api.weatherapi.com/v1/current.json?q=Fergana&key=447d854f7833407797592742251604').json()
    context = {
        'temp_c': round(data.get('current').get('temp_c')),
        'condition': data.get('current').get('condition'),
        'localtime': datetime.datetime.today(),
    }
    return context




def categories_processor(request):
    categories = Category.objects.all()
    return {'categories': categories}
