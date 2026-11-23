// Из-под labadmin: проверка и удаление лишнего действия remove
db = db.getSiblingDB("hotel_lab13");
printjson(db.getRole("roomEditor",{showPrivileges:true}));
db.updateRole("roomEditor",{privileges:[{resource:{db:"hotel_lab13",collection:"rooms"},actions:["find","insert","update"]}]});
// Затем под editor13: db.rooms.deleteOne({roomNo:303}) -> Unauthorized
