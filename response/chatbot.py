# -*- coding: utf-8 -*-
import json
from response import Parameters
from response.apps import ResponseConfig

from response.Parameters import logger
import time
import re
import requests

#To get approval limit
def getlimit( approver) :
   logger.debug ('getting limit')
   response = requests.get(url = (Parameters.approval_url+ approver))
   
   logger.debug (response)
   res = ''   
  
   try:
     response = response.json() 
     res  = response[Parameters.limit]

   except (KeyError) as ex:
       logger.error('Error')
       logger.error (ex)

       res = response [Parameters.error]
       logger.info (res)
          
   return res;    

#To get email address
def getEmailAddress( region , responseJson):
    logger.debug ('get EmailAddress')
    response = requests.get(url = (Parameters.invoice_email_url +region) )
    logger.debug (response)
    res = ''
    
    try:
     response = response.json() 
     logger.info (response)
     email  = response[Parameters.email_ad]
     
     res = responseJson.replace (Parameters.email, email)

    except (KeyError) as ex:
       logger.error('Error')
       logger.error (ex)

       res = response [Parameters.error]
    
    logger.info (res)

    return res;

#To identify entities in user input
def getEntities (textmessage):

    logger.debug ('get Entities')
    response = requests.get(url = (Parameters.ner_url +textmessage+'/') )
    logger.debug (response)
    data = response.json()
    
    return data;

#get small talk response
def getSmallTalkResponse (textmessage):

    response = requests.get(url = (Parameters.smalltalk_url+ textmessage+'/'))    
    logger.debug (response.text)
    data = response.text

    return data;

#To get approval response
def getApprovalResponse(ner, responseJson):
    
    logger.debug ('get Approval Response')
    responses = set()
    
    try:
     for ne in ner:
       if ne[Parameters.label] == Parameters.approver_ne : 
	
         limit = getlimit(ne[Parameters.text])
        
         responses.add (limit)

    except (RuntimeError, TypeError, NameError, KeyError) as ex:
       logger.error('Error')
       logger.error (ex)

       res = responseJson [Parameters.default]
       responses.add (res)

    return responses;

#To get invoice status
def getInvoiceStatus(ner, responseJson):
    logger.debug ('get Invoice Status')
    responses = set()
    
    try:
     for ne in ner:
      if ne[Parameters.label] == Parameters.date or ne[Parameters.label] == Parameters.org:
    
        response = requests.get(url = (Parameters.invoice_status_url+ ne[Parameters.text]+'/'))
        status = response.json()
        res = responseJson [Parameters.response]
        res = res.replace (Parameters.status, status[Parameters.inv_status])
        res = res.replace (Parameters.amount, status[Parameters.inv_amount])
        responses.add (res)

    except (RuntimeError, TypeError, NameError, KeyError) as ex:
       logger.error('Error')
       logger.error (ex)

       res = responseJson [Parameters.default]
       responses.add (res)
    
    return responses;

#To get invoice email
def getInvoiceSubProcess (ner, responseJson):
   
    responses = set()
    logger.debug ('get Invoice SubProcess')
    for ne in ner:
	#query email
      if ne[Parameters.label] == Parameters.gpe :
        res = getEmailAddress(ne[Parameters.text], responseJson [Parameters.response])
                
        responses.add (res)

    return responses;

#To get rush payment response
def getRushpayment (ner, responseJson):
    
    responses = set()
    logger.debug ('get Rush payment')
    res = Parameters.rush_pay_response
      
    responses.add (res)

    return responses;

#Get response for user input
def get_chatbot_response(textmessage):
    
    logger.info ('Chatbot input : ' + textmessage)
    textmessage = re.sub(r'[^\w]', ' ', textmessage)
    textmessage = re.sub(' +',' ', textmessage)
    chat_response = set()

    with open(Parameters.responsefile) as json_data:
           responseJson = json.load(json_data)
           logger.debug(responseJson)
           json_data.close()

           logger.debug ('responseJson file loaded ')

    response = requests.get(url = (Parameters.intent_url + textmessage+'/'))
 
# extracting data in json format
    data = response.json()
    logger.info ('Chatbot intent : ' + str(data))
    intent = data[Parameters.Label]
    probability = data [Parameters.probability]

    if float (probability) > Parameters.confidence:

      if intent == Parameters.SmallTalk:
         talk = getSmallTalkResponse (textmessage)
         chat_response.add(talk)
         logger.info ('SmallTalk response : ' + str(chat_response))

      else :  
         ner = getEntities (textmessage)
         logger.info ('ner response : ' + str(ner))
                  

         switcher = {
          Parameters.ApprovalPolicy: getApprovalResponse,
          Parameters.InvoiceStatus: getInvoiceStatus,
          Parameters.InvoiceSubProcess: getInvoiceSubProcess,
          Parameters.Rushpayment: getRushpayment
      }

         func = switcher.get(intent, lambda: "Sorry, I don't know")
         # Execute the function
         chat_response =  func(ner, responseJson[intent])
         
         logger.info ('Chatbot chat_response : ' + str(len(chat_response)))
         if len(chat_response) == 0:
           default = responseJson[intent][Parameters.default]
           logger.info (default)
           chat_response.add(default)
    logger.info (chat_response)
    if chat_response == '' or len(chat_response) == 0:
          chat_response.add(responseJson[Parameters.default])
          logger.info (chat_response)
        

    return(chat_response.pop())



