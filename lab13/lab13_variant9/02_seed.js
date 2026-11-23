db = db.getSiblingDB("hotel_lab13");
db.rooms.insertMany([
 {roomNo:101,type:"single",pricePerNight:50,status:"free"},
 {roomNo:102,type:"double",pricePerNight:70,status:"busy"},
 {roomNo:103,type:"double",pricePerNight:70,status:"free"},
 {roomNo:201,type:"suite",pricePerNight:150,status:"free"},
 {roomNo:202,type:"single",pricePerNight:55,status:"busy"},
 {roomNo:203,type:"double",pricePerNight:75,status:"cleaning"},
 {roomNo:301,type:"suite",pricePerNight:160,status:"free"},
 {roomNo:302,type:"double",pricePerNight:80,status:"busy"},
 {roomNo:303,type:"single",pricePerNight:60,status:"free"},
 {roomNo:304,type:"suite",pricePerNight:170,status:"maintenance"}]);
db.reservations.insertMany([
 {resId:1,roomNo:102,guest:"Guest A",paid:true},
 {resId:2,roomNo:202,guest:"Guest B",paid:false},
 {resId:3,roomNo:302,guest:"Guest C",paid:true},
 {resId:4,roomNo:201,guest:"Guest D",paid:false},
 {resId:5,roomNo:301,guest:"Guest E",paid:true},
 {resId:6,roomNo:103,guest:"Guest F",paid:true},
 {resId:7,roomNo:303,guest:"Guest G",paid:false},
 {resId:8,roomNo:101,guest:"Guest H",paid:true},
 {resId:9,roomNo:203,guest:"Guest I",paid:true},
 {resId:10,roomNo:304,guest:"Guest J",paid:false}]);
db.audit_events.insertMany([{event:"seed",source:"lab"},{event:"room_status_changed",roomNo:102}]);
