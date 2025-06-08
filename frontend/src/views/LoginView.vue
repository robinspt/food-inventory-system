<template>
  <div class="login-page-content">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>用户登录</span>
        </div>
      </template>
      <el-form :model="form" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="form.username"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input type="password" v-model="form.password"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">登录</el-button>
          <el-button @click="goToRegister">没有账号？去注册</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

export default defineComponent({
  name: 'LoginView',
  setup() {
    const router = useRouter()
    const form = reactive({
      username: '',
      password: '',
    })

    const onSubmit = async () => {
      try {
        const response = await axios.post('http://localhost:5000/api/login', form)
        if (response.status === 200) {
          ElMessage.success('登录成功！')
          // In a real app, you would store the token here
          router.push('/') // Redirect to home or dashboard
        } else {
          ElMessage.error(response.data.error || '登录失败')
        }
      } catch (error: any) {
        console.error('Login error:', error)
        ElMessage.error(error.response?.data?.error || '登录过程中发生错误')
      }
    }

    const goToRegister = () => {
      router.push('/register')
    }

    return {
      form,
      onSubmit,
      goToRegister,
    }
  },
})
</script>

<style scoped>
.login-page-content {
  display: flex;
  justify-content: center;
  align-items: flex-start; /* Align at the top of the available space */
  /* Removed max-width and margin: 0 auto; to allow filling App.vue el-main */
}

.box-card {
  width: 400px;
  max-width: 90%;
}

.card-header {
  font-size: 18px;
  font-weight: bold;
}
</style> 