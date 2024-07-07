<!-- index.vue -->
<template>
  <div class="chat-dialog">
    <div class="pdf-viewer-container" v-if="pdfUrl">
      <div class="pdf-viewer">
        <iframe :src="pdfUrl" frameborder="0" width="100%" height="100%"></iframe>
      </div>
    </div>
    <div class="chat-container" :class="{ 'full-width': !pdfUrl }">
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
            'assistant-message': message.role === 'assistant',
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
        <label
          for="pdf-upload"
          class="upload-button"
          :class="{ 'mobile-upload': isMobile }"
          :disabled="isUploading || isAssistantResponding"
          :style="{
            backgroundColor: isUploading || isAssistantResponding ? '#ccc' : '#1890ff',
            cursor: isUploading || isAssistantResponding ? 'not-allowed' : 'pointer',
          }"
        >
          <upload-outlined v-if="isMobile" />
          <span v-else>上传PDF文件</span>
        </label>
        <input
          id="pdf-upload"
          type="file"
          @change="uploadPDF"
          accept=".pdf"
          :disabled="isUploading || isAssistantResponding"
          style="display: none"
        />
        <a-input
          v-model:value="inputMessage"
          placeholder="输入您的消息..."
          @keyup.enter="handleInputMessage"
          :disabled="isUploading || isAssistantResponding"
        />
        <a-button
          type="primary"
          @click="handleInputMessage"
          :disabled="isAssistantResponding || isUploading"
          :style="{
            opacity: isAssistantResponding || isUploading ? 0.5 : 1,
            cursor: isAssistantResponding || isUploading ? 'not-allowed' : 'pointer',
          }"
        >{{ isAssistantResponding ? "回复中..." : isUploading ? "正在上传..." : "发送" }}</a-button>
        <a-button
          v-if="isUploading || isAssistantResponding"
          type="danger"
          @click="cancelRequest"
        >
          取消
        </a-button>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, nextTick, onMounted } from 'vue';
import { useMessage } from '/@/hooks/web/useMessage';
import * as marked from 'marked';
import { UploadOutlined } from '@ant-design/icons-vue';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

const messages = ref<Message[]>([]);
const inputMessage = ref('');
const { createMessage } = useMessage();
const renderedContent = computed(() => {
  return (content) => marked.parse(content);
});

const chatMessagesContainer = ref(null);
let autoScroll = true;
const isAssistantResponding = ref(false);
const isUploading = ref(false);
const pdfUrl = ref('');
const isMobile = ref(false);
let controller: AbortController | null = null;

const scrollToBottom = () => {
  nextTick(() => {
    if (autoScroll && chatMessagesContainer.value) {
      chatMessagesContainer.value.scrollTop = chatMessagesContainer.value.scrollHeight;
    }
  });
};

const toggleAutoScroll = () => {
  autoScroll = !autoScroll;
};

const baseUrl = import.meta.env.VITE_API_BASE_URL;

const uploadPDF = async (event: Event) => {
  if (isUploading.value || isAssistantResponding.value) return;

  isUploading.value = true;
  messages.value.push({ role: 'assistant', content: '文件上传中...' });

  const file = (event.target as HTMLInputElement).files?.[0];
  if (!file || file.type !== 'application/pdf') {
    createMessage.error('请选择一个PDF文件');
    isUploading.value = false;
    return;
  }

  pdfUrl.value = URL.createObjectURL(file);

  const formData = new FormData();
  formData.append('file', file);

  controller = new AbortController();

  try {
    const response = await fetch(`${baseUrl}/rag/upload`, {
      method: 'POST',
      body: formData,
      signal: controller.signal,
    });

    const lastMessageIndex = messages.value.length - 1;
    if (response.ok) {
      const reader = response.body?.getReader();
      if (!reader) {
        createMessage.error('无法读取响应');
        isUploading.value = false;
        return;
      }

      const decoder = new TextDecoder();
      let receivedData = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        receivedData += extractResultFromJSON(chunk);

        messages.value.splice(lastMessageIndex, 1); // Remove the "文件上传中..." message
        messages.value.push({ role: 'assistant', content: receivedData });
        scrollToBottom();
      }
    } else {
      createMessage.error('上传PDF文件失败');
      messages.value.splice(lastMessageIndex, 1); // Remove the "文件上传中..." message
    }
  } catch (error) {
    if (error.name !== 'AbortError') {
      createMessage.error('上传PDF文件失败');
      messages.value.splice(lastMessageIndex, 1); // Remove the "文件上传中..." message
    }
  } finally {
    controller = null;
    isUploading.value = false;
  }
};

const handleInputMessage = async () => {
  if (inputMessage.value.trim() === '' || isAssistantResponding.value || isUploading.value) return;

  sendMessage();
};

const sendMessage = async () => {
  isAssistantResponding.value = true;
  messages.value.push({ role: 'user', content: inputMessage.value });
  messages.value.push({ role: 'assistant', content: '回复中...' }); // Add a "回复中..." message

  // Clear the input message immediately
  inputMessage.value = '';

  controller = new AbortController();

  try {
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    const raw = JSON.stringify({
      question: messages.value[messages.value.length - 2].content, // The user's question
    });

    const requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: raw,
      signal: controller.signal,
    };

    const response = await fetch(`${baseUrl}/rag/ask`, requestOptions);

    if (response.ok) {
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let receivedData = '';

      const lastMessageIndex = messages.value.length - 1;
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        receivedData += extractResultFromJSON(chunk);

        messages.value.splice(lastMessageIndex, 1); // Remove the "回复中..." message
        messages.value.push({ role: 'assistant', content: receivedData });
        scrollToBottom(); // Scroll down after updating the message content
      }
    } else {
      createMessage.error('聊天请求失败,请重试');
    }
  } catch (error) {
    if (error.name !== 'AbortError') {
      createMessage.error('聊天请求失败,请重试');
    }
  } finally {
    controller = null;
    isAssistantResponding.value = false;
  }
};

const cancelRequest = () => {
  if (controller) {
    controller.abort();
    isUploading.value = false;
    isAssistantResponding.value = false;
  }
};

const extractResultFromJSON = (jsonString: string) => {
  try {
    const data = JSON.parse(jsonString);
    if (data && data.result) {
      return data.result;
    }
  } catch (error) {
    // 忽略解析错误
  }
  return '';
};

onMounted(() => {
  const userAgent = navigator.userAgent;
  isMobile.value = /iPhone|iPad|iPod|Android/i.test(userAgent);
});
</script>

<style lang="less" scoped>
.chat-dialog {
  display: flex;
  height: 100%;
  background-color: #f5f5f5;

  .pdf-viewer-container {
    width: 50%;
    height: 100%;
    border-right: 1px solid #e8e8e8;
    display: flex;
    flex-direction: column;

    .pdf-viewer {
      flex: 1;
      overflow: auto;
    }
  }

  .chat-container {
    width: 50%;
    display: flex;
    flex-direction: column;

    &.full-width {
      width: 100%;
    }

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

      .upload-button {
        display: inline-block;
        padding: 6px 12px;
        background-color: #1890ff;
        color: #fff;
        border-radius: 4px;
        cursor: pointer;
        margin-right: 12px;

        &.mobile-upload {
          padding: 6px;
          font-size: 18px;
        }
      }

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

        &:disabled {
          background-color: #f5f5f5;
          cursor: not-allowed;
        }
      }

      .ant-btn {
        border-radius: 20px;
        font-weight: 500;
      }
    }
  }
}
</style>