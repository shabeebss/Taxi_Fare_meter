from django.contrib import admin
from django.urls import path, include

from fareapp import views

urlpatterns = [
    path('', views.landing),
    path('login', views.login),
    path('login_post',views.login_post),
    path('cregister',views.cregister),
    path('cregister_post',views.cregister_post),
    path('dregister',views.dregister),
    path('dregister_post',views.dregister_post),
    path('Adminhome',views.Adminhome),
    path('Managevtype', views.Managevtype),
    path('Add_vtype', views.Add_vtype),
    path('insert_vtype', views.insert_vtype),
    path('vtype_delete/<id>', views.vtype_delete),
    path('Edit_vtype/<id>', views.Edit_vtype),
    path('Edit_vtype_add', views.Edit_vtype_add),
    path('Verify_driver',views.Verify_driver),
    path('admin_view_more_drivers/<id>',views.admin_view_more_drivers),
    path('accept_driver/<id>',views.accept_driver),
    path('block_driver/<id>',views.block_driver),
    path('unblock_driver/<id>',views.unblock_driver),
    path('reject_driver/<id>',views.reject_driver),
    path('view_registered_customer',views.view_registered_customer),
    path('view_rating',views.view_rating),
    path('generate_qr/<id>',views.generate_qr),
    path('view_trip_history2',views.view_trip_history2),
    path('viewdriver',views.viewdriver),
    path('fetch_driver_details',views.fetch_driver_details),



    path('Driverhome',views.Driverhome),
    path('searchuser',views.searchuser),

    path('add1',views.add1),
    path('add3',views.add3),
    path('add2/<id>',views.add2),
    path('start_ride',views.start_ride),
    path('generate_bill/<int:id>/', views.generate_bill, name='generate_bill'),

    path('driver_view_users',views.driver_view_users),
    path('view_trip_history',views.view_trip_history),
    path('driver_profile',views.driver_profile),
    path('edit_profile/<id>',views.edit_profile),
    path('view_rating1',views.view_rating1),
    path('change_password',views.change_password),

    path('Customerhome', views.Customerhome),
    path('customer_edit_profile/<id>', views.customer_edit_profile),
    path('view_trip_history1',views.view_trip_history1,name='view_trip_history1'),
    path('view_drivers',views.view_drivers),
    path('view_drivers_view_more/<id>',views.view_drivers_view_more),
    path('view_profile',views.view_profile),

    path('user_pay_proceed/<id>/<amt>', views.user_pay_proceed),
    path('on_payment_success', views.on_payment_success),
    path('add_rating', views.add_rating),
    path('driver_view_feedbacks', views.driver_view_feedbacks),
    


]
