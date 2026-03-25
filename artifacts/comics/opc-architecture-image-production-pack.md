# OPC 架构知识漫画｜真出图执行包

## 目标

把当前漫画素材包推进到可直接执行生图的阶段。

---

## 一、首批出图范围

建议先出这 4 张：

1. **封面**
2. **第 1 页**（复杂任务压境 + 启动 OPC）
3. **第 5 页**（8 槽并发 + 第 9 个排队）
4. **第 6 页**（自动回报 + CEO 收口）

原因：
- 最能代表整套视觉语言
- 最能验证核心架构点是否被读懂
- 最适合先定风格，再扩全书

---

## 二、建议生图顺序

### Step 1：封面
先锁定：
- CEO 形象
- 指挥室整体气质
- 中控台样式
- 8 个工作舱阵列感

### Step 2：第 1 页
锁定：
- 复杂任务风暴
- 启动时刻
- 三层结构亮相方式

### Step 3：第 5 页
锁定：
- 8 槽并发可视化
- 第 9 个排队任务拟人化风格
- 中控台 UI 语言

### Step 4：第 6 页
锁定：
- 自动回报视觉
- 结果回流路径
- CEO 最终收口主屏

---

## 三、推荐引用文件

- 主脚本：`artifacts/comics/opc-architecture-comic-script.md`
- 分镜表：`artifacts/comics/opc-architecture-storyboard-table.md`
- 角色锚点：`artifacts/comics/opc-architecture-character-bible.md`
- 全局 prompt：`artifacts/comics/opc-architecture-prompts.md`
- 分页 prompt：`artifacts/comics/opc-architecture-page-prompts.md`

---

## 四、建议输出目录

```text
artifacts/comics/renders/
  cover/
  page-01/
  page-05/
  page-06/
```

---

## 五、每页建议产量

为了先定风格，建议每个目标页先产：
- 2~4 张候选图

确认风格稳定后，再补其余页面。

---

## 六、执行建议

- 先用统一风格前缀出图
- 若角色漂移，先回到 character bible 做强化 prompt
- 若系统结构表达不清，优先增强构图说明，而不是堆术语
- 若页面太像海报，需补 panel composition 描述

---

## 七、完成定义

当前包交付到这一步时，已经满足：
- 可直接喂给 AI 生图
- 可按页执行第一轮视觉探索
- 可形成封面 + 关键页的第一版图片样张

下一步一旦开始跑图，就进入真正的图片成品阶段。
