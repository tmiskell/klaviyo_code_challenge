def retrieve_list( ):
    from register.models import Address
    recipient_list = Address.objects.all()
    return recipient_list
