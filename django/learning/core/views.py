from django.shortcuts import render, HttpResponse

# Create your views here.

def hello(request):
    return HttpResponse('Hello! I am learning Django!')

def add(request, x, y):
    return HttpResponse(f'The sum of {x} and {y} is {x + y}')

def subtract(request, x, y):
    return HttpResponse(f'The difference of {x} and {y} is {x - y}')

def multiply(request, x, y):
    return HttpResponse(f'The product of {x} and {y} is {x * y}')

def divide(request, x, y):
    return HttpResponse(f'The quotient of {x} and {y} is {x / y}')
