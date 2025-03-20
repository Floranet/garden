from django.urls import path
from.import views

urlpatterns = [
    path('index/',views.index,name='index'),
    path('',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('select/',views.select,name='select'),
    path('userlist/',views.userlist,name="userlist"),
    path('delete_user/<int:id>/',views.delete_user,name="delete_user"),
    path('userProfile/',views.userProfile,name="userProfile"),
    path('update_profile/',views.update_profile,name="update_profile"),
    path('proupdate/',views.proupdate,name="proupdate"),
    path('userHome/',views.userHome,name='userHome'),
    path('adminlogin/',views.adminlogin,name='adminlogin'),
    path('adminhome/',views.adminhome,name='adminhome'),
    path('feedback_rate/',views.feedback_rate,name='feedback_rate'),
    path('feedback_success/',views.feedback_success,name='feedback_success'),
    path('feedbacklist/',views.feedbacklist,name='feedbacklist'),
    path('delete_feedback/<int:id>/',views.delete_feedback,name='delete_feedback'),
    path('profreg/',views.profreg,name='profreg'),
    path('proflogin/',views.proflogin,name='proflogin'),
    path('prolist/',views.prolist,name="prolist"),
    path('delete_prof/<int:id>/',views.delete_prof,name="delete_prof"),
    path('profProfile/',views.profProfile,name="profProfile"),
    path('update_pro/',views.update_pro,name="update_pro"),
    path('prfupdate/',views.prfupdate,name="prfupdate"),
    path('profhome/',views.profhome,name='profhome'),
    # path('calendar/', views.calendar_view, name='calendar'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('prof_logout/', views.prof_logout, name='prof_logout'),
    # path('callist/',views.callist,name='callist'),
    # path('delete_reminder/<int:id>/',views.delete_reminder,name='delete_reminder'),
    path('admin_dash/',views.admin_dash,name='admin_dash'),
    path('feedback_rate/',views.feedback_rate,name='feedback_rate'),
    path('feedback_success/',views.feedback_success,name='feedback_success'),
    path('feedbacklist/',views.feedbacklist,name='feedbacklist'),
    path('delete_feedback/<int:id>/',views.delete_feedback,name='delete_feedback'),
    path('feedrate/',views.feedrate,name='feedrate'),
    path('feedsuc/',views.feedsuc,name='feedsuc'),
    path('feedlist/',views.feedlist,name='feedlist'),
    path('delete_feed/<int:id>/',views.delete_feed,name='delete_feed'),
    path('add_products/',views.add_products,name='add_products'),
    path('product_list/',views.product_list,name='product_list'),
    path('delete_prod/<int:id>/',views.delete_prod,name="delete_prod"),
    path('user_prod/',views.user_prod,name='user_prod'),
    path('addcart/<int:id>/',views.addcart,name='addcart'),
    path('add_cart/',views.add_cart,name='add_cart'),
    path('cart_list/',views.cart_list,name='cart_list'),
    path('update_status/',views.update_status,name='update_status'),
    path('up_status/',views.up_status,name='up_status'),
    path('payment/',views.payment,name='payment'),
    path('paymenthandler/',views.paymenthandler,name='paymenthandler'),
    path('cartlist/',views.cartlist,name='cartlist'),
    path('delete_cart/<int:cart_id>/',views.delete_cart,name='delete_cart'),
    path('paymentlist/',views.paymentlist,name='paymentlist'),
    path('vdo/',views.vdo,name='vdo'),
    path('edu/',views.edu,name='edu'),
    path('resource/<int:resource_id>/', views.resource_detail, name='resource_detail'),
    path('resource_list/',views.resource_list,name='resource_list'), 
    path('delete_res/',views.delete_res,name="delete_res"),   
    path('addshop/',views.addshop,name="addshop"), 
    path('shoplist/',views.shoplist,name="shoplist"), 
    path('deleteshop/<int:sid>/',views.deleteshop,name="deleteshop"),
    path('user_shoplist/',views.user_shoplist,name="user_shoplist"),
    path('ashoplist/',views.ashoplist,name="ashoplist"),
    path('edit_Shop/<int:sid>/',views.edit_shop,name="edit_shop"),
    path('dashboard/', views.dashboard_view, name='dashboard'),  # Dashboard view
    path('tools/', views.calendar, name='tools'),
    path('add_task/', views.add_task, name='add_task'),
    path('delete_task/', views.delete_task, name='delete_task'),
    path('paymentt/', views.payment_details, name='payment_details'),
    path('download-payment-pdf/<int:payment_id>/', views.download_payment_pdf, name='download_payment_pdf'),  # Tools page
    path('check-reminders/', views.check_reminders, name='check_reminders'),
    path('tasklist/', views.tasklist, name='tasklist'),
    path('complete_task/<int:task_id>/', views.complete_task, name='complete_task'),
    path('calendernew/', views.calendernew, name='calendarnew'),
    path('get-events/', views.get_events, name='get_events'),
    path('chat/', views.chat_list, name='chat_list'),
    path('logout/', views.logout, name='logout'),
    path('chat/<str:user_type>/<str:username>/', views.chat_detail, name='chat_detail'),
    
    path('community/', views.community, name='community'),
    path('main_page/', views.main_page, name='main_page'),
    path('upload_photo/', views.upload_photo, name='upload_photo'),
    path('photo_detail/<photo_id>/', views.photo_detail, name='photo_detail'),
    path('toggle_like/<photo_id>/', views.toggle_like, name='toggle_like'),
    path('add_comment/<photo_id>/', views.add_comment, name='add_comment'),
    path('delete_comment/<comment_id>/', views.delete_comment, name='delete_comment'),
    path('share_photo/<photo_id>/', views.share_photo, name='share_photo'),
    path('view_my_photos/', views.view_my_photos, name='view_my_photos'),
    path('delete_my_photo/<photo_id>/', views.delete_my_photo,name='delete_my_photo'),


    
    path('forgot_password/',views.forgot_password, name='forgot_password'),
    path('reset_password/<str:token>/',views.reset_password, name='reset_password'),
    ]
