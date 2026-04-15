---
name: uniapp-ui
description: "UniApp + UnoCSS + WotUI page generator from designs. Converts screenshots or HTML/CSS to UniApp pages. Features: intelligent component mapping with priority (custom components, then WotUI, then built-in), 6 page templates (form, list, detail, tab, search, grid), auto-analyze custom components, cross-platform compatibility checks. Use for: creating UniApp pages, converting designs to code, mobile app/mini-program/H5 development. Actions: generate, create, build, convert, analyze, design. Tech: Vue3, UnoCSS, Wot Design Uni, UniApp."
---

# UniApp UI - 设计稿到 UniApp 代码生成器

## 概述

这个 skill 可以将设计稿（文本描述、HTML/CSS）自动转换为 UniApp + UnoCSS + Wot Design Uni 的生产就绪代码。通过智能组件映射和页面模板系统，快速生成跨平台兼容的移动应用页面。

### 核心功能

1. **智能组件映射** - 自动识别 HTML/CSS 并映射到 WotUI 组件或自定义组件
2. **页面模板系统** - 6 种基础模板（表单、列表、详情、Tab、搜索、网格）
3. **自定义组件分析** - 自动扫描项目组件并优先使用
4. **跨平台兼容** - 生成的代码支持 H5、微信小程序、App
5. **最佳实践内置** - 自动应用 Vue3、UnoCSS、UniApp 最佳实践

## 前置要求

确保已安装 Python 3.8+：

```bash
python3 --version
```

如未安装，请按以下方式安装：

**macOS:**
```bash
brew install python3
```

**Ubuntu/Linux:**
```bash
sudo apt-get update && sudo apt-get install python3 python3-pip
```

**Windows:**
下载并安装 Python from https://www.python.org/downloads/

## 使用流程

### 7 步工作流

#### Step 1: 分析设计输入

**输入方式:**
- 文本描述（如："创建一个登录页面，包含用户名、密码输入框和登录按钮"）
- HTML/CSS 代码片段
- 设计要求文档

**分析内容:**
- 页面类型（form/list/detail/tab/search/grid）
- 所需组件（button/input/cell/etc）
- 布局结构
- 交互需求

**示例:**
```
用户: 我需要一个商品列表页，包含搜索框、商品卡片（图片、标题、价格），支持下拉刷新和上拉加载更多。
```

#### Step 2: 选择页面模板

使用搜索引擎匹配最合适的模板：

```bash
python3 scripts/search.py "list refresh load-more" --domain template
```

**6 个可用模板:**
1. **form-page** - 表单页（登录、注册、设置、反馈）
2. **list-page** - 列表页（新闻、订单、商品、聊天）
3. **detail-page** - 详情页（商品详情、文章、用户资料）
4. **tab-page** - Tab 页（首页、分类）
5. **search-page** - 搜索页（搜索结果、筛选）
6. **grid-page** - 网格页（分类网格、相册）

#### Step 3: 映射组件

**优先级系统:**
1. **自定义组件** (Priority 1) - 项目中的自定义组件
2. **WotUI 组件** (Priority 2) - Wot Design Uni 组件库
3. **UniApp 内置组件** (Priority 3) - view/text/image 等
4. **直接实现** (Fallback) - 使用 UnoCSS + 基础组件

**搜索命令:**

```bash
# 搜索自定义组件（如果已运行 analyze_components.py）
python3 scripts/search.py "product card" --domain custom

# 搜索 WotUI 组件
python3 scripts/search.py "button primary" --domain wotui
python3 scripts/search.py "input text field" --domain wotui
python3 scripts/search.py "list cell" --domain wotui

# 搜索 UnoCSS 样式模式
python3 scripts/search.py "card container" --domain unocss

# 搜索最佳实践
python3 scripts/search.py "navigation" --domain best-practice
```

#### Step 4: 生成代码

基于选定的模板和组件映射生成完整的 .vue 文件：

**生成内容包括:**
- 完整的 Vue3 SFC 结构（`<template>`, `<script setup>`, `<style scoped>`）
- UnoCSS 原子化样式类
- WotUI 或自定义组件
- 响应式数据和方法
- UniApp 生命周期钩子（onLoad, onShow, onReady）
- 错误处理和加载状态
- 跨平台兼容代码

#### Step 5: 应用最佳实践

自动检查并应用最佳实践：

```bash
# 搜索相关最佳实践
python3 scripts/search.py "form validation" --domain best-practice
python3 scripts/search.py "list performance" --domain best-practice
```

**检查项包括:**
- UniApp 跨平台兼容性
- Vue3 Composition API 规范
- UnoCSS 原子类使用
- WotUI 组件正确集成
- 性能优化（虚拟列表、懒加载）

#### Step 6: 质量检查

运行质量检查清单（见下文"质量检查清单"章节）。

#### Step 7: 输出代码

提供完整的、生产就绪的 .vue 文件代码。

---

## 自定义组件分析

### 为什么需要自定义组件分析？

如果你的项目已经有自定义组件（如 ProductCard、UserAvatar），应该优先使用这些组件而不是重复实现。

### 如何使用

**扫描项目并生成组件映射:**

```bash
# 分析项目组件
python3 scripts/analyze_components.py /path/to/your/uniapp-project

# 指定输出文件
python3 scripts/analyze_components.py /path/to/your/uniapp-project -o data/components.csv
```

**脚本会:**
1. 扫描项目 `components/` 目录下的所有 .vue 文件
2. 提取组件元数据（Props、Emits、Slots、CSS 类名）
3. 生成 `components.csv` 文件
4. 自动赋予最高优先级（Priority 1）

**生成的 components.csv 示例:**
```csv
No,Component Name,File Path,HTML Pattern,CSS Classes,Props,Slots,Events,Use Case,Category,Code Example,Priority
1,ProductCard,components/ProductCard.vue,<view class='product-card'>,product-card card-item,{"title":"string","price":"number","image":"string"},default,"click","商品展示卡片",card,"<ProductCard :title='商品' :price='99.9' />",1
```

---

## 搜索命令参考

### 5 个搜索域

| 域名 | 用途 | CSV 文件 | 示例查询 |
|------|------|---------|---------|
| `custom` | 自定义组件 | components.csv | "product card image" |
| `wotui` | WotUI 组件 | wotui.csv | "button primary large" |
| `template` | 页面模板 | templates.csv | "form login submit" |
| `unocss` | UnoCSS 模式 | unocss-patterns.csv | "flex center card" |
| `best-practice` | 最佳实践 | best-practices.csv | "navigation storage" |

### 搜索语法

```bash
# 基础搜索
python3 scripts/search.py "<query>" --domain <domain>

# 限制结果数量
python3 scripts/search.py "<query>" --domain <domain> -n 5

# JSON 输出
python3 scripts/search.py "<query>" --domain <domain> --json
```

### 搜索示例

**搜索 WotUI 组件:**
```bash
# 按钮组件
python3 scripts/search.py "button primary action" --domain wotui

# 输入框组件
python3 scripts/search.py "input text clearable" --domain wotui

# 列表单元格
python3 scripts/search.py "cell list item link" --domain wotui

# 表单组件
python3 scripts/search.py "form validation" --domain wotui
```

**搜索页面模板:**
```bash
# 表单页模板
python3 scripts/search.py "form login register" --domain template

# 列表页模板
python3 scripts/search.py "list scroll refresh" --domain template

# 详情页模板
python3 scripts/search.py "detail product image" --domain template
```

**搜索样式模式:**
```bash
# 布局模式
python3 scripts/search.py "flex center" --domain unocss
python3 scripts/search.py "card container shadow" --domain unocss

# 按钮样式
python3 scripts/search.py "button full-width" --domain unocss
```

**搜索最佳实践:**
```bash
# 导航相关
python3 scripts/search.py "navigation" --domain best-practice

# 存储相关
python3 scripts/search.py "storage" --domain best-practice

# 性能优化
python3 scripts/search.py "performance list" --domain best-practice
```

---

## 质量检查清单

### UniApp 跨平台兼容性
- [ ] 使用 `<view>`, `<text>`, `<image>` 等 UniApp 组件
- [ ] 避免使用 Web-only 标签（div, span, a）
- [ ] 使用 `uni.*` API 而非 Web API（如 `uni.navigateTo` 代替 `router.push`）
- [ ] 图片路径使用相对路径或 HTTPS URL
- [ ] 避免 Web-only 事件（如 onMouseOver）

### Vue 3 Composition API
- [ ] 使用 `<script setup>` 语法
- [ ] Props 使用 `defineProps<T>()`
- [ ] Emits 使用 `defineEmits<T>()`
- [ ] 响应式数据使用 `ref()` 或 `reactive()`
- [ ] 计算值使用 `computed()`
- [ ] 生命周期钩子：onLoad, onShow, onReady, onHide, onUnload

### UnoCSS 原子化样式
- [ ] 优先使用原子类而非内联样式
- [ ] 使用响应式类（sm: md: lg:）
- [ ] 使用语义化颜色或直接颜色值
- [ ] 间距使用一致的比例（p-4, m-2, gap-4）
- [ ] 避免不必要的任意值 `[value]`

### WotUI 组件集成
- [ ] 组件导入正确
- [ ] Props 名称和类型匹配文档
- [ ] 事件绑定使用 `@event-name`
- [ ] 使用组件提供的 TypeScript 类型
- [ ] 主题定制使用 CSS 变量

### 代码质量
- [ ] 表单有验证规则
- [ ] 适当的 TypeScript 类型注解

---

## 完整使用示例

### 示例 1: 创建登录页面

**Step 1: 描述需求**
```
创建一个登录页面，包含：
- 用户名输入框
- 密码输入框（隐藏字符）
- "记住我"复选框
- 登录按钮（全宽、主色调）
- "忘记密码"链接
```

**Step 2: 选择模板**
```bash
python3 scripts/search.py "form login" --domain template
# 结果: form-page (表单页模板)
```

**Step 3: 搜索组件**
```bash
# 搜索输入框
python3 scripts/search.py "input text" --domain wotui
# 结果: wd-input

# 搜索密码框
python3 scripts/search.py "input password" --domain wotui
# 结果: wd-input (type="password")

# 搜索复选框
python3 scripts/search.py "checkbox" --domain wotui
# 结果: wd-checkbox

# 搜索按钮
python3 scripts/search.py "button primary block" --domain wotui
# 结果: wd-button
```

**Step 4: 生成代码**

生成的 login.vue:
```vue
<template>
  <view class="flex flex-col h-screen bg-gray-50">
    <wd-navbar title="登录" />

    <scroll-view class="flex-1" scroll-y>
      <view class="p-4">
        <view class="text-center mb-8">
          <text class="text-2xl font-bold text-gray-900">欢迎回来</text>
        </view>

        <wd-form ref="formRef" :model="formData" :rules="rules">
          <wd-form-item label="用户名" prop="username">
            <wd-input
              v-model="formData.username"
              prefix-icon="user"
              placeholder="请输入用户名"
              clearable
            />
          </wd-form-item>

          <wd-form-item label="密码" prop="password">
            <wd-input
              v-model="formData.password"
              type="password"
              prefix-icon="lock"
              placeholder="请输入密码"
            />
          </wd-form-item>

          <wd-form-item>
            <wd-checkbox v-model="remember">记住我</wd-checkbox>
          </wd-form-item>

          <wd-button
            block
            type="primary"
            :loading="loading"
            @click="handleLogin"
          >
            登录
          </wd-button>

          <view class="text-center mt-4">
            <text
              class="text-blue-500"
              @click="goToForgotPassword"
            >
              忘记密码？
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

const formRef = ref<FormInstance>()
const loading = ref(false)
const remember = ref(false)

const formData = ref({
  username: '',
  password: ''
})

const rules = {
  username: [
    { required: true, message: '用户名不能为空' }
  ],
  password: [
    { required: true, message: '密码不能为空' },
    { min: 6, message: '密码至少6个字符' }
  ]
}

const handleLogin = async () => {
  try {
    await formRef.value?.validate()
    loading.value = true

    // 登录逻辑
    const res = await uni.request({
      url: '/api/login',
      method: 'POST',
      data: formData.value
    })

    // 保存 token
    uni.setStorageSync('token', res.data.token)

    // 跳转到首页
    uni.switchTab({ url: '/pages/index/index' })
  } catch (error) {
    uni.showToast({
      title: '登录失败',
      icon: 'error'
    })
  } finally {
    loading.value = false
  }
}

const goToForgotPassword = () => {
  uni.navigateTo({ url: '/pages/forgot-password/index' })
}
</script>
```

**Step 5: 检查最佳实践**
```bash
python3 scripts/search.py "form validation navigation" --domain best-practice
```

**Step 6: 质量检查**
- ✅ 使用 UniApp 组件（view, text, scroll-view）
- ✅ 使用 `<script setup>` 和 TypeScript
- ✅ 表单验证规则完整
- ✅ 错误处理（try-catch）
- ✅ 使用 `uni.*` API（navigateTo, switchTab, setStorageSync）
- ✅ 原子化 UnoCSS 类

---

## 资源说明

### scripts/
可执行脚本，用于搜索和分析：

- **core.py** - BM25 搜索引擎核心
- **search.py** - CLI 搜索接口
- **analyze_components.py** - 自定义组件分析器

### data/
CSV 数据库文件：

- **wotui.csv** - Wot Design Uni 组件映射（70+ 组件）
- **components.csv** - 自定义组件映射（自动生成）
- **templates.csv** - 页面模板元数据
- **unocss-patterns.csv** - UnoCSS 常用模式
- **uni-components.csv** - UniApp 内置组件
- **best-practices.csv** - 最佳实践指南

### templates/
页面模板文件：

- **form-page.vue** - 表单页模板
- **list-page.vue** - 列表页模板
- **detail-page.vue** - 详情页模板
- **tab-page.vue** - Tab 页模板
- **search-page.vue** - 搜索页模板
- **grid-page.vue** - 网格页模板

### references/
参考文档（按需加载）：

- **wotui-api.md** - Wot Design Uni API 完整参考
- **unocss-presets.md** - UnoCSS 预设和快捷方式
- **uni-lifecycle.md** - UniApp 生命周期详解

---

## 常见问题

### Q: 如何添加新的自定义组件到映射？
A: 重新运行 analyze_components.py 脚本，它会自动扫描并更新 components.csv。

### Q: 生成的代码在小程序上报错怎么办？
A: 检查是否使用了 Web-only API 或组件。运行质量检查清单中的跨平台兼容性检查。

### Q: 如何自定义组件样式？
A: 使用 UnoCSS 原子类或添加 scoped 样式。避免直接修改 WotUI 组件内部样式。

### Q: 支持暗黑模式吗？
A: Wot Design Uni 支持暗黑模式。使用 CSS 变量进行主题定制。

### Q: 如何优化长列表性能？
A: 搜索最佳实践 `python3 scripts/search.py "list performance" --domain best-practice`，考虑使用虚拟滚动或分页加载。
