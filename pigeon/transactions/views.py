from django.shortcuts import render, get_object_or_404, redirect
from .forms import TransactionForm, ProductForm, AcceptanceForm
from accounts.models import Seller, Buyer, User
from django.contrib.auth.decorators import login_required
from .models import Transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.db.models import Q



@login_required
def transaction_list(request):
    current_user = get_object_or_404(User, id=request.user.id)
    transactions = Transaction.objects.filter(initiator = request.user)
    return render(request, "transactions/list.html", {'transactions': transactions})

@login_required
def transaction_detail(request, id):
    transaction = get_object_or_404(Transaction, id=id)
    product_list = transaction.products.all()
    return render(request, "transactions/transaction/detail.html", {'transaction': transaction, 'product_list':product_list})


def transaction_preview(request, id):
    transaction = get_object_or_404(Transaction, id=id)
    product_list = transaction.products.all()
    acceptance_form = AcceptanceForm(initial={'transaction':transaction})

    return render(request, "transactions/transaction/preview.html", {'transaction': transaction, 'product_list':product_list, 'acceptance_form': acceptance_form})

@login_required
def transaction_create(request):
    current_user = get_object_or_404(User, id=request.user.id)
    if request.method == 'POST':
        
        transaction_form = TransactionForm(request.POST, prefix="transaction")
        product_form = ProductForm(request.POST, prefix="product")

        if transaction_form.is_valid() and product_form.is_valid():
            transaction_data = transaction_form.cleaned_data
            # Create the transaction instance first
            transaction = transaction_form.save(commit=False)
            if transaction_data["initiator_role"] == 'buyer':
                # Returns a tuple of (object: object, boolean: created)
                buyer_instance = Buyer.objects.get_or_create(user_id=request.user.id)
                # Access the returned instance object
                transaction.buyer = buyer_instance[0]
                
            else:
                seller_instance = Seller.objects.get_or_create(user_id=request.user.id)
                transaction.seller = seller_instance[0]
            transaction.initiator = current_user
            transaction.save()
            product = product_form.save(commit=False)
            product.transaction = transaction
            product.save()
            print("Transaction has been saved")
            return redirect("dashboard")

    else:
        transaction_form = TransactionForm(prefix="transaction")
        product_form = ProductForm(prefix="product")
    
    return render(request, 
                  'transactions/transaction/create.html',
                  {'transaction_form': transaction_form,
                   'product_form':product_form})


class TransactionAcceptanceView(LoginRequiredMixin, FormView):
    transaction = None
    form_class = AcceptanceForm

    def form_valid(self, form):
        self.transaction = form.cleaned_data['transaction']

        breakpoint()
        if self.transaction.seller == None:
            seller_instance, created = Seller.objects.get_or_create(user_id=self.request.user.id)
            #breakpoint()
            #self.transaction.seller.add(seller_instance[0])
            self.transaction.seller = seller_instance[0]
        else:
            buyer_instance, created = Buyer.objects.get_or_create(user_id=self.request.user.id)
            #self.transaction.buyer.add(buyer_instance[0])
            self.transaction.buyer=buyer_instance
        return super().form_valid(form)
    
    def get_success_url(self):
        return redirect('dashboard')