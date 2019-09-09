from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Stock, Info
from .forms import StockForm, InfoForm
from django.core.mail import send_mail
import random, time
from .functions import *
# Create your views here.


def home(request):
    return render(request, 'home.html')


@login_required
def stocks(request):
    stocks_list = Stock.objects.filter(owner=request.user)
    current_info = safe_get(request, Info)

    arr_in_stocks_list = []
    body = ''

    if current_info is not None:
        for i in stocks_list:
            arr_in_stocks_list.append(list(str(i).split(" ")))

    if request.method == 'POST' and 'run-process' in request.POST:
        for i in arr_in_stocks_list:
            finance_url = BASE_URL + i[0]
            body, passed, current_price = compare_price(finance_url, float(i[1]), current_info.user_agent, body)

            current_stock = Stock.objects.get(owner=request.user, nasdaq_symbol=i[0])
            current_stock.passed = passed
            current_stock.current_price = current_price
            current_stock.save()

            time.sleep(random.randint(1, 3))
        send_mail(
            'Stock Price Report',
            body,
            current_info.gmail_address,
            [request.user.email],
            fail_silently=False,
        )
        return redirect('stocks')

    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            flag = False
            for i in arr_in_stocks_list:
                print(i[0])
                if i[0] == form.cleaned_data['nasdaq_symbol']:
                    flag = True
                    stock = Stock.objects.get(nasdaq_symbol=i[0], owner=request.user)
                    break

            if not flag:
                stock = form.save(commit=False)
                stock.owner = request.user
                finance_url = BASE_URL + stock.nasdaq_symbol

                if current_info is not None:
                    body, passed, current_price = compare_price(finance_url, float(stock.set_price),
                                                                current_info.user_agent, body)
                else:
                    error_message = "You are missing user info"
                    return render(request, 'stocks.html', {'stocks': arr_in_stocks_list, 'form': StockForm,
                                                           'body': body, 'error': error_message})

                stock.current_price = current_price
                stock.passed = passed
                stock.save()
                return redirect('stocks')
            else:
                message = 'Do you want to edit %s? Click on ' %stock.nasdaq_symbol
                return render(request, 'stocks.html', {'stocks': arr_in_stocks_list, 'form': form,
                                                       'body': body,'message': message})

    else:
        form = StockForm()

    return render(request, 'stocks.html', {'stocks': arr_in_stocks_list, 'form': form,
                                           'body': body})

@login_required
def info(request):
    ret_info = Info.objects.filter(owner=request.user)
    ret_list = []
    for i in ret_info:
        ret_list.append(list(str(i).split(" ")))
    current_info = safe_get(request, Info)

    if request.method == 'POST':
        form = InfoForm(request.POST)
        if current_info is None:
            if form.is_valid():
                info = form.save(commit=False)
                info.owner = request.user
                info.save()
                return redirect('info')
        else:
            if form.is_valid():
                ret_info.delete()
                info = form.save(commit=False)
                info.owner = request.user
                info.save()
                return redirect('info')
    else:
        form = InfoForm()
    return render(request, 'info.html', {
         'ret_info': ret_list, 'form': form
    })

@login_required
def update(request):
    stocks_list = Stock.objects.filter(owner=request.user)
    arr_in_stocks_list = []
    for i in stocks_list:
        arr_in_stocks_list.append(list(str(i).split(" ")))
    current_info = safe_get(request, Info)
    body = ''
    if request.method == 'POST' and 'update' in request.POST:
        form = StockForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data['nasdaq_symbol']
            stock = safe_get_nasdaq(request, Stock, search_query)
            if stock is not None:
                stock.delete()
                stock = form.save(commit=False)
                stock.owner = request.user
                finance_url = BASE_URL + stock.nasdaq_symbol

                if current_info is not None:
                    body, passed, current_price = compare_price(finance_url, float(stock.set_price),
                                                                current_info.user_agent, body)
                else:
                    error_message = "You are missing user info"
                    return render(request, 'update.html', {'stocks': arr_in_stocks_list, 'form': StockForm,
                                                           'error': error_message, 'body': body})

                stock.current_price = current_price
                stock.passed = passed
                stock.save()
                return redirect('update')
            else:
                error_message = "Search query not found"
                return render(request, 'update.html', {'stocks': arr_in_stocks_list, 'form': StockForm,
                                                       'error': error_message, 'body': body})

    if request.method == 'POST' and 'delete' in request.POST:
        form = StockForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data['nasdaq_symbol']
            stock = safe_get_nasdaq(request, Stock, search_query)

            if stock is not None:
                stock.delete()
                return render(request, 'update.html', {'stocks': arr_in_stocks_list, 'form': StockForm,
                                                       'message': "Successfully deleted", 'body': body})
            else:
                error_message = "Search query not found"
                return render(request, 'update.html', {'stocks': arr_in_stocks_list, 'form': StockForm,
                                                       'error': error_message, 'body': body})
    else:
        form = StockForm()
    return render(request, 'update.html', {'stocks': arr_in_stocks_list, 'form': form, 'body': body})





