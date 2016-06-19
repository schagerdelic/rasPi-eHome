var PythonShell = require('python-shell');
var net = require('net');
var fs = require('fs');

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
		this.sensorName             = config["sensorName"];
		this.targetName             = config["targetName"];
				
		this.targetState = 3;
		this.currentState= 3;
		
		this.targetTemp = 22.2;
		this.currentTemp = 19.9;
		
		this.dispUnits = 0;
		
		this.currentHumidity = 66.6;
		
		this.settingsFileName ='/var/www/html/eHome/eHomeSettings.json'
		this.heizungsValsFileName ='/var/www/html/eHome/eHomeHeizungVals.json'
		
		this.service = new Service.Thermostat (this.name);
		//this.service = new Service.Window (this.name);

		//this.log(this.service, "Hello this is Gerhard");

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


		this.service.getCharacteristic(Characteristic.TargetTemperature).props["minValue"] = 20;
		this.service.getCharacteristic(Characteristic.TargetTemperature).props["maxValue"] = 30;
				//
		//	FHEM Interface
		//
		console.log('START')
		var fhem_host = '127.0.0.1';
		var fhem_port = 7072; 
		
		this.client = new net.Socket();
		that = this;
	
		this.client.connect(fhem_port, fhem_host, function() {
			console.log("CONNECT")
			that.client.write('\n\n\n')
			//client.write('exit')
			//client.destroy();
		}); 
		
		this.client.on('data', this.receive.bind(this));
		

  		this.client.on('error', function(error){
			that.log("FHEM ERROR");
			that.log(error)
		});
	
		this.getTargetHeatingCoolingState();
		this.getCurrentHeatingCoolingState();
		this.getCurrentTemperature();
		this.getTargetTemperature();
		
		
	}

	HMThermostatAccessory.prototype.receive = function(data){
		//this.log('FHEM:' + data);
		//this.client.write('get sensor_bad param temperature');
	}

	HMThermostatAccessory.prototype.receiveCurTemp = function(data){
		this.log('FHEM Cur Temp:' + data);
		this.currentTemp = parseFloat(data);
		//this.service.setCharacteristic(Characteristic.CurrentTemperature, this.currentTemp);

	}

	HMThermostatAccessory.prototype.getServices = function() {
		this.log("GETSERVICES:");
		return [this.service];
	}



	HMThermostatAccessory.prototype.getTargetHeatingCoolingState = function(callback) {
		this.log("GET TARGET HEAT COOL:");
		var f = fs.readFileSync(this.settingsFileName).toString();
		var eHomeSettings = JSON.parse(f);
		//this.log("JSON");
		//this.log(eHomeSettings.HeizungAn);
		//this.log(eHomeSettings.HeizungsModus);
		if (eHomeSettings.HeizungAn == true) {
			if (eHomeSettings.HeizungsModus == "An")
				this.targetState = 1;
			if (eHomeSettings.HeizungsModus == "Kalender")
				this.targetState = 3;
		}
		else {
			this.targetState = 0;
		}
			
		if (callback)	
			callback(null, this.targetState);
	}

	HMThermostatAccessory.prototype.setTargetHeatingCoolingState = function(state, callback) {
		this.log("SET TARGET HEAT COOL:", state);
		this.targetState = state;
		
		var f = fs.readFileSync(this.settingsFileName).toString();
		var eHomeSettings = JSON.parse(f);
		//this.log(f);
		//this.log(eHomeSettings.HeizungAn);
		//this.log(eHomeSettings.HeizungsModus);

		if (state == 0)
			eHomeSettings.HeizungAn = false;
		
		if (state == 1) {		
			eHomeSettings.HeizungAn = true;
			eHomeSettings.HeizungsModus = "An";
		}
		
		if (state == 3) {
			eHomeSettings.HeizungAn = true;
			eHomeSettings.HeizungsModus = "Kalender";
		}

		f = JSON.stringify(eHomeSettings);
		//this.log(f);
		fs.writeFileSync(this.settingsFileName,f)
		
		callback(0);
	}
	
// SET TARGET HEAT COOL: 0..off
// SET TARGET HEAT COOL: 1..heat
// SET TARGET HEAT COOL: 2..cool
// SET TARGET HEAT COOL: 3..auto
	HMThermostatAccessory.prototype.getCurrentHeatingCoolingState = function(callback) { // here we could chek the FHEM get param if Heating is really on???
		this.log("GET CUR HEAT COOL:");

		var f = fs.readFileSync(this.settingsFileName).toString();
		var eHomeSettings = JSON.parse(f);
		//this.log("JSON");
		//this.log(eHomeSettings.HeizungAn);
		//this.log(eHomeSettings.HeizungsModus);
		if (eHomeSettings.HeizungAn == true) {
			if (eHomeSettings.HeizungsModus == "An")
				this.currentState = 1;
			if (eHomeSettings.HeizungsModus == "Kalender")
				this.currentState = 3;
		}
		else {
			this.currentState = 0;
		}
		
		this.currentState = 3; // here we could chek the FHEM get param if Heating is really on???
		
		if (callback)	
			callback(null, this.currentState);
	}

	HMThermostatAccessory.prototype.getTargetTemperature = function(callback) {
		this.log("GET TARGET TEMP:");
		var f = fs.readFileSync(this.settingsFileName).toString();
		var eHomeSettings = JSON.parse(f);
		
		this.targetTemp = parseFloat(eHomeSettings[this.targetName]);

		//this.log("STRING");
		//this.log(this.targetTemp);

		if (callback)	
			callback(null, this.targetTemp);
	}

	HMThermostatAccessory.prototype.setTargetTemperature = function(temp, callback) {
		this.log("SET TARGET TEMP:", temp);
		this.targetTemp = temp;

		var f = fs.readFileSync(this.settingsFileName).toString();
		var eHomeSettings = JSON.parse(f);
		
		eHomeSettings[this.targetName] = this.targetTemp.toString();
		
		f = JSON.stringify(eHomeSettings);
		fs.writeFileSync(this.settingsFileName,f)
		
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
		this.client.on('data', this.receiveCurTemp.bind(this));
		this.client.write('get ' + this.sensorName + ' param temperature\n');
		if (callback)	
			callback(null, this.currentTemp);
	}

	HMThermostatAccessory.prototype.getCurrentRelativeHumidity = function(callback) {
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
  
  //FAKE_SENSOR.randomizeTemperature();
  
  // update the characteristic value so interested iOS devices can get notified
  this.log("CurrentTemperature: RANDOM SET");
  sensor
    .getService(Service.Thermostat)
    .setCharacteristic(Characteristic.CurrentTemperature, 17.7);
    //.setCharacteristic(Characteristic.CurrentTemperature, FAKE_SENSOR.currentTemperatur);
  
}, 3000);
*/
