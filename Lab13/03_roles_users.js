db = db.getSiblingDB("hotel_lab13");
db.createRole({role:"roomViewer",roles:[],privileges:[{resource:{db:"hotel_lab13",collection:"rooms"},actions:["find"]}]});
db.createRole({role:"roomEditor",roles:[],privileges:[{resource:{db:"hotel_lab13",collection:"rooms"},actions:["find","insert","update","remove"]}]});
db.createRole({role:"eventAuditor",roles:[],privileges:[{resource:{db:"hotel_lab13",collection:"audit_events"},actions:["find"]}]});
db.createUser({user:"viewer13",pwd:passwordPrompt(),roles:[{role:"roomViewer",db:"hotel_lab13"}]});
db.createUser({user:"editor13",pwd:passwordPrompt(),roles:[{role:"roomEditor",db:"hotel_lab13"}]});
db.createUser({user:"auditor13",pwd:passwordPrompt(),roles:[{role:"eventAuditor",db:"hotel_lab13"}]});
