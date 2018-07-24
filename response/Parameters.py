intent_url = "http://localhost:8001/Intent/"
smalltalk_url = "http://localhost:8003/smalltalk/"
ner_url = "http://localhost:8002/ner/"
invoice_status_url = 'http://localhost:3000/invoice/'
approval_url = 'http://localhost:3000/approval/'
invoice_email_url = 'http://localhost:3000/invoicecontacts/'
SmallTalk = 'SmallTalk'
ApprovalPolicy = 'ApprovalPolicy'
InvoiceStatus = 'InvoiceStatus'
InvoiceSubProcess = 'InvoiceSubProcess'
Rushpayment = 'Rushpayment'
responsefile = 'response/chatbot_response.json'
gpe = 'GPE'
approver_ne = 'APPROVER'
invoice_ne = 'INVOICE_NUMBER'
org = 'ORG'

Label = 'Label'
probability = 'Probability'
confidence = .65
label = 'Label'
response = 'response'
approver = '<approver>'
amount = '<amount>'
email = '<email>'
text = 'text'
status = '<status>'
amount = '<amount>'
inv_status = 'Invoice status'
inv_amount = 'Invoice Amount'
date = 'DATE'
default = 'default'
limit = 'limit'
email_ad = 'email'
error = 'Error Message'

rush_pay_response = "To have the supplier paid before the due date in case where there is a direct business and financial impact, request can be made to  HelpDesk@abc.com along with the following details 1.Business Justification. 2.Invoice Copy or Invoice Details. 3.Email approval"


import logging

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

fileHandler = logging.FileHandler("{0}/{1}.log".format(".", "chatbot"))
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

