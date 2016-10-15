# -*- coding: utf-8 -*-
import json

import pytest
from hamcrest import *
import requests


class TestHh:
    area_codes = dict(RUSSIA=113,
                      SPB=2)

    def make_request(self, api_node, base_url='https://api.hh.ru/', **params):
        __tracebackhide__ = True
        response = {}
        try:
            params['encoding'] = "utf-8"
            response = json.loads(requests.get(base_url + api_node, params=params).text)
        except ValueError as err:
            print ("\nJSON decode error\n {}".format(err))
        except requests.exceptions.HTTPError as err:
            print ("\nHTTPError\n {}".format(err))
        except requests.exceptions.RequestException as err:
            print ("\nRequestException\n {}".format(err))
        except Exception as err:
            print ("\nSomething is wrong\n {}".format(err))
        if not response:
            pytest.fail("Problem with request to {}".format(api_node))
        return response


    def test_number_of_countries(self):
        countries_node = 'areas/countries'
        json_countries = self.make_request(countries_node)
        assert len(json_countries) == 138

    @pytest.mark.parametrize(
        "node, search_text, area, expected_result",
        [
            ("employers", u"новые облачные", area_codes['RUSSIA'], u"Новые Облачные Технологии"),
            ("vacancies", u"QA Automation Engineer (Server)", area_codes['SPB'], u"QA Automation Engineer (Server)"),
        ])
    def test_search(self, node, search_text, area, expected_result):
        print "\nDescription (cause of unicode hell):\ntest_search for node = %s, search_text = %s, area = %s, expected_result = %s in search results"%(node, search_text, area, expected_result)
        json_companies = self.make_request(node, text=search_text, area=area)
        company_names = [item.get('name', '') for item in json_companies.get('items', {})]
        assert_that(expected_result in company_names)
