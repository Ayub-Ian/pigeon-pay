from django.shortcuts import render, get_object_or_404, redirect
from .forms import TransactionForm, ProductForm, AcceptanceForm, ProductFileForm, RecepientDetailsForm
from accounts.models import Seller, Buyer, User
from django.contrib.auth.decorators import login_required
from .models import Transaction, TransactionHistory
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from payment.forms import MpesaSTKForm
from .tasks import send_confirmation_email




@login_required
def transaction_list(request):
    buyer_instance = get_object_or_404(Buyer, user_id=request.user.id)
    seller_instance = get_object_or_404(Seller, user_id=request.user.id)
    transactions = Transaction.objects.filter(
        Q(initiator = request.user) |
        Q(seller = seller_instance) | 
        Q(buyer = buyer_instance)
    )
    return render(request, "transactions/list.html", {'transactions': transactions})

@login_required
def transaction_detail(request, id):
    transaction = get_object_or_404(Transaction, id=id)
    product_list = transaction.products.all()
    return render(request, "transactions/transaction/detail.html", {'transaction': transaction, 'product_list':product_list, 'MpesaSTKForm': MpesaSTKForm})


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
        
        if transaction_form.is_valid():
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
            transaction.status = Transaction.ACTION_REQUIRED
            transaction.action_description = "Please review and accept the terms."
            transaction.save()


            if request.POST['submission_type'] == 'file':
                product_file_form = ProductFileForm(request.POST, request.FILES, prefix="product_file")
                product_file = product_file_form.save(commit=False)
                product_file.transaction = transaction
                product_file.save()
            elif request.POST['submission_type'] == 'manual':
                product_form = ProductForm(request.POST, prefix="product")
                product = product_form.save(commit=False)
                product.transaction = transaction
                product.save()


            TransactionHistory.objects.create(
            transaction=transaction,
            user=current_user,
            action_description="Transaction was created by {}: ({})".format(transaction_data['initiator_role'],current_user)
            )
            
            recepient_details_form = RecepientDetailsForm(request.POST, prefix="recepient")
            if recepient_details_form.is_valid():
                recepient_details = recepient_details_form.cleaned_data

            transaction_data = {
                'title' : transaction.title,
                'amount' : transaction.amount,
                'role' : transaction.initiator_role,
                'reference_no': transaction.reference_no,
                'shareable_url': transaction.shareable_url
            }
            send_confirmation_email.delay(transaction=transaction_data,
                                          sender_name=current_user.first_name, 
                                          sender_email=current_user.get_username(),
                                          recepient_mail=recepient_details['email'],
                                          recepient_name=recepient_details['name'] )
            
            return redirect(reverse("transactions:transaction_created", args=[transaction.id]))

    else:
        transaction_form = TransactionForm(prefix="transaction")
        product_form = ProductForm(prefix="product")
        product_file_form = ProductFileForm(prefix="product_file")
        recepient_details_form = RecepientDetailsForm(prefix="recepient")
    
    return render(request, 
                  'transactions/transaction/create.html',
                  {'transaction_form': transaction_form,
                   'product_form':product_form,
                   'product_file_form': product_file_form,
                   'recepient_details_form': recepient_details_form})

@login_required
def transaction_created(request, id):
    transaction = get_object_or_404(Transaction, id= id)
    return render(request, 'transactions/transaction/created.html', {'transaction': transaction})

class TransactionAcceptanceView(LoginRequiredMixin, FormView):
    transaction = None
    form_class = AcceptanceForm

    def form_valid(self, form):
        self.transaction = form.cleaned_data['transaction']

        if form.is_valid():
            if self.transaction.seller == None:
                 # If seller is None, create a Seller instance and associate it with the transaction
                seller_instance, created = Seller.objects.get_or_create(user_id=self.request.user.id)
                self.transaction.seller = seller_instance
            else:
                # If seller is already assigned, assume we are updating the buyer
                buyer_instance, created = Buyer.objects.get_or_create(user_id=self.request.user.id)
                self.transaction.buyer = buyer_instance
        else:
            print(form.errors)


        self.transaction.save()
                
        self.transaction.status = Transaction.ACTION_REQUIRED
        self.transaction.action_description = "Please pay for the for transaction."


        TransactionHistory.objects.create(
            transaction=self.transaction,
            user=self.request.user,
            action_description="Transaction was accepted by: ({})".format(self.request.user)
        )
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('transactions:transaction_detail',
                            args=[self.transaction.id])