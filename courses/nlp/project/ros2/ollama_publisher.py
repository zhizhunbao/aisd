#!/usr/bin/env python3
"""
ROS 2 RAG Ollama Publisher Node (Part 2).

Subscribes to the 'words' topic (Whisper STT output),
queries local Ollama with knowledge.txt as RAG context,
and publishes the generated answer to the 'ollama_reply' topic.

Architecture:
  [Whisper STT] --words--> [OllamaPublisher] --ollama_reply--> [SpeakClient]

Local Ollama (localhost:11434) handles LLM generation.
knowledge.txt provides the RAG knowledge base context.
"""
import os
import sys
import time

try:
    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import String
except ImportError:
    print("ROS2 (rclpy) not installed. This module requires ROS2 environment.")
    print("Run this on the loaner laptop with ROS2 installed.")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("'requests' library not installed. Run: pip install requests")
    sys.exit(1)


# ── Whisper hallucination filter ─────────────────────────────────────────
# Known phrases that Whisper outputs when there is no real speech
HALLUCINATION_PHRASES = [
    "thank you", "thanks for watching", "subscribe",
    "like and subscribe", "see you next time",
    "you", "bye", "okay", "oh",
    "the end", "hmm", "uh", "um",
]


def is_hallucination(text: str) -> bool:
    """Filter out Whisper hallucinations and noise."""
    t = text.strip().lower()
    if len(t) < 3:
        return True
    if t in HALLUCINATION_PHRASES:
        return True
    # Repetition check: if > 60% of words are the same word
    words = t.split()
    if len(words) >= 3:
        from collections import Counter
        most_common_count = Counter(words).most_common(1)[0][1]
        if most_common_count / len(words) > 0.6:
            return True
    return False


class OllamaPublisher(Node):
    """
    ROS 2 node that bridges Whisper speech-to-text output
    to the local Ollama language model with knowledge.txt context.

    Parameters
    ----------
    ollama_url : str
        URL of the local Ollama API (default: 'http://localhost:11434').
    model : str
        Ollama model name (default: 'qwen2.5:0.5b').
    knowledge_file : str
        Path to knowledge.txt RAG context file.

    Subscriptions
    -------------
    words : std_msgs/String
        Transcribed text from Whisper STT (words_publisher).

    Publications
    ------------
    ollama_reply : std_msgs/String
        Generated answer from Ollama.
    """

    def __init__(self):
        super().__init__('ollama_publisher')

        # ── ROS 2 Parameters ─────────────────────────────────────────────
        self.declare_parameter('ollama_url', 'http://localhost:11434')
        self.ollama_url = (
            self.get_parameter('ollama_url').get_parameter_value().string_value
        )

        self.declare_parameter('model', 'qwen2.5:0.5b')
        self.model = (
            self.get_parameter('model').get_parameter_value().string_value
        )

        self.declare_parameter(
            'knowledge_file',
            os.path.expanduser('~/ros2_ws/knowledge/knowledge.txt')
        )
        self.knowledge_file = (
            self.get_parameter('knowledge_file')
            .get_parameter_value().string_value
        )

        # ── Load knowledge.txt as RAG context ─────────────────────────────
        self.knowledge = self._load_knowledge()

        # ── Publisher: ollama_reply ───────────────────────────────────────
        self.pub = self.create_publisher(String, 'ollama_reply', 10)

        # ── Subscriber: words (from Whisper STT) ─────────────────────────
        self.sub = self.create_subscription(String, 'words', self.cb, 10)

        # Prevent overlapping requests
        self.busy = False

        self.get_logger().info(
            f'[Init] OllamaPublisher initialized\n'
            f'  Ollama URL  : {self.ollama_url}\n'
            f'  Model       : {self.model}\n'
            f'  Knowledge   : {self.knowledge_file}\n'
            f'  Context len : {len(self.knowledge)} chars'
        )

    def _load_knowledge(self) -> str:
        """Load knowledge.txt file as RAG context string."""
        try:
            with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            self.get_logger().info(
                f'[Knowledge] Loaded {len(content)} chars from {self.knowledge_file}'
            )
            return content
        except FileNotFoundError:
            self.get_logger().warn(
                f'[Knowledge] File not found: {self.knowledge_file}'
            )
            return ""

    # ── Callback: Incoming speech text ───────────────────────────────────
    def cb(self, msg: String):
        """Handle incoming transcribed text from the Whisper model."""
        text = msg.data.strip()
        if text == "" or self.busy:
            return

        # Filter Whisper hallucinations
        if is_hallucination(text):
            self.get_logger().info(f'[Filter] Hallucination ignored: "{text}"')
            return

        self.busy = True
        self.get_logger().info(f'[Words] Received: "{text}"')

        try:
            reply = self._query_ollama(text)
        except Exception as e:
            self.get_logger().error(f'[Error] Ollama API error: {e}')
            self.busy = False
            return

        reply = (reply or "").strip()
        if reply:
            out = String()
            out.data = reply
            self.pub.publish(out)
            self.get_logger().info(f'[Reply] Published: "{out.data}"')

            # ── Dynamic cooldown to prevent echo loop ────────────────
            # gTTS speaks ~3 words/sec; wait for playback to finish
            # before accepting new input, otherwise the mic picks up
            # the speaker output and creates an infinite loop.
            word_count = len(reply.split())
            wait_time = max(15, word_count // 3 + 5)
            self.get_logger().info(
                f'[Cooldown] {word_count} words → waiting {wait_time}s'
            )
            time.sleep(wait_time)
        else:
            self.get_logger().warn('[Reply] Empty response from Ollama')

        self.busy = False

    # ── Query local Ollama API ───────────────────────────────────────────
    def _query_ollama(self, user_text: str) -> str:
        """
        Query local Ollama with knowledge.txt as system context.

        POST http://localhost:11434/api/generate
        {
            "model": "qwen2.5:0.5b",
            "system": "<knowledge context>",
            "prompt": "<user question>",
            "stream": false
        }
        """
        system_prompt = (
            "You are a helpful AI textbook assistant. "
            "Answer the user's question based on the following knowledge base. "
            "Be concise and accurate. If the answer is not in the knowledge base, "
            "say so honestly.\n\n"
            "=== KNOWLEDGE BASE ===\n"
            f"{self.knowledge}\n"
            "=== END KNOWLEDGE BASE ==="
        )

        payload = {
            "model": self.model,
            "system": system_prompt,
            "prompt": user_text,
            "stream": False,
        }

        self.get_logger().info(
            f'[Ollama] Sending query to local Ollama ({self.model})...'
        )
        res = requests.post(
            f'{self.ollama_url}/api/generate',
            json=payload,
            timeout=60.0,
        )
        res.raise_for_status()

        data = res.json()
        answer = data.get("response", "I could not generate an answer.")

        self.get_logger().info(
            f'[Ollama] Response generated ({len(answer)} chars)'
        )
        return answer


def main(args=None):
    rclpy.init(args=args)
    node = OllamaPublisher()
    try:
        node.get_logger().info('[Run] Node spinning, waiting for words...')
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('[Shutdown] Keyboard interrupt received')
    except Exception as e:
        node.get_logger().error(f'[Error] Node execution failed: {str(e)}')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
