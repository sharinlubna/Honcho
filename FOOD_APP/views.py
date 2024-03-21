from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required



#send email
def order_email_to_client(email, message1):
    subject = "Order Placed"
    message = message1
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

# Create your views here.
def index(request):
    menu = Food_items.objects.all()

    return render(request,'index.html', locals())
#
# def Notification_count(request):
#
#     return render(request,'user_header.html',locals())


def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def login_page(request):
    return render(request,'login.html')

@login_required
def userhome(request):
    menu = Food_items.objects.all().order_by('-id')
    count = Notification.objects.filter(user=request.user.id, read=False).count()
    return render(request,'user_home.html', locals())

@login_required
def Admin_Dashboard(request):
    from datetime import datetime
    today_date = datetime.now()
    recent = Order.objects.filter(order_date__year=today_date.year,
                                  order_date__month=today_date.month,
                                  order_date__day=today_date.day)
    user_details = User.objects.filter(user_type=3)
    item = Food_items.objects.all()
    orders = Order.objects.all()
    delivery = Order.objects.filter(status=3)
    count = 0
    dcount = 0
    total = 0
    for i in orders:
        count += 1
        if i.status == 3:
            dcount += 1
            total += i.total_price
    n_count = Notification.objects.filter(user=request.user.id, read=False).count()
    return render(request, 'Admin_Dashboard.html', locals())

@login_required
def user_profile(request):
    return render(request, 'user_profile.html')

@login_required
def updateprofile(request):
    uid = request.user.id
    data = User.objects.filter(id=uid)
    count = Notification.objects.filter(user=request.user.id, read=False).count()
    return render(request, 'user_update.html',locals())

@login_required
def OrderDetails(request):
    try:
        user = User.objects.filter(id=request.user.id)
        order = Order.objects.filter(user=request.user.id).order_by('-order_date')
        food = Food_items.objects.all()
        count = Notification.objects.filter(user=request.user, read=False).count()
        order_date_list = []
        total_list = []

        for i in order:
            if i.order_date in order_date_list:
                continue
            else:
                order_date_list.append(i.order_date)
        print(order_date_list)
        #
        # total = 0
        for j in order_date_list:
            total = 0
            for k in order:
                if j == k.order_date:
                    total += k.total_price
            total_list.append(total)
        print(total_list)

        return render(request, 'order-details.html', locals())
    except Order.DoesNotExist:
        return render(request, 'empty-order.html', locals())



# this function is to redirect to the update page

@login_required
def userupdate(request):
    if request.method == 'POST':
        count = Notification.objects.filter(user=request.user, read=False).count()
        first_name = str(request.POST['first_name']).title()
        last_name = str(request.POST['last_name']).title()
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        name = first_name + " " + last_name

        id = request.user.id

        User.objects.filter(id=id).update(first_name=first_name,
                                          last_name=last_name,
                                          email=email,
                                          phone_number=phone_number,
                                          name=name,
                                          username=email)
        return redirect(user_profile)
    else:
        return render(request, 'user_update.html')

def user_signup(request):
    if request.method == 'POST':
        fname = str(request.POST.get('first_name')).title()
        lname = str(request.POST.get('last_name')).title()
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        name = fname + " " + lname
        try:
            User.objects.get(username=email)
            return render(request, 'login.html')
        except User.DoesNotExist:
            user = User.objects.create(name=name,
                                       first_name=fname,
                                       last_name=lname,
                                       email=email,
                                       phone_number=phone_number,
                                       username=email,
                                       is_superuser=0,
                                       is_staff=0,
                                       user_type=3,)
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect(userhome)
    else:
        return render(request, 'login.html')


def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_staff == 1:
                if user.is_superuser == 1:
                    login(request, user)
                    return redirect(Admin_Dashboard)
                else:
                    pass
            else:
                login(request, user)
                return redirect(userhome)
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(index)


# admin operations
@login_required
def All_items(request):
    items = Food_items.objects.all()
    count = Notification.objects.filter(user=request.user.id, read=False).count()

    # burger = Food_items.objects.filter(category="Burger")
    return render(request, 'items.html', locals())

@login_required
def add_item(request):
    count = Notification.objects.filter(user=request.user.id, read=False).count()

    return render(request, 'add_item.html',locals())

# to add items to the table

@login_required
def Added_Items(request):
    if request.method == "POST":
        item_name = request.POST.get('item_name').title()
        item_code = request.POST.get('item_code')
        category = request.POST.get('category')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        try:
            Food_items.objects.get(item_code=item_code)
            return render(request, 'add_item.html', {'error': 'already exist'})
        except Food_items.DoesNotExist:
            item = Food_items.objects.create(item_code=item_code,
                                             item_name=item_name,
                                             category=category,
                                             price=price,
                                             description=description,
                                             image=image)
            item.save()
            return redirect(All_items)
    else:
        return render(request, 'add_item.html')


@login_required
def edit_item(request,id):
    item = Food_items.objects.filter(id=id)
    count = Notification.objects.filter(user=request.user.id, read=False).count()

    return render(request,'edit_item.html', locals())

@login_required
def updated_item(request, id):
    if request.method == "POST":
        item_name = request.POST.get('item_name').title()
        item_code = request.POST.get('item_code')
        category = request.POST.get('category')
        price = request.POST.get('price')
        old_price = request.POST.get('old_price')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        Food_items.objects.filter(id=id).update(item_code=item_code,
                                                item_name=item_name,
                                                category=category,
                                                price=price,
                                                old_price=old_price,
                                                description=description)
        instance = get_object_or_404(Food_items, id=id)
        if image:
            instance.image = image
        instance.save()
        return redirect(All_items)
    else:
        return redirect(edit_item)


@login_required
def delete_item(request,id):
    Food_items.objects.filter(id=id).delete()
    return redirect(All_items)

@login_required
def Order_ds(request):
    new_orders = Order.objects.filter(status=1).order_by('-order_date')
    pending_orders = Order.objects.filter(status=2).order_by('-order_date')
    delivered_orders = Order.objects.filter(status=3).order_by('-order_date')
    cancelled_orders = Order.objects.filter(status=4).order_by('-order_date')
    return render(request, 'order_ds.html', locals())

@login_required
def Accept_item(request,id):

    current_order = Order.objects.get(id=id)
    user = User.objects.get(id=current_order.user_id)
    # for i in current_order:
    #     user_id = i.user_id
    Order.objects.filter(id=id).update(status=2)

    # order = Order.objects.all()
    food = Food_items.objects.all()
    for i in food:
        item = i.item_name
    message1 = 'your order {} is accepted'.format(item)
    Notification.objects.create(user=user,
                                read=False,
                                message=message1)

    return redirect(Order_ds)

@login_required
def Pending_item(request,id):
    Order.objects.filter(id=id).update(status=3)
    current_order = Order.objects.get(id=id)
    user = User.objects.get(id=current_order.user_id)
    food = Food_items.objects.all()
    for i in food:
        item = i.item_name
    message1 = 'your order {} is delivered'.format(item)
    Notification.objects.create(user=user,
                                read=False,
                                message=message1)
    return redirect(Order_ds)

@login_required
def Cancel_item(request,id):
    Order.objects.filter(id=id).update(status=4)
    current_order = Order.objects.get(id=id)
    user = User.objects.get(id=current_order.user_id)
    food = Food_items.objects.all()
    for i in food:
        item = i.item_name
    message1 = 'your order {} is cancelled'.format(item)
    Notification.objects.create(user=user,
                                read=False,
                                message=message1)


    # send email
    userdata = User.objects.filter(id=current_order.user_id)
    for i in userdata:
        email = i.email

    order_email_to_client(email, message1)

    return redirect(Order_ds)

@login_required
def Users_ds(request):
    address = Address.objects.all()
    user = User.objects.filter(user_type=3)
    return render(request, 'users_ds.html', locals())




#user operations
@login_required
def Menu_items(request):
    count = Notification.objects.filter(user=request.user, read=False).count()
    menu = Food_items.objects.all()
    return render(request, 'menu_items.html', locals())

@login_required
def Add_to_Cart(request, id):
    count = Notification.objects.filter(user=request.user, read=False).count()
    cart_item = Cart.objects.filter(item_id=id, user_id=request.user.id)
    food_details = Food_items.objects.filter(id=id)
    # all_food = Food_items.objects.all()

    try:
        Cart.objects.get(item_id=id, user_id=request.user.id)
        for i in cart_item:
            quantity = i.quantity
            # item_id = i.id
        quantity += 1

        for j in food_details:
            price = j.price

        total = price * quantity

        Cart.objects.filter(item_id=id).update(quantity=quantity, item_total=total)
        my_cart = Cart.objects.filter(user_id=request.user.id)
        # finding grand total
        grand_total = 0
        item_count = 0
        for i in my_cart:
            grand_total += i.item_total
            item_count += i.quantity
        # return render(request, 'cart.html', locals())
        return redirect(All_Cart_items)

    except Cart.DoesNotExist:
        for j in food_details:
            price = j.price
        new_cart_item = Cart.objects.create(item_id=id,
                                            user_id=request.user.id,
                                            quantity=1,
                                            item_total=price)
        new_cart_item.save()

        my_cart = Cart.objects.filter(user_id=request.user.id)

        #finding grand total
        grand_total = 0
        item_count = 0
        for i in my_cart:
            grand_total += i.item_total
            item_count += i.quantity
        # return render(request, 'cart.html', locals())
        return redirect(All_Cart_items)

@login_required
def All_Cart_items(request):
    count = Notification.objects.filter(user=request.user, read=False).count()
    my_cart = Cart.objects.filter(user_id=request.user.id)
    if my_cart:
        all_food = Food_items.objects.all()
        # finding grand total
        grand_total = 0
        item_count = 0
        for i in my_cart:
            grand_total += i.item_total
            item_count += i.quantity
        return render(request, 'cart.html', locals())
    else:
        return render(request, 'emptyCart.html')

@login_required
def update_quantity_minus(request):
    if request.method == 'POST':
        id = request.POST.get('item_id')
        price = float(request.POST.get('price'))
        quantity = int(request.POST.get('quantity'))-1
        total = price * quantity
        print(quantity,price,total)
        Cart.objects.filter(item_id=id).update(quantity=quantity, item_total=total)
        return redirect(All_Cart_items)
    else:
        return redirect(All_Cart_items)

@login_required
def update_quantity_plus(request):
    if request.method == 'POST':
        id = request.POST.get('item_id')
        price = float(request.POST.get('price'))
        quantity = int(request.POST.get('quantity'))+1
        total = price * quantity
        print(quantity,price,total)
        Cart.objects.filter(item_id=id).update(quantity=quantity, item_total=total)
        return redirect(All_Cart_items)
    else:
        return redirect(All_Cart_items)

@login_required
def Delete_CartItem(request,id):
    count = Notification.objects.filter(user=request.user, read=False).count()
    my_cart = Cart.objects.filter(user_id=request.user.id)
    if my_cart:
        Cart.objects.filter(id=id).delete()
        return redirect(All_Cart_items)
    else:
        return render(request, 'emptyCart.html')

@login_required
def Add_Address(request,id):
    count = Notification.objects.filter(user=request.user, read=False).count()
    if request.method == 'POST':

        house_no = request.POST.get('house_no')
        land_mark = request.POST.get('land_mark')
        city = request.POST.get('city')
        district = request.POST.get('district')
        pin_code = request.POST.get('pin_code')
        food_details = Food_items.objects.filter(id=id)
        user = request.user
        try:
            Address.objects.get(user_id=user.id)
            data = Address.objects.filter(user_id=request.user.id)
            return render(request, 'order.html', locals())
        except Address.DoesNotExist:
            user_address = Address.objects.create(house_no=house_no,
                                                  user=user,
                                                  email=user.email,
                                                  land_mark=land_mark,
                                                  city=city,
                                                  district=district,
                                                  pin_code=pin_code)
            user_address.save()
            data = Address.objects.filter(user_id=request.user.id)
            food_details = Food_items.objects.filter(id=id)
            return render(request, 'order.html', locals())
    else:
        return render(request, 'order.html')


@login_required
def Update_address(request):
    count = Notification.objects.filter(user=request.user, read=False).count()
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        house_no = request.POST.get('house_no')
        land_mark = request.POST.get('land_mark')
        city = request.POST.get('city')
        district = request.POST.get('district')
        pin_code = request.POST.get('pin_code')
        food_details = Food_items.objects.filter(id=item_id)
        user = request.user
        # Address.objects.get(user=request.user.id)
        Address.objects.update(user=user,
                               house_no=house_no,
                               land_mark=land_mark,
                               city=city,
                               district=district,
                               pin_code=pin_code)
        # update_address.save()
        data = Address.objects.filter(user_id=request.user.id)
        # food_details = Food_items.objects.filter(id=id)
        return render(request, 'order.html', locals())
    else:
        return render(request, 'order.html')


@login_required
def Order_item(request, id):
    count = Notification.objects.filter(user=request.user, read=False).count()
    try:
        Address.objects.get(user_id=request.user.id)
        data = Address.objects.filter(user_id=request.user.id)
        food_details = Food_items.objects.filter(id=id)
        return render(request, 'order.html', locals())
    except Address.DoesNotExist:
        food_details = Food_items.objects.filter(id=id)
        return render(request, 'order.html', locals())


@login_required
def Place_order(request):
    count = Notification.objects.filter(user=request.user.id, read=False).count()
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        item_id = request.POST.get('item_id')
        food_details = Food_items.objects.filter(id=item_id)
        for i in food_details:
            # print(i.item_name)
            price = i.price
        total_price = quantity * float(price)
        # print(total_price)
        user_id = request.user.id
        user_data = User.objects.get(id=user_id)
        import datetime
        x = datetime.datetime.now()

        data = Order.objects.create(quantity=quantity,
                                    item_id=item_id,
                                    user_id=user_id,
                                    order_date=x,
                                    total_price=total_price,
                                    status=1)
        data.save()
        order_details = Order.objects.filter(user_id=user_id, order_date=x)
        address = Address.objects.filter(user_id=user_id)

        # notification generation
        for i in order_details:
            oid = i.id

        message1 = "Your order '#{order_id}' successfully placed".format(order_id=oid)
        Notification.objects.create(user=user_data,
                                    read=False,
                                    message=message1)
        for x in food_details:
            code = x.item_code
        user = User.objects.filter(id=request.user.id)
        admin = User.objects.get(id=13)
        message2 = "You have new order from {} , item {} " .format(request.user.name, code)
        Notification.objects.create(user=admin,
                                    read=False,
                                    message=message2)

        #send email
        for i in user:
            email = i.email

        order_email_to_client(email,message1)

        return render(request, 'invoice.html', locals())
    else:
        return redirect('user_home')



@login_required
def Order_all_item(request):
    count = Notification.objects.filter(user=request.user, read=False).count()
    try:
        user = User.objects.get(id=request.user.id)
        Address.objects.get(user=user)
        data = Address.objects.filter(user_id=request.user.id)
        my_cart = Cart.objects.filter(user=user)
        return render(request, 'order-all.html', locals())
    except Address.DoesNotExist:
        user = User.objects.get(id=request.user.id)
        my_cart = Cart.objects.filter(user=user)
        return render(request, 'order-all.html', locals())


@login_required
def AddAddress(request):
    count = Notification.objects.filter(user=request.user, read=False).count()
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        house_no = request.POST.get('house_no')
        land_mark = request.POST.get('land_mark')
        city = request.POST.get('city')
        district = request.POST.get('district')
        pin_code = request.POST.get('pin_code')
        user = request.user
        try:
            Address.objects.get(user_id=user.id)
            data = Address.objects.filter(user_id=request.user.id)
            return render(request, 'order.html', locals())
        except Address.DoesNotExist:
            user_address = Address.objects.create(house_no=house_no,
                                                  user=user,
                                                  email=user.email,
                                                  land_mark=land_mark,
                                                  city=city,
                                                  district=district,
                                                  pin_code=pin_code)
            user_address.save()
            data = Address.objects.filter(user_id=request.user.id)
            return render(request, 'order-all.html', locals())
    else:
        return render(request, 'order-all.html')


@login_required
def PlaceCartOrder(request):
    count = Notification.objects.filter(user=request.user, read=False).count()
    import datetime
    my_cart = Cart.objects.filter(user=request.user.id)

    user = User.objects.get(id=request.user.id)
    x = datetime.datetime.now()
    from datetime import date

    today = date.today()
    for i in my_cart:
        food = Food_items.objects.get(id=i.item_id)
        new_order = Order.objects.create(item=food,user=user,order_date=x,quantity=i.quantity,total_price=i.item_total,status=1)
        new_order.save()


    # adding notification
    pro_count = Cart.objects.filter(user=request.user.id).count()
    message1 = 'you have ordered {} items'.format(pro_count)
    Notification.objects.create(user=user,
                                read=False,
                                message=message1)

    admin = User.objects.get(id=13)
    message2 = "You have new order from {} , {} items ".format(request.user.name, pro_count)
    Notification.objects.create(user=admin,
                                read=False,
                                message=message2)




    my_order = Order.objects.filter(user=user,order_date=x)

    for i in my_order:
        oid = i.id

    food_details = Food_items.objects.all()
    item_count = 0
    grand_total = 0
    for i in my_cart:
        item_count += i.quantity
        grand_total += i.item_total

    address = Address.objects.filter(user=user)

    Cart.objects.filter(user=user).delete()

    # send email
    userdata = User.objects.filter(id=request.user.id)
    for i in userdata:
        email = i.email

    order_email_to_client(email, message1)

    return render(request, 'invoice-all.html', locals())


@login_required
def User_Notification(request):
    print(request.user)
    count = Notification.objects.filter(user=request.user.id, read=False).count()
    # user = User.objects.get(id=request.user.id)
    notifications = Notification.objects.filter(user=request.user.id).order_by('-datetime')

    # Get the current time
    current_time = datetime.now()

    # Fetch orders for the current user
    orders = Order.objects.filter(user=request.user.id)

    # Calculate time ago for each notification
    for i in notifications:
        current_time = datetime.now()
        time_difference = current_time - i.datetime
        total_seconds = int(time_difference.total_seconds())

        if total_seconds < 60:
            i.time_ago = f"{total_seconds} seconds ago"
        elif total_seconds < 3600:
            i.time_ago = f"{total_seconds // 60} minutes ago"
        elif total_seconds < 86400:  # Less than 24 hours
            i.time_ago = f"{total_seconds // 3600} hours ago"
        elif total_seconds < 172800:  # Less than 48 hours (1 day)
            i.time_ago = "1 day ago"
        elif total_seconds < 604800:  # Less than a week
            i.time_ago = f"{total_seconds // 86400} days ago"
        elif total_seconds < 1209600:  # Less than 2 weeks (1 week)
            i.time_ago = "1 week ago"
        else:
            weeks = total_seconds // 604800
            i.time_ago = f"{weeks} weeks ago"

    for i in notifications:
        i.read = True
        i.save()
    return render(request, 'notification.html', locals())


@login_required
def Admin_Notification(request):
    user = User.objects.get(is_superuser=1)
    print(user.id)
    count = Notification.objects.filter(user=user.id, read=False).count()
    # user = User.objects.get(id=request.user.id)
    notifications = Notification.objects.filter(user=request.user.id).order_by('-datetime')

    # Get the current time
    current_time = datetime.now()

    # Fetch orders for the current user
    # orders = Order.objects.filter(user=user)

    # Calculate time ago for each notification
    for i in notifications:
        current_time = datetime.now()
        time_difference = current_time - i.datetime
        total_seconds = int(time_difference.total_seconds())

        if total_seconds < 60:
            i.time_ago = f"{total_seconds} seconds ago"
        elif total_seconds < 3600:
            i.time_ago = f"{total_seconds // 60} minutes ago"
        elif total_seconds < 86400:  # Less than 24 hours
            i.time_ago = f"{total_seconds // 3600} hours ago"
        elif total_seconds < 172800:  # Less than 48 hours (1 day)
            i.time_ago = "1 day ago"
        elif total_seconds < 604800:  # Less than a week
            i.time_ago = f"{total_seconds // 86400} days ago"
        elif total_seconds < 1209600:  # Less than 2 weeks (1 week)
            i.time_ago = "1 week ago"
        else:
            weeks = total_seconds // 604800
            i.time_ago = f"{weeks} weeks ago"

    # read true

    for i in notifications:
        i.read = True
        i.save()

    return render(request, 'Admin_Notification.html', locals())


