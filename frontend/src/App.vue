<template>
  <el-container>
    <el-header>
      <el-menu mode="horizontal" :router="true">
        <el-menu-item index="/">首页</el-menu-item>
        <el-menu-item index="/register">注册</el-menu-item>
        <el-menu-item index="/login">登录</el-menu-item>
        <el-menu-item index="/inventory">库存列表</el-menu-item>
        <el-menu-item index="/add-food-item">添加食品项</el-menu-item>
      </el-menu>
    </el-header>
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { ElContainer, ElHeader, ElMain, ElMenu, ElMenuItem } from 'element-plus'

export default defineComponent({
  name: 'App',
  components: {
    ElContainer,
    ElHeader,
    ElMain,
    ElMenu,
    ElMenuItem,
  },
})
</script>

<style scoped>
.el-header {
  padding: 0;
}

.el-menu--horizontal > .el-menu-item {
  height: 60px;
  line-height: 60px;
}

.el-main {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}
</style>
