// Importing relevant Libraries
const express = require("express");
const WebSocket = require('ws');
const http = require("http");
const app = express();
const server = http.createServer(app);
const { spawn } = require('child_process');
const port = 3300;

var realtimeDistance = 0;

const py = spawn('python3', ["./setup.py"]);

py.stdout.on('data', (data) => {
	console.log("Data from Python: " + data);
	//var dataFromPy = JSON.parse(data);
	//console.log(dataFromPy["Distance"]);
});

py.stdout.on('end', function(){
 	console.log("Python input ended");
});

py.on('close', function(){
	console.log("Python connection closed");
});

const wss = new WebSocket.Server({
	port: 3301
});

// WebSocket Input Handler
wss.on('connection', function connection(ws) {
	console.log("Client Connected");
	
	// Update current distance data to debug console
	setInterval(() => ws.send(realtimeDistance), 250);

	// Parse the data recieved from the client and pipe it accordingly
	ws.onmessage = function(event) {
		var msg = JSON.parse(event.data);
		var type = msg.type;
		var data = msg.data;
		switch(type) {
			case "customDistance":
				console.log("customDistance Data: " + data);
				const distanceDataToPy = JSON.stringify(
				{
					type: "customDistance",
					data: data
				})
				py.stdin.write(distanceDataToPy + "\n");
				break;
			case "control":
				console.log("control Data: " + data);
				const controlDataToPy = JSON.stringify(
				{
					type: "control",
					data: data
				})
				py.stdin.write(controlDataToPy + "\n");
				break;
			case "manual":
				console.log("manual Data: " + data);
				const manualDataToPy = JSON.stringify(
				{
					type: "manual",
					data: data
				})
				py.stdin.write(manualDataToPy + "\n");
				break
			default:
				console.log("Error: Such type is not considered");
		}
	};
});

server.listen(port, () => console.log(`Listening on port ${port}`));
