# MBTI Typing Skill

![MBTI Typing Skill hero](docs/assets/mbti-typing-hero.png)

一个严肃的 Codex MBTI 判型 skill。它不靠“神判”和标签感，而是把每个类型当成可证伪假设，用多轮访谈、证据账本、runner-up、反证和回归测试来逼近更可靠的判型。

> MBTI 可以作为自我理解语言，但不能用于临床诊断、招聘筛选、升学筛选、法律判断，不能决定一个人的价值或未来。

## Session Lab、Benchmark Arena、Calibration Lab 和 Playground

想先把自己的材料丢进去试一轮，可以打开本地优先的 Session Lab：

- [GitHub Pages Session Lab](https://zaoqu-liu.github.io/mbti-typing-skill/session-lab.html)
- [本地 Session Lab 文件](docs/session-lab.html)
- [GitHub Pages Benchmark Arena](https://zaoqu-liu.github.io/mbti-typing-skill/case-gallery.html)
- [本地 case gallery 文件](docs/case-gallery.html)
- [GitHub Pages Calibration Lab](https://zaoqu-liu.github.io/mbti-typing-skill/calibration-lab.html)
- [本地 Calibration Lab 文件](docs/calibration-lab.html)
- [GitHub Pages playground](https://zaoqu-liu.github.io/mbti-typing-skill/playground.html)
- [本地 playground 文件](docs/playground.html)

Session Lab 会把一个判型主张和零散材料转换成启发式候选榜、证据账本、类型对决、下一轮问题、报告草稿、可复制 Codex prompt、share link、Import JSON 恢复入口和 session state export。Benchmark Arena 是一个 adversarial case gallery，展示误判 trap、runner-up、falsifier、可复用 prompt 和 benchmark issue seed。Calibration Lab 允许用户粘贴一段判型报告，立刻得到 Calibration Receipt、修复 prompt、JSON receipt 和失败 issue seed。Interactive Playground 保留为更快的视觉流程预览。

## 先看一分钟 Demo

![Typing journey map](docs/assets/typing-journey-map.png)

如果你是第一次点进来，推荐按这个顺序看：

- [Visual tour](docs/visual-tour.md)：这个仓库的视觉阅读路径。
- [Benchmark Arena](docs/case-gallery.html)：用来观察 trap、runner-up、falsifier 的对抗样例库。
- [Calibration Lab](docs/calibration-lab.html)：用 blind calibration loop 检查报告是否漏掉 benchmark 预期。
- [Blind Review Protocol](docs/blind-review-protocol.md)：用匿名化多评审矩阵检查 top-1、top-2、runner-up、falsifier、boundary 和 overclaim。
- [Consent Redaction Protocol](docs/consent-redaction-protocol.md)：让真实用户的延迟反馈能在同意、脱敏、撤回和最小化暴露的约束下进入项目。
- [Demo session](docs/demo-session.md)：一次 ENTJ vs INTJ vs INFP 的短样例会话。
- [Sample report](docs/sample-report.md)：最终报告应该长什么样。
- [Copy-paste prompt recipes](prompts/prompt-recipes.md)：六个可直接复制的启动 prompt。

目标不是让用户被漂亮话哄住，而是让用户觉得：每一轮追问都真的接住了上一轮的矛盾。

## 产品体验蓝图

这个仓库不是“文件堆”，而是一个可以被第一次访问者快速理解的产品入口：先试、再看证据、再安装、再贡献。

### GitHub Visitor Experience Map

![GitHub Visitor Experience Map](docs/assets/repository-experience-map.svg)

这张图回答“用户第一次点进 GitHub 后该怎么走”：不同访问意图会被路由到 Session Lab、share link、Codex prompt、安装命令或 benchmark 贡献入口。

### Typing Engine Blueprint

![Typing Engine Blueprint](docs/assets/typing-engine-blueprint.svg)

这张图回答“为什么它不是普通 MBTI 问卷”：16 型始终是候选宇宙，证据先进入 ledger，再进入相邻类型对决、反证门和报告审计。

### Trust Loop Dashboard

![Trust Loop Dashboard](docs/assets/trust-loop-dashboard.svg)

这张图回答“为什么这个开源项目会越用越准”：真实误判会变成 benchmark，benchmark 进入回归测试，测试结果再约束 GitHub Pages、Release 和 README 首屏体验。

### Benchmark Arena Pipeline

![Benchmark Arena Pipeline](docs/assets/benchmark-arena-pipeline.svg)

这张图回答“为什么公开 case gallery 不会和 benchmark 数据漂移”：`skill/mbti-typing/examples/benchmark-cases.json` 是唯一源头，`scripts/sync_case_gallery.py` 做 source-of-truth sync，`docs/case-gallery.html` 只展示同步后的数据，测试门禁会检查两边完全一致。

### Benchmark Type Coverage Matrix

![Benchmark Type Coverage Matrix](docs/assets/type-coverage-matrix.svg)

这张图回答“是不是 16 型都真的被测到了”：扩展后的 benchmark suite 已经让 16 个 MBTI type code 都至少作为 leading hypothesis 出现一次。16 / 16 covered 不是心理测量真值声明，而是说明每个类型都有对应的 runner-up、trap、evidence tags 和 falsifier theme。

### Calibration Loop Map

![Calibration Loop Map](docs/assets/calibration-loop-map.svg)

这张图回答“为什么用户会反复回来用”：用户粘贴判型报告，经过可见校准门，拿到 Calibration Receipt、修复 prompt 和 `calibration_result.yml` issue seed。允许的粘性来自更精准的反馈闭环，而不是假确定性或身份操控。

### Blind Review Arena

![Blind Review Arena](docs/assets/blind-review-arena.svg)

这张图回答“怎么证明它不是自嗨”：把样例包匿名化并隐藏参考答案，让不同 reviewer 或模型独立输出 leading、runner-up、证据标签、falsifier 和边界声明，再由 `examples/blind-review-matrix.json` 和 `scripts/blind_review_audit.py` 汇总 top-1、top-2、runner-up 保存率和 overclaim 风险。

### Consent Feedback Loop

![Consent Feedback Loop](docs/assets/consent-feedback-loop.svg)

这张图回答“真实用户材料怎么安全进入开源项目”：`docs/consent-redaction-protocol.md` 定义同意、脱敏、撤回和最小化暴露要求，`examples/consented-followup-packet.json` 提供可审计样例，`.github/ISSUE_TEMPLATE/consented_followup.yml` 给贡献者结构化入口，`scripts/consent_redaction_audit.py` 把 raw private chat、直接标识符、第三方细节和缺失反馈挡在 release 之前。

## 它解决什么问题

普通 MBTI 判型常见问题：

- 单题定型。
- 把压力状态当正常人格。
- ENTJ/INTJ、INFP/INFJ 这种相邻类型过早锁死。
- 用漂亮叙事代替证据链。
- 把 MBTI、Big Five、九型、A/T、依恋、文化背景混成一锅。

这个 skill 强制 agent 做几件事：

- 保留候选集，而不是直接下结论。
- 给每条证据写支持什么、反驳什么、替代解释是什么。
- 保留 runner-up。
- 每轮只攻击当前最关键的不确定性。
- 最终必须写“什么证据会让我改判”。

## 系统长什么样

```mermaid
flowchart LR
    A[用户回答 / 对话记录 / 旧报告] --> B[候选集]
    B --> C[证据账本]
    C --> D{最大分歧}
    D -->|相邻类型| E[类型对决]
    D -->|矛盾材料| F[反证追问]
    D -->|报告风险| G[质量审计]
    E --> H[校准结论]
    F --> H
    G --> H
    H --> I[runner-up + 反证条件]
```

## 安装

```bash
git clone https://github.com/Zaoqu-Liu/mbti-typing-skill.git
cp -R mbti-typing-skill/skill/mbti-typing ~/.codex/skills/
```

然后在 Codex 中使用：

```text
Use $mbti-typing to run a rigorous multi-round MBTI typing interview.
```

## 典型用法

```text
Use $mbti-typing。别人说我是 INFP，但我经常测出 ENTJ。你持续追问，直到能证实或证伪。
```

```text
Use $mbti-typing 帮我区分 ENTJ vs INTJ，不要泛泛问外向内向，要切 Te-dom vs Ni-dom。
```

```text
Use $mbti-typing 审核这份人格报告，重点看过度自信、循环论证、缺少排除性诊断、框架混用。
```

## 体验原则

它让用户“上瘾”的方式不是奉承，而是：

- 每轮都告诉你候选榜怎么变。
- 每轮只切一个真正关键的分叉。
- 把矛盾当核心材料。
- 允许用户纠错，并用纠错更新模型。
- 最终给出可用洞察，而不是一个死标签。

示例节奏：

```text
这一轮真正有用的是三点：
1. ...
2. ...
3. ...

当前候选榜：
- 第一候选：TYPE。原因：...
- 第二候选：TYPE。原因：...

现在最大的矛盾：
...

下一轮只打一个点：...
```

## 质量验证

```bash
make test
```

会验证：

- skill 文件齐全。
- 16 型覆盖。
- pair duel 数量。
- benchmark cases 合法。
- case gallery 和 benchmark JSON 完全同步。
- calibration lab 和 benchmark JSON 完全同步。
- blind review matrix 可以被审计并输出可见指标。
- consented follow-up packet 必须通过同意、脱敏、隐私和反馈门禁。
- golden fixtures 回归通过。
- Python 脚本语法通过。
- 没有缓存污染。

当前预期：

```text
Score: 35/35 (100.00%)
Regression passed for 16 golden fixtures.
Session Lab Audit: 61/61 (100.00%)
Blind Review Audit: 93/93 (100.00%)
Blind Review Metrics: top1: 5/6 (83.33%); top2: 6/6 (100.00%)
Consent Redaction Audit: 78/78 (100.00%)
Consent Redaction Metrics: packets=2; observations=6; states=5; privacy_safe=2/2; feedback=2/2
Case Gallery Source Sync: PASS (16 cases match)
Case Gallery Audit: 48/48 (100.00%)
Calibration Lab Source Sync: PASS (16 cases match)
Calibration Lab Audit: 53/53 (100.00%)
Repository UX Score: 245/245 (100.00%)
```

完整评估模型见 [docs/evaluation.md](docs/evaluation.md)，交互体验原则见 [docs/experience-principles.md](docs/experience-principles.md)。

## 开源贡献

欢迎贡献：

- 新的误判案例。
- 更锋利的类型对决问题。
- 更强的报告审计规则。
- 更真实的 golden fixtures。
- 更自然、更有穿透力的中文输出模板。

详见 [CONTRIBUTING.md](CONTRIBUTING.md)。
