from flask import Flask, render_template, request, jsonify
from azure_avatar import submit_job, check_job_status

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start_job", methods=["POST"])
def start_job():
    data = request.get_json()
    text = data.get("text")
    job_id = submit_job(text)
    return jsonify({"job_id": job_id})

@app.route("/check_job/<job_id>")
def check_job(job_id):
    status, video_url = check_job_status(job_id)
    return jsonify({"status": status, "video_url": video_url})

if __name__ == "__main__":
    app.run(debug=True)
