# 本册资料来源与核验说明

**核验日期：2026 年 8 月 12 日。** 本册的中国大陆法律与标识说明按核验日的现行规则编写，不代替针对具体案件的法律意见。平台授权和产品功能会更新，商业发布前必须重新查看当前条款。

## 图片生成、提示词与编辑边界

- [NeurIPS 2020：Denoising Diffusion Probabilistic Models](https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html)：说明扩散概率模型用于高质量图像合成；本册据此把常见生成模型描述为视觉生成系统，而不是可验证的精确三维复原工具。
- [Adobe Firefly：有效图片提示词](https://helpx.adobe.com/ca/firefly/web/generate-images-with-text-to-image/generate-images-using-text-prompts/writing-effective-text-prompts.html)：用于主体、环境、构图、风格和迭代的产品操作示例。它不能证明提示词可以保证人物或商品像素完全不变。

## 中国大陆肖像、个人信息和 AI 标识

- [《中华人民共和国民法典》第一千零一十八至一千零二十条](https://www.court.gov.cn/zixun/xiangqing/233181.html)：支持肖像权、未经同意原则和法律规定的合理实施情形。
- [《中华人民共和国个人信息保护法》第二十八至三十一条](https://www.samr.gov.cn/wljys/gzzd/art/2023/art_3ef1e889c1e644d4b65b5f5c7f432386.html)：支持敏感个人信息范围、特定目的、充分必要、严格保护和相关同意要求。
- [《人工智能生成合成内容标识办法》](https://www.nrta.gov.cn/art/2025/3/14/art_113_70340.html?xxgkhide=1)：自 2025 年 9 月 1 日施行；第十条要求用户发布生成合成内容时主动声明并使用服务提供者的标识功能。

## 老照片保存与备份

- [美国国会图书馆：个人数字档案扫描基础](https://blogs.loc.gov/thesignal/2014/03/personal-digital-archiving-the-basics-of-scanning/)：建议保留信息量较高的主文件，并把较小的 JPEG 作为工作或分享副本。
- [美国国会图书馆：视觉材料电子保存指南](https://www.loc.gov/preservation/resources/rt/guide/guid_exc.html)：区分保存主文件与访问副本，并说明分辨率、色彩、压缩和文件格式都会影响保存质量。
- [CISA：保护设备中的数据](https://www.cisa.gov/resources-tools/training/how-protect-data-stored-your-devices)：支持重要数据需要独立备份，并避免单点故障造成永久丢失。

## AI 编程、依赖和 API 密钥

- [NIST SP 800-218 安全软件开发框架](https://csrc.nist.gov/projects/ssdf)：用于软件依赖、来源、开发环境、风险记录和安全验证的通用边界。
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)：支持 API 密钥等机密需要集中管理、审计、轮换和防泄漏。
- [OWASP：移动应用中硬编码 API 密钥的风险](https://mas.owasp.org/MASWE-0005/)：说明泄露的按量计费 API 密钥可能导致未经授权调用和经济损失。

## 怎样理解这些来源

提示词中的“保持不变”只是约束请求，不是技术保证。法律允许、平台允许、素材有授权和按规则标识是四个不同问题。重要照片应保留未经编辑的高质量主文件和至少两处备份；代码和依赖应先解释权限、来源和写入位置，再在副本或测试环境中运行。
