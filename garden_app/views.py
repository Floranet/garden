from django.shortcuts import render, redirect,Http404,HttpResponse,get_object_or_404
from .import models
from django.contrib import messages
from .models import user_reg,Feed_user,prof_reg,Feed_prof,cart,pay,resource,shop,products,Reminder,Checklist,Task,pTask,pReminder
import razorpay
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
from datetime import datetime
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse
from django.core.exceptions import ValidationError

# Create your views here.

def index(request):
    return render(request,'index.html')


def select(request):
    return render(request,'select.html')


#user----------------------------------------------------------------------------------------------

from django.shortcuts import render, redirect
from .models import user_reg  # Import your model

from django.contrib.auth.hashers import check_password

from django.contrib.auth.hashers import check_password

def password_validation(value):
    if len(value) < 8 or not any(char.isdigit() for char in value) or not any(char.isupper() for char in value):
        raise ValidationError('Password must be at least 8 characters long, contain at least one digit, and one uppercase letter.')

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = user_reg.objects.filter(email=email).first()  # Retrieve the user

        if user and check_password(password, user.password):  # Compare using check_password
            request.session['id'] = user.id
            request.session['ema'] = user.email
            
            if user.status == 'approved':
                return redirect('userHome')
            else:
                return render(request, 'login.html', {'error': 'Your account is not yet approved. Please wait until the admin approves your registration.'})
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password.'})

    return render(request, 'login.html')



from django.contrib.auth.hashers import make_password

from django.contrib.auth.hashers import make_password

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import user_reg  # Ensure this model is correctly defined

def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        email = request.POST.get("email")
        phone = request.POST.get("phone") or ''
        password = request.POST.get("password")  # Retrieve password without validators
        confirm_password = request.POST.get("confirm_password")

        # Check if email already exists
        if user_reg.objects.filter(email=email).exists():
            alert_message = "<script>alert('EMAIL ALREADY EXISTS'); window.location.href='/register/';</script>"
            return HttpResponse(alert_message)

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'register.html')

        # Validate password using Django's built-in validation
        try:
            validate_password(password)  
        except ValidationError as e:
            messages.error(request, ' '.join(e.messages))  # Show validation errors
            return render(request, 'register.html')

        # Hash the password before saving
        hashed_password = make_password(password)

        # Create new user entry
        user = user_reg(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password=hashed_password,  # Store hashed password
            address=address,
            status='applied',
        )
        user.save()

        messages.success(request, 'Registration successful! You can now log in.')
        return render(request, 'login.html')

    return render(request, 'register.html')


def userlist(request):
    user = user_reg.objects.all()
    return render(request,'userlist.html',{'user':user})

def delete_user(request,id):
    try:
        user = user_reg.objects.get(id=id)
        user.delete()
        return redirect('userlist')
    except user_reg.DoesNotExist:
       raise Http404('User does not exist')


def userProfile(request):
    email = request.session.get('ema')
    print(email)  # Get the user's email from the session

    # Ensure the user is logged in
    if email:
        try:
            # Fetch user information
            cr = user_reg.objects.get(email=email)
            payments = pay.objects.filter(email=email)
            
            # Fetch cart items for the logged-in user
            cart_items = cart.objects.filter(email=email)  # Assuming the cart model has an email field

            # Prepare user information for rendering
            user_info = {
                'first_name': cr.first_name,
                'last_name': cr.last_name,
                'address': cr.address,
                'phone': cr.phone,
                'email': cr.email,
                'cart_items': cart_items,
                'payments': payments,
                }  # Add cart items to the context
            
            return render(request, 'userProfile.html', user_info)
        except user_reg.DoesNotExist:
            # Handle case where user does not exist
            return render(request, 'userProfile.html', {'error': 'User  not found.'})
    else:
        # Redirect to login or show an error if not logged in
        return render(request, 'login.html', {'error': 'You must be logged in to view your profile.'})


def update_profile(request):
    email=request.session['ema']
    cr =user_reg.objects.get(email=email)
    if cr:
        user_info = {
            'first_name':cr.first_name,
            'last_name':cr.last_name,
            'address':cr.address,
            'phone':cr.phone,
            'email':cr.email,
            'password':cr.password,
            'confirm_password':cr.confirm_password,
        }
        return render(request,'update_profile.html',user_info)
    else:
        return render(request,'update_profile.html')

def proupdate(request):
    email=request.session['ema']
    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')

        data=user_reg.objects.get(email=email)
        data.first_name=first_name
        data.last_name=last_name
        data.address=address
        data.phone=phone
        data.email=email
        data.password=password
        data.confirm_password=confirm_password

        data.save()

        cr =user_reg.objects.get(email=email)
        if cr:
             user_info = {
            'first_name':cr.first_name,
            'last_name':cr.last_name,
            'address':cr.address,
            'phone':cr.phone,
            'email':cr.email,
            'password':cr.password,
            'confirm_password':cr.confirm_password,
        }
        return render(request,'userProfile.html',user_info)
    else:
        return render(request,'update_profile.html')


def userHome(request):
    return render(request,'userHome.html')

def user_logout(request):
     request.session.flush()
     return render(request, 'index.html')

#feedback--------user---------------------------------------------------------------------------------
def feedback_rate(request):
    if request.method == "POST":
        feedback_text = request.POST.get('feedback_text')
        rating = request.POST.get('rating')
        
        if not feedback_text or not rating:
            # Handle missing fields
            alert_message = "<script>alert('Please fill in all required fields.'); window.location.href='/feedback_rate';</script>"
            return HttpResponse(alert_message)
        
        try:
            rating = int(rating)
            if rating not in [1, 2, 3, 4, 5]:
                raise ValueError("Invalid rating value")
        except (ValueError, TypeError):
            # Handle invalid rating
            alert_message = "<script>alert('Invalid rating value. Please select a valid rating.'); window.location.href='/feedback_rate';</script>"
            return HttpResponse(alert_message)

        # Create and save the Feedback instance
        feed_user = Feed_user(
            feedback_text=feedback_text,
            rating=rating
        )
        feed_user.save()

        # Redirect to a success page
        return redirect('feedback_success')
    
    else:
        # Render the feedback form
        return render(request, 'feedback_rate.html')
    
def feedback_success(request):
    return render(request, 'feedback_success.html')

def feedbacklist(request):
    feed = Feed_user.objects.all()
    return render(request,'feedbacklist.html',{'feed':feed})

def delete_feedback(request,id):
    try:
        feed =Feed_user.objects.get(id=id)
        feed.delete()
        return redirect('feedbacklist')
    except Feed_user.DoesNotExist:
       raise Http404('feed does not exist') 

#admin--------------------------------------------------------------------------------------------

def adminlogin(request):
    if request.method=="POST":
       email=request.POST.get('email')
       password=request.POST.get('password')
       b='admin@gmail.com'
       c='admin'
       if email==b:
           if password==c:
               return render(request,'adminhome.html')
    return render(request,'adminlogin.html')

def adminhome(request):
    return render(request,'adminhome.html')

def admin_dash(request):
    return render(request,'admin_dash.html')       
    
#-----Professional--------------------------------------------------------------------------------------------
from django.contrib.auth.hashers import make_password
from django.contrib.auth import password_validation
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import prof_reg

def profreg(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        add = request.POST.get("add")
        em = request.POST.get("em")
        phno = request.POST.get("phno") or ''  # Ensure phone is not None
        passw = request.POST.get("passw",validators=[password_validation])
        confirm_pass = request.POST.get("confirm_pass")

        if prof_reg.objects.filter(em=em).exists():
            alert_message="<script> alert('EMAIL ALREADY EXIST'); window.location.href='/profreg/'; </script>"
            return HttpResponse(alert_message)
        if passw != confirm_pass:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'profreg.html')
        
        try:
            password_validation.validate_password(passw)
        except Exception as e:
            messages.error(request, f'Password validation failed: {e}')
            return render(request, 'profreg.html')

        # Hash the password before saving
        hashed_password = make_password(passw) 

        prof = prof_reg(
            fname=fname,
            lname=lname,
            em=em,
            phno=phno,  # Phone can be empty or a string
            passw=passw,
            confirm_pass=confirm_pass,
            add=add,
            status='applied',
        )
        prof.save()

        messages.success(request, 'Registration successful! You can now log in.')
        return render(request,'proflogin.html')

    return render(request, 'profreg.html')

from django.contrib.auth.hashers import check_password

def proflogin(request):
    if request.method == "POST":
        em = request.POST.get('em')
        passw = request.POST.get('passw')
        pr = prof_reg.objects.filter(em=em).first()  # Get user by email
        
        if pr and check_password(passw, pr.passw):  # Correctly check hashed password
            request.session['id'] = pr.id
            request.session['email'] = pr.em

            if pr.status == 'approved': 
                return redirect('profhome')  # Redirect if approved
            else: 
                return render(request, 'proflogin.html', {'error': 'Your account is not yet approved. Please wait until the admin approves your registration.'})
        else:
            return render(request, 'proflogin.html', {'error': 'Invalid email or password.'})
    
    return render(request, 'proflogin.html')

    

def prolist(request):
    prof = prof_reg.objects.all()
    return render(request,'prolist.html',{'prof':prof})

def delete_prof(request,id):
    try:
        prof = prof_reg.objects.get(id=id)
        prof.delete()
        return redirect('prolist')
    except prof_reg.DoesNotExist:
       raise Http404('This professional does not exist')

def profProfile(request):
    em=request.session['email']
    pr = prof_reg.objects.get(em=em)
    up_vdo = resource.objects.filter(name=pr)  # 'name' it's the ForeignKey field

    if pr:
        prof_info = {
            'fname':pr.fname,
            'lname':pr.lname,
            'add':pr.add,
            'phno':pr.phno,
            'em':pr.em,
            'passw':pr.passw,
            'confirm_pass':pr.confirm_pass,
            'up_vdo':up_vdo,
        }
        return render(request,'profProfile.html',prof_info)
    else:
        return render(request,'profProfile.html')


def update_pro(request):
    em=request.session['email']
    if not em:  
        return redirect('proflogin') 
    
    pr =prof_reg.objects.get(em=em)
    if pr:
        prof_info = {
            'fname':pr.fname,
            'lname':pr.lname,
            'add':pr.add,
            'phno':pr.phno,
            'em':pr.em,
            'passw':pr.passw,
            'confirm_pass':pr.confirm_pass,
        }
        return render(request,'update_pro.html',prof_info)
    else:
        return render(request,'update_pro.html')

from django.contrib.auth.hashers import make_password

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import prof_reg  # Import your professor model

def prfupdate(request):
    if request.method == "POST":
        # Retrieve professor using session email
        email = request.session.get("email")
        if not email:
            messages.error(request, "You must be logged in to update your profile.")
            return redirect("proflogin")

        prof = get_object_or_404(prof_reg, em=email)

        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        address = request.POST.get("address", "").strip()
        phone = request.POST.get("phone", "").strip()
        password = request.POST.get("password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()

        # Validate required fields
        if not all([first_name, last_name, address, phone]):
            messages.error(request, "All fields are required!")
            return redirect("update_pro")

        # Update professor details
        prof.fname = first_name
        prof.lname = last_name
        prof.add = address
        prof.phno = phone

        # Handle password update
        if password:
            if password == confirm_password:
                prof.passw = make_password(password)  # Hash the password
            else:
                messages.error(request, "Passwords do not match!")
                return redirect("update_pro")

        prof.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("profProfile")

    return render(request, "update_pro.html")



def profhome(request):
    return render(request,'profhome.html')

def prof_logout(request):
     request.session.flush()
     return render(request, 'index.html')

#feedback-----
def feedrate(request):
    if request.method == "POST":
        feedback_text = request.POST.get('feedback_text')
        rating = request.POST.get('rating')
        
        if not feedback_text or not rating:
            # Handle missing fields
            alert_message = "<script>alert('Please fill in all required fields.'); window.location.href='/feedrate';</script>"
            return HttpResponse(alert_message)
        
        try:
            rating = int(rating)
            if rating not in [1, 2, 3, 4, 5]:
                raise ValueError("Invalid rating value")
        except (ValueError, TypeError):
            # Handle invalid rating
            alert_message = "<script>alert('Invalid rating value. Please select a valid rating.'); window.location.href='/feedrate';</script>"
            return HttpResponse(alert_message)

        # Create and save the Feedback instance
        feed_prof = Feed_prof(
            feedback_text=feedback_text,
            rating=rating
        )
        feed_prof.save()

        # Redirect to a success page
        return redirect('feedsuc')
    
    else:
        # Render the feedback form
        return render(request, 'feedrate.html')
    
def feedsuc(request):
    return render(request,'feedsuc.html')

def feedlist(request):
    feedb = Feed_prof.objects.all()
    return render(request,'feedlist.html',{'feedb':feedb})

def delete_feed(request,id):
    try:
        feed =Feed_prof.objects.get(id=id)
        feed.delete()
        return redirect('feedlist')
    except Feed_prof.DoesNotExist:
       raise Http404('feed does not exist') 


    
def add_products(request):
    if request.method == "POST":
        img = request.FILES.get("img")
        prod_name = request.POST.get("prod_name")
        prod_type = request.POST.get("prod_type")
        quantity=request.POST.get("quantity")
        price = request.POST.get("price")
        seller_name = request.POST.get("seller_name") or '' 
        seller_phone = request.POST.get("seller_phone")  or ''

        prod = products(
            img=img,
            prod_name=prod_name,
            prod_type=prod_type,
            quantity=quantity,
            price=price, 
            seller_name=seller_name,
            seller_phone=seller_phone,
        )
        prod.save()

        # messages.success(request, 'Product is successfully entered')
        return render(request,'profhome.html')
    return render(request, 'add_products.html')

def product_list(request):
    prod = products.objects.all()
    return render(request,'product_list.html',{'prod':prod})

def delete_prod(request,id):
    try:
        prod = products.objects.get(id=id)
        prod.delete()
        return redirect('product_list')
    
    except products.DoesNotExist:
       raise Http404('This products does not exist')
    
#Shop----------------------

def user_prod(request):
    prod = products.objects.all()
    return render(request,'user_prod.html',{'prod':prod})

def addcart(request,id):
    email=request.session['ema']
    dt=products.objects.get(id=id)
    j=dt.img
    b=dt.prod_name
    c=dt.prod_type
    d=dt.quantity
    e=dt.price
    f=dt.seller_name
    g=dt.seller_phone
    return render(request,"addcart.html",{'j':j,'b':b,'c':c,'d':d,'e':e,'f':f,'g':g,'m':email})



def add_cart(request):
    if request.method == 'POST':
        prod_name = request.POST.get('prod_name')
        prod_type = request.POST.get('prod_type')
        quantity = int(request.POST.get('quantity'))
        price = request.POST.get('price')
        seller_name = request.POST.get('seller_name')
        seller_phone = request.POST.get('seller_phone')

        data = products.objects.get(prod_name=prod_name)
        a = data.quantity
        b = int(a)
        newquantity = int(b - quantity)

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        cr = user_reg.objects.get(email=email)
        cr.first_name = first_name
        cr.last_name = last_name
        cr.phone = phone
        cr.email = email

        if newquantity < 0:
            return render(request, 'error.html')
        else:
            data.quantity = newquantity
            data.save()

        # Save new Cart instance
        cart(prod_name=prod_name, prod_type=prod_type, quantity=quantity, price=price, 
             seller_name=seller_name, seller_phone=seller_phone, first_name=first_name, 
             phone=phone, email=email).save()

        return render(request, 'userHome.html', {'products': products.objects.all()})


    else:
        return render(request, 'addcart.html')

    
def cart_list(request):
    cr = cart.objects.all()
    return render(request,'cart_list.html',{'cr':cr})

def cartlist(request):
    email = request.session.get('ema') 
    if not email:
        return redirect('login')  

    prod = cart.objects.filter(email=email)  # Use filter instead of all()
    return render(request, 'cartlist.html', {'prod': prod})


def delete_cart(request,id):
    try:
        prod =cart.objects.get(id=id)
        prod.delete()
        return redirect('cartlist')
    except cart.DoesNotExist:
       raise Http404('Product does not exist')


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import cart  # Ensure the models are imported correctly



def delete_cart(request, cart_id):
    if request.method == 'POST':
        # Print debugging information (Ensure cart_id is converted to a string)
        print("Deleting cart item with ID: " + str(cart_id))
        
        # Retrieve the cart item
        sr = get_object_or_404(cart, id=cart_id)
        
        # Retrieve the related product
        try:
            product = products.objects.get(prod_name=sr.prod_name)
            print("Restoring quantity for product: " + str(product.prod_name))  # Example debug
            product.quantity += sr.quantity  # Restore the quantity
            product.save()
        except products.DoesNotExist:
            messages.error(request, "Product not found to restore quantity.")
        
        # Delete the cart item
        sr.delete()
        messages.success(request, 'Product has been deleted from the cart.')
        
        # Redirect to the appropriate page
        return redirect('userHome')

    # Handle GET requests (if accessed by mistake)
    
    return render(request,'cartlist.html')



#user/prof status-------------------------------------------------------------------

def update_status(request):
    if request.method=="POST":
        email=request.POST.get('email')
        status=request.POST.get('status')
        if not email or not status:
            return redirect('userlist')
        if status not in['applied','approved','rejected']:
            return redirect('userlist')
        constr=get_object_or_404(user_reg,email=email)
        constr.status=status
        constr.save()
        return redirect('userlist')
    
def up_status(request):
    if request.method=="POST":
        em=request.POST.get('em')
        status=request.POST.get('status')
        if not em or not status:
            return redirect('prolist')
        if status not in['applied','approved','rejected']:
            return redirect('prolist')
        constr=get_object_or_404(prof_reg,em=em)
        constr.status=status
        constr.save()
        return redirect('prolist')
    
#- payment------------------------------------------------------------------------------------------

def payment(request):
    email = request.session['ema']
    cr = cart.objects.filter(email=email)
    totalprice = 0

    for i in cr:
        # Multiply the price by the slot
        calculated_price = int(i.price) * int(i.quantity)

        # Save the payment information with the calculated price
        pay(
            prod_name=i.prod_name,
            phone=i.phone,
            price=calculated_price,  # Use calculated price here
            email=i.email,
            quantity=i.quantity
        ).save()
        try:

            loo=i.prod_name
        

            send_mail(
                    subject='FloraNet - Receipt',
                    message=(
                        f'Dear {email},\n\n'
                        f"You have purchased {loo}.\n"
                        f'Here\'s your purchased product details.\n'
                        f"Total Price: ${calculated_price}\n"
                    
                        f'Regards,\nFloraNet'
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                
                )
        except Exception as e:
            print(e)

        # Accumulate the total price
        totalprice += calculated_price

        # Delete the booking entry after processing
        i.delete()

    # Convert the total price for payment processing (e.g., Razorpay expects amount in paise)
    totalprice = int(totalprice * 100)  # Convert to paise (100 paise = 1 INR)
    amount = totalprice

    print('Total amount is', str(amount))
    currency = 'INR'

    # Create a Razorpay order
    razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='0'))

    # Extract Razorpay order ID for the new payment
    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler/'

    # Pass necessary details to the template for Razorpay payment integration
    context = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,
        'currency': currency,
        'callback_url': callback_url
    }

    return render(request, 'payment.html', context=context)


@csrf_exempt
def paymenthandler(request):

    if request.method=="POST":
        try:
            payment_id= request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id','')
            signature = request.POST.get('razorpay_signature','')
            params_dict = {
                'razorpay_order_id':razorpay_order_id,
                'razorpay_payment':payment_id,
                'razorpay_signature':signature
            }
            result=razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount=20000
                try:
                    razorpay_client.payment.capture(payment_id,amount)

                    return render(request, 'payment_success.html')
                except:

                    return render(request, 'payment_failed.html')
            else:

                return render(request, 'payment_failed.html')
        except Exception as e:

            return render(request,'userHome.html')
        
    else:
        return render(request,'userHome.html')
    
def paymentlist(request):
    payment = pay.objects.all()
    return render(request,'paymentlist.html',{'payment':payment})

#-Resources------------------------------------------------------------------------------------------------------
from django.shortcuts import render, redirect
from .models import resource
from .models import prof_reg

def vdo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        em = request.session.get('email')  # Get the session email
        
        # Try to get the user instance by email (use filter or try-except for error handling)
        try:
            user = prof_reg.objects.get(em=em)  # Get the user instance by email
        except prof_reg.DoesNotExist:
            # Handle the case where the user does not exist, e.g., show an error message
            return redirect('error_page')  # Redirect to an error page or show an error message
        
        # Get the files uploaded (video or image)
        video_file = request.FILES.get('video_file')
        image_file = request.FILES.get('image_file')

        if title and (video_file or image_file) and description and user:
            # If a video is uploaded
            if video_file:
                res = resource(
                    title=title,
                    video_file=video_file,
                    description=description,
                    name=user
                )
            # If an image is uploaded
            elif image_file:
                res = resource(
                    title=title,
                    image_file=image_file,
                    description=description,
                    name=user
                )
            res.save()
            return redirect('profhome')  # Redirect to the profile or home page after saving

    return render(request, 'vdo.html')




def edu(request):
    resources = resource.objects.all()  # Fetch all resources (video, article, note, image)
    
    # Check if the user is a professor
    is_professor = False
    if request.session.get('em'):  # Assuming the email is saved in the session
        try:
            user = prof_reg.objects.get(em=request.session['em'])
            is_professor = True
        except prof_reg.DoesNotExist:
            pass  # Not a professor

    context = {
        'resources': resources,
        'is_professor': is_professor  # Pass the role status to the template
    }
    
    return render(request, 'edu.html', context)

def resource_detail(request, resource_id):
    try:
        resource_item = resource.objects.get(id=resource_id)  # Fetch the video resource by id
    except resource.DoesNotExist:
        return render(request, '404.html')  # If not found, return a 404 page
    
    return render(request, 'resource_detail.html', {'resource': resource_item})

def resource_list(request):
    res = resource.objects.all()
    return render(request, 'resource_list.html', {'res': res})


from django.http import JsonResponse

def get_resources(request):
    resources = [
        {
            "title": "Learn Figma - UI/UX Design Essentials",
            "image_url": "https://via.placeholder.com/300",
            "lessons": 6,
            "duration": "36m 56s",
            "level": "Beginner",
            "rating": "5.0",
            "price": 79
        },
        {
            "title": "Complete Python Bootcamp",
            "image_url": "https://via.placeholder.com/300",
            "lessons": 6,
            "duration": "36m 56s",
            "level": "Beginner",
            "rating": "5.0",
            "price": 79
        }
    ]
    return JsonResponse(resources, safe=False)


def delete_res(request,title):
    try:
        res = resource.objects.get(title=title)
        res.delete()
        return redirect('resource_list')
    
    except resource.DoesNotExist:
       raise Http404('This data does not exist')
    
  # SHOP LIST----------------------------------------------  
def addshop(request):
        if 'email' in request.session:
            semail=request.session['email']
            prof=prof_reg.objects.get(em=semail)
            if request.method=="POST":
                name = request.POST.get("name")
                shopid =request.POST.get("shopid")
                img = request.FILES.get("img")
                phone=request.POST.get('phone')
                description = request.POST.get('description')
                email = request.POST.get('email')
                category =request.POST.get('category')
                location =request.POST.get('location')
                if shop.objects.filter(shopid=shopid).exists():
                    alert_message="<script>alert('ALREADY EXIST'); window.location.href='/addshop/';</script>"
                    return HttpResponse(alert_message)
                else:
                    shop(name=name,shopid=shopid,img=img,phone=phone,description=description,email=email,category=category,location=location,professional=prof).save()
                    return redirect('profhome')
            else:
                return render(request,'addshop.html')
        else:
            alert_message="<script>alert('LOGIN FAILED'); window.location.href='/proflogin/';</script>"
            return HttpResponse(alert_message)
        
def shoplist(request):
    if 'email' in request.session:
        semail=request.session['email']
        prof=prof_reg.objects.get(em=semail)
        shops=shop.objects.filter(professional=prof)
        return render(request,'shoplist.html',{'shops':shops})
    else:
        alert_message="<script>alert('LOGIN FAILED'); window.location.href='/proflogin/';</script>"
        return HttpResponse(alert_message)


def deleteshop(request,sid):
    if 'email' in request.session:
        shops=shop.objects.filter(id=sid)
        shops.delete()
        return redirect('shoplist')
    
def edit_shop(request, sid):
    shop_instance = shop.objects.get(id=sid)
    
    if request.method == "POST":
        shop_instance.name = request.POST.get("name")
        shop_instance.shopid = request.POST.get("shopid")
        shop_instance.description = request.POST.get("description")
        shop_instance.location = request.POST.get("location")
        shop_instance.category = request.POST.get("category")

        if 'img' in request.FILES:
            shop_instance.img = request.FILES['img']  # Update image only if a new one is uploaded

        shop_instance.save()  # Save the updated shop details
        messages.success(request, "Shop updated successfully!")  
        return redirect('shoplist')  # Redirect to the shop list page after saving

    shop_info = {
        'name': shop_instance.name,
        'shopid': shop_instance.shopid,
        'description': shop_instance.description,
        'location': shop_instance.location,
        'category': shop_instance.category,
    }

    return render(request, 'edit_shop.html', shop_info)

    

def user_shoplist(request):
    category = request.GET.get('category', '')
    location = request.GET.get('location', '')

    shops = shop.objects.all()

    if category:
        shops = shops.filter(category=category)
    if location:
        shops = shops.filter(location__icontains=location)

    return render(request, 'user_shoplist.html', {'shops': shops})


def ashoplist(request):
    shops = shop.objects.all()
    return render(request, 'ashoplist.html', {'shops': shops})

from django.shortcuts import render, redirect, get_object_or_404
from .models import user_reg, Reminder, Checklist
from django.contrib import messages

def tools(request):
    # email = request.session.get('email')
    # if not email:
    #     return redirect('login')

    # user = user_reg.objects.get(email=email)
    # categories = Category.objects.filter(user=user)  # Fetch all categories for the logged-in user

    return render(request, 'tools.html')
    # , {
    #     'categories': categories,  # Pass the categories to the template
    # })




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import user_reg,Checklist, Reminder
from datetime import date

def dashboard_view(request):
    email = request.session.get('email')
    if not email:
        return redirect('login')

    user = user_reg.objects.get(email=email)

  

# Payment Receipt---------------------------------------------------------------------------------

from django.shortcuts import render
from .models import pay

def payment_details(request):
    # Get the email from the request
    if 'email'  in request.session:
        email = request.session['email']
    
    # Filter the pay model by the provided email
    payments = pay.objects.filter(email=email) if email else None

    # Render the results to a template
    return render(request, 'paymentt.html', {'payments': payments, 'email': email})


from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import pay

def download_payment_pdf(request, payment_id):
    # Get the payment record
    try:
        payment = pay.objects.get(id=payment_id)
    except pay.DoesNotExist:
        return HttpResponse("Payment record not found.", status=404)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="payment_{payment.id}.pdf"'

    # Generate the PDF
    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica", 12)


    p.drawString(100, 740, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    p.drawString(400, 740, f"Receipt No: {payment.id}")

    # Itemized Details
    p.drawString(100, 710, "Product Details")
    p.line(100, 705, 500, 705)

    p.drawString(100, 685, f"Product: {payment.prod_name}")
    p.drawString(100, 665, f"Quantity: {payment.quantity}")
    p.drawString(100, 645, f"Unit Price: ${payment.price:.2f}")

    # Total Calculation
    total_price = payment.quantity * payment.price
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, 625, f"Total: ${total_price:.2f}")

    # Customer Info
    p.setFont("Helvetica", 12)
    p.drawString(100, 600, "Customer Details")
    p.line(100, 595, 500, 595)

    p.drawString(100, 575, f"Phone: {payment.phone}")
    p.drawString(100, 555, f"Email: {payment.email}")

    # Footer
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, 520, "Thank you for your purchase!")
    
    # Finalize the PDF
    p.showPage()
    p.save()

    return response



## management-----------------------------------------------------------------------------------------------------------


import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import Task
from .models import user_reg

def add_task(request):
    if request.method == 'POST':
        email = request.session.get('ema')
        print(email)
        if email:
        
            data = json.loads(request.body)
            task_title = data.get('task_title')
            print(task_title)
            task_status = data.get('task_status')
            print(task_status)
            
            user = user_reg.objects.get(email=email)
            print(user)
        
            try:
            # Create a new task and save it to the database
                task = Task(title=task_title, status=task_status, user=user)
                task.save()
                return JsonResponse({'status': 'success', 'message': 'Task added successfully!'})
            except Exception as e:
                print(e)

                return JsonResponse({'status': 'error', 'message': 'Task title is required!'})
        else:
            data = json.loads(request.body)
            task_title = data.get('task_title')
            task_status = data.get('task_status')
            email = request.session.get('email')
            print("email",email)
            user = prof_reg.objects.get(em =email)
        
            if task_title:
            # Create a new task and save it to the database
                taskd = pTask(title=task_title, status=task_status, user=user)
                taskd.save()
                return JsonResponse({'status': 'success', 'message': 'Task added successfully!'})

            return JsonResponse({'status': 'error', 'message': 'Task title is required!'})
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request method!'})

def delete_task(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        task_title = data.get('task_title')
        email = request.session.get('email')
        user = user_reg.objects.get(email=email)

        if task_title:
            try:
                # Find the task by title and delete it
                task = Task.objects.get(title=task_title, user=user)
                task.delete()
                return JsonResponse({'status': 'success', 'message': 'Task deleted successfully!'})
            except Task.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Task not found!'})

        return JsonResponse({'status': 'error', 'message': 'Task title is required!'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method!'})


# # calendar--------------------------------------------------------------------------------

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import user_reg , prof_reg

from django.shortcuts import render, redirect
from .models import user_reg, prof_reg, Reminder, pReminder

from django.shortcuts import render, redirect
from .models import user_reg, prof_reg, Reminder, pReminder

def calendar(request):
    # Check session for the correct email depending on user type
    prof_email = request.session.get('email')  # Email for professor
    user_email = request.session.get('ema')  # Email for customer

    if not prof_email and not user_email:
        return redirect('login')  # If neither email is in session, redirect to login

    ur = None
    reminders = []

    # Check if the logged-in user is a customer (user_reg) or a professional (prof_reg)
    if user_email:
        try:
            # User is a customer
            ur = user_reg.objects.get(email=user_email)
            reminders = Reminder.objects.filter(user=ur)  # Fetch customer reminders
        except user_reg.DoesNotExist:
            return redirect('login')  # If customer not found, redirect to login

    elif prof_email:
        try:
            # User is a professor
            ur = prof_reg.objects.get(em=prof_email)
            reminders = pReminder.objects.filter(user=ur)  # Fetch professional reminders
        except prof_reg.DoesNotExist:
            return redirect('login')  # If professor not found, redirect to login

    # Handle POST request for adding a reminder
    if request.method == 'POST':
        title = request.POST.get('title')
        date = request.POST.get('date')
        time = request.POST.get('time')
        venue = request.POST.get('venue')
        reminder_text = request.POST.get('reminder_text')

        if title and date:
            task_status = request.POST.get('task_status', 'False') == 'True'

            # Save reminder based on user type
            if isinstance(ur, user_reg):
                reminder = Reminder(
                    title=title,
                    date=date,
                    time=time,
                    reminder_text=reminder_text,
                    user=ur,
                    venue=venue,
                    task_status=task_status,
                )
                reminder.save()
            else:
                reminder = pReminder(
                    title=title,
                    date=date,
                    time=time,
                    reminder_text=reminder_text,
                    user=ur,
                    venue=venue,
                    task_status=task_status,
                )
                reminder.save()

            return redirect('tools')  # ✅ Correct, using the URL name

    return render(request, 'tools.html', {'reminders': reminders})


# def callist(request):
#     ur = user_reg.objects.get(email=email)
#     reminders = Reminder.objects.filter(user=ur)
#     cal = Reminder.objects.all()
#     return render(request,'callist.html',{'cal':cal})


# def callist(request):
#     if 'email'  in request.session:
#         email = request.session['email']
#         if user_reg.objects.filter(email=email).exists():
#             ur = user_reg.objects.get(email=email)
#             reminders = Reminder.objects.filter(user=ur)  # Private reminders for the customer
#         else:
#             ur = prof_reg.objects.get(em=email)
#             reminders = pReminder.objects.all()  # Public reminders for the professor
    
#     return render(request, 'tools.html', {'reminders': reminders})



def delete_reminder(request, id):
    try:
        # Try to delete the customer's reminder
        cal = Reminder.objects.get(id=id)
        cal.delete()
    except Reminder.DoesNotExist:
        try:
            # If it's not a customer's reminder, try deleting a professional's reminder
            cal = pReminder.objects.get(id=id)
            cal.delete()
        except pReminder.DoesNotExist:
            raise Http404('Reminder does not exist')

    return redirect('calendar')  # Redirect to calendar after deleting


from django.shortcuts import render
from django.utils.timezone import now
from django.core.mail import send_mail
from .models import Reminder, user_reg,Task  # Import user_reg
import threading

def send_email_reminder(reminder):
    """ Function to send reminder emails asynchronously """
    if reminder.user and reminder.user.email:  # Ensure user has an email
        subject = f"Reminder: {reminder.title}"
        message = f"Reminder Details:\n{reminder.reminder_text}"
        recipient = [reminder.user.email]

        def send_email():
            send_mail(subject, message, 'nefsal003@gmail.com', recipient)

        # Run email sending in a separate thread
        email_thread = threading.Thread(target=send_email)
        email_thread.start()

def check_reminders(request):
    """ View to check reminders and send emails """

    # Fetch logged-in user from session
    email = request.session.get('email')
    
    if email:
        try:
            user = user_reg.objects.get(email=email)  # Get user from DB
        except user_reg.DoesNotExist:
            return render(request, 'reminders.html', {'error': 'User not found'})

        # Check reminders for the logged-in user
        current_time = now().time()
        current_date = now().date()

        reminders = Reminder.objects.filter(user=user, date=current_date, time__lte=current_time, task_status=False)

        for reminder in reminders:
            send_email_reminder(reminder)  # Call email function
            reminder.task_status = True  # Mark as done
            reminder.save()

    return render(request, 'reminders.html', {'reminders': reminders})


# def task_list(request):
#     cr = Task.objects.all()
#     return render(request,'task_list.html',{'cr':cr})

from django.shortcuts import render
from .models import Task, pTask, user_reg, prof_reg

def tasklist(request):
    sender_email = request.session.get('email') or request.session.get('ema')  # Retrieve email from session
    tasks = []  # Default empty list

    try:
        if user_reg.objects.filter(email=sender_email).exists():
            user = user_reg.objects.get(email=sender_email)
            tasks = Task.objects.filter(user=user)  # Fetch tasks for user_reg

        elif prof_reg.objects.filter(em=sender_email).exists():
            user = prof_reg.objects.get(em=sender_email)
            tasks = pTask.objects.filter(user=user)  # Fetch tasks for prof_reg

    except Exception as e:
        print("Error:", e)

    return render(request, 'tasklist.html', {'tk': tasks})



from django.shortcuts import get_object_or_404, redirect
from .models import Task, pTask

def complete_task(request, task_id):
    try:
        # Try fetching from Task model (for user_reg)
        task = get_object_or_404(Task, id=task_id)
    except:
        # If not found in Task, try fetching from pTask model (for prof_reg)
        task = get_object_or_404(pTask, id=task_id)

    # Mark task as completed
    task.status = True
    task.save()

    return redirect('tasklist')  # Redirect back to the task list



from django.http import JsonResponse
from .models import Reminder

def get_events(request):
    try:
        events = Reminder.objects.all()
        event_list = []

        for event in events:
            event_list.append({
                'title': event.title,
                'start': event.date.strftime('%Y-%m-%d'),  # Ensure date is in 'YYYY-MM-DD' format
                'description': event.reminder_text,
                'venue':event.venue,
                'timeRange': event.time.strftime('%H:%M'),  # Include the time if needed
                
            })

        return JsonResponse(event_list, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    


from django.shortcuts import render
from .models import Reminder
from django.contrib.auth.decorators import login_required

def calendernew(request):
    # Get session variables: 'ema' for customer and 'email' for professor.
    prof_email = request.session.get('email')  # For professor
    user_email = request.session.get('ema')    # For customer

    if not prof_email and not user_email:
        return redirect('login')  # Redirect to login page if no user session.

    reminders_data = []

    if user_email:
        # Logged in as a customer:
        try:
            user = user_reg.objects.get(email=user_email)
        except user_reg.DoesNotExist:
            return redirect('login')

        # Fetch the customer's reminders from the 'Reminder' model
        user_reminders = Reminder.objects.filter(user=user)
        
        # Also fetch *all* professor reminders from the 'pReminder' model
        prof_reminders = pReminder.objects.all()

        # Log the query results for debugging
        print("User Reminders:", user_reminders)
        print("Professor Reminders:", prof_reminders)

        # Format customer reminders
        reminders_data = [
            {
                "id": r.id,
                "title": r.title,
                "description": r.reminder_text,
                "date": r.date.strftime("%Y-%m-%d"),
                "time": r.time.strftime("%H:%M"),
                "venue": r.venue,
                "status": r.task_status,
            }
            for r in user_reminders
        ]
        
        # Append all professor reminders
        reminders_data.extend([
            {
                "id": r.id,
                "title": r.title,
                "description": r.reminder_text,
                "date": r.date.strftime("%Y-%m-%d"),
                "time": r.time.strftime("%H:%M"),
                "venue": r.venue,
                "status": r.task_status,
            }
            for r in prof_reminders
        ])

    elif prof_email:
        # Logged in as a professor:
        try:
            user = prof_reg.objects.get(em=prof_email)
        except prof_reg.DoesNotExist:
            return redirect('login')

        # Fetch only this professor's reminders from 'pReminder' model
        reminders = pReminder.objects.filter(user=user)

        # Log the query result for debugging
        print("Professor Reminders:", reminders)

        reminders_data = [
            {
                "id": r.id,
                "title": r.title,
                "description": r.reminder_text,
                "date": r.date.strftime("%Y-%m-%d"),
                "time": r.time.strftime("%H:%M"),
                "venue": r.venue,
                "status": r.task_status,
            }
            for r in reminders
        ]

    # Render the reminders in the template
    return render(request, 'calendernew.html', {'reminders': reminders_data})


from django.shortcuts import render, redirect
from .models import  ChatMessage
from django.contrib.auth.decorators import login_required  

# List Artists and Buyers
def chat_list(request):
    artists = user_reg.objects.all()
    buyers = prof_reg.objects.all()
    return render(request, 'chat_list.html', {'artists': artists, 'buyers': buyers})

from django.shortcuts import render, redirect, get_object_or_404
from .models import  ChatMessage

from django.shortcuts import render, redirect, get_object_or_404
from .models import ChatMessage, user_reg, prof_reg
from django.contrib.auth.decorators import login_required

def chat_detail(request, user_type, username):
    sender_email = request.session.get('email') or request.session.get('ema')
    print(sender_email)

    sender = None
    receiver = None
    messages = []

    try:
        # Determine sender type and use the correct field
        if user_reg.objects.filter(email=sender_email).exists():
            sender = user_reg.objects.get(email=sender_email)
            sender_name = sender.first_name  # user_reg uses 'first_name'
        elif prof_reg.objects.filter(em=sender_email).exists():
            sender = prof_reg.objects.get(em=sender_email)
            sender_name = sender.fname  # prof_reg uses 'fname'
        else:
            return redirect('login')
        

        # Determine receiver and use correct field
        if user_type == 'artist':
            receiver = get_object_or_404(user_reg, first_name=username)
            receiver_name = receiver.first_name
        else:
            receiver = get_object_or_404(prof_reg, fname=username)
            receiver_name = receiver.fname

        # Fetch chat messages
        messages = ChatMessage.objects.filter(
            sender__in=[sender_name, receiver_name],
            receiver__in=[sender_name, receiver_name]
        ).order_by('timestamp')

    except Exception as e:
        print("Error:", e)

    print("Receiver:", receiver)

    # Handle sending a message
    if request.method == 'POST':
        content = request.POST.get('content')
        media = request.FILES.get('media')

        if content.strip() or media:
            ChatMessage.objects.create(
                sender=sender_name,  # Use the correct name field
                receiver=receiver_name,
                content=content,
                media=media if media else None
            )

        return redirect('chat_detail', user_type=user_type, username=username)

    # Process media types for display
    for message in messages:
        if message.media:
            if message.media.name.endswith(('.jpg', '.jpeg', '.png')):
                message.media_type = 'image'
            elif message.media.name.endswith(('.mp4', '.avi', '.mov')):
                message.media_type = 'video'
            else:
                message.media_type = 'unknown'

    return render(request, 'chat_detail.html', {
        'receiver': receiver,
        'messages': messages,
        'sender': sender
    })

    
def logout(request):
    request.session.flush()  # Clear the session
    return redirect('index') 


# Community------------------------------------------------------------------------------

def community(request):
    return render(request, 'community.html')
    
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.contrib.contenttypes.models import ContentType
from .models import Photo, Like, Comment, Share, PhotoView, user_reg, prof_reg

from django.core.exceptions import ObjectDoesNotExist

from django.core.exceptions import ObjectDoesNotExist

def get_user_from_session(request):
    if 'ema' in request.session:
        try:
            # Try to fetch the user_reg first
            farmer_user = user_reg.objects.get(email=request.session['ema'])
            return farmer_user, 'farmer'
        except ObjectDoesNotExist:
            pass  # If user is not found, move to the next check

    if 'email' in request.session:
            try:
                # Try fetching a buyer
                buyer_user = prof_reg.objects.get(em=request.session['email'])
                return buyer_user, 'buyer'
            except ObjectDoesNotExist:
                pass  # If buyer is not found, return None at the end

    return None



def upload_photo(request):
    user ,a = get_user_from_session(request)
    if not user:
        return redirect('login')  # Update with your login URL

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        
        if image:
            content_type = ContentType.objects.get_for_model(user.__class__)
            photo = Photo.objects.create(
                content_type=content_type,
                object_id=user.id,
                title=title,
                description=description,
                image=image
            )
            messages.success(request, 'Photo uploaded successfully!')
            return redirect('photo_detail', photo_id=photo.id)
    return render(request, 'upload_photo.html', {'user': user,'a':a})

def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    user,a = get_user_from_session(request)
    
    if not user:
        return redirect('login')

    # Increment view count
    content_type = ContentType.objects.get_for_model(user.__class__)
    view, created = PhotoView.objects.get_or_create(
        content_type=content_type,
        object_id=user.id,
        photo=photo
    )
    
    if created:
        Photo.objects.filter(id=photo_id).update(views=F('views') + 1)
    
    # Check if user has liked
    try:
        user_like = Like.objects.get(
            content_type=content_type,
            object_id=user.id,
            photo=photo
        )
    except Like.DoesNotExist:
        user_like = None
    
    comments = Comment.objects.filter(photo=photo, parent=None).order_by('-created_at')
    
    context = {
        'photo': photo,
        'comments': comments,
        'user_like': user_like,
        'user': user,
    }
    return render(request, 'photo_detail.html', context)

def toggle_like(request, photo_id):
    user,a = get_user_from_session(request)
    if not user:
        return JsonResponse({'error': 'Login required'}, status=401)

    photo = get_object_or_404(Photo, id=photo_id)
    is_like = request.POST.get('is_like') == 'true'
    
    content_type = ContentType.objects.get_for_model(user.__class__)
    like, created = Like.objects.get_or_create(
        content_type=content_type,
        object_id=user.id,
        photo=photo,
        defaults={'is_like': is_like}
    )
    
    if not created:
        if like.is_like == is_like:
            like.delete()
            action = 'removed'
        else:
            like.is_like = is_like
            like.save()
            action = 'updated'
    else:
        action = 'added'
    
    return JsonResponse({
        'action': action,
        'like_count': photo.like_count
    })

def add_comment(request, photo_id):
    user,a = get_user_from_session(request)
    if not user:
        return JsonResponse({'error': 'Login required'}, status=401)
    
    photo = get_object_or_404(Photo, id=photo_id)
    text = request.POST.get('text')
    parent_id = request.POST.get('parent_id')
    
    parent = None
    if parent_id:
        parent = get_object_or_404(Comment, id=parent_id)
    
    content_type = ContentType.objects.get_for_model(user.__class__)
    comment = Comment.objects.create(
        content_type=content_type,
        object_id=user.id,
        photo=photo,
        text=text,
        parent=parent
    )
    
    comment_count = photo.comment_count if parent is None else None
    return JsonResponse({
        'comment_id': comment.id,
        'username': f"{user.email}",
        'text': comment.text,
        'created_at': comment.created_at.strftime('%B %d, %Y %H:%M'),
        'comment_count': comment_count
    })

def delete_comment(request, comment_id):
    user,a = get_user_from_session(request)
    if not user:
        return JsonResponse({'error': 'Login required'}, status=401)

    content_type = ContentType.objects.get_for_model(user.__class__)
    comment = get_object_or_404(Comment, 
        id=comment_id, 
        content_type=content_type,
        object_id=user.id
    )
    
    photo = comment.photo
    is_main_comment = comment.parent is None
    comment.delete()
    new_count = photo.comment_count if is_main_comment else None
    
    return JsonResponse({
        'success': True,
        'comment_count': new_count
    })

def share_photo(request, photo_id):
    user,a = get_user_from_session(request)
    if not user:
        return JsonResponse({'error': 'Login required'}, status=401)

    photo = get_object_or_404(Photo, id=photo_id)
    platform = request.POST.get('platform')
    
    content_type = ContentType.objects.get_for_model(user.__class__)
    Share.objects.create(
        content_type=content_type,
        object_id=user.id,
        photo=photo,
        platform=platform
    )
    
    return JsonResponse({'success': True})

def main_page(request):
    user,a = get_user_from_session(request)
    print(a,"a")
    if not user:
        return redirect('login')
    
    search_query = request.GET.get('search', '')
    
    if search_query:
        photos = Photo.objects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        ).order_by('-created_at')
    else:
        photos = Photo.objects.all().order_by('-created_at')
    
    paginator = Paginator(photos, 12)
    page = request.GET.get('page')
    photos = paginator.get_page(page)
    
    context = {
        'user': user,
        'photos': photos,
        'search_query': search_query,
        'a':a
    }
    return render(request, 'main_cm.html', context)

def view_my_photos(request):
    user,a = get_user_from_session(request)
    if not user:
        return redirect('login')
    
    content_type = ContentType.objects.get_for_model(user.__class__)
    search_query = request.GET.get('search', '')
    
    if search_query:
        photos = Photo.objects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query),
            content_type=content_type,
            object_id=user.id
        ).order_by('-created_at')
    else:
        photos = Photo.objects.filter(
            content_type=content_type,
            object_id=user.id
        ).order_by('-created_at')
    
    paginator = Paginator(photos, 12)
    page = request.GET.get('page')
    photos = paginator.get_page(page)
    
    context = {
        'user': user,
        'photos': photos,
        'search_query': search_query,
        'a':a
    }
    return render(request, 'view_my_photos.html', context)

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def delete_my_photo(request, photo_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    user,a = get_user_from_session(request)
    if not user:
        return JsonResponse({'error': 'Login required'}, status=401)

    content_type = ContentType.objects.get_for_model(user.__class__)
    photo = get_object_or_404(Photo, 
        id=photo_id,
        content_type=content_type,
        object_id=user.id
    )
    photo.delete()
    
    return JsonResponse({'success': True})

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.urls import reverse
from .models import user_reg

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user = user_reg.objects.filter(email=email).first()
        
        if user:
            # Generate unique token (temporary password or reset link)
            reset_token = get_random_string(length=32)
            user.reset_token = reset_token  # Store token in DB (add this field to your model)
            user.save()

            # Generate password reset link
            reset_link = request.build_absolute_uri(reverse('reset_password', args=[reset_token]))

            # Send email with reset link
            send_mail(
                "Password Reset Request - FloraNet",
                f"Click the link below to reset your password:\n{reset_link}",
                "FloraNet",  # Replace with your email
                [email],
                fail_silently=False,
            )

            messages.success(request, "A password reset link has been sent to your email.")
            return redirect('login')

        else:
            messages.error(request, "Email not found! Please enter a registered email.")
    
    return render(request, 'forgot_password.html')

from django.contrib.auth.hashers import make_password

def reset_password(request, token):
    user = user_reg.objects.filter(reset_token=token).first()
    
    if not user:
        messages.error(request, "Invalid or expired reset token.")
        return redirect('login')

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, "reset_password.html", {"token": token})

        # Hash the password before saving
        user.password = make_password(new_password)
        user.reset_token = ""  # Clear reset token after successful reset
        user.save()

        messages.success(request, "Your password has been successfully reset! Please log in.")
        return redirect("login")

    return render(request, "reset_password.html", {"token": token})


from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.urls import reverse
from .models import prof_reg  # Use prof_reg for professional users
from django.contrib.auth.hashers import make_password

# Forgot password view for professional users
def prof_forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user = prof_reg.objects.filter(em=email).first()
        
        if user:
            # Generate unique token (temporary password or reset link)
            reset_token = get_random_string(length=32)
            user.reset_token = reset_token  # Store token in DB (add this field to your model)
            user.save()

            # Generate password reset link
            reset_link = request.build_absolute_uri(reverse('prof_reset_password', args=[reset_token]))

            # Send email with reset link
            send_mail(
                "Password Reset Request - FloraNet",
                f"Click the link below to reset your password:\n{reset_link}",
                "FloraNet",  # Replace with your email
                [email],
                fail_silently=False,
            )

            messages.success(request, "A password reset link has been sent to your email.")
            return redirect('proflogin')

        else:
            messages.error(request, "Email not found! Please enter a registered email.")
    
    return render(request, 'prof_forgotpass.html')  # You can create a similar template for professional users

# Reset password view for professional users
def prof_reset_password(request, token):
    user = prof_reg.objects.filter(reset_token=token).first()
    
    if not user:
        messages.error(request, "Invalid or expired reset token.")
        return redirect('proflogin')

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, "prof_reset_password.html", {"token": token})

        # Hash the password before saving
        user.passw = make_password(new_password)  # Make sure to use the field name 'passw'
        user.reset_token = ""  # Clear reset token after successful reset
        user.save()

        messages.success(request, "Your password has been successfully reset! Please log in.")
        return redirect("proflogin")

    return render(request, "prof_resetpass.htmll", {"token": token})  # You can create this template for professional users
