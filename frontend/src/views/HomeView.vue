<template>
  <div class="home">
    <h1>欢迎来到食品入库与过期记录系统</h1>
    <p>这是一个简化版的首页。</p>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'HomeView',
})
</script>

<style scoped>
.home {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
</style> 