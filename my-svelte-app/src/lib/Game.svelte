<script lang="ts">
    import { onMount } from "svelte";
    import Phaser from "phaser";
  
    let game: Phaser.Game | null = null;
  
    onMount(() => {
      const config: Phaser.Types.Core.GameConfig = {
        type: Phaser.AUTO,
        width: 800,
        height: 600,
        parent: "game-container",
        scene: {
          preload,
          create,
          update
        }
      };
  
      game = new Phaser.Game(config);
  
      function preload(this: Phaser.Scene) {
        this.load.image("logo", "https://labs.phaser.io/assets/sprites/phaser3-logo.png");
      }
  
      function create(this: Phaser.Scene) {
        const logo = this.add.image(400, 300, "logo");
        this.tweens.add({
          targets: logo,
          y: 500,
          duration: 2000,
          yoyo: true,
          repeat: -1
        });
      }
  
      function update(this: Phaser.Scene) {
        // 每帧更新逻辑
      }
  
      // 清理，防止热更新内存泄漏
      return () => {
        if (game) {
          game.destroy(true);
          game = null;
        }
      };
    });
  </script>
  
  <div id="game-container" style="width: 100%; height: 100%;"></div>
  