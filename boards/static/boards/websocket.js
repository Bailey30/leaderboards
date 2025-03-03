import { updateScoreList } from "./utils.js";

export class WebsocketManager {
  constructor(board_id) {
    console.log({ board_id });
    console.log("[Creating new websocket instance.]");

    const path =
      board_id || board_id === 0 ? `/ws/score/${board_id}/` : "/ws/score/";
    this.socket = new WebSocket("ws://" + window.location.host + path);

    this.socket.onopen = this.onOpen;
    this.socket.onclose = this.onClose;
    this.socket.onmessage = this.onMessage;
  }

  onOpen() {
    console.log("[Websocket connected.]");
  }

  onClose() {
    console.error("Score socket closed unexpectedly");
  }

  onMessage(e) {
    const data = JSON.parse(e.data);
    console.log({ data });
    const message = data.message;

    console.log(`[Websocket message received: ${JSON.stringify(message)}]`);

    updateScoreList(message);
  }

  sendMessage(message) {
    if (this.socket.readyState === WebSocket.OPEN) {
      console.log("Sending message.");

      this.socket.send(
        JSON.stringify({
          message,
        }),
      );
    }
  }
}

// if (!window.scoreSocket) {
//   console.log("[No window.scoreSocket. Connecting Now]");
//   const scoreSocket = new WebSocket(
//     "ws://" + window.location.host + "/ws/score/",
//   );
//
//   scoreSocket.onmessage = (e) => {
//     const data = JSON.parse(e.data);
//     const message = data.message;
//
//     console.log(`[Websocket message received: ${message}]`);
//   };
//
//   scoreSocket.onopen = () => {
//     console.log("[Websocket connected.]");
//   };
//
//   scoreSocket.onclose = () => {
//     console.error("Score socket closed unexpectedly");
//   };
//
//   window.scoreSocket = scoreSocket;
//   console.log(window.scoreSocket);
// } else {
//   console.log(["window.scoreSocket already conneted."]);
// }
//
// export function sendMessage() {
//   console.log("Sending message.");
//
//   const score_form = document.getElementById("score_form");
//   const { board_id, id_username, id_score } = score_form.elements;
//
//   scoreSocket.send(
//     JSON.stringify({
//       message: {
//         board_id: board_id.value,
//         username: id_username.value,
//         score: id_score.value,
//       },
//     }),
//   );
// }
