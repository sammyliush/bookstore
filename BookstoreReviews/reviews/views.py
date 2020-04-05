from django.shortcuts import render
from django.http import HttpResponse
import requests
import datetime
import logging
import json
# Create your views here.

import os
os.environ['no_proxy'] = '*'

logger = logging.getLogger('django')

CONTENT_TYPE = "application/json"

RATINGS_SVC_URL = "http://ratingsservice:8083/ratings/ratings/"
temp = os.getenv("RATINGS_SVC_URL")
if temp is not None and len(temp) >= 0:
    RATINGS_SVC_URL = temp
logger.info("RATINGS_SVC_URL is %s" % RATINGS_SVC_URL)

BOOK_RATINGS = {}
has_inialized = False

SPACE = "&nbsp;"

NONE_PROXY = {'http':None, "https":None, "all-proxy":None}

VERSION = 'V3'


def inialize_data():
    for i in range(100):
        rating = {}
        rating['review number'] = str(100 + i)
        if i == 0:
            rating['review version'] = VERSION
        elif ( i % 2 == 0):
            rating['review message'] = 'This is a good book'
        else:
            rating['review message'] = 'This is a bad book'
        BOOK_RATINGS[str(i)] = rating
    has_inialized = True


def blank(request):
    log_request_header("blank@" + VERSION, requests)
    response_str = "Hello world, reviews " + VERSION + " @ " + str(datetime.datetime.now()) + " !"
    return HttpResponse(response_str)


def get_review(request):
    """get review and rating"""

    log_request_header("get_review@" + VERSION, request)

    logger.info("Enter function get_review()")

    #initialize data
    if not has_inialized:
        inialize_data()

    logger.info("Request method is " + request.method)

    if request.method == "GET":
        #get id
        book_id = request.GET.get('id')
        logger.info("book_id is " + str(book_id))
        book_rating = {}
        response_str = ""

        #get review
        if not book_id or len(book_id) == 0:
            logger.info("Book with id " + book_id + " is null")
            return HttpResponse("No id specified")
        elif book_id not in BOOK_RATINGS.keys():
            logger.info("Book with id " + book_id + " doesn't exist")
            return HttpResponse("No record found for book with id " + book_id)
        else:
            logger.info("Book with id "+ book_id + " has review records")
            book_rating = BOOK_RATINGS[book_id]
            for key in book_rating.keys():
                response_str += SPACE + SPACE + key +": " + book_rating[key] + "<br>"

        #get rating
        response_str += "<b>Ratings:</b><br>"
        try:
            details_data_dict = get_ratings(request, book_id=book_id)
            if len(details_data_dict) > 0:
                for key in details_data_dict.keys():
                    response_str += SPACE + SPACE + key + ": " + details_data_dict[key] + "<br>"
        except Exception as ex:
            logger.error("Failed to get rating record for book with id " + book_id)
            response_str += str(ex.__cause__)

        logger.info("response_str: " + response_str)
        return HttpResponse(response_str)



def get_ratings(request, book_id):
    log_request_header("get_ratings@" + VERSION, request)

    response_str = ""
    response_text = ""
    headers = passTracingHeaders(request)

    try:
        #session = requests.session()
        #session.trust_env = False
        logger.info("Call rating service on " + RATINGS_SVC_URL + " with book_id " + book_id)
        rating_request = requests.get(RATINGS_SVC_URL, params={'id':book_id}, proxies=NONE_PROXY, headers=headers)
        response_text = rating_request.text
    except Exception as err:
        logger.error("Calling rating service failed! Error: " + str(err))
        raise Exception("Error!" + str(err))

    if response_text == "" or response_text == "No record found":
        raise Exception("No record found for book with id " + book_id)
    else:
        # details_data 类型为 dict
        details_data_dict = json.loads(rating_request.content)
        return details_data_dict

def log_request_header(func_name, request):
    logger.info("---------  Headers of request into " + func_name + ": ------")
    for key in request.headers:
        logger.info(key + ": " + request.headers[key])

def passTracingHeaders(request):
    headers = {}

    for key in request.headers:
        val = request.headers.get(key)
        if val is not None:
            headers[key] = val

    return headers