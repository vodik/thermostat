function getSocket() {
  const ws_scheme = window.location.protocol === "https:" ? "wss:" : "ws:";
  const ws_uri = ws_scheme + "//" + window.location.host + "/api/v1/sensor/ws";
  return new WebSocket(ws_uri);
}

function poll() {
  const status = document.getElementById('status');
  const results = document.getElementById('results');

  const socket = getSocket();
  socket.onopen = function() {
      status.innerHTML = 'connected';
      status.style.color = 'green';
  }

  socket.onclose = function() {
      status.innerHTML = 'disconnected';
      status.style.color = 'red';
  }

  socket.onmessage = function(msg){
      const data = JSON.parse(msg.data);
      results.innerHTML = 'Temperature: ' + data.temperature.toFixed(1) + '°C';
      results.innerHTML += '<br>Humidity: ' + data.humidity.toFixed(1) + '%';
      results.innerHTML += '<br>Humidex factor: ' + data.humidex.toFixed(1);
      results.innerHTML += '<br>' + data.message;
  }
}

window.onload = poll;
