# 本册资料来源与核验说明

**核验日期：2026 年 8 月 12 日。** 本册介绍的是模型家族和工程方法，不给厂商做总排名。论文中的实验结果只支持论文测试过的模型、数据和任务；模型更新后，结论的强弱可能变化。

## 模型家族、隐私与生命周期

- [NIST AI 风险管理框架](https://www.nist.gov/itl/ai-risk-management-framework)：用于 AI 系统生命周期、风险、人工监督和测试验证的通用边界。
- [NIST 隐私框架](https://www.nist.gov/privacy-framework)：支持隐私要从数据处理、治理和风险管理判断，而不能只由模型参数多少推出。

## 嵌入、语义检索与 RAG

- [Sentence-BERT 原始论文](https://aclanthology.org/D19-1410/)：支持把句子映射为可用余弦相似度比较的嵌入，并用于语义相似检索。
- [NeurIPS 2020：RAG 原始论文](https://papers.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html)：支持检索器与生成模型结合；论文使用开放域知识源，说明 RAG 并不只限于封闭的指定文件。
- [PMLR：RAG 知识源投毒与检测研究](https://proceedings.mlr.press/v318/moradi26a.html)：支持检索资料可能被污染、相关片段不自动等于权威事实。

## 微调、工具、智能体与上下文

- [LoRA 原始论文](https://arxiv.org/abs/2106.09685)：用于区分全量微调与冻结基础权重、训练新增适配参数的参数高效微调。
- [NIST 生成式 AI 风险管理框架 NIST AI 600-1](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)：用于生成式 AI 虚构、数据隐私、信息完整性和人类监督风险。
- [TACL 2024：Lost in the Middle](https://aclanthology.org/2024.tacl-1.9/)：在多文档问答和键值检索实验中发现，相关信息位置变化会显著影响一些长上下文模型的表现；支持“窗口放得下不等于每处都能稳健使用”。

## 怎样理解这些来源

“小模型”“大模型”“多模态”和“智能体”没有一个能覆盖全部产品的单一尺寸线或营销名称。隐私主要取决于是否本机处理、是否上传、权限、遥测、日志、账号管理和服务政策。选择工具时，应以自己的任务、当前版本和可重复测试为准。
