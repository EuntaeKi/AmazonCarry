/* Written By: 	  Euntae Ki
 * Functionality: Hosts a web server, establishes bidirectional communication 
 * 		  between the server & the client, and the python script & the server.
 *		  The data will be transferred in JSON format for both communication.
 *
 */

// Importing relevant Libraries & Background Process
const express = require("express");
const WebSocket = require('ws');
const http = require("http");
const app = express();
const server = http.createServer(app);
const { spawn } = require('child_process');
const py = spawn('python3', ["./setup.py"]);

// Constant Declaration
const port = 3300;
var realtimeDistance = 0;
var cameraDetected = false;
var detectCue = false;

var dataToClient = JSON.stringify(
	{
		"distance": realtimeDistance,
		"camera": cameraDetected,
		"detectCue": detectCue
	});


// Data Interpretation of Python Script
py.stdout.on('data', (data) => {
	console.log("Data from Python: " + data);
	var dataFromPy = JSON.parse(data);
	realtimeDistance = dataFromPy["distance"];
	cameraDetected = dataFromPy["camera"];
	detectCue = dataFromPy["detectCue"];
});

py.stdout.on('end', function(){
 	//console.log("Python input ended");
});

py.on('close', function(){
	//console.log("Python connection closed");
});

// WebSocket Input Handler
const wss = new WebSocket.Server({ port: 3301 });

function updateClientData() {
	dataToClient = JSON.stringify(
	{
		"distance": Math.round(realtimeDistance * 100) / 100,
		"camera": cameraDetected,
		"detectCue": detectCue
	});
}

wss.on('connection', function connection(ws) {
	console.log("Client Connected");
	
	// Update current distance data to debug console
	setInterval(() => updateClientData(), 50);
	setInterval(() => ws.send(dataToClient), 50);

	// Parse the data recieved from the client and pipe it accordingly
	ws.onmessage = function(event) {
		var msg = JSON.parse(event.data);
		var type = msg.type;
		var data = msg.data;
		switch(type) {
			case "customDistance":
				//console.log("customDistance Data: " + data);
				const distanceDataToPy = JSON.stringify(
				{
					type: "customDistance",
					data: data
				})
				py.stdin.write(distanceDataToPy + "\n");
				break;
			case "control":
				//console.log("control Data: " + data);
				const controlDataToPy = JSON.stringify(
				{
					type: "control",
					data: data
				})
				py.stdin.write(controlDataToPy + "\n");
				break;
			case "manual":
				//console.log("manual Data: " + data);
				const manualDataToPy = JSON.stringify(
				{
					type: "manual",
					data: data
				})
				py.stdin.write(manualDataToPy + "\n");
				break
			case "detectCue":
				//console.log("detectCue Data: " + data);
				const detectCueDataToPy = JSON.stringify(
				{
					type: "detectCue",
					data: data
				})
				py.stdin.write(detectCueDataToPy + "\n");
				break
			default:
				//console.log("Error: Such type is not considered");
		}
	};
});

server.listen(port, () => console.log(`Listening on port ${port}`));
