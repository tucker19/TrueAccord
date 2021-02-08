'''
Created on Feb 4, 2021

@author: Adam Howell
'''
from datetime import timedelta
from dateutil import parser
import urllib.request, json

def print_data(data):
    for anything in data:
        print(json.dumps(anything, indent=4))
        
def next_payment(debt_data_dict, payment_plan_data_dict, payment_data_dict):
    for debt_data in debt_data_dict:
        is_in_payment_plan = debt_data.get('is_in_payment_plan')
        remaining_amount = None
        next_payment_due_date_str = None
        
        if is_in_payment_plan:
            debt_id = debt_data.get('id')
            
            for payment_plan_data in payment_plan_data_dict:
                if debt_id == payment_plan_data.get('debt_id'):
                    payment_plan_id = payment_plan_data.get('debt_id')
                    amount_to_pay = payment_plan_data.get('amount_to_pay')
                    installment_frequency = payment_plan_data.get('installment_frequency')
                    next_payment_value = 7 if installment_frequency == 'WEEKLY' else 14
                    start_date_str = payment_plan_data.get('start_date')
                    start_payment_date = parser.parse(start_date_str)
                    next_payment_date = start_payment_date + timedelta(days=next_payment_value)
                    next_payment_due_date_str = next_payment_date.strftime("%Y-%m-%d")
                    remaining_amount = amount_to_pay
                    
                    for payment_data in payment_data_dict:
                        if payment_plan_id == payment_data.get('payment_plan_id'):
                            payment_date = parser.parse(payment_data.get('date'))
                            if payment_date <= next_payment_date:
                                amount_paid = payment_data.get('amount')
                                remaining_amount -= amount_paid
                                
                                if remaining_amount <= 0.0:
                                    remaining_amount = None
                                    next_payment_due_date_str = None
                                    break
                    
                    
                        
        debt_data.update({'remaining_amount':remaining_amount, 'next_payment_due_date':next_payment_due_date_str})
    return debt_data_dict
        
def is_associated_with_payment_plan(data1, data2):
    for debt_data in data1:
        is_in_payment_plan = False
        debt_id = debt_data.get('id')
        debt_amount = debt_data.get('amount')
        
        for payment_plan in data2:
            if debt_id == payment_plan.get('debt_id') and debt_amount == payment_plan.get('amount_to_pay'):
                is_in_payment_plan = True
                
        debt_data.update({'is_in_payment_plan':is_in_payment_plan})    
    return data1

def get_data(url):
    jsonurl = urllib.request.urlopen(url)
    return json.loads(jsonurl.read())

def main(debt_url, payment_plan_url, payments_url):
    
    debt_data = get_data(debt_url)
    payment_plan_data = get_data(payment_plan_url)
    payments_data = get_data(payments_url)
    
    debt_data = is_associated_with_payment_plan(debt_data, payment_plan_data)
    debt_data = next_payment(debt_data, payment_plan_data, payments_data)
    print_data(debt_data)
    
    print(json.dumps(payment_plan_data, indent=4))
    print(json.dumps(payments_data, indent=4))
    
    
#main("https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/debts", 
#     "https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/payment_plans", 
#     "https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/payments")
