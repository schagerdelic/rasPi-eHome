//var PythonShell = require('python-shell');
var eHome = require('../eHome');

var Service, Characteristic;


	module.exports = function(homebridge){
		Service = homebridge.hap.Service;
		Characteristic = homebridge.hap.Characteristic;
		homebridge.registerAccessory("homebridge-FS20-light", "FS20light", FS20LightAccessory);
	}


	function FS20LightAccessory(log, config) {
		this.log = log;

		// url info

		this.name                   = config["name"];
		this.systemName                   = config["systemName"];
		
		this.service = new Service.Lightbulb(this.name);

		//this.log(this.service, "Hello this is Gerhard");

		this.service
			.getCharacteristic(Characteristic.On)
			.on('get', this.getOn.bind(this))
			.on('set', this.setOn.bind(this));

	}
/*
	FS20LightAccessory.prototype.runMakro = function(deviceName,cmd){
		var pyOptions ={scriptPath: '/home/pi/eHome/homeputer_HomematicOnly/Monitoring/', args:[deviceName+cmd] };
		PythonShell.run('runMakro.py',pyOptions, function (err) {if (err) console.log(err); console.log('runMakro DONE');});
	}
*/

	FS20LightAccessory.prototype.getServices = function() {
		this.log("GETSERVICES:");
		return [this.service];
	}

	FS20LightAccessory.prototype.getOn = function(callback) {
		this.log("GETON:");
		var on = true;
		callback(null, on);
	}

	FS20LightAccessory.prototype.setOn = function(on, callback) {
		this.log("SETON:", on);
		if (on)
			eHome.runMakro(this.systemName,"An");
		else
			eHome.runMakro(this.systemName,"Aus");
		
		callback(0);
	}

/*
	FS20LightAccessory.prototype = {


	setPowerState: function(powerOn, callback) {
	this.log("POWERON:", powerOn);
		
		if (powerOn) {
			this.log("Setting power state to on", powerOn);
		} else {
			this.log("Setting power state to off", powerOn);
		}
		
	
	},
  
  getPowerState: function(callback) {
	this.log("Getting power state");
	
  },


	identify: function(callback) {
		this.log("myFS20 Identify requested!");
		callback(); // success
	},

	getServices: function() {
		
			return [this.service];
	}
};
*/
