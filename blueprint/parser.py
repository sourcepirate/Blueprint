"""Parses a json file"""

from __future__ import print_function

import os
import sys
import json
from jsonschema import validate, ValidationError, SchemaError
from .fetcher import Fetcher

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

def json_from_file(path):
    _cwd = os.getcwd()
    _np = os.path.join(_cwd, path)
    _fp = open(_np, "r")
    return json.load(_fp)

class Case(dict):
    """Case for each blueprint tests"""

    def __init__(self, url, 
                 method="GET",
                 headers={},
                 payload={},
                 conditions =[]
                 ):
       
       self._url = url
       self._method = method.lower()
       self._headers = headers
       self._payload = payload
       self._conditions = conditions

       _overall = {
           "url": self._url,
           "method": self._method,
           "headers": self._headers,
           "payload": self._payload,
           "conditions": []
       }

       for condition in conditions:
           _overall["conditions"].append(condition)
       super(Case, self).__init__(_overall)

    def validate(self):
        """Validate all conditions with the response"""
        fetcher = Fetcher(self._url, method = self._method, payload=self._payload, headers=self._headers)
        response = fetcher.execute()
        flags = []
        for condition in self._conditions:
            flag, reason = condition.checkit(response)
            condition.update({"status": flag, "reason": reason})
            flags.append(condition)
        return flags

    def run_case(self):
        validations = self.validate()
        flag = False
        for check in validations:
            sys.stdout.write(BOLD)
            print(check.name)
            print(check.description)
            if check.get("status"):
                sys.stdout.write(GREEN)
                print("OK!!!")
            else:
                sys.stdout.write(RED)
                print(check.get("reason"))
        if not all(validations):
            sys.stdout.write(RED)
            print("Failed!!!!")
        else:
            flag = True
            sys.stdout.write(GREEN)
            print("Success!!!")
        sys.stdout.write(RESET)
        return flag
                

class Condition(dict):
    
    def __init__(self, name, description, check):
        self.name = name
        self.description = description
        self.check = check
        super(Condition, self).__init__({
            "name": self.name,
            "description": self.description,
            "check": self.check
        })

    def checkit(self, response):
        try:
            validate(response, self.check)
            return True, None
        except (ValidationError, SchemaError) as e:
            return False, str(e)

def parse_json(_json):
    """parse json to get caseses"""
    cases = _json.get("cases", [])
    _checks = []
    for _case in cases:
        url = _case.get("url")
        method = _case.get("method", "GET")
        payload = _case.get("payload", {})
        headers = _case.get("headers", {})
        cons = _case.get("checks", [])
        _conditions = []
        for _condition in cons:
            name = _condition.get("name")
            desc = _condition.get("description")
            check = _condition.get("check")
            condition = Condition(name, desc, check)
            _conditions.append(condition)
        check = Case(url, method=method, payload=payload, headers=headers, conditions=_conditions)
        _checks.append(check)
    return _checks


def run(file_path):
    _json = json_from_file(file_path)
    cases = parse_json(_json)
    flags = []
    for case in cases:
        _flag = case.run_case()
        flags.append(_flag)
    return all(flags)