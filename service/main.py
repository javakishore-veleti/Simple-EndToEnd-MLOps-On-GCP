from flask import Flask, jsonify
from service.dtos.states import StatesReq, StatesResp
from service.util.objects import ObjectsFactory
import os

print("Hello World")
app = Flask(__name__)

# objects_factory = ObjectsFactory()
# objects_factory.initialize()


import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
)

LOGGER = logging.getLogger(__name__)


@app.route("/")
def main():
    resp = StatesResp()
    req = StatesReq()
    ObjectsFactory.get_instance().get_states_dao().find_all(req, resp)
    return jsonify({"status": "Success", "row_count": resp.row_count, "ctx_data": resp.ctx_data})

@app.route("/setup-cloud-local-envs", methods=["POST"])
def setup_cloud():
    resp = StatesResp()
    message = ObjectsFactory.get_instance().get_states_dao().setup_cloud_resources(resp)
    return jsonify({"status": "Success", "message": message, "ctx_data": resp.ctx_data})

@app.route("/find-states", methods=["GET"])
def find_states():
    resp = StatesResp()
    req = StatesReq()
    ObjectsFactory.get_instance().get_states_dao().find_all(req, resp)
    return jsonify({"status": "Success", "row_count": resp.row_count, "ctx_data": resp.ctx_data})


@app.route('/convert-csv-to-parquet', methods=['POST'])
def convert_csv_to_parquet():
    resp = StatesResp()
    req = StatesReq()
    return ObjectsFactory.get_instance().get_states_dao().convert_csv_to_parquet(req, resp)


@app.route('/upload-parquet', methods=['POST'])
def upload_parquet():
    LOGGER.info("Upload parquet Entered")
    resp = StatesResp()
    req = StatesReq()
    response = ObjectsFactory.get_instance().get_states_dao().upload_parquet(req, resp)

    LOGGER.info(f"Upload parquet Exiting response {response}")
    return response


app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5052)))

print(__name__)

