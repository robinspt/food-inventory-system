<template>
  <el-card class="box-card notification-card">
    <template #header>
      <div class="card-header">
        <span>过期通知</span>
        <el-button class="button" text @click="fetchNotifications">刷新</el-button>
      </div>
    </template>
    <div v-if="notifications.length === 0" class="empty-notifications">
      <p>暂无过期或临期食品通知。</p>
    </div>
    <el-scrollbar v-else height="300px">
      <div v-for="item in notifications" :key="item.id" class="notification-item">
        <el-alert
          :title="getNotificationTitle(item)"
          :type="getNotificationType(item)"
          :closable="false"
          show-icon
        >
          <p>生产日期: {{ item.production_date }}</p>
          <p>保质期: {{ item.expiry_period_value }} {{ item.expiry_period_unit === 'days' ? '天' : '月' }}</p>
          <p>过期日期: {{ item.expiration_date }}</p>
          <p>数量: {{ item.quantity }}</p>
          <p>存储位置: {{ item.storage_location || 'N/A' }}</p>
        </el-alert>
      </div>
    </el-scrollbar>
  </el-card>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage, ElCard, ElButton, ElAlert, ElScrollbar } from 'element-plus'
import { format, parseISO, isPast, differenceInDays } from 'date-fns'

interface FoodItemNotification {
  id: number;
  name: string;
  production_date: string;
  expiry_period_value: number;
  expiry_period_unit: string;
  quantity: number;
  storage_location: string;
  expiration_date: string;
  status: string; // 'active', 'warning', 'expired'
}

export default defineComponent({
  name: 'NotificationList',
  components: {
    ElCard,
    ElButton,
    ElAlert,
    ElScrollbar,
  },
  setup() {
    const notifications = ref<FoodItemNotification[]>([])

    const fetchNotifications = async () => {
      try {
        const response = await axios.get<FoodItemNotification[]>('http://localhost:5000/api/notifications')
        notifications.value = response.data.map(item => ({
          ...item,
          production_date: format(parseISO(item.production_date), 'yyyy-MM-dd'),
          expiration_date: format(parseISO(item.expiration_date), 'yyyy-MM-dd'),
        }))
        if (notifications.value.length === 0) {
          ElMessage.info('暂无过期或临期食品通知。')
        } else {
          ElMessage.success('通知已更新。')
        }
      } catch (error) {
        console.error('Error fetching notifications:', error)
        ElMessage.error('获取通知失败')
      }
    }

    const getNotificationType = (item: FoodItemNotification) => {
      if (item.status === 'expired') {
        return 'error'
      } else if (item.status === 'warning') {
        return 'warning'
      } else {
        return 'info' // Default or for other statuses if applicable
      }
    }

    const getNotificationTitle = (item: FoodItemNotification) => {
      const expDate = parseISO(item.expiration_date);
      const today = new Date();

      if (item.status === 'expired') {
        return `已过期: ${item.name} (过期日期: ${item.expiration_date})`
      } else if (item.status === 'warning') {
        const daysLeft = differenceInDays(expDate, today);
        return `即将过期: ${item.name} (剩余 ${daysLeft} 天过期)`
      } else {
        return `通知: ${item.name}`
      }
    }

    onMounted(() => {
      fetchNotifications()
    })

    return {
      notifications,
      fetchNotifications,
      getNotificationType,
      getNotificationTitle,
    }
  },
})
</script>

<style scoped>
.notification-card {
  margin-top: 20px;
  width: 100%;
  max-width: 600px; /* Optional: limit width */
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
  font-weight: bold;
}

.notification-item {
  margin-bottom: 15px;
}

.empty-notifications {
  text-align: center;
  padding: 20px;
  color: #909399;
}
</style> 