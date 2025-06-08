<template>
  <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
    <el-form-item label="食品名称" prop="name">
      <el-input v-model="form.name"></el-input>
    </el-form-item>

    <el-form-item label="日期输入方式">
      <el-radio-group v-model="form.dateInputType">
        <el-radio label="production_and_expiry">生产日期 + 保质期</el-radio>
        <el-radio label="direct_expiration">直接过期日期</el-radio>
      </el-radio-group>
    </el-form-item>

    <template v-if="form.dateInputType === 'production_and_expiry'">
      <el-form-item label="生产日期" prop="production_date">
        <el-date-picker
          v-model="form.production_date"
          type="date"
          placeholder="选择日期"
          value-format="YYYY-MM-DD"
        ></el-date-picker>
      </el-form-item>
      <el-form-item label="保质期" prop="expiry_period_value">
        <el-input-number v-model="form.expiry_period_value" :min="1"></el-input-number>
        <el-select v-model="form.expiry_period_unit" placeholder="选择单位" style="margin-left: 10px;">
          <el-option label="天" value="days"></el-option>
          <el-option label="月" value="months"></el-option>
        </el-select>
      </el-form-item>
    </template>

    <template v-else-if="form.dateInputType === 'direct_expiration'">
      <el-form-item label="过期日期" prop="expiration_date">
        <el-date-picker
          v-model="form.expiration_date"
          type="date"
          placeholder="选择日期"
          value-format="YYYY-MM-DD"
        ></el-date-picker>
      </el-form-item>
    </template>

    <el-form-item label="数量" prop="quantity">
      <el-input-number v-model="form.quantity" :min="1"></el-input-number>
    </el-form-item>
    <el-form-item label="存储位置" prop="storage_location">
      <el-input v-model="form.storage_location"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm">提交</el-button>
      <el-button @click="resetForm">重置</el-button>
    </el-form-item>
  </el-form>
</template>

<script lang="ts">
import { defineComponent, reactive, ref, watch } from 'vue'
import { ElForm, ElFormItem, ElInput, ElSelect, ElOption, ElDatePicker, ElInputNumber, ElButton, ElMessage, ElRadioGroup, ElRadio } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'

export default defineComponent({
  name: 'FoodItemForm',
  components: {
    ElForm,
    ElFormItem,
    ElInput,
    ElSelect,
    ElOption,
    ElDatePicker,
    ElInputNumber,
    ElButton,
    ElRadioGroup,
    ElRadio,
  },
  props: {
    initialData: {
      type: Object,
      default: () => ({}),
    },
  },
  emits: ['submit'],
  setup(props, { emit }) {
    const formRef = ref<FormInstance>()
    const form = reactive({
      name: '',
      dateInputType: 'production_and_expiry', // Default input type
      production_date: '',
      expiry_period_value: 1,
      expiry_period_unit: 'days',
      expiration_date: '',
      quantity: 1,
      storage_location: '',
    })

    const rules = reactive<FormRules>({
      name: [{ required: true, message: '请输入食品名称', trigger: 'blur' }],
      quantity: [{ required: true, message: '请输入数量', trigger: 'blur' }],
    })

    // Dynamic rules based on dateInputType
    watch(() => form.dateInputType, (newType) => {
      if (newType === 'production_and_expiry') {
        rules.production_date = [{ required: true, message: '请选择生产日期', trigger: 'change' }];
        rules.expiry_period_value = [{ required: true, message: '请输入保质期值', trigger: 'blur' }];
        rules.expiry_period_unit = [{ required: true, message: '请选择保质期单位', trigger: 'change' }];
        rules.expiration_date = []; // Remove direct expiration date rule
      } else {
        rules.production_date = []; // Remove production date rule
        rules.expiry_period_value = []; // Remove expiry period value rule
        rules.expiry_period_unit = []; // Remove expiry period unit rule
        rules.expiration_date = [{ required: true, message: '请选择过期日期', trigger: 'change' }];
      }
      // Trigger re-validation to apply new rules immediately
      formRef.value?.validateField(['production_date', 'expiry_period_value', 'expiry_period_unit', 'expiration_date']);
    }, { immediate: true }); // Run immediately on component mount

    watch(
      () => props.initialData,
      (newVal) => {
        if (newVal) {
          Object.assign(form, newVal)
          // Determine dateInputType based on initialData for editing mode
          if (newVal.expiration_date && !newVal.production_date) {
            form.dateInputType = 'direct_expiration';
          } else if (newVal.production_date && newVal.expiry_period_value && newVal.expiry_period_unit) {
            form.dateInputType = 'production_and_expiry';
          }
        }
      },
      { immediate: true }
    )

    const submitForm = async () => {
      if (!formRef.value) return
      try {
        await formRef.value.validate()
        const submittedData: any = { ...form };

        if (form.dateInputType === 'production_and_expiry') {
          delete submittedData.expiration_date;
        } else {
          delete submittedData.production_date;
          delete submittedData.expiry_period_value;
          delete submittedData.expiry_period_unit;
        }
        delete submittedData.dateInputType;
        emit('submit', submittedData)
        ElMessage.success('表单验证成功，数据已提交！')
      } catch (error) {
        ElMessage.error('表单验证失败，请检查输入！')
        console.error(error)
      }
    }

    const resetForm = () => {
      if (!formRef.value) return
      formRef.value.resetFields()
      form.dateInputType = 'production_and_expiry'; // Reset to default
    }

    return {
      formRef,
      form,
      rules,
      submitForm,
      resetForm,
    }
  },
})
</script>

<style scoped>
/* 可以添加一些样式 */
</style> 