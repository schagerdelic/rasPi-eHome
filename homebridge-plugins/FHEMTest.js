var fhem = require("./FHEMInterface.js");


fhem.connect();


fhem.sendCmd('get');


fhem.destroy();



