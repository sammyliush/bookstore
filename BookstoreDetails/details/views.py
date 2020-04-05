from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
import datetime
import logging
import json


# Create your views here.

CONTENT_TYPE = 'application/json'

AUTHOR = 'author'
PUBLISH_DATE = "publish_data"
DESCRIPTION = 'description'

VERESION = 'V3'

BOOK_DETAILS = {'0':{AUTHOR:VERESION, PUBLISH_DATE:'2001-10-01', DESCRIPTION:'This is a book about China'},
                '1':{AUTHOR:'Jack Ma', PUBLISH_DATE:'2001-10-01', DESCRIPTION:'This is a book about China'},
                '2':{AUTHOR:'Pony Ma', PUBLISH_DATE:'2010-11-11', DESCRIPTION:'This is a book about England'},
                '3':{AUTHOR:'John Ma', PUBLISH_DATE:'2020-10-01', DESCRIPTION:'This is a book about American'}}

logger = logging.getLogger('django')


def blank(requests):
    log_request_header("blank@" + VERESION, requests)
    response_str = "Hello world, details " + VERESION + " @ " + str(datetime.datetime.now()) + " !"
    return HttpResponse(response_str)


def get_detail(requests):
    log_request_header("get_detail@" + VERESION, requests)

    if requests.method == "GET":
        #get id
        book_id = requests.GET.get('id')
        logger.info("To get details for book with id " + book_id)
        logging.info("book_id is " + str(book_id))
        if book_id in BOOK_DETAILS.keys():
            logger.info("Book with id " + book_id + " exists")
            return HttpResponse(json.dumps(BOOK_DETAILS[book_id]), content_type=CONTENT_TYPE)
        else:
            return HttpResponse("No record found")

def log_request_header(func_name, request):
    logger.info("---------  Headers of request into " + func_name + ": ------")
    for key in request.headers:
        logger.info(key + ": " + request.headers[key])
