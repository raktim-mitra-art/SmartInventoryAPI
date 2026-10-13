from flask import Flask,jsonify,request
from ai_module import analyze_feedback
import json

app = Flask(__name__)
DB_FILE="inventory.json"

def init_db():
    try:
        with open(DB_FILE,'r') as f:
            json.load(f)
    except:
        with open(DB_FILE,"w") as f:
            json.dump([],f)

init_db()


@app.route("/")
def home():
    return {"message":"Smart Inventory API is running"}

@app.route("/inventory",methods=["GET"])
def get_inventory():
    with open(DB_FILE,"r") as f:
        return jsonify(json.load(f))

@app.route("/add",methods=["POST"])
def add_item():
    item = request.get_json(silent=True)
    if not isinstance(item,dict):
        return jsonify({
            "success":False,
            "message":"please provide a valid json object"
        }),400
    with open(DB_FILE,"r",encoding="utf-8") as f:
        data=json.load(f)
    data.append(item)
    with open(DB_FILE,"w",encoding="utf-8") as f:
        json.dump(data,f,indent=4)
    return jsonify({"success": True, "message":"items added","item":item}),201

# inventory_data=[{
#     "ProductId":"P001",
#     "ProductName":"Copper Rod",
#     "Stock":120,
#     "Price":500
# },
# {
#     "ProductId":"P002",
#     "ProductName":"Aluminium Sheet",
#     "Stock":80,
#     "Price":800
# },
# ]

# @app.route("/inventory",methods=["GET"])
# def inventory():
    return inventory_data


@app.route("/feedback",methods=["POST"])
def feedback(): 
    data=request.get_json(silent=True)
    if not isinstance(data,dict):
        return jsonify({"error":"Provide valid json"}),400

    feedback_text=data.get("feedback","")
    if not isinstance(feedback_text,str) or not feedback_text.strip():
        return jsonify({"error":"Feedback text is required"}),401

    sentiment = analyze_feedback(feedback_text)

    return jsonify({
        "feedback":feedback_text,
        "sentiment_score":sentiment
    })




if __name__=="__main__":
    app.run(
        host="127.0.0.1",
        port=8000,
        debug=False
    )
