"""REST Controller

Here you'll find handlers for RESTful API, which is meant to be stateless
"""

import tornado
from tornado.escape import json_decode

from scheduler.utils import routes

from scheduler.view import BaseRESTController

import requests

@routes('/api/kpi_schedule/', name="kpi_api")
class KPIApiHandler(BaseRESTController):
    """Register"""
    @tornado.web.asynchronous
    def post(self):
        group = json_decode(self.request.body).get('group')
        self.write(requests
                    .get('http://api.rozklad.org.ua/v1/groups/{}/lessons'
                                                        .format(group)).text)
        self.finish()


@routes("/api/", name="api")
class ApiHandler(BaseRESTController):
    """API Handler"""
    pass
