<template>
  <div class="inventory-list-content">
    <h1>食品库存列表</h1>
    <el-button type="primary" @click="goToAddFoodItem">添加食品项</el-button>
    <el-table :data="foodItems" style="width: 100%; margin-top: 20px;" border>
      <el-table-column prop="name" label="名称" width="180"></el-table-column>
      <el-table-column prop="quantity" label="数量" width="100"></el-table-column>
      <el-table-column prop="storage_location" label="存储位置" width="180"></el-table-column>
      <el-table-column prop="production_date" label="生产日期" width="150"></el-table-column>
      <el-table-column label="保质期值" width="100">
        <template #default="scope">
          {{ (scope.row.expiry_period_unit === 'days' || scope.row.expiry_period_unit === 'months') && scope.row.expiry_period_value > 0 ? scope.row.expiry_period_value : '-' }}
        </template>
      </el-table-column>
      <el-table-column label="保质期单位" width="120">
        <template #default="scope">
          <span v-if="scope.row.expiry_period_unit === 'days'">天</span>
          <span v-else-if="scope.row.expiry_period_unit === 'months'">月</span>
          <span v-else>-</span>
        </template>
      </el-table-column>
      <el-table-column prop="expiration_date" label="过期日期" width="150">
        <template #default="scope">
          <el-tag :type="getExpirationTagType(scope.row.expiration_date)">{{ scope.row.expiration_date }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'
import { format, parseISO, isPast, isBefore } from 'date-fns'

interface FoodItem {
  id: number;
  name: string;
  production_date: string;
  expiry_period_value: number;
  expiry_period_unit: string;
  quantity: number;
  storage_location: string;
  expiration_date: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export default defineComponent({
  name: 'InventoryListView',
  setup() {
    const router = useRouter()
    const foodItems = ref<FoodItem[]>([])

    const fetchFoodItems = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/food_items')
        foodItems.value = response.data.map((item: FoodItem) => ({ ...item, production_date: format(parseISO(item.production_date), 'yyyy-MM-dd'), expiration_date: format(parseISO(item.expiration_date), 'yyyy-MM-dd') }))
      } catch (error) {
        console.error('Error fetching food items:', error)
        ElMessage.error('获取食品列表失败')
      }
    }

    const getExpirationTagType = (expirationDate: string) => {
      const today = new Date();
      const expDate = parseISO(expirationDate);
      const sevenDaysFromNow = new Date();
      sevenDaysFromNow.setDate(today.getDate() + 7);

      if (isPast(expDate) && !isBefore(expDate, today)) { // If today is the expiration date
        return 'danger';
      } else if (isPast(expDate)) { // If already expired
        return 'info';
      } else if (isBefore(expDate, sevenDaysFromNow)) { // Expiring within 7 days
        return 'warning';
      } else {
        return ''; // Default type (green/success)
      }
    };

    const handleEdit = (row: FoodItem) => {
      // ElMessage.info(`编辑食品项: ${row.name}`)
      router.push({ path: `/manage-food-item/${row.id}` });
    }

    const handleDelete = async (id: number) => {
      ElMessageBox.confirm(
        '确定要删除此食品项吗？',
        '警告',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        }
      )
        .then(async () => {
          try {
            await axios.delete(`http://localhost:5000/api/food_items/${id}`)
            ElMessage.success('删除成功！')
            fetchFoodItems() // Refresh list
          } catch (error) {
            console.error('Error deleting food item:', error)
            ElMessage.error('删除失败')
          }
        })
        .catch(() => {
          ElMessage.info('已取消删除')
        })
    }

    const goToAddFoodItem = () => {
      router.push('/add-food-item'); // Assuming you'll add a route for this
    }

    onMounted(() => {
      fetchFoodItems()
    })

    return {
      foodItems,
      handleEdit,
      handleDelete,
      goToAddFoodItem,
      getExpirationTagType
    }
  },
})
</script>

<style scoped>
.inventory-list-content {
  display: flex;
  flex-direction: column;
  align-items: flex-start; /* Change to flex-start for top alignment */
  padding: 20px;
  overflow-x: auto; /* 允许水平滚动 */
  /* Removed max-width and margin: 0 auto; to allow filling App.vue el-main */
}

h1 {
  margin-bottom: 20px; /* Space between title and button */
}
</style> 