from os import lseek
from warnings import filters
from webbrowser import get
from requests.exceptions import RetryError
import frappe
import requests
import json
import importlib.util
from frappe.utils import cstr
import traceback
import requests
from frappe.utils import logger
import math
from datetime import datetime
from datetime import date



def create_journal_entry(doc,method=None):
	print(doc.as_dict(),"/////////////////////")
	# try:
	if doc.cd_eligible :
		customer_name = doc.party
		account_paid = doc.paid_from
		cd_account = doc.cd_account_
		amount = doc.cd_amount
		customers = frappe.db.get_list("Payment Entry",{"name":doc.name},['party'])
		print(customers,"...................")
		if customer_name == customers[0].party:
			print(customer_name,account_paid,cd_account,amount,"//////,,,,,,,,,,,,,,,,,")
			data = frappe.get_doc({"doctype":"Journal Entry","voucher_type":"Journal Entry","posting_date":doc.posting_date,
                          "accounts":[
							  {
								"doctype":"Journal Entry Account",
								"account":cd_account,
								"debit_in_account_currency":amount
							  },
							  {
								"doctype":"Journal Entry Account",
								"account":account_paid,
								"party_type":"Customer",
								"party":customer_name,
								"credit_in_account_currency":amount
							  },

							]
            })
			data.docstatus = 1
			data.insert()
			frappe.db.commit()
	# except Exception as e:
	# 	print(str(e))