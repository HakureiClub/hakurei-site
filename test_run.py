import pytest
import aiohttp
from sanic.utils import sanic_endpoint_test

from runtime import hakureiclub_app_runapp

def test_endpoint_homepage():
    request, response = sanic_endpoint_test(hakureiclub_app_runapp, uri='/')
    assert response.status == 200
