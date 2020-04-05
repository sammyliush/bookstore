from django.shortcuts import render
from django.http import HttpResponse
import datetime
import logging
import json
# Create your views here.

logger = logging.getLogger('django')
CONTENT_TYPE = "application/json"
BOOK_RATINGS = {}

VERSION = "V3"

for i in range(100):
    rating = {}
    rating['score'] = str(100 + i)
    if i == 0:
        rating['rating'] = VERSION
    elif ( i % 2 == 0):
        rating['rating'] = 'golden'
    else:
        rating['rating'] = 'siliver'
    BOOK_RATINGS[str(i)] = rating


def blank(request):
    log_request_header("blank@" + VERSION, request)
    response_str = "Hello world, retaings " + VERSION + " @ " + str(datetime.datetime.now()) + " !"
    return HttpResponse(response_str)


def get_rating(requests):
    log_request_header("get_rating@" + VERSION, requests)
    if requests.method == "GET":
        #get id
        book_id = requests.GET.get('id')
        logger.info("To get rating for book with id " + str(book_id))
        if not book_id or len(book_id) == 0:
            return HttpResponse("No id specified")
        else:
            if book_id in BOOK_RATINGS.keys():
                logger.info("Book with id " + book_id + " has rating")
                return HttpResponse(json.dumps(BOOK_RATINGS[book_id]), content_type=CONTENT_TYPE)
            else:
                logger.info("Book with id " + book_id + " has no rating")
                return HttpResponse("No record found")

def log_request_header(func_name, request):
    logger.info("---------  Headers of request into " + func_name + ": ------")
    for key in request.headers:
        logger.info(key + ": " + request.headers[key])