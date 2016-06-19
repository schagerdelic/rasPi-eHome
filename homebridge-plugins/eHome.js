var PythonShell = require('python-shell');
var mutex = require( 'node-mutex' )();
 
 
mutex.lock( 'key', function( err, unlock ) {
  if ( err ) {
  	console.error( err );
  	console.error( 'Unable to acquire lock' );
  }
  //synchronized code block 
 
  unlock();
});




var eHome = module.exports = function eHome () {

};

eHome.pincode = "012-33-210";
eHome.cnt = 0;

eHome.runMakro = function(deviceName,cmd){

	mutex.lock( 'eHomeRunMakro', function( err, unlock ) {
	  if ( err ) {
		console.error( err );
		console.error( 'Unable to acquire lock' );
	  }
	  // synchronized code block 
		console.log('runMakro:', deviceName, cmd);
		var pyOptions ={scriptPath: '/home/pi/eHome/homeputer_HomematicOnly/Monitoring/', args:[deviceName+cmd] };
		PythonShell.run('runMakro.py',pyOptions, 
			function (err) {					// called after py script finished
				if (err) console.log(err); 
				console.log('runMakro DONE');
				eHome.cnt = eHome.cnt + 1;
				console.log('runMakro:', eHome.cnt); 
				unlock();						// only release lock after py script finished
			});
	});

}

