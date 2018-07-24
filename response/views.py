from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from response import chatbot
from django.template import loader

from response.Parameters import logger


@csrf_exempt
def input(request):

     if request.method == 'POST':
       logger.debug ('Request reached in chatbot views')
       inputString  = request.POST['text']
       response = ''
       if inputString != '' or len(inputString) > 0:
         logger.info ('User input -->'+ inputString )
         response = chatbot.get_chatbot_response(inputString)
         logger.debug ('response -->'+ response )
       template = loader.get_template('response/input.html')
       context={'response':response,}

       return HttpResponse( template.render(context, request))
    
     else:
        template = loader.get_template('response/input.html')
        context={}
        return HttpResponse(template.render(context, request))

@csrf_exempt
def getChatbotResponse(request, inputString):
    
    logger.debug ('Request reached in chatbot views')
    logger.info ('User input -->'+ inputString )
    response = chatbot.get_chatbot_response(inputString)
    logger.debug ('response -->'+ response )

    return HttpResponse( response)
