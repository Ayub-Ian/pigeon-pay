import uuid


def create_new_ref_number():
    from .models import Transaction
    not_unique = True
    while not_unique:
        unique_ref = uuid.uuid4().hex[:10]
        if not Transaction.objects.filter(reference_no=unique_ref):
            not_unique = False
    return str(unique_ref)

