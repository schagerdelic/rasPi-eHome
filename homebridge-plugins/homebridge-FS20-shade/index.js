//var PythonShell = require('python-shell');
var eHome = require('../eHome');


var Service, Characteristic;


	module.exports = function(homebridge){
		Service = homebridge.hap.Service;
		Characteristic = homebridge.hap.Characteristic;
		homebridge.registerAccessory("homebridge-FS20-shade", "FS20Shade", FS20ShadeAccessory);
	}


	function FS20ShadeAccessory(log, config) {
		this.log = log;

		// url info

		this.name                   = config["name"];
		this.systemName             = config["systemName"];
		
		this.targetPos = 55;
		this.currentPos = 55;
		this.posState = 2;
		
		this.service = new Service.WindowCovering (this.name);
		//this.service = new Service.Window (this.name);

		//this.log(this.service, "Hello this is Gerhard");

		this.service
			.getCharacteristic(Characteristic.TargetPosition)
			.on('get', this.getTargetPos.bind(this))
			.on('set', this.setTargetPos.bind(this));
		this.service
			.getCharacteristic(Characteristic.CurrentPosition)
			.on('get', this.getCurrentPos.bind(this));
		this.service
			.getCharacteristic(Characteristic.PositionState)
			.on('get', this.getPosState.bind(this));
			


	}
/*
	FS20ShadeAccessory.prototype.runMakro = function(deviceName,cmd){
		var pyOptions ={scriptPath: '/home/pi/eHome/homeputer_HomematicOnly/Monitoring/', args:[deviceName+cmd] };
		PythonShell.run('runMakro.py',pyOptions, function (err) {if (err) console.log(err); console.log('runMakro DONE');});
	}
*/

	FS20ShadeAccessory.prototype.getServices = function() {
		this.log("GETSERVICES:");
		return [this.service];
	}


// TARGETPOS = 0 ... geschlossen
// TARGETPOS = 100...offen
	FS20ShadeAccessory.prototype.getTargetPos = function(callback) {
		this.log("GET TARGET POS:");
		callback(null, this.targetPos);
	}

	FS20ShadeAccessory.prototype.setTargetPos = function(pos, callback) {
		this.log("SET TARGET POS:", pos);
		this.targetPos = pos;
		if (pos == 100) {
			//this.currentPos = 0;
			eHome.runMakro(this.systemName,"Auf");
		}
		else {
			//this.currentPos = 1;
			eHome.runMakro(this.systemName,"Zu")
		}
		callback(0);
	}

	FS20ShadeAccessory.prototype.getCurrentPos = function(callback) {
		this.log("GET CURRENT POS:");
		callback(null, this.currentPos);
	}


//Characteristic.PositionState.DECREASING = 0;
//Characteristic.PositionState.INCREASING = 1;
//Characteristic.PositionState.STOPPED = 2;
	FS20ShadeAccessory.prototype.getPosState = function(callback) {
		this.log("GET POS STATE:");
		callback(0, this.posState);
	}

