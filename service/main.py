from flask import Flask

from service.dtos.states import StatesReq, StatesResp
from service.util.objects import ObjectsFactory
import os

app = Flask(__name__)

objects_factory = ObjectsFactory()
objects_factory.initialize()

@app.route("/")
def main():
    req = StatesReq()
    resp = StatesResp()

    objects_factory.get_states_dao().find_all(req, resp)

    results = {}
    results.update({"data": resp.__dict__})

    return results


if __name__ == "__main__":
    print("hello")
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5052)))