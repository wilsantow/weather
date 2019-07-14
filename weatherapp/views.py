from django.shortcuts import render,redirect
import requests
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=c0f56de0aaca634c7c539ec3631e040b'
    
    err_msg = ''
    message = ''
    message_class = ''
    
    if request.method == 'POST':
        form = CityForm(request.POST)
        
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count=City.objects.filter(name=new_city).count()
            
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                
                if r['cod'] == 200:
                    form.save()
                    
                else:
                    err_msg='City does not exist'
    
             
                
            else:
                err_msg = 'City already exists! '
  
    if err_msg:
        message = err_msg
        message_class = 'is-danger'
    
    else:
        message = 'City added sucessfully'
        message_class = 'is-sucesss '
    
    
    
    
    form=CityForm()


    cities=City.objects.all()
    weather_data =[]
    
    for city in cities:
        
        city_weather = requests.get(url.format(city)).json()
    
    
        weather = {
        'city' : city,
        'temperature' : round((city_weather['main']['temp']-32)*5/9),
        'description' : city_weather['weather'][0]['description'],
        'icon' : city_weather['weather'][0]['icon']
        }
    
        weather_data.append(weather)
        print(weather_data)
    context = {
        'weather_data' : weather_data,
        'form': form,
        'message':message,
        'message_class' : message_class
    }
    return render(request,'weatherapp/index.html',context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete(),
    return redirect('home')


