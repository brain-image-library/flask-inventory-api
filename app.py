import os
import json
import urllib.request
from flask import Flask, request, redirect, abort

app = Flask(__name__)

server = "https://download.brainimagelibrary.org/inventory/"


@app.route("/", methods=["GET"])
def hello():
    return redirect("https://www.brainimagelibrary.org")


@app.route("/assets", methods=["GET"])
def list():
    # Get the input string from the URL
    filename = "list"

    # Define the URL where the JSON file is located
    path = f"{server}{filename}.json"
    print(path)

    # Check if the JSON file exists at the given URL
    try:
        urllib.request.urlopen(path)
    except urllib.error.HTTPError as e:
        # The file doesn't exist
        return "JSON file not found at {}".format(path)
    else:
        # The file exists, so download it
        json_data = urllib.request.urlopen(path).read()

        # load it into a python dict
        json_dict = json.loads(json_data)
        data = json_dict

        return data


@app.route("/asset", methods=["GET"])
def get():
    # Get the input string from the URL
    filename = request.args.get("filename")
    query = request.args.get("query")

    if filename is None:
        abort(404)

    # Define the URL where the JSON file is located
    path = f"{server}{filename}.json"
    print(path)

    # Check if the JSON file exists at the given URL
    try:
        urllib.request.urlopen(path)
    except urllib.error.HTTPError as e:
        # The file doesn't exist
        return "JSON file not found at {}".format(path)
    else:
        # The file exists, so download it
        json_data = urllib.request.urlopen(path).read()

        # load it into a python dict
        json_dict = json.loads(json_data)

        # Extract the json block
        if query:
            data = json_dict[query]
        else:
            data = json_dict

        # Save the downloaded JSON file in the app's directory
        with open(filename + ".json", "wb") as f:
            f.write(json_data)

        return data


if __name__ == "__main__":
    app.run(debug=True)
