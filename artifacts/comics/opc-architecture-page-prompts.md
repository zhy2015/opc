# OPC 架构知识漫画｜分页 Prompt 包

## 全局固定前缀

Use a consistent visual style across all pages: Chinese knowledge comic, clean futuristic sci-fi command center, cinematic infographic storytelling, semi-realistic illustration, high readability, stable character design, unified blue-gray palette with red warning accents, CEO as calm central strategist, control plane as orchestration console, child agents in isolated work pods, clear panel composition.

---

## 封面 Prompt

A Chinese knowledge comic cover about OPC architecture. One calm CEO stands in the central command room, facing a glowing orchestration control plane. Behind the CEO are eight illuminated independent work pods arranged in a precise arc. Outside the glass wall, a giant complex task storm approaches, with floating Chinese keywords like research, verification, analysis, writing, summary. Strong visual hierarchy, futuristic command center, clean sci-fi infographic style, blue-gray palette with red alert accents, highly polished and readable.

---

## 第 1 页 Prompt

A full comic page in a futuristic command center. Page theme: why OPC starts only for complex decomposable tasks. Show a giant complex task storm outside the command room, the CEO facing an overloaded main screen, two decision options (handle alone vs activate OPC), then pressing an activate OPC button, then a final panel showing the three-layer architecture: CEO session, control plane, child sessions x8. Chinese knowledge comic, cinematic infographic storytelling, clear narrative sequence, dramatic opening.

### 第 1 页重点
- 压力感
- 启动时刻
- “不是所有简单任务都要开 OPC”
- 三层结构首次亮相

---

## 第 2 页 Prompt

A Chinese knowledge comic page explaining the three-layer structure of OPC. The CEO breaks one large mission into multiple modular task cards. A control plane console routes these cards into different execution pods. Several child agents work in parallel in separate pods. Final panel clearly shows three layers: CEO for thinking and final synthesis, control plane for orchestration and collection, child sessions for isolated execution. Futuristic command room, infographic clarity, clean and structured layouts.

### 第 2 页重点
- CEO 思考与拆解
- Control Plane 调度而不思考
- Child 只做专项执行

---

## 第 3 页 Prompt

A Chinese knowledge comic page about independent sessions and isolated context. Three adjacent but isolated work pods, each with different task materials on screens, clearly separated by walls. One child agent notices a warning that says it only handles assigned work. The CEO dispatches different briefing packets from the control plane. Strong emphasis on isolated context, no shared mind, no cross-pod leakage. Clean sci-fi knowledge comic style.

### 第 3 页重点
- 独立 session = 独立上下文
- 不能共享脑
- CEO 必须精确分发上下文包

---

## 第 4 页 Prompt

A Chinese knowledge comic page focused on governance rules. A giant glowing rules board appears in the command room: only CEO can dispatch tasks. Arrows only flow from CEO to control plane to child pods. One child agent tries to press a nested spawn button and receives a bright red forbidden warning. The scene should strongly communicate no nested spawning, centralized control, and system stability. Futuristic system-governance comic style, strong red warning accents.

### 第 4 页重点
- 只有 CEO 能派单
- Child 不能再生 child
- 规则是为了防失控

---

## 第 5 页 Prompt

A Chinese knowledge comic page about concurrency slots. The control plane shows exactly eight active running slots. Eight work pods are occupied. A ninth task character holding a number 9 card waits in a clearly marked queue area. Then one finished pod releases a slot and the queued task enters. The page must clearly show that 8 is the maximum number of simultaneous child sessions, not the total number of tasks. Dynamic infographic comic style, clear flow arrows, fast rhythm.

### 第 5 页重点
- 8 = 同时运行上限
- 第 9 个排队
- 排队不等于失败

---

## 第 6 页 Prompt

A Chinese knowledge comic ending page about auto-reporting and final synthesis. Multiple completed child pods send result cards back through glowing pipelines into the control plane. The control plane categorizes and forwards them to the CEO. The CEO then assembles one unified final answer on the main screen. Final panel shows the complete stable system: CEO in the center, orchestration console in front, eight pods behind, calm and resolved atmosphere. Clean futuristic infographic storytelling, satisfying ending.

### 第 6 页重点
- Child 自动回报
- Control Plane 负责回收
- 最终答案只由 CEO 汇总形成

---

## 逐页负面约束

### 通用 negative prompt
- no fantasy armor
- no medieval aesthetics
- no messy chaotic composition
- no overly cartoonish chibi style
- no extra hidden child agents
- no control plane as humanoid character
- no child agents discussing globally together in one room

### 语义负面约束
- 不要把 CEO 画成亲手执行所有细节
- 不要把 control plane 画成第二个会思考的主角
- 不要把 child 画成共享一个上下文
- 不要把第 9 个任务画成失败或被驱逐
- 不要让 child 直接对外交付最终答案
