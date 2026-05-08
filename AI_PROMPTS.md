# Agent 交互日志

**团队名称：** CodeWithAI_Team
**成员名单：** 成员1, 成员2, 成员3
**使用的 AI Coding Agent 工具：** Claude Code

---

## 🤖 交互记录

### 第一次对话：项目初始化

**用户提示词：**
> 请使用 Streamlit 写一个看板，帮我读取当前目录下的 `data/signal_samples.csv`，在网页上加个大标题，然后用 st.map() 把数据里的纬度(Latitude)和经度(Longitude)画在地图上。

**AI 回复：**
[AI 生成了初始的 Streamlit 应用框架]

---

### 第二次对话：添加数据加载和缓存

**用户提示词：**
> 帮我用 pandas 读取 CSV 数据，并且添加 @st.cache_data 装饰器来缓存数据，加快加载速度。

**AI 回复：**
[AI 添加了 load_data 函数和缓存装饰器]

---

### 第三次对话：实现信号热力地图配色

**用户提示词：**
> 请在地图上根据 RSRP_dBm 的值来给点上色：大于 -90dBm 显示绿色，小于 -110dBm 显示红色，中间值显示黄色。使用 pydeck 的 ScatterplotLayer 来实现。

**AI 回复：**
[AI 添加了 get_color_by_rsrp 函数和 pydeck ScatterplotLayer]

---

### 第四次对话：添加数据统计图表

**用户提示词：**
> 在地图下方添加两个图表：一个是柱状图统计各频段(Band)的基站数量，另一个是饼图显示不同终端类型(TerminalType)的占比。

**AI 回复：**
[AI 使用 plotly.express 添加了柱状图和饼图]

---

### 第五次对话：实现侧边栏筛选功能

**用户提示词：**
> 在网页左侧添加一个侧边栏，包含一个下拉菜单用来筛选频段(Band)，和一个滑动条用来筛选 RSRP 范围。当用户调整筛选器时，右侧的地图和图表要实时更新。

**AI 回复：**
[AI 添加了 st.sidebar 和筛选逻辑]

---

### 第六次对话：实现3D地图

**用户提示词：**
> 请添加一个 3D 地图视图，让信号点以柱状图的形式"站起来"，柱子的高度随下载速率(Download_Mbps)变化，颜色仍然根据 RSRP 显示。

**AI 回复：**
[AI 使用 pydeck ColumnLayer 实现了 3D 地图]

---

### 第七次对话：添加单元测试

**用户提示词：**
> 请帮我生成一份单元测试文件 test_app.py，包含对 load_data 函数和 get_color_by_rsrp 函数的测试用例，以及数据完整性校验测试。

**AI 回复：**
[AI 生成了 pytest 测试文件]

---

### 第八次对话：修复运行错误和优化

**用户提示词：**
> 运行时报错了，提示 pydeck 缺少 mapbox token。帮我修改代码，使用免费的 mapbox 样式或者添加错误处理。

**AI 回复：**
[AI 添加了 map_style 配置和错误处理逻辑]

---

## 📝 关键提示词模板

```markdown
# 基础功能提示词
"请使用 Streamlit + pandas 读取 data/signal_samples.csv 数据"

# 地图可视化提示词
"使用 pydeck ScatterplotLayer 绘制散点图，根据 RSRP_dBm 配色"

# 图表统计提示词
"用 plotly express 创建柱状图统计 Band 分布，创建饼图统计终端类型"

# 筛选器提示词
"在 st.sidebar 添加 selectbox 筛选频段，slider 筛选 RSRP 范围"

# 3D 效果提示词
"用 pydeck ColumnLayer 实现 3D 柱状图，高度对应 Download_Mbps"

# 测试提示词
"用 pytest 编写单元测试，测试数据加载和颜色函数"
```

## 🎯 AI 使用心得

1. **明确输入输出**：告诉 AI 输入是什么（哪个 CSV 文件）、输出要什么（什么样的图表）
2. **渐进式迭代**：先实现基础功能，再逐步添加高级特性
3. **提供具体技术栈**：指定使用 pydeck、plotly、streamlit 等具体库
4. **描述预期效果**：如"红色表示信号弱，绿色表示信号强"
5. **让 AI 修错误**：直接复制报错信息给 AI，它能帮你定位和修复

---

*本日志由 Claude Code 辅助生成，记录了使用自然语言指挥 AI 编程的完整过程。*