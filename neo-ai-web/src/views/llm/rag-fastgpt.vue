<template>
  <div class="chat-dialog">
    <div v-if="messages.length === 0" class="chat-header">
      <div class="avatar">
        <img src="../../assets/images/ai-avatar.png" alt="Assistant Avatar" />
      </div>
      <div class="header-info">
        <h2>AI助手</h2>
        <p>我是您的智能助手,欢迎与我对话!</p>
      </div>
    </div>
    <div
      class="chat-messages"
      @click.stop="toggleAutoScroll"
      ref="chatMessagesContainer"
    >
      <div v-if="messages.length === 0" class="welcome-message">
        <p>有什么我可以帮您的吗?请随时向我提问!</p>
      </div>
      <div
        v-for="(message, index) in messages"
        :key="index"
        class="message"
        :class="{
          'user-message': message.role === 'user',
          'assistant-message': message.role === 'assistant'
        }"
      >
        <div class="avatar" v-if="message.role === 'assistant'">
          <img src="../../assets/images/ai-avatar.png" alt="Assistant Avatar" />
        </div>
        <div class="content">
          <span v-html="renderedContent(message.content)"></span>
        </div>
      </div>
    </div>
    <div class="chat-input">
      <a-input
        v-model:value="inputMessage"
        placeholder="输入您的消息..."
        @keyup.enter="sendMessage"
      />
      <a-button
        type="primary"
        @click="sendMessage"
        :disabled="isAssistantResponding"
        >{{ isAssistantResponding ? '回复中...' : '发送' }}</a-button
      >
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, nextTick } from 'vue';
import { useMessage } from '/@/hooks/web/useMessage';
import * as marked from 'marked';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

const messages = ref<Message[]>([]);
const inputMessage = ref('');
const { createMessage } = useMessage();

const renderedContent = (content: string) => marked.parse(content);

const chatMessagesContainer = ref(null);
let autoScroll = true;
const isAssistantResponding = ref(false);

const scrollToBottom = () => {
  nextTick(() => {
    if (autoScroll && chatMessagesContainer.value) {
      chatMessagesContainer.value.scrollTop =
        chatMessagesContainer.value.scrollHeight;
    }
  });
};

const toggleAutoScroll = () => {
  autoScroll = !autoScroll;
};

const sendMessage = async () => {
  if (inputMessage.value.trim() === '' || isAssistantResponding.value) return;

  isAssistantResponding.value = true;
  messages.value.push({
    role: 'user',
    content: inputMessage.value
  });
  messages.value.push({
    role: 'assistant',
    content: ''
  }); // Add an empty message for streaming

  // Clear the input message immediately
  inputMessage.value = '';

  try {
    const myHeaders = new Headers();
    myHeaders.append('Content-Type', 'application/json');

    const raw = JSON.stringify({
      chatId: '111',
      stream: true,
      detail: false,
      messages: messages.value.map((msg) => ({
        content: msg.content,
        role: msg.role
      }))
    });

    const requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: raw
    };

    const baseUrl = import.meta.env.VITE_API_BASE_URL;
    const response = await fetch(`${baseUrl}/rag_fastgpt/ask`, requestOptions);

    if (response.ok) {
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let receivedData = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        receivedData += chunk;

        const parsedChunk = parseChunk(chunk);
        const lastMessageIndex = messages.value.length - 1;
        messages.value[lastMessageIndex].content += parsedChunk;
        scrollToBottom(); // Scroll down after updating the message content
      }
    } else {
      createMessage.error('聊天请求失败,请重试');
    }
  } catch (error) {
    createMessage.error('聊天请求失败,请重试');
  } finally {
    isAssistantResponding.value = false;
  }
};

const parseChunk = (chunk: string): string => {
  let result = '';
  try {
    const jsonArray = JSON.parse(chunk);
    for (const json of jsonArray) {
      if (json.choices && json.choices.length > 0) {
        const choice = json.choices[0];
        if (choice.delta && choice.delta.content) {
          result += choice.delta.content;
        }
      }
    }
  } catch (e) {
    // Ignore JSON parsing errors
  }
  return result;
};

</script>

<style lang="less" scoped>
.chat-dialog {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #f5f5f5;

  .chat-header {
    display: flex;
    align-items: center;
    padding: 16px;
    background-color: #fff;
    border-bottom: 1px solid #e8e8e8;

    .avatar {
      width: 60px;
      height: 60px;
      margin-right: 16px;

      img {
        width: 100%;
        height: 100%;
        border-radius: 50%;
        object-fit: cover;
      }
    }

    .header-info {
      h2 {
        font-size: 20px;
        font-weight: bold;
        color: #333;
        margin-bottom: 8px;
      }

      p {
        font-size: 14px;
        color: #666;
      }
    }
  }

  .chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 16px;

    .welcome-message {
      text-align: center;
      color: #666;
      font-size: 14px;
      margin-bottom: 16px;
    }

    .message {
      display: flex;
      margin-bottom: 20px;

      .avatar {
        width: 40px;
        height: 40px;
        margin-right: 12px;

        img {
          width: 100%;
          height: 100%;
          border-radius: 50%;
          object-fit: cover;
        }
      }

      .content {
        max-width: 70%;
        padding: 12px 16px;
        border-radius: 12px;
        font-size: 14px;
        line-height: 1.4;
        word-wrap: break-word;
      }

      &.user-message {
        justify-content: flex-end;

        .content {
          background-color: #1890ff;
          color: #fff;
          border-bottom-right-radius: 4px;
        }
      }

      &.assistant-message {
        justify-content: flex-start;

        .content {
          background-color: #fff;
          color: #333;
          border-bottom-left-radius: 4px;
          box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
        }
      }
    }
  }

  .chat-input {
    display: flex;
    align-items: center;
    padding: 16px;
    background-color: #fff;
    border-top: 1px solid #e8e8e8;

    .ant-input {
      flex: 1;
      margin-right: 12px;
      border-radius: 20px;
      border: none;
      padding: 10px 16px;
      font-size: 14px;
      background-color: #f0f0f0;
      transition: background-color 0.3s;

      &:focus {
        background-color: #fff;
        box-shadow: 0 0 0 2px #1890ff;
      }
    }

    .ant-btn {
      border-radius: 20px;
      font-weight: 500;
    }
  }
}
</style>