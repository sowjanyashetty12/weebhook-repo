
from datetime import datetime
from flask import Flask, jsonify, request, json,render_template
from db_connection import store_event,collection

app=Flask(__name__)


@app.route("/")
def landingpage():
    return render_template("index.html")


@app.route("/webhook" ,methods=["POST"])
def eventcheck():
   print(request.headers)
   event_type = request.headers.get('X-GitHub-Event')


   if event_type=="push":
    jsondata=request.form.get('payload')
    # print(jsondata)
    data=json.loads(jsondata)
    author_name=data["pusher"]["name"]
    branch_name = data['ref'].split('/')[-1]
    time=data["head_commit"]["timestamp"]
    print(type(time))
    hash=data["head_commit"]["id"]
    eventdetails ={'request_id':hash,'author':author_name,'action':event_type,'from_branch':branch_name,'to_branch':branch_name,
                  'time_stamp':time}
    store_event(eventdetails)
    print(f"{author_name} pushed to {branch_name} on {time}")


    
   elif event_type=="pull_request":
    
    jsondata=request.form.get('payload')
    # print(jsondata)
    data=json.loads(jsondata)
    author = data['pull_request']['user']['login']
    from_branch = data['pull_request']['head']['ref']
    to_branch = data['pull_request']['base']['ref']
    timestamp = data['pull_request']['created_at']
    pullrequestid=data['pull_request']['id']
    
    
    if  data["action"] == "closed" and data["pull_request"]["merged"]:
     event_type="merge"
     eventdetails ={'request_id':pullrequestid,'author':author,'action':event_type,'from_branch':from_branch,'to_branch':to_branch,
                  'time_stamp':timestamp}
     print(event_type)
     store_event(eventdetails)
     print(f"{author} merged branch {from_branch} to {to_branch} on {timestamp}")
    else: 
     eventdetails ={'request_id':pullrequestid,'author':author,'action':event_type,'from_branch':from_branch,'to_branch':to_branch,
                  'time_stamp':timestamp}
     store_event(eventdetails)
     print(f"{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}")
    
    # for merge
   elif event_type == "pull_request" and data["action"] == "closed" and data["pull_request"]["merged"]:
    author = data['pull_request']['user']['login']
    from_branch = data['pull_request']['head']['ref']
    to_branch = data['pull_request']['base']['ref']
    timestamp = data['pull_request']['merged_at']
    store_event(eventdetails)
    print(f"{author} merged branch {from_branch} to {to_branch} on {timestamp}")
    eventdetails ={'request_id':pullrequestid,'author':author,'action':event_type,'from_branch':from_branch,'to_branch':to_branch,
                  'time_stamp':timestamp}
        
    
   return event_type


@app.route('/events', methods=['GET'])
def get_latest_events():
    # Query MongoDB to get the latest events
    latest_events = list(collection.find().sort('time_stamp',-1).limit(5))
    # latest_events_sorted = sorted(latest_events, key=lambda x: datetime.strptime(x['time_stamp'], '%Y-%m-%dT%H:%M:%S%z'), reverse=True)
    for event in latest_events:
     event['_id'] = str(event['_id'])
     
    #  print(latest_events)
    return json.dumps(latest_events)
if __name__=="__main__":
    app.run(debug=True)
