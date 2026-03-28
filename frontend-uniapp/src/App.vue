<script setup lang="ts">
import { onLaunch } from "@dcloudio/uni-app"
onLaunch(() => {
  // App launched
})
</script>

<style>
page {
  background-color: #FFF8DC;
  font-family: system-ui, -apple-system, sans-serif;
  -webkit-tap-highlight-color: transparent;
  color: #1C1917;
}

* {
  box-sizing: border-box;
}

button::after {
  border: none;
}

/* 全局按钮样式优化 */
button {
  outline: none;
  appearance: none;
}

/* placeholder样式 */
::-webkit-input-placeholder {
  color: #D8BFD8;
}

:-moz-placeholder {
  color: #D8BFD8;
}

::-moz-placeholder {
  color: #D8BFD8;
}

:-ms-input-placeholder {
  color: #D8BFD8;
}
</style>
