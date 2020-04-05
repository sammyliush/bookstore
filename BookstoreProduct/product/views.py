from django.shortcuts import render
from django.http import HttpResponse
import requests,json
import datetime
import logging

# Create your views here.

import os
os.environ['no_proxy'] = '*'

logger = logging.getLogger('django')

#try to get details service URL from Env

DETAILS_SVC_URL = "http://detailsservice:8082/details/details/"

temp = os.getenv("DETAILS_SVC_URL")
if temp is not None and len(temp) >= 0:
    DETAILS_SVC_URL = temp

logger.info("DETAILS_SVC_URL is %s" % DETAILS_SVC_URL)


RATINGS_SVC_URL = "http://ratingsservice:8083/ratings/ratings/"
temp = os.getenv("RATINGS_SVC_URL")
if temp is not None and len(temp) >= 0:
    RATINGS_SVC_URL = temp

logger.info("RATINGS_SVC_URL is %s" % RATINGS_SVC_URL)

REVIEWS_SVC_URL = "http://reviewsservice:8084/reviews/reviews/"
temp = os.getenv("REVIEWS_SVC_URL")
if temp is not None and len(temp) >= 0:
    REVIEWS_SVC_URL = temp

logger.info("REVIEWS_SVC_URL is %s" % REVIEWS_SVC_URL)

SPACE = "&nbsp;"


# f_handler = logging.FileHandler('/Users/Sammy/bookstore/debug.log')
# f_handler.setLevel(logging.INFO)
# logger.addHandler(f_handler)

VERSION = 'V3'

def blank(requests):
    log_request_header("blank@" + VERSION, requests)
    response_str = "Hello world, product " + VERSION + " @ " + str(datetime.datetime.now()) + " !"
    return HttpResponse(response_str)


def product(request):
    logger.info("Enter product()")

    log_request_header("product@" + VERSION, request)

    response_str = ""
    book_id = ""
    response_str = ""

    #显示当前时间
    response_str += "<b>Version: " + VERSION + "</b>, " + str(datetime.datetime.now()) + "<hr>"

    #for each book
    for i in range(1):
        book_id = str(i)

        logger.info("Getting data for book with id " + book_id)

        response_str += "<b>Book " + str(book_id) + "</b><br>"

        #get book details
        response_str += "Details:<br>"
        details_info = get_book_details(request, book_id)
        logger.info("deails info: " + details_info)
        response_str += details_info

        #get book reviews
        response_str += "Reviews:<br>"
        reviews_info = get_book_reviews(request, book_id)
        logger.info("reviews info: " + reviews_info)
        response_str += reviews_info

        response_str += "<hr>"

        #return response
    return HttpResponse(response_str)



def get_book_details(request, book_id):

    log_request_header("get_book_details@" + VERSION, request)

    """get one book's details information"""
    response_str = ""
    headers = passTracingHeaders(request)
    try:
        detail_request = requests.get(DETAILS_SVC_URL, params={'id': book_id}, headers=headers)
        response_text = detail_request.text

        if response_text == "" or response_text == "No record found":
            response_str += SPACE + SPACE + "No details record found for book with id " + book_id + "<br>"
        else:
            # details_data 类型为 dict
            details_data = json.loads(detail_request.content)
            for key in details_data.keys():
                response_str += SPACE + SPACE + key.title() + ": " + details_data[key] + "<br>"
    except Exception as err:
        response_str = SPACE + SPACE + "Failed to get details for book " + book_id + " !" + str(err)

    return response_str


def get_book_reviews(request, book_id):

    log_request_header("get_book_reviews@" + VERSION, request)

    """get one book's review information"""
    response_str = ""
    response_text =""
    headers = passTracingHeaders(request)
    try:
        review_request = requests.get(REVIEWS_SVC_URL, params={'id': book_id}, headers=headers)
        response_text = review_request.text
        response_str += SPACE + SPACE + response_text + "<br>"
    except Exception as err:
        response_str = SPACE + SPACE + "Failed to get reviews for book " + book_id + " !" + str(err)

    return response_str


def details(request):

    log_request_header("details@" + VERSION, request)

    response_str = ""
    book_id = "1"
    for i in range(10):
        book_id = str(i)
        try:
            detail_request = requests.get(DETAILS_SVC_URL, params={'id':book_id})
            response_text = detail_request.text
        except Exception as err:
            response_str = "Error!" + str(err)

        if response_text == "" or response_text == "No record found":
            response_str += "Book " + book_id + " " + response_text + "<br><hr>"
        else:
            response_str += "<b> Book " + book_id + " :<br></b>"
            #details_data 类型为 dict
            details_data = json.loads(detail_request.content)
            for key in details_data.keys():
                response_str += key.title() + ": " + details_data[key] + "<br>"
            response_str += "<hr>"

    return HttpResponse(response_str)

def ratings(request):

    log_request_header("ratings@" + VERSION, request)

    response_str = ""
    response_text = ""
    book_id = "1"

    for i in range(10):
        book_id = str(i)
        try:
            session = requests.session()
            session.trust_env = False
            rating_request = requests.get(RATINGS_SVC_URL, params={'id':book_id})
            response_text = rating_request.text
        except Exception as err:
            response_str = "Error!" + str(err)

        if response_text == "" or response_text == "No record found":
            response_str += "Book " + book_id + " " + response_text + "<br><hr>"
        else:
            response_str += "<b> Book " + book_id + " :<br></b>"
            # details_data 类型为 dict
            details_data = json.loads(rating_request.content)
            for key in details_data.keys():
                response_str += key.title() + ": " + details_data[key] + "<br>"
            response_str += "<hr>"

    return HttpResponse(response_str)

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