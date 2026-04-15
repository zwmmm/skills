<template>
  <view class="flex flex-col h-screen bg-gray-50">
    <!-- 导航栏 -->
    <wd-navbar
      :title="pageTitle"
      left-icon="back"
      @click-left="goBack"
    />

    <!-- 主容器 -->
    <scroll-view class="flex-1 overflow-y-auto" scroll-y>
      <view class="p-4">
        <!-- 页面标题（可选） -->
        <view v-if="showHeader" class="text-center mb-8">
          <text class="text-2xl font-bold text-gray-900">{{ headerTitle }}</text>
          <text v-if="headerSubtitle" class="block text-sm text-gray-500 mt-2">{{ headerSubtitle }}</text>
        </view>

        <!-- 表单 -->
        <wd-form
          ref="formRef"
          :model="formData"
          :rules="rules"
          class="form-wrapper"
        >
          <!-- 表单项占位符 - 实际使用时替换为具体表单项 -->
          <!-- {{FORM_ITEMS}} -->

          <!-- 示例表单项 -->
          <wd-form-item label="示例字段" prop="exampleField">
            <wd-input
              v-model="formData.exampleField"
              placeholder="请输入内容"
              clearable
            />
          </wd-form-item>

          <!-- 提交按钮 -->
          <view class="mt-8">
            <wd-button
              block
              type="primary"
              size="large"
              :loading="loading"
              @click="handleSubmit"
            >
              {{ submitText }}
            </wd-button>
          </view>

          <!-- 底部链接（可选） -->
          <view v-if="showFooterLink" class="text-center mt-4">
            <text
              class="text-sm text-blue-500"
              @click="handleFooterLinkClick"
            >
              {{ footerLinkText }}
            </text>
          </view>
        </wd-form>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { FormInstance } from 'wot-design-uni'

// ==================== 配置项 ====================
// 以下变量可根据实际需求修改

const pageTitle = ref('表单页面')
const showHeader = ref(true)
const headerTitle = ref('填写信息')
const headerSubtitle = ref('请完善以下信息')
const submitText = ref('提交')
const showFooterLink = ref(false)
const footerLinkText = ref('其他操作')

// ==================== 状态管理 ====================

const formRef = ref<FormInstance>()
const loading = ref(false)

// 表单数据 - 根据实际需求定义字段
const formData = ref({
  exampleField: '',
  // 添加更多字段
  // {{FORM_DATA}}
})

// 表单验证规则
const rules = {
  exampleField: [
    { required: true, message: '该字段不能为空' }
  ],
  // 添加更多验证规则
  // {{FORM_RULES}}
}

// ==================== 方法 ====================

/**
 * 表单提交处理
 */
const handleSubmit = async () => {
  try {
    // 1. 验证表单
    await formRef.value?.validate()

    // 2. 开始加载
    loading.value = true

    // 3. 提交数据到服务器
    // {{SUBMIT_LOGIC}}
    const res = await uni.request({
      url: '/api/submit', // 替换为实际接口
      method: 'POST',
      data: formData.value
    })

    // 4. 处理成功响应
    uni.showToast({
      title: '提交成功',
      icon: 'success',
      duration: 2000
    })

    // 5. 延迟后跳转或关闭页面
    setTimeout(() => {
      uni.navigateBack()
      // 或跳转到其他页面
      // uni.redirectTo({ url: '/pages/success/index' })
    }, 1000)

  } catch (error: any) {
    // 处理验证失败或请求错误
    console.error('表单提交失败:', error)

    uni.showToast({
      title: error.message || '提交失败',
      icon: 'error',
      duration: 2000
    })
  } finally {
    loading.value = false
  }
}

/**
 * 返回上一页
 */
const goBack = () => {
  uni.navigateBack()
}

/**
 * 底部链接点击处理
 */
const handleFooterLinkClick = () => {
  // 根据实际需求处理
  // 例如：跳转到忘记密码、注册页面等
  // uni.navigateTo({ url: '/pages/other/index' })
  console.log('底部链接被点击')
}

// ==================== 生命周期 ====================

/**
 * 页面加载时
 * 可以在这里接收路由参数、初始化数据等
 */
// onLoad((options) => {
//   // 接收路由参数
//   if (options.id) {
//     // 根据 id 加载数据
//   }
// })
</script>

<style scoped>
.form-wrapper {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

/* 自定义样式根据需要添加 */
/* 优先使用 UnoCSS 原子类而非自定义样式 */
</style>
