'''
Created on Feb 5, 2021

@author: Adam Howell
'''

import unittest
from work import working

class TestTrueAccordTestCode(unittest.TestCase):
    
    def test_ingest(self):
        debts_json = [
          {
            "amount": 123.46,
            "id": 0
          },
          {
            "amount": 100,
            "id": 1
          },
          {
            "amount": 4920.34,
            "id": 2
          },
          {
            "amount": 12938,
            "id": 3
          },
          {
            "amount": 9238.02,
            "id": 4
          }
        ]
        
        debts_data = working.get_data("https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/debts")
        self.assertEqual(debts_json, debts_data)
        
        payment_plans_json = [
          {
            "amount_to_pay": 102.5,
            "debt_id": 0,
            "id": 0,
            "installment_amount": 51.25,
            "installment_frequency": "WEEKLY",
            "start_date": "2020-09-28"
          },
          {
            "amount_to_pay": 100,
            "debt_id": 1,
            "id": 1,
            "installment_amount": 25,
            "installment_frequency": "WEEKLY",
            "start_date": "2020-08-01"
          },
          {
            "amount_to_pay": 4920.34,
            "debt_id": 2,
            "id": 2,
            "installment_amount": 1230.085,
            "installment_frequency": "BI_WEEKLY",
            "start_date": "2020-01-01"
          },
          {
            "amount_to_pay": 4312.67,
            "debt_id": 3,
            "id": 3,
            "installment_amount": 1230.085,
            "installment_frequency": "WEEKLY",
            "start_date": "2020-08-01"
          }
        ]
        
        payment_plans_data = working.get_data("https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/payment_plans")
        self.assertEqual(payment_plans_json, payment_plans_data)
        
        payments_json = [
          {
            "amount": 51.25,
            "date": "2020-09-29",
            "payment_plan_id": 0
          },
          {
            "amount": 51.25,
            "date": "2020-10-29",
            "payment_plan_id": 0
          },
          {
            "amount": 25,
            "date": "2020-08-08",
            "payment_plan_id": 1
          },
          {
            "amount": 25,
            "date": "2020-08-08",
            "payment_plan_id": 1
          },
          {
            "amount": 4312.67,
            "date": "2020-08-08",
            "payment_plan_id": 2
          },
          {
            "amount": 1230.085,
            "date": "2020-08-01",
            "payment_plan_id": 3
          },
          {
            "amount": 1230.085,
            "date": "2020-08-08",
            "payment_plan_id": 3
          },
          {
            "amount": 1230.085,
            "date": "2020-08-15",
            "payment_plan_id": 3
          }
        ]
        
        payments_data = working.get_data("https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/payments")
        self.assertEqual(payments_json, payments_data)
        
    def test_payment_plan_association(self):
        debts_data = working.get_data("https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/debts")
        pyament_plans_data = working.get_data("https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/payment_plans")
        
        debts_json = [
          {
            "amount": 123.46,
            "id": 0,
            'is_in_payment_plan': False
          },
          {
            "amount": 100,
            "id": 1,
            'is_in_payment_plan': True
          },
          {
            "amount": 4920.34,
            "id": 2,
            'is_in_payment_plan': True
          },
          {
            "amount": 12938,
            "id": 3,
            'is_in_payment_plan': False
          },
          {
            "amount": 9238.02,
            "id": 4,
            'is_in_payment_plan': False
          }
        ]
        
        debts_data = working.is_associated_with_payment_plan(debts_data, pyament_plans_data)
        self.assertEqual(debts_json, debts_data)
    
    def test_next_payment_calculation(self):
        debts_data = working.get_data("https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/debts")
        pyament_plans_data = working.get_data("https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api/payment_plans")
        
        debts_json = [
          {
            "amount": 123.46,
            "id": 0,
            'is_in_payment_plan': False,
            'remaining_amount': None, 
            'next_payment_due_date': None
          },
          {
            "amount": 100,
            "id": 1,
            'is_in_payment_plan': True,
            'remaining_amount': 75, 
            'next_payment_due_date': '2020-08-08 00:00:00'
          },
          {
            "amount": 4920.34,
            "id": 2,
            'is_in_payment_plan': True,
            'remaining_amount': 3690.255, 
            'next_payment_due_date': '2020-01-15 00:00:00'
          },
          {
            "amount": 12938,
            "id": 3,
            'is_in_payment_plan': False,
            'remaining_amount': None, 
            'next_payment_due_date': None
          },
          {
            "amount": 9238.02,
            "id": 4,
            'is_in_payment_plan': False,
            'remaining_amount': None, 
            'next_payment_due_date': None
          }
        ]
        
        debts_data = working.is_associated_with_payment_plan(debts_data, pyament_plans_data)
        debts_data = working.next_payment(debts_data, pyament_plans_data)
        self.assertEqual(debts_json, debts_data)