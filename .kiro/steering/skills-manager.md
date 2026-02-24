---
inclusion: always
---

# Skills Manager

Proactively load specialized skills when user queries match keywords below. Skills provide domain-specific guidance, workflows, and best practices.

## Core Rules

1. **Automatic Detection**: Scan user queries for keywords (English or Chinese) and load matching skills immediately
2. **File Location**: Skills are in `.agent/skills/{skill-name}/SKILL.md`
3. **Matching Strategy**: Support exact matches, partial matches, and related terms
4. **Priority**: When multiple skills match, prefer the most specific one
5. **Validation**: Before applying, verify SKILL.md has proper structure (objectives, use cases, instructions)
6. **References**: Load additional context from `.agent/skills/{skill-name}/references/` if available
7. **Clarification**: If ambiguous, ask user which skill domain they need


## Skill Mappings

### 🛠️ Development

| Keywords | Skill |
| --- | --- |
| docx, word, markdown, md, convert, word to markdown, docx to md, document conversion, pandoc, mammoth, python-docx, 转换, 文档转换 | `dev-docx_to_md` |
| pptx, powerpoint, pdf, convert, presentation, slides, ppt to pdf, pptx to pdf, presentation conversion, 演示文稿, 转换, 幻灯片, PPT转PDF | `dev-pptx_to_pdf` |
| download, data download, dataset, fetch data, download file, API download, kaggle, huggingface, sklearn, UCI, data acquisition, wget, curl, requests, http download, file download, batch download, 下载, 数据下载, 数据集, 获取数据, 下载文件, API下载, 数据获取, 批量下载 | `dev-data_download` |
| git, version control, commit, push, pull, branch, merge, rebase, conflict, repository, github, gitlab, gitignore, workflow, 版本控制, 提交, 推送, 拉取, 分支, 合并, 变基, 冲突, 仓库, 工作流 | `dev-git` |
| discover, resource discovery, evaluation, benchmark, selection, 发现, 资源发现, 评测, 选型 | `dev-resource_discovery` |
| code standards, naming conventions, directory structure, refactor, code organization, project structure, 代码规范, 命名规范, 目录结构, 重构, 代码组织, 项目结构 | `dev-code_standards` |
| code style, formatting, linter, lint, prettier, eslint, ruff, black, type check, pre-commit, 代码风格, 格式化, 类型检查 | `dev-code_style` |
| web scraping, scrape, scraping, crawler, crawl, playwright, selenium, beautifulsoup, data extraction, extract content, anti-bot, browser automation, medium article, blog content, download article, save webpage, 网页抓取, 抓取网页, 抓取, 爬虫, 数据提取, 提取内容, 反爬虫, 浏览器自动化, 网页内容, 文章内容, 保存网页 | `dev-web_scraping` |
| pdf, extract, convert, markdown, bilingual, translation, academic, paper, slides, 提取, 转换, 双语, 中英文, 翻译, 学术, 论文, 课件 | `dev-pdf_processing` |
| translation, technical translation, bilingual documentation, terminology, localization, i18n, 翻译, 技术翻译, 双语文档, 术语, 本地化 | `dev-translation` |
| document review, documentation quality, consistency check, accuracy, readability, technical writing, content organization, error detection, check document, 文档审查, 文档质量, 一致性检查, 准确性, 可读性, 技术写作, 内容组织, 错误检测, 检查文档 | `dev-document_review` |
| code comment, annotation, docstring, JSDoc, 代码注释, 注释规范 | `dev-code_comment` |
| code review, review, PR review, pull request, 代码审查, 代码评审 | `dev-code_reviewer` |
| communication standards, team communication, 沟通规范, 团队沟通 | `dev-communication_standards` |
| documentation standards, doc standards, 文档规范, 文档标准 | `dev-documentation_standards` |
| markdown check, markdown lint, markdownlint, md check, markdown 检查, MD 检查 | `dev-markdown_check` |
| product manager, PM, product management, 产品经理, 产品管理 | `dev-product_manager` |
| quality standards, code quality, quality assurance, 质量标准, 代码质量 | `dev-quality_standards` |
| security, security standards, vulnerability, OWASP, 安全, 安全规范, 漏洞 | `dev-security_standards` |
| architect, system architect, 架构师, 系统架构师 | `dev-senior_architect` |
| backend, backend development, server-side, 后端, 后端开发 | `dev-senior_backend` |
| data engineer, data pipeline, ETL, 数据工程师, 数据管道 | `dev-senior_data_engineer` |
| devops, CI/CD, deployment, infrastructure, 运维, 部署, 基础设施 | `dev-senior_devops` |
| frontend, frontend development, React, Vue, 前端, 前端开发 | `dev-senior_frontend` |
| fullstack, full-stack, full stack, 全栈, 全栈开发 | `dev-senior_fullstack` |
| QA, quality assurance, testing, test strategy, 测试, 质量保证, 测试策略 | `dev-senior_qa` |
| security engineer, penetration test, security audit, 安全工程师, 渗透测试, 安全审计 | `dev-senior_security` |
| source annotation, source reference, citation, 来源标注, 引用标注 | `dev-source_annotation` |
| TDD, test driven development, test first, 测试驱动开发 | `dev-tdd_guide` |
| tech stack, technology evaluation, framework comparison, 技术栈, 技术评估, 框架对比 | `dev-tech_stack_evaluator` |
| UX designer, user experience design, 用户体验设计师 | `dev-ux_designer` |
| weka, data mining, ARFF, J48, 数据挖掘 | `dev-weka` |

### 📖 Concepts & Math

| Keywords | Skill |
| --- | --- |
| glossary, concept, terminology, definition, 术语, 概念, 词汇表, 定义 | `concept-glossary` |
| math, mathematics, formula, equation, linear algebra, calculus, probability, statistics, 数学, 公式, 方程, 线性代数, 微积分, 概率, 统计 | `math-concept-library` |

### 🤖 AI Technology

| Keywords | Skill |
| --- | --- |
| agent, AI agent, framework selection, 智能体, 框架选型 | `ai-agents` |
| prompt, prompt engineering, 提示词 | `ai-prompts` |
| skill, claude skill | `ai-skills` |
| llm, language model, 大模型, 语言模型 | `ai-llm_models` |

### 🎓 AI Learning

| Keywords | Skill |
| --- | --- |
| machine learning, ML, 机器学习 | `ai_learning-ml` |
| deep learning, DL, 深度学习 | `ai_learning-dl` |
| LLM learning, 大模型学习 | `ai_learning-llm` |
| NLP, natural language processing, 自然语言处理 | `ai_learning-nlp` |
| machine vision, MV, computer vision, CV, 机器视觉 | `ai_learning-mv` or `ai_learning-cv` |
| RAG, retrieval augmented generation, 检索增强 | `ai_learning-rag` |
| reinforcement learning, RL, Q-learning, Q learning, Bellman, Bellman equation, MDP, Markov decision process, policy gradient, actor-critic, temporal difference, TD learning, SARSA, DQN, deep Q network, reward function, agent environment, 强化学习, Q学习, 贝尔曼方程, 马尔可夫决策过程, 策略梯度, 时序差分 | `ai_learning-rl` |

### 💼 Career Development

| Keywords | Skill |
| --- | --- |
| resume, CV, 简历 | `career-resume` |
| interview, 面试 | `career-interview` |
| job search, 求职 | `career-job_search` |
| certification, 认证 | `career-certification` |
| entrepreneurship, 创业 | `career-entrepreneurship` |

### 🛂 Immigration & Identity

| Keywords | Skill |
| --- | --- |
| visa, 签证 | `identity-visa` or `immigration-visa_renewal` |
| PR, permanent residence, immigration, 永居, 移民 | `immigration-pr_application` |
| work permit, 工签 | `immigration-work_permit` |
| citizenship, 入籍 | `immigration-citizenship` |
| family sponsorship, 家庭团聚, 担保 | `immigration-family_sponsorship` |
| SSN, social security number, 社保号 | `identity-ssn` |
| driver's license, 驾照 | `identity-driving` or `transportation-driving_license` |

### 💰 Finance

| Keywords | Skill |
| --- | --- |
| banking, 银行 | `finance-banking` |
| credit card, 信用卡 | `finance-credit_card` |
| insurance, 保险 | `finance-insurance` |
| investment, 投资 | `finance-investment` |
| remittance, 汇款 | `finance-remittance` |
| tax, 报税 | `finance-tax` |

### 🏠 Housing

| Keywords | Skill |
| --- | --- |
| rental, 租房 | `housing-rental` |
| home buying, 买房 | `housing-home_buying` |
| moving, 搬家 | `housing-moving` |
| furniture, 家具 | `housing-furniture` |
| utilities, 水电煤 | `housing-utilities` |

### 🚗 Transportation

| Keywords | Skill |
| --- | --- |
| car buying, 买车 | `transportation-car_buying` |
| car insurance, 车险 | `transportation-car_insurance` |
| public transit, 公交 | `transportation-public_transit` |
| flight, 机票 | `transportation-flight` |

### 🏥 Healthcare

| Keywords | Skill |
| --- | --- |
| family doctor, 家庭医生 | `healthcare-family_doctor` |
| clinic visit, 看病 | `healthcare-clinic_visit` |
| pharmacy, 药房 | `healthcare-pharmacy` |
| health insurance, 医疗保险 | `healthcare-health_insurance` |
| mental health, 心理健康 | `healthcare-mental_health` |
| childcare, 托儿 | `healthcare-childcare` |

### 📚 Education

| Keywords | Skill |
| --- | --- |
| school selection, 选校 | `education-school_selection` |
| credential evaluation, 学历认证 | `education-credential_evaluation` |
| language learning, 语言学习 | `education-language_learning` |
| skill training, 培训 | `education-skill_training` |
| tutoring, 补习 | `education-tutoring` |
| child education, 子女教育 | `education-child_education` |

### 🍽️ Daily Life

| Keywords | Skill |
| --- | --- |
| delivery, package delivery, 快递, 包裹 | `daily_life-delivery` |
| dining, restaurant, eating out, 餐饮, 外出就餐 | `daily_life-dining` |
| internet service, ISP, broadband, WiFi, 网络服务, 宽带 | `daily_life-internet` |
| mobile, telecom, phone plan, SIM, 手机, 电信, 话费 | `daily_life-mobile_telecom` |
| pets, pet care, veterinary, 宠物, 宠物护理, 兽医 | `daily_life-pets` |
| secondhand, used items, thrift, 二手, 二手物品 | `daily_life-secondhand` |
| shopping, online shopping, deals, 购物, 网购 | `daily_life-shopping` |
| storage, self storage, 仓储, 存储 | `daily_life-storage` |

### 🍕 Food & Shopping

| Keywords | Skill |
| --- | --- |
| deals, coupons, discounts, 优惠, 折扣, 优惠券 | `food_shopping-deals` |
| grocery, supermarket, 超市, 杂货 | `food_shopping-grocery` |
| restaurants, food recommendations, 餐厅推荐, 美食 | `food_shopping-restaurants` |

### 🔧 Home Services

| Keywords | Skill |
| --- | --- |
| cleaning, house cleaning, 清洁, 家政 | `home_services-cleaning` |
| repair, home repair, maintenance, 维修, 家庭维修 | `home_services-repair` |

### ⚖️ Legal

| Keywords | Skill |
| --- | --- |
| consumer rights, refund, complaint, 消费者权益, 退款, 投诉 | `legal-consumer_rights` |
| labor rights, employment law, 劳动权益, 劳动法 | `legal-labor_rights` |
| legal consultation, lawyer, 法律咨询, 律师 | `legal-legal_consultation` |
| rental contract, lease, 租房合同, 租约 | `legal-rental_contract` |
| traffic accident, car accident, 交通事故, 车祸 | `legal-traffic_accident` |

### 🎭 Social & Leisure

| Keywords | Skill |
| --- | --- |
| Chinese community, 华人社区, 中文社区 | `social-chinese_community` |
| cultural events, festivals, 文化活动, 节日 | `social-cultural_events` |
| dating, relationships, 约会, 交友 | `social-dating` |
| religion, church, temple, 宗教, 教堂, 寺庙 | `social-religion` |
| volunteering, volunteer, 志愿者, 义工 | `social-volunteering` |
| entertainment, movies, concerts, 娱乐, 电影, 演唱会 | `leisure-entertainment` |
| fitness, gym, exercise, workout, 健身, 运动, 锻炼 | `leisure-fitness` |

### 🎉 Life Events

| Keywords | Skill |
| --- | --- |
| funeral, memorial, 葬礼, 追悼 | `life_events-funeral` |
| wedding, marriage, 婚礼, 结婚 | `life_events-wedding` |

### ✈️ Travel

| Keywords | Skill |
| --- | --- |
| car rental, rent a car, 租车 | `travel-car_rental` |
| hotel, accommodation, lodging, 酒店, 住宿 | `travel-hotel` |
| travel flight, booking flight, 旅行机票, 订机票 | `travel-travel_flight` |
| travel planning, itinerary, trip, vacation, 旅行规划, 行程, 度假 | `travel-travel_planning` |

### 📱 Communication

| Keywords | Skill |
| --- | --- |
| internet service, ISP, provider, 网络服务商 | `communication-internet_service` |
| phone plan, mobile plan, carrier, 手机套餐, 运营商 | `communication-phone_plan` |
| shipping, mail, courier, 邮寄, 快递, 物流 | `communication-shipping` |

### 📝 Learning & Study

| Keywords | Skill |
| --- | --- |
| notes, note-taking, study notes, lecture notes, organize notes, course materials, study guide, 笔记, 记笔记, 学习笔记, 课堂笔记, 整理笔记, 课程资料, 学习指南 | `learning-note_taking` |
| code generation, generate code, lab code, assignment code, jupyter, python script, homework code, 生成代码, 写代码, 作业代码 | `learning-code_generation` |
| assignment document, Lab.docx, submission document, word document, screenshots, discussion, analysis, 作业文档, 提交文档, 截图, 讨论, 分析 | `learning-assignment_document` |
| consistency, check consistency, verify files, compare files, validate code, .py .ipynb .md, 一致性, 检查一致, 验证文件, 对比文件, 验证代码 | `learning-code_consistency` |
| markdown to word, md转docx, convert to docx, pandoc, word document, format document, 转换docx, 生成word, 格式化文档 | `learning-md_to_docx` |
| notebook conversion, ipynb转py, py转ipynb, convert notebook, jupyter convert, nbconvert, jupytext, script to notebook, notebook to script, 转换notebook, 笔记本转换 | `learning-notebook_conversion` |
| submit lab, lab submission, prepare submission, zip file, upload assignment, brightspace, 提交lab, 作业提交, 准备提交, 打包, 上传作业 | `learning-lab_submission` |
| brightspace scraper, scrape brightspace, download course, course materials, scrape slides, scrape labs, LMS scraper, brightspace抓取, 抓取课程, 下载课程, 课程资料, 抓取slides, 抓取labs, 学习平台抓取 | `learning-brightspace_scraper` |
| textbook vectorization, pdf vectorization, semantic search textbook, embedding textbook, query textbook, knowledge base, 教科书向量化, PDF向量化, 语义搜索, 知识库 | `learning-textbook_vectorization` |
| bilingual content, dual language, translation template, bilingual markdown, original and translation, 双语内容, 双语模板, 翻译模板, 中英对照 | `learning-bilingual_content` |
| automated study material, auto generate, study material generation, 自动生成学习材料 | `learning-automated_study_material` |
| cheat sheet, cheatsheet, exam sheet, crib sheet, review sheet, 小抄, 速查表, 考试小抄, 复习表 | `learning-cheat_sheet` |
| code screenshot, screenshot code, carbon, 代码截图 | `learning-code_screenshot` |
| lecture storyline, lecture flow, lecture outline, 课程故事线, 讲座大纲 | `learning-lecture_storyline` |
| logic consistency, logical check, reasoning check, 逻辑一致性, 逻辑检查 | `learning-logic_consistency` |
| quiz, quiz generation, practice questions, exam prep, 测验, 生成题目, 练习题, 考试准备 | `learning-quiz_generation` |
| quiz notes, quiz note taking, 测验笔记 | `learning-quiz_note_taking` |
| slide formatting, format slides, presentation format, 幻灯片格式, 格式化幻灯片 | `learning-slide_formatting` |
| tutorial notebook, tutorial, interactive tutorial, 教程 notebook, 交互式教程 | `learning-tutorial_notebook` |


## Execution Workflow

When a user query is received:

1. **Scan for keywords** - Check query text against all keyword mappings (case-insensitive, both languages)
2. **Identify matches** - List all skills with matching keywords
3. **Select skill** - Choose the most specific match; if tied, ask user to clarify
4. **Load skill file** - Read `.agent/skills/{skill-name}/SKILL.md`
5. **Validate structure** - Ensure file contains objectives, use cases, and instructions sections
6. **Load references** - If `.agent/skills/{skill-name}/references/` exists, load relevant files
7. **Apply guidance** - Follow the skill's instructions to assist the user
8. **Silent operation** - Don't announce that you're loading a skill; just apply it naturally
