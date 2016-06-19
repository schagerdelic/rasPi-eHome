var PythonShell = require('python-shell');


var Service, Characteristic;


	module.exports = function(homebridge){
		Service = homebridge.hap.Service;
		Characteristic = homebridge.hap.Characteristic;
		homebridge.registerAccessory("homebridge-HM-thermostat", "HMThermostat", HMThermostatAccessory);
	}


	function HMThermostatAccessory(log, config) {
		this.log = log;

		// url info

		this.name                   = config["name"];
		this.systemName             = config["systemName"];
		
		this.targetState = 3;
		this.currentState= 3;
		
		this.targetTemp = 22.2;
		this.currentTemp = 19.9;
		
		this.dispUnits = 0;
		
		this.currentHumidity = 66.6;
		
		this.service = new Service.Thermostat (this.name);
		//this.service = new Service.Window (this.name);

		this.log(this.service, "Hello this is Gerhard");

		this.service
			.getCharacteristic(Characteristic.TargetHeatingCoolingState)
			.on('get', this.getTargetHeatingCoolingState.bind(this))
			.on('set', this.setTargetHeatingCoolingState.bind(this));
		this.service
			.getCharacteristic(Characteristic.CurrentHeatingCoolingState)
			.on('get', this.getCurrentHeatingCoolingState.bind(this));
		this.service
			.getCharacteristic(Characteristic.CurrentTemperature)
			.on('get', this.getCurrentTemperature.bind(this));			
		this.service
			.getCharacteristic(Characteristic.TargetTemperature)
			.on('get', this.getTargetTemperature.bind(this))
			.on('set', this.setTargetTemperature.bind(this));
		this.service
			.getCharacteristic(Characteristic.TemperatureDisplayUnits)
			.on('get', this.getTemperatureDisplayUnits.bind(this))
			.on('set', this.setTemperatureDisplayUnits.bind(this));
		this.service
			.getCharacteristic(Characteristic.CurrentRelativeHumidity)
			.on('get', this.getCurrentRelativeHumidity.bind(this));

	}

	HMThermostatAccessory.prototype.runMakro = function(deviceName,cmd){
		var pyOptions ={scriptPath: '/home/pi/eHome/homeputer_HomematicOnly/Monitoring/', args:[deviceName+cmd] };
		PythonShell.run('runMakro.py',pyOptions, function (err) {if (err) console.log(err); console.log('runMakro DONE');});
	}


	HMThermostatAccessory.prototype.getServices = function() {
		this.log("GETSERVICES:");
		return [this.service];
	}



	HMThermostatAccessory.prototype.getTargetHeatingCoolingState = function(callback) {
		this.log("GET TARGET HEAT COOL:");
		callback(null, this.targetState);
	}

	HMThermostatAccessory.prototype.setTargetHeatingCoolingState = function(state, callback) {
		this.log("SET TARGET HEAT COOL:", state);
		this.targetState = state;
		callback(0);
	}
	
	HMThermostatAccessory.prototype.getCurrentHeatingCoolingState = function(callback) {
		this.log("GET CUR HEAT COOL:");
		callback(null, this.currentState);
	}

	HMThermostatAccessory.prototype.getTargetTemperature = function(callback) {
		this.log("GET TARGET TEMP:");
		callback(null, this.targetTemp);
	}

	HMThermostatAccessory.prototype.setTargetTemperature = function(temp, callback) {
		this.log("SET TARGET TEMP:", temp);
		this.targetTemp = temp;
		callback(0);
	}

	HMThermostatAccessory.prototype.getTemperatureDisplayUnits = function(callback) {
		this.log("GET TARGET UNIT:");
		callback(null, this.dispUnits);
	}

	HMThermostatAccessory.prototype.setTemperatureDisplayUnits = function(units, callback) {
		this.log("SET TARGET HUNIT:", units);
		this.dispUnits = units;
		callback(0);
	}

	HMThermostatAccessory.prototype.getCurrentTemperature = function(callback) {
		this.log("GET CUR TEMP");
		callback(null, this.currentTemp);
	}

	HMThermostatAccessory.prototype.getCurrentRelativeHumidity = function(callback) {
		this.log("GET CUR HUMID:");
		callback(null, this.currentHumidity);
	}

// SET TARGET HEAT COOL: 0..off
// SET TARGET HEAT COOL: 1..heat
// SET TARGET HEAT COOL: 2..cool
// SET TARGET HEAT COOL: 3..auto

// UNITS: 0..Celsius
// UNITS: 1..Fahrenheit
/*
setInterval(function() {
  
  FAKE_SENSOR.randomizeTemperature();
  
  // update the characteristic value so interested iOS devices can get notified
  console.log("CurrentTemperature: RANDOM SET");
  sensor
    .getService(Service.Thermostat)
    .setCharacteristic(Characteristic.CurrentTemperature, 17.7);
    //.setCharacteristic(Characteristic.CurrentTemperature, FAKE_SENSOR.currentTemperatur);
  
}, 3000);
*/
