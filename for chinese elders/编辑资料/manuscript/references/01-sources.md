# 本册资料来源与核验说明

**核验日期：2026 年 8 月 12 日。** 本册把标准机构、同行评审研究、政府或监管材料和产品官方文档分开使用。技术论文支持的是特定机制或实验边界，不代表所有模型都完全相同；产品命令、政策和网页以后可能变化。

## 模型训练、部署、微调与出错机制

- [NIST AI RMF：AI 参与者任务与生命周期](https://airc.nist.gov/airmf-resources/airmf/appendices/app-a-descriptions-of-ai-actor-tasks/)：区分模型开发与训练、产品部署、运行监测和贯穿生命周期的测试验证。
- [PMLR：Mechanics of Next Token Prediction with Self-Attention](https://proceedings.mlr.press/v238/li24f.html)：支持 Transformer 语言模型以输入序列为条件进行下一 Token 预测的机制说明。
- [InstructGPT 原始论文](https://arxiv.org/abs/2203.02155)：支持指令微调和人类反馈会改变模型回答行为；论文同时说明模型仍可能编造事实和犯错。
- [NIST 生成式 AI 风险管理框架 NIST AI 600-1](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)：支持“confabulation（虚构式错误）”属于生成式 AI 的重要风险，流畅输出不等于事实可靠。
- [LoRA 原始论文](https://arxiv.org/abs/2106.09685)：说明全量微调可重新训练全部模型参数，而 LoRA 冻结预训练权重、训练新增低秩参数。

## 终端、本地模型和动态产品事实

- [Qwen Code 中文快速入门](https://qwenlm.github.io/qwen-code-docs/zh/users/quickstart/)与[架构说明](https://qwenlm.github.io/qwen-code-docs/zh/developers/architecture/)：支持 `qwen` 启动、认证以及终端界面与模型服务分层的例子。
- [Ollama 命令行说明](https://docs.ollama.com/cli)：支持 `ollama run 模型名称` 的本地模型入口示例。

## 数据污染、投毒、模型坍塌与 RAG 污染

- [NIST AI 100-2：对抗性机器学习攻击与缓解分类](https://csrc.nist.gov/pubs/ai/100/2/e2025/final)：支持数据投毒是带有操纵意图、发生在学习过程中的攻击概念。
- [中国《人工智能安全治理框架》2.0 版发布说明](https://www.cac.gov.cn/2025-09/15/c_1759653448369123.htm?type=h5)：用于中国 AI 安全风险治理背景。
- [《自然》：递归训练中的模型坍塌研究](https://www.nature.com/articles/s41586-024-07566-y)与[作者更正](https://www.nature.com/articles/s41586-025-08905-3.pdf)：支持特定实验条件下尾部信息可能丢失；不能外推为“所有合成数据都必然有害”。
- [PMLR：RAG 知识源投毒与检测研究](https://proceedings.mlr.press/v318/moradi26a.html)：支持外部知识源被恶意内容污染后，检索与回答可能被定向操纵。

## AI 信息差销售、仿冒与高风险收费案例

- [中央网信办：“清朗·整治 AI 应用乱象”专项行动](https://www.cac.gov.cn/2026-04/30/c_1779289298718765.htm)：支持仿冒、套壳 AI 网站和应用等治理背景。
- [市场监管总局：人工智能领域不正当竞争典型案例](https://www.samr.gov.cn/xw/zj/art/2026/art_0bea53d4e3904015a340b4e83241a8ec.html)：支持相似页面、图标和“本地部署工具”混淆案例。
- [仿冒 DeepSeek 手机木马安全预警](https://szwljb.sz.gov.cn/aqjs/aqyj/content/post_1537043.html)：支持诱导更新、无障碍权限、短信、通讯录和应用列表风险。
- [公安机关关于免费软件、收费群组和高价教程的提醒](https://www.xuancheng.gov.cn/OpennessContent/show/3480987.html)：支持公开软件和资料被包装成高价服务的案例。
- [司法部智慧普法平台：AI 培训套路调查](https://legalinfo.moj.gov.cn/zhfxfzzx/fzzxyw/202503/t20250328_516534.html)：支持变现承诺、课程收费和后续资源费案例。
- [市场监管总局与中消协：老年人药品、保健品消费风险提示](https://www.samr.gov.cn/zt/ndzt/2025n/zhzznjsjzwhgpjzsczx/zjbs/art/2025/art_61f214e066344c959d86309db2bdba1b.html)：支持私域直播、健康咨询、限时优惠和高价商品的风险结构。
- [深圳证监局：非法荐股骗局风险提示](https://www.csrc.gov.cn/shenzhen/c105615/c7638512/content.shtml)：支持“AI 量化选股”等技术权威包装和高额服务费风险。

## 怎样理解这些来源

政府通报可以证明通报中的案例、机构、年份和行为，但不能证明所有类似产品都有同样问题。厂商文档可以证明其当时公开的命令和功能，不能独立证明“最好”或“最安全”。涉及付款、安装和账号时，仍要核对当前官方入口、开发者身份、合同、退款与隐私条款。
