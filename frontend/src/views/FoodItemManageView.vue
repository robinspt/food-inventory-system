<template>
  <div class="food-item-manage-content">
    <h1>{{ isEditMode ? '编辑食品项' : '添加食品项' }}</h1>
    <FoodItemForm @submit="handleFormSubmit" :initialData="initialFormData" />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import FoodItemForm from '../components/FoodItemForm.vue'

interface FoodItem {
  id?: number;
  name: string;
  production_date: string;
  expiry_period_value: number;
  expiry_period_unit: string;
  quantity: number;
  storage_location: string;
  expiration_date?: string; // Optional for form, will be calculated by backend
  status?: string;
}

export default defineComponent({
  name: 'FoodItemManageView',
  components: {
    FoodItemForm,
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const isEditMode = computed(() => !!route.params.id)
    const initialFormData = ref<FoodItem>({} as FoodItem)

    const fetchFoodItem = async (id: number) => {
      try {
        console.log(`Fetching food item with ID: ${id}`);
        const response = await axios.get(`http://localhost:5000/api/food_items/${id}`)
        initialFormData.value = response.data
        console.log('Fetched initial form data:', initialFormData.value);
      } catch (error) {
        console.error('Error fetching food item:', error)
        ElMessage.error('获取食品项失败')
        router.push('/inventory') // Redirect if item not found
      }
    }

    onMounted(() => {
      console.log('FoodItemManageView mounted. isEditMode:', isEditMode.value, 'route.params.id:', route.params.id);
      if (isEditMode.value) {
        fetchFoodItem(Number(route.params.id))
      }
    })

    const handleFormSubmit = async (formData: FoodItem) => {
      try {
        if (isEditMode.value) {
          await axios.put(`http://localhost:5000/api/food_items/${route.params.id}`, formData)
          ElMessage.success('食品项更新成功！')
        } else {
          await axios.post('http://localhost:5000/api/food_items', formData)
          ElMessage.success('食品项添加成功！')
        }
        router.push('/inventory') // Redirect to inventory list after submission
      } catch (error: any) {
        console.error('Error submitting form:', error)
        ElMessage.error(error.response?.data?.error || '保存食品项失败')
      }
    }

    return {
      isEditMode,
      initialFormData,
      handleFormSubmit,
    }
  },
})
</script>

<style scoped>
.food-item-manage-content {
  display: flex;
  flex-direction: column;
  align-items: flex-start; /* Change to flex-start for top alignment */
  /* Removed max-width and margin: 0 auto; to allow filling App.vue el-main */
}

h1 {
  margin-bottom: 20px; /* Space between title and form */
}
</style> 