
from datetime import datetime
from flask import Flask,request, json,render_template
from db_connection import store_event,collection
import logging
import pytz

app=Flask(__name__)
logging.basicConfig(level=logging.INFO)



@app.route("/")
def landingpage():
 app.logger.info("Accessed landing page")
 return render_template("index.html")


@app.route("/webhook" ,methods=["POST"])
def eventcheck():
 app.logger.info("Received webhook request")
 event_type = request.headers.get('X-GitHub-Event')


 if event_type=="push":
  jsondata=request.form.get('payload')
  data=json.loads(jsondata)
  author_name=data["pusher"]["name"]
  branch_name = data['ref'].split('/')[-1]
  time=data["head_commit"]["timestamp"]
  original_datetime = datetime.fromisoformat(time)
  formatted_date_time = original_datetime.strftime("%dth %B %Y - %I:%M%p")
  hash=data["head_commit"]["id"]
  eventdetails ={'request_id':hash,'author':author_name,'action':event_type,'from_branch':branch_name,'to_branch':branch_name,
                'time_stamp':formatted_date_time}
  store_event(eventdetails)
  app.logger.info(f"{author_name} pushed to {branch_name} on {formatted_date_time}")


    
 elif event_type=="pull_request":
    
  jsondata=request.form.get('payload')
  
  data=json.loads(jsondata)
  author = data['pull_request']['user']['login']
  from_branch = data['pull_request']['head']['ref']
  to_branch = data['pull_request']['base']['ref']
  timestamp = data['pull_request']['created_at']
  pullrequestid=data['pull_request']['id']
  utc_time_str = timestamp
  ist_timezone = pytz.timezone('Asia/Kolkata')
  utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.utc)
  ist_time = utc_time.astimezone(ist_timezone)
  day_of_month = ist_time.strftime("%d")
  if day_of_month.endswith("1") and day_of_month != "11":
        suffix = "st"
  elif day_of_month.endswith("2") and day_of_month != "12":
        suffix = "nd"
  elif day_of_month.endswith("3") and day_of_month != "13":
        suffix = "rd"
  else:
        suffix = "th"
  formatted_date_time = ist_time.strftime(f"%d{suffix} %B %Y - %I:%M%p")
  if  data["action"] == "closed" and data["pull_request"]["merged"]:
   event_type="merge"
   eventdetails ={'request_id':pullrequestid,'author':author,'action':event_type,'from_branch':from_branch,'to_branch':to_branch,
                  'time_stamp':formatted_date_time}
   store_event(eventdetails)
   app.logger.info(f"{author} merged branch {from_branch} to {to_branch} on {formatted_date_time}")
  else: 
   eventdetails ={'request_id':pullrequestid,'author':author,'action':event_type,'from_branch':from_branch,'to_branch':to_branch,
                  'time_stamp':formatted_date_time}
   store_event(eventdetails)
   app.logger.info(f"{author} submitted a pull request from {from_branch} to {to_branch} on {formatted_date_time}")
 return event_type


@app.route('/events', methods=['GET'])
def get_latest_events():
 app.logger.info("Retrieving latest events")
 latest_events = list(collection.find().sort('time_stamp',-1).limit(5))
 for event in latest_events:
  event['_id'] = str(event['_id'])
 return json.dumps(latest_events)
if __name__=="__main__":
 app.run(host='0.0.0.0', port=5001)

