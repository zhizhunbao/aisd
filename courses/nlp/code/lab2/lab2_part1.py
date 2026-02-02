"""
CST8507 Lab 2 Part 1: ELIZA Chatbot
Author: Peng Wang
Student Number: 041107730

A rule-based chatbot that simulates a psychotherapist using pattern matching
and regular expressions. Implements the classic ELIZA approach with
predefined rules and pronoun substitution.
"""

# ============================================================
# 步骤0：导入模块
# Step 0: Import modules
# ============================================================

# 导入正则表达式模块，用于模式匹配
# Import regular expression module for pattern matching
import re

# 导入随机模块，用于随机选择回复
# Import random module for selecting random responses
import random


# ============================================================
# 步骤1：定义代词替换规则
# Step 1: Define pronoun substitution rules
# ============================================================

# 代词替换规则：将用户视角转换为ELIZA回复视角
# Pronoun substitution rules: convert user perspective to ELIZA response perspective
# 使用占位符避免替换冲突（如 me -> you -> I 的问题）
# Use placeholders to avoid replacement conflicts (e.g., me -> you -> I issue)
PRONOUN_PAIRS = [
    (r'\bi\b', '__YOU__'),
    (r'\bmy\b', '__YOUR__'),
    (r'\bme\b', '__YOU2__'),
    (r'\bam\b', '__ARE__'),
    (r'\byou\b', '__I__'),
    (r'\byour\b', '__MY__'),
]

# 占位符到最终文本的映射
# Placeholder to final text mapping
PLACEHOLDER_MAP = {
    '__YOU__': 'you',
    '__YOUR__': 'your',
    '__YOU2__': 'you',
    '__ARE__': 'are',
    '__I__': 'I',
    '__MY__': 'my',
}


# ============================================================
# 步骤2：定义ELIZA对话规则
# Step 2: Define ELIZA conversation rules
# ============================================================

# 规则列表：每个规则包含 (正则模式, 回复模板列表)
# Rule list: each rule contains (regex pattern, list of response templates)
RULES = [
    # 规则组1：问候语
    # Rule Group 1: Greetings
    (
        r'\b(hello|hi|hey)\b',
        [
            "Hello. How are you feeling today?",
            "Hi there. What would you like to talk about?",
            "Hello. Please tell me what is on your mind.",
        ]
    ),

    # 规则组2：情感表达 - "I feel ..."
    # Rule Group 2: Feelings - "I feel ..."
    (
        r'i feel (.*)',
        [
            "Why do you feel {0}?",
            "Do you often feel {0}?",
            "What makes you feel {0}?",
        ]
    ),

    # 规则组2：情感表达 - "I am ..."
    # Rule Group 2: Feelings - "I am ..."
    (
        r'i am (.*)',
        [
            "How long have you been {0}?",
            "Why do you think you are {0}?",
            "Do you enjoy being {0}?",
        ]
    ),

    # 规则组3：家庭相关
    # Rule Group 3: Family
    (
        r'\b(mother|father|parents|sister|brother)\b',
        [
            "Tell me more about your family.",
            "How do you feel about your family?",
            "Does your family influence you a lot?",
        ]
    ),

    # 规则组4：用户提问 - "why ..."
    # Rule Group 4: Questions to ELIZA - "why ..."
    (
        r'why (.*)',
        [
            "Why do you think {0}?",
            "What do you think the answer is?",
        ]
    ),

    # 规则组4：用户提问 - "can you ..."
    # Rule Group 4: Questions to ELIZA - "can you ..."
    (
        r'can you (.*)',
        [
            "What makes you think I can {0}?",
            "Why do you ask if I can {0}?",
        ]
    ),

    # 规则组5：负面情绪
    # Rule Group 5: Negative Emotions
    (
        r'\b(sad|unhappy|depressed|miserable)\b',
        [
            "I'm sorry you feel that way.",
            "What do you think is causing this?",
            "Do you often feel like this?",
        ]
    ),
]

# 规则组6：默认回复（无匹配时使用）
# Rule Group 6: Default responses (used when no rules match)
DEFAULT_RESPONSES = [
    "Please go on.",
    "Tell me more.",
    "Can you elaborate on that?",
]


# ============================================================
# 步骤3：实现代词转换函数
# Step 3: Implement pronoun transformation function
# ============================================================

def transform_pronouns(text):
    """转换代词，将用户视角转换为ELIZA回复视角
    Transform pronouns from user perspective to ELIZA response perspective"""

    # 第一阶段：将所有代词替换为占位符
    # Phase 1: Replace all pronouns with placeholders
    result = text
    for pattern, placeholder in PRONOUN_PAIRS:
        result = re.sub(pattern, placeholder, result, flags=re.IGNORECASE)

    # 第二阶段：将占位符替换为最终文本
    # Phase 2: Replace placeholders with final text
    for placeholder, final_text in PLACEHOLDER_MAP.items():
        result = result.replace(placeholder, final_text)

    return result


# ============================================================
# 步骤4：实现输入规范化函数
# Step 4: Implement input normalization function
# ============================================================

def normalize_input(text):
    """规范化用户输入：转换为小写并去除多余空格
    Normalize user input: convert to lowercase and remove extra whitespace"""

    # 转换为小写
    # Convert to lowercase
    text = text.lower()

    # 去除多余空格
    # Remove extra whitespace
    text = ' '.join(text.split())

    return text


# ============================================================
# 步骤5：实现响应生成函数
# Step 5: Implement response generation function
# ============================================================

def get_response(user_input):
    """根据用户输入生成ELIZA回复
    Generate ELIZA response based on user input"""

    # 规范化输入
    # Normalize input
    normalized = normalize_input(user_input)

    # 检查退出命令
    # Check for exit command
    if normalized in ['exit', 'quit', 'bye', 'goodbye']:
        return None

    # 遍历所有规则，寻找匹配
    # Iterate through all rules to find a match
    for pattern, responses in RULES:
        match = re.search(pattern, normalized, re.IGNORECASE)
        if match:
            # 随机选择一个回复模板
            # Randomly select a response template
            response = random.choice(responses)

            # 如果有捕获组，进行代词转换并替换
            # If there are capture groups, transform pronouns and substitute
            if match.groups():
                captured = match.group(1)
                transformed = transform_pronouns(captured)
                response = response.format(transformed)

            return response

    # 无匹配时使用默认回复
    # Use default response when no rules match
    return random.choice(DEFAULT_RESPONSES)


# ============================================================
# 步骤6：运行ELIZA聊天机器人演示
# Step 6: Run ELIZA chatbot demonstration
# ============================================================

def main():
    """运行ELIZA聊天机器人演示
    Run ELIZA chatbot demonstration"""

    print("=" * 60)
    print("ELIZA Chatbot")
    print("A rule-based psychotherapist simulation")
    print("=" * 60)
    print()

    # 测试用例 - 展示各种规则的匹配
    # Test cases - demonstrate various rule matching
    test_inputs = [
        'hi',
        'i feel sad',
        'i am not feeling well',
        'long time',
        'my mother is always worried about me',
        'why do you ask me that',
        'can you help me',
        'i am depressed',
        'exit',
    ]

    # 运行对话演示
    # Run conversation demonstration
    for user_input in test_inputs:
        print(f"You:  {user_input}")

        # 生成回复
        # Generate response
        response = get_response(user_input)

        # 检查是否退出
        # Check if exit
        if response is None:
            print("ELIZA: Goodbye!")
            break

        print(f"ELIZA: {response}")
        print()


# 程序入口点
# Program entry point
if __name__ == "__main__":
    main()
