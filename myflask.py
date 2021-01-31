from flask import Flask
import json


class MyFlask(Flask):
    def process_response(self, response):
        resp = json.loads(response.get_data())
        resp.update({"status": response.status_code})
        response.set_data(json.dumps(resp))
        return super().process_response(response)
