const scoreSocket = new WebSocket(
  "ws://" + window.location.host + "/ws/score/",
);

scoreSocket.onmessage = (e) => {
  const data = JSON.parse(e.data);
  const message = data.message;

  console.log(`[Websocket message received: ${message}]`);
};

scoreSocket.onclose = () => {
  console.error("Score socket closed unexpectedly");
};

export function sendMessage(message) {
  scoreSocket.send(
    JSON.stringify({
      message: message,
    }),
  );
}
