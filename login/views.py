from django.shortcuts import render
from django.shortcuts import HttpResponse

# Create your views here.

def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        temp = {'user':username, 'pwd':password}
        user_list.append(temp)
    return render(request, 'index.html', {'data':user_list})