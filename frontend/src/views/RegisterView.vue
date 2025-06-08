<template>
  <div class="register-page-content">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>用户注册</span>
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
          <el-button type="primary" @click="onSubmit">注册</el-button>
          <el-button @click="goToLogin">已有账号？去登录</el-button>
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
  name: 'RegisterView',
  setup() {
    const router = useRouter()
    const form = reactive({
      username: '',
      password: '',
    })

    const onSubmit = async () => {
      try {
        const response = await axios.post('http://localhost:5000/api/register', form)
        if (response.status === 201) {
          ElMessage.success('注册成功！')
          router.push('/login')
        } else {
          ElMessage.error(response.data.error || '注册失败')
        }
      } catch (error: any) {
        console.error('Registration error:', error)
        ElMessage.error(error.response?.data?.error || '注册过程中发生错误')
      }
    }

    const goToLogin = () => {
      router.push('/login')
    }

    return {
      form,
      onSubmit,
      goToLogin,
    }
  },
})
</script>

<style scoped>
.register-page-content {
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