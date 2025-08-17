<script lang="ts">
  import Game from "./lib/Game.svelte";

  let socket: WebSocket | null = null;

  function connect() {
    socket = new WebSocket("ws://localhost:8080");

    socket.onopen = () => console.log("connected");
    socket.onmessage = (event: MessageEvent) => {
      const data = JSON.parse(event.data);
      console.log("收到消息", data);
    };
  }

  connect();
</script>

<main>
  <div class="sidebar">
    <div>
      <input placeholder="输入消息..." />
      <button class="send-btn">send</button>
    </div>
  </div>

  <div class="game-area">
    <Game />
  </div>
</main>

<style>
  main {
    display: flex;
    height: 61vh;
  }
  .sidebar {
    display: flex;
    align-items: end;
    width: 260px;
    background: rgb(33, 33, 33);
    padding: 1rem;
  }
  .send-btn {
    /* margin-top: 10px; 上边距 */
    /* margin-bottom: 5px; 下边距 */
    margin-left: 8px;
    /* margin-right: 0; */
    /* 或者写成简写 */
    /* margin: 10px 0 5px 0; 上右下左 */
  }
  .game-area {
    flex: 1;
  }
</style>
