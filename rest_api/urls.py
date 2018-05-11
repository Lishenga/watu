from django.urls import include, path
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .controllers import UsersController, BillingController, TransactionsController, MessagingController
from .settings import configs, countries, rates


urlpatterns = [
    
    path('CreateCustomer/', UsersController.create_customer),
    path('UpdateCustomer/', UsersController.update_customer),
    path('DeleteCustomer/', UsersController.delete_customer),
    path('GetAllCustomers/', UsersController.get_all_customers),
    path('AuthenticateUser/', UsersController.get_customer_email_login),
    path('ViewAllCustomerCards/',UsersController.get_customer_cards),
    path('ResetUserPassword/',UsersController.update_customer_password),
    path('GetParticularCustomer/', UsersController.get_particular_customer_details),
    path('ViewParticularCustomersTransactions/', TransactionsController.get_customer_transactions),
    path('CreateStripeCustomer/', BillingController.create_stripe_customer),
    path('CreateStripeCard/', BillingController.create_stripe_customer_card),
    path('CreateStripeCardCharge/', BillingController.create_stripe_customer_charge),

    #path('DisbursePayments/', BillingController.disburse_cash_MPESA),
    #path('LipishaAccountBalance/', BillingController.lipisha_account_balance),
    #path('MpesaConfirmTransaction/', BillingController.lipisha_confirm_transactions),
    #path('LipishaGetTransactions/', BillingController.lipisha_get_transactions),
    #path('TriggerTransaction/', TransactionsController.convert_and_send_actual),

  
   
    path('finance/SendMoneytest/', BillingController.test_africa_send_money), 
    path('finance/GetStripeBalance/', BillingController.get_stripe_balance), 
    path('finance/ViewAllTransactions/', TransactionsController.get_all_transactions),  

    #chats
    path('ChatloadAllchat/', MessagingController.load_chat),
    path('ChatSendMessage/', MessagingController.send_message),
    path('ChatGetMessages/', MessagingController.get_messages), 
    path('ChatSetPlayerDetails/',MessagingController.set_player_details),
    path('ChatGetPlayerDetails/',MessagingController.get_player_details),

    path('settings/SetDefaultTariffPercentage/',configs.set_default_tariff_percentage),
    path('settings/SetDefaultCoreCurrency/',configs.set_default_currency),
    path('settings/CreateCountry/',countries.create_country),
    path('settings/ViewCountries/',countries.view_country),
    path('settings/DeleteCountry/',countries.delete_country),
    path('settings/UpdateCountry/',countries.update_country),

    path('settings/CreateRate',rates.create_rate),
    path('settings/UpdateRate',rates.update_rate),
    path('settings/ViewAllRates',rates.view_rates),
    path('settings/ShowParticularRateDetails',rates.get_particular_rate)

]