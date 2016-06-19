
var net = require('net');



function FHEMInterface(){
	this.client = new net.Socket();
	
}

FHEMInterface.prototyp.connect = function(){
	
	console.log('START')
	var fhem_host = '127.0.0.1';
	var fhem_port = 7072; 

	this.client.connect(fhem_port, fhem_host, function() {
		console.log("CONNECT")
		client.write('\n\n\n')
		//client.write('exit')
		//client.destroy();
	}); 
	

}

client.on('connection', function(){
	console.log('connected')
}); 

client.on('data', function(data){
	console.log('DATA: ' + data);
}); 

client.on('error', function(error){
	console.log(error)
});

var sendCmd = function (cmd){
	client.write(cmd)
}

var destroy = function (cmd){
	client.destroy()
}

module.exports = {
	connect : connect,
	sendCmd : sendCmd,
	destroy : destroy
}

