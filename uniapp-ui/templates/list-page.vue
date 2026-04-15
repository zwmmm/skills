<template>
  <view class="flex flex-col h-screen bg-gray-50">
    <!-- 导航栏 -->
    <wd-navbar
      :title="pageTitle"
      :left-icon="showBackButton ? 'back' : ''"
      @click-left="goBack"
    />

    <!-- 搜索栏（可选） -->
    <view v-if="showSearch" class="search-bar bg-white px-4 py-2">
      <wd-search
        v-model="searchText"
        placeholder="搜索..."
        @search="handleSearch"
        @clear="handleSearchClear"
      />
    </view>

    <!-- 列表内容 -->
    <wd-pull-refresh
      v-model="refreshing"
      @refresh="onRefresh"
      class="flex-1"
    >
      <scroll-view
        class="h-full overflow-y-auto"
        scroll-y
        @scrolltolower="onReachBottom"
      >
        <!-- 列表项 -->
        <view v-if="list.length > 0" class="list-content">
          <view
            v-for="item in list"
            :key="item.id"
            class="list-item"
            @click="handleItemClick(item)"
          >
            <!-- 列表项占位符 - 实际使用时替换为具体内容 -->
            <!-- {{LIST_ITEM_TEMPLATE}} -->

            <!-- 示例：使用 wd-cell -->
            <wd-cell
              :title="item.title"
              :value="item.value"
              :label="item.label"
              is-link
              center
            >
              <!-- 自定义图标或图片 -->
              <template v-if="item.image" #icon>
                <image
                  class="w-40px h-40px rounded mr-3"
                  :src="item.image"
                  mode="aspectFill"
                />
              </template>
            </wd-cell>
          </view>
        </view>

        <!-- 空状态 -->
        <view v-else-if="!loading && list.length === 0" class="empty-container">
          <wd-empty :description="emptyText" />
        </view>

        <!-- 加载更多状态 -->
        <view v-if="loadingMore" class="loading-more text-center py-4">
          <wd-loading type="circular" />
          <text class="text-sm text-gray-500 ml-2">加载中...</text>
        </view>

        <!-- 没有更多数据 -->
        <view v-if="!hasMore && list.length > 0" class="no-more text-center py-4">
          <text class="text-sm text-gray-400">已加载全部</text>
        </view>
      </scroll-view>
    </wd-pull-refresh>
  </view>
</template>

<script setup lang="ts">
import { ref, onLoad } from 'vue'

// ==================== 配置项 ====================

const pageTitle = ref('列表页面')
const showBackButton = ref(true)
const showSearch = ref(true)
const emptyText = ref('暂无数据')
const pageSize = ref(10) // 每页数据量

// ==================== 状态管理 ====================

// 列表数据
const list = ref<any[]>([])

// 搜索关键词
const searchText = ref('')

// 分页参数
const page = ref(1)
const hasMore = ref(true)

// 加载状态
const loading = ref(false)
const refreshing = ref(false)
const loadingMore = ref(false)

// ==================== 方法 ====================

/**
 * 加载列表数据
 * @param isRefresh 是否为下拉刷新
 */
const loadList = async (isRefresh = false) => {
  // 防止重复加载
  if (loading.value || loadingMore.value) return

  // 如果没有更多数据且不是刷新，直接返回
  if (!hasMore.value && !isRefresh) return

  try {
    // 设置加载状态
    if (isRefresh) {
      refreshing.value = true
      page.value = 1
      list.value = []
      hasMore.value = true
    } else if (page.value === 1) {
      loading.value = true
    } else {
      loadingMore.value = true
    }

    // 发起请求
    // {{LOAD_DATA_LOGIC}}
    const response = await uni.request({
      url: '/api/list', // 替换为实际接口
      data: {
        page: page.value,
        pageSize: pageSize.value,
        keyword: searchText.value
      }
    })

    // 处理响应数据
    const data = response.data?.data || []

    // 判断是否还有更多数据
    if (data.length < pageSize.value) {
      hasMore.value = false
    }

    // 更新列表
    if (isRefresh || page.value === 1) {
      list.value = data
    } else {
      list.value.push(...data)
    }

  } catch (error: any) {
    console.error('加载列表失败:', error)

    uni.showToast({
      title: error.message || '加载失败',
      icon: 'error',
      duration: 2000
    })
  } finally {
    loading.value = false
    refreshing.value = false
    loadingMore.value = false
  }
}

/**
 * 下拉刷新
 */
const onRefresh = () => {
  loadList(true)
}

/**
 * 上拉加载更多
 */
const onReachBottom = () => {
  if (hasMore.value && !loading.value && !loadingMore.value) {
    page.value++
    loadList()
  }
}

/**
 * 搜索
 */
const handleSearch = () => {
  page.value = 1
  hasMore.value = true
  loadList(true)
}

/**
 * 清空搜索
 */
const handleSearchClear = () => {
  searchText.value = ''
  handleSearch()
}

/**
 * 列表项点击
 */
const handleItemClick = (item: any) => {
  // 跳转到详情页
  // {{ITEM_CLICK_LOGIC}}
  uni.navigateTo({
    url: `/pages/detail/index?id=${item.id}`
  })
}

/**
 * 返回上一页
 */
const goBack = () => {
  uni.navigateBack()
}

// ==================== 生命周期 ====================

/**
 * 页面加载时
 */
onLoad((options) => {
  // 接收路由参数
  // if (options.keyword) {
  //   searchText.value = options.keyword
  // }

  // 加载初始数据
  loadList()
})
</script>

<style scoped>
.search-bar {
  border-bottom: 1px solid #f0f0f0;
}

.list-content {
  background-color: #ffffff;
}

.list-item {
  border-bottom: 1px solid #f5f5f5;
}

.list-item:last-child {
  border-bottom: none;
}

.empty-container {
  display: flex;
  align-items: center;
  justify-center;
  min-height: 400px;
}

.loading-more {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 优先使用 UnoCSS 原子类而非自定义样式 */
</style>
