# 《看懂 AI》来源与事实核验台账

**建立日期：** 2026-08-12

## 1. 证据等级

| 等级 | 来源 | 在书中的用途 |
|---|---|---|
| A | 法律法规、监管机构、厂商官方文档/条款/价格页 | 产品事实、规则、版本、价格、官方功能 |
| B | 同行评审论文、大学/研究机构报告、标准组织 | 机制、效果、群体研究与限制 |
| C | 可靠媒体、专业测评、消费者调查 | 案例、市场观察；不能单独证明技术能力 |
| D | 商家宣传、用户帖子、短视频、未验证截图 | 只作为待核验主张或骗局案例，不作为事实依据 |

所有动态事实必须记录“最后核验日期”。厂商自己的基准结果标为“厂商报告”，不能改写成客观总排名。

## 2. 监管与法律

| 主题 | 来源 | 用途 | 状态 |
|---|---|---|---|
| 生成式 AI 服务基本规则 | [《生成式人工智能服务管理暂行办法》](https://www.miit.gov.cn/zcfg/qtl/art/2023/art_f4e8f71ae1dc43b0980b962907b7738f.html) | 服务责任、数据与内容治理背景 | 已纳入；出版前复核 |
| 生成式 AI 备案公示 | [国家网信办公告](https://www.cac.gov.cn/2026-05/13/c_1780413225190669.htm) | 模型名称、备案号/上线编号披露 | 已纳入；动态 |
| AI 生成内容标识 | [《人工智能生成合成内容标识办法》全文](https://www.nrta.gov.cn/art/2025/3/14/art_113_70340.html?xxgkhide=1) | 显式/隐式标识及用户发布义务 | 2026-08-12 已完整核对；自 2025-09-01 施行 |
| 个性化推荐权利 | [互联网信息服务算法推荐管理规定](https://www.cac.gov.cn/2022-01/04/c_1642894606364259.htm) | 关闭个性化推荐、用户标签 | 已纳入研究池 |
| 肖像权 | [《民法典》第一千零一十八至一千零二十条](https://www.court.gov.cn/zixun/xiangqing/233181.html) | 肖像制作、使用、公开的一般规则与合理实施情形 | 2026-08-12 已核对正式法条 |
| 敏感个人信息 | [《个人信息保护法》第二十八至三十一条](https://www.samr.gov.cn/wljys/gzzd/art/2023/art_3ef1e889c1e644d4b65b5f5c7f432386.html) | 生物识别、医疗健康、金融账户和未成年人信息等隐私分级 | 2026-08-12 已核对正式法条 |
| AI 应用乱象治理 | [中央网信办专项行动](https://www.cac.gov.cn/2026-04/30/c_1779289298718765.htm) | 仿冒、套壳应用、非法账号交易与虚假流量 | 2026-08-12 已核验 |
| 涉 AI 乱象举报 | [中央网信办举报专区](https://www.cac.gov.cn/2026-06/12/c_1782660002371256.htm) | 举报入口与违规分类 | 2026-08-12 已核验 |
| 仿冒 AI 产品不正当竞争 | [市场监管总局典型案例](https://www.samr.gov.cn/xw/zj/art/2026/art_0bea53d4e3904015a340b4e83241a8ec.html) | 仿冒官方页面、“本地部署工具”混淆案例 | 2026-08-12 已核验 |

## 3. AI 原理

| 主题 | 来源 | 用途 | 状态 |
|---|---|---|---|
| AI 开发、部署与运行阶段 | [NIST AI RMF Actor Tasks](https://airc.nist.gov/airmf-resources/airmf/appendices/app-a-descriptions-of-ai-actor-tasks/) | 区分模型开发/训练、产品部署、运行监测与测试验证 | 2026-08-12 已核验 |
| 下一 Token 预测 | [PMLR 2024：Mechanics of Next Token Prediction with Self-Attention](https://proceedings.mlr.press/v238/li24f.html) | 第一册第 2 章的语言模型训练机制 | 2026-08-12 已核验；同行评审 |
| 指令微调与人类反馈 | [InstructGPT 原始论文](https://arxiv.org/abs/2203.02155) | 指令训练、偏好训练及仍会编造事实的边界 | 2026-08-12 已核验；原始研究 |
| 语言模型虚构式错误 | [NIST AI 600-1 生成式 AI 风险管理框架](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) | 第一册第 2 章幻觉/虚构机制与风险 | 2026-08-12 已核验；标准机构 |
| RAG 原始方法 | [NeurIPS 2020：Retrieval-Augmented Generation](https://papers.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html) | 第二册第 4 章；外部知识源不只限于指定私有文件 | 2026-08-12 已核验；原始论文 |
| 句子嵌入与语义检索 | [ACL 2019：Sentence-BERT](https://aclanthology.org/D19-1410/) | 第二册嵌入与余弦相似度语义检索 | 2026-08-12 已核验；原始论文 |
| 全量微调与 LoRA | [LoRA 原始论文](https://arxiv.org/abs/2106.09685) | 全量权重更新与冻结基础权重、训练新增低秩参数的区别 | 2026-08-12 已核验；原始论文 |
| 长上下文使用限制 | [TACL 2024：Lost in the Middle](https://aclanthology.org/2024.tacl-1.9/) | 窗口放得下不等于所有位置都能稳健使用 | 2026-08-12 已核验；同行评审；不外推到所有未来模型 |
| 扩散式图片生成 | [NeurIPS 2020：Denoising Diffusion Probabilistic Models](https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html) | 第四册图片生成机制的范围限定 | 2026-08-12 已核验；原始论文 |
| 终端 CLI 与模型的分层 | [Qwen Code 架构](https://qwenlm.github.io/qwen-code-docs/zh/developers/architecture/) | CLI 是输入、显示、会话和工具层，不是基础模型 | 2026-08-12 已核验 |
| 终端启动 AI 工具 | [Qwen Code 中文快速入门](https://qwenlm.github.io/qwen-code-docs/zh/users/quickstart/) | `qwen` 启动、认证与模型提供方 | 2026-08-12 已核验；动态 |
| 终端运行本地模型 | [Ollama CLI Reference](https://docs.ollama.com/cli) | `ollama run` 示例与本地模型入口 | 2026-08-12 已核验；动态 |
| API 直接调用模型 | [DeepSeek Chat Completions API](https://api-docs.deepseek.com/zh-cn/api/create-chat-completion/) | 不经网页调用模型、模型标识与 Token 用量 | 2026-08-12 已核验；动态 |
| AI 数据投毒与对抗攻击 | [NIST AI 100-2](https://csrc.nist.gov/pubs/ai/100/2/e2025/final) | 数据投毒定义、攻击阶段与缓解分类 | 2026-08-12 已核验 |
| 中国 AI 安全风险分类 | [《人工智能安全治理框架》2.0版发布说明](https://www.cac.gov.cn/2025-09/15/c_1759653448369123.htm?type=h5) | 数据安全、模型安全和治理背景 | 2026-08-12 已核验 |
| 递归合成数据与模型坍塌 | [Nature 2024 研究](https://www.nature.com/articles/s41586-024-07566-y) | 解释未经控制递归训练的退化风险与边界 | 2026-08-12 已核验；不外推为所有合成数据必然有害 |
| RAG 知识库投毒 | [PMLR 2026 研究](https://proceedings.mlr.press/v318/moradi26a.html) | 知识源污染怎样影响检索和回答 | 2026-08-12 已核验 |

## 4. 产品官方资料

| 产品/主题 | 官方来源 | 用途 | 最后核验 |
|---|---|---|---|
| DeepSeek 价格 | [API 价格](https://api-docs.deepseek.com/zh-cn/quick_start/pricing) | 成本示例 | 2026-08-12 |
| DeepSeek 版本 | [更新日志](https://api-docs.deepseek.com/updates/) | 更新节奏 | 2026-08-12 |
| 豆包产品 | [豆包官网](https://www.doubao.com/) | 官方入口 | 2026-08-12 |
| Kimi 功能 | [新用户指南](https://www.kimi.com/zh-cn/help/new-user-guide/overview) | 长文档、联网、模型选择 | 2026-08-12 |
| Kimi 会员 | [价格页](https://www.kimi.com/zh-cn/resources/kimi-k3-pricing) | 动态价格 | 2026-08-12 |
| 千问模型 | [Qwen 官方博客](https://qwenlm.github.io/blog/) | 模型发布时间与能力主张 | 2026-08-12 |
| 腾讯元宝 | [官方应用商店页面](https://apps.apple.com/cn/app/%E5%85%83%E5%AE%9D-%E8%85%BE%E8%AE%AF%E5%85%A8%E8%83%BDai%E5%8A%A9%E6%89%8B/id6480446430) | 提供者、功能、价格 | 2026-08-12 |
| 文心 | [文心官网](https://wenxin.baidu.com/home) | 官方入口 | 2026-08-12 |
| ChatGPT 支持地区 | [OpenAI 官方支持地区](https://help.openai.com/en/articles/7947663-chatgpt-supported-countries) | 中国大陆使用边界 | 2026-08-12；出版前必查 |

## 5. 对话教学、提示词与企业内容生产

| 主题 | 来源 | 用途 | 状态 |
|---|---|---|---|
| 提示词设计与迭代 | [OpenAI Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering) | 清楚指令、上下文、示例和迭代方法 | 2026-08-12 已核验；产品细节动态 |
| 简洁指令、语气和验收边界 | [OpenAI Model guidance](https://developers.openai.com/api/docs/guides/latest-model) | 避免重复指令；说明目标、约束、成功标准和输出风格 | 2026-08-12 已核验；不用厂商评测数字作通用结论 |
| 生成式 AI 教学设计 | [UNESCO：Guidance for generative AI in education and research](https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research?hub=67098) | 人本教学、苏格拉底式对话、探究学习和风险边界 | 2026-08-12 已核验 |
| 办公提示词四要素与迭代 | [Google Docs Editors Help](https://support.google.com/docs/answer/15013615?hl=en) | 角色、任务、背景、格式及多轮改进；公司内容示例 | 2026-08-12 已核验；产品功能动态 |
| 从模板改成自己的提示词 | [Microsoft Support：Edit a Copilot prompt](https://support.microsoft.com/en-us/microsoft-365-copilot/edit-a-copilot-prompt-to-make-it-your-own) | 调整目标、受众、文体、长度和风格 | 2026-08-12 已核验；产品功能动态 |
| 企业营销工作流 | [Microsoft Learn：Marketing Use Case](https://learn.microsoft.com/en-us/training/modules/empower-workforce-copilot-marketing/) | 市场资料、活动计划、文案、多渠道内容和效果分析的分阶段流程 | 2026-08-12 已核验；仅作为常见工作流示例 |
| 营销提示词与人工评估 | [HubSpot Academy：AI for Marketing](https://academy.hubspot.com/courses/AI-for-Marketers) | 文本与视觉内容、结果评估、隐私和偏见边界 | 2026-08-12 已核验；行业培训资料 |
| 图片提示词和参考图角色 | [Adobe Firefly：Writing effective text prompts](https://helpx.adobe.com/ca/firefly/web/generate-images-with-text-to-image/generate-images-using-text-prompts/writing-effective-text-prompts.html)、[Adobe Express：Create images](https://helpx.adobe.com/express/web/image-creation-and-editing/generate-and-edit-with-ai/text-to-image.html) | 主体、描述、构图/风格参考、迭代和营销图片案例 | 2026-08-12 已核验；产品功能动态 |

## 6. 信息生态与核验入口

| 主题 | 来源 | 用途 | 状态 |
|---|---|---|---|
| 中国互联网联合辟谣平台 | [piyao.org.cn](https://www.piyao.org.cn/) | 公共信息核验入口 | 已纳入 |
| 健康科普辟谣 | [国家卫生健康委健康科普平台](https://www.nhc.gov.cn/kppypt/index.shtml) | 健康信息核验 | 已纳入 |
| 老年人虚假短视频研究 | [中国人民大学相关期刊论文页](https://cjjc.ruc.edu.cn/CN/Y2023/V45/I2/127) | 第 9 章群体与传播研究 | 待阅读全文和方法复核 |

## 7. 反诈与消费者救济

| 主题 | 来源 | 用途 | 状态 |
|---|---|---|---|
| 96110 与 110 | [公安机关官方说明示例](https://gaj.nanjing.gov.cn/njsgaj/202103/t20210331_2865220.html) | 紧急反诈处置 | 需补全国性权威入口 |
| 12315、保健品风险 | [市场监管总局消费提示](https://www.samr.gov.cn/xw/sj/art/2025/art_a5fe6982180c4219b263bbba42bfd77b.html) | 消费维权与健康商品骗局 | 已纳入研究池 |
| 私域直播健康骗局 | [市场监管总局材料](https://www.samr.gov.cn/zt/ndzt/2025n/zhzznjsjzwhgpjzsczx/zjbs/art/2025/art_61f214e066344c959d86309db2bdba1b.html) | 案例结构 | 已纳入研究池 |
| 仿冒 DeepSeek 木马 | [深圳市互联网违法和不良信息举报办公室安全预警](https://szwljb.sz.gov.cn/aqjs/aqyj/content/post_1537043.html) | 假更新、无障碍权限、短信与通讯录窃取 | 2026-08-12 已核验 |
| 免费软件和部署教程的信息差收费 | [宣城市公安局提醒](https://www.xuancheng.gov.cn/OpennessContent/show/3480987.html) | 免费入口、收费群组与高价教程案例 | 2026-08-12 已核验；市场数字出版前复核 |
| AI 培训和二次收费 | [司法部智慧普法平台调查](https://legalinfo.moj.gov.cn/zhfxfzzx/fzzxyw/202503/t20250328_516534.html) | 变现承诺、普通内容、高价资源费 | 2026-08-12 已核验 |
| AI 量化选股骗局 | [深圳证监局风险提示](https://www.csrc.gov.cn/shenzhen/c105615/c7638512/content.shtml) | AI 权威包装高风险金融销售 | 2026-08-12 已核验 |
| 自动续费陷阱 | [司法部智慧普法平台调查](https://legalinfo.moj.gov.cn/pub/sfbzhfx/zhfxfzzx/fzzxrdtj/202411/t20241111_509326.html) | 低价试用、自动续费与取消提示 | 2026-08-12 已核验 |

## 8. 引用规则

1. 正文中的动态数字必须能追溯到本表中的具体页面。
2. 每条价格同时写明币种、计价单位、消费者/API 身份和核验日期。
3. “免费”必须说明是否含额度、会员、广告或应用内购买。
4. “可在中国大陆使用”应验证注册、登录、付款和服务条款，不只验证网页能打开。
5. 医疗、金融和法律结论不以单一模型公司资料为权威来源。
6. 引用模型回答只能作为实验材料，不能作为事实来源。
7. 网页失效时保留标题、发布机构、发布日期和访问日期，再寻找官方替代链接。

## 9. 数字保存与软件安全

| 主题 | 来源 | 用途 | 状态 |
|---|---|---|---|
| 照片扫描主文件与工作副本 | [美国国会图书馆：个人数字档案扫描基础](https://blogs.loc.gov/thesignal/2014/03/personal-digital-archiving-the-basics-of-scanning/) | 第四册老照片主文件、工作副本和格式边界 | 2026-08-12 已核验 |
| 视觉材料保存质量 | [美国国会图书馆：视觉材料电子保存指南](https://www.loc.gov/preservation/resources/rt/guide/guid_exc.html) | 分辨率、色彩、压缩、文件格式与访问副本 | 2026-08-12 已核验 |
| 独立备份 | [CISA：保护设备中的数据](https://www.cisa.gov/resources-tools/training/how-protect-data-stored-your-devices) | 避免单点故障和永久数据丢失 | 2026-08-12 已核验 |
| 安全软件开发与依赖 | [NIST SP 800-218 SSDF](https://csrc.nist.gov/projects/ssdf) | 依赖来源、开发环境、风险记录和验证 | 2026-08-12 已核验 |
| API 密钥与机密管理 | [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)、[硬编码 API 密钥风险](https://mas.owasp.org/MASWE-0005/) | 密钥泄露、轮换、权限和按量计费经济损失 | 2026-08-12 已核验；第二项页面标为 beta |

## 10. 仍需补强的研究

- [x] 生成式 AI 训练、虚构式错误、RAG、嵌入、微调和长上下文的原始或标准来源
- [ ] 中国大陆主要产品逐项实际注册和订阅路径测试
- [ ] 适合年长读者的中文数字可访问性研究
- [ ] 推荐算法和同质信息暴露的中国情境研究
- [ ] AI 健康建议的可靠性与风险研究
- [ ] 共享账号、第三方输入法和文件上传的数据风险案例
- [ ] 各官方产品的账号注销、数据导出和模型训练退出方式
