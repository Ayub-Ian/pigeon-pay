from django.shortcuts import render

def transaction_create(request):
    return render(request, 'transactions/transaction/create.html')
