<template>
  <PageWrapper title="文本省略示例">
    <CollapseContainer class="w-full bg-white rounded-md mb-4" title="Ellipsis 基本使用">
      <EllipsisText :maxWidth="240">{{ text }}</EllipsisText>
    </CollapseContainer>
    <CollapseContainer class="w-full bg-white rounded-md mb-4" title="Ellipsis 多行省略">
      <EllipsisText :line="2">{{ text }}</EllipsisText>
    </CollapseContainer>
    <CollapseContainer class="w-full bg-white rounded-md mb-4" title="Ellipsis 点击展开">
      <EllipsisText expand :line="3">{{ text }}</EllipsisText>
    </CollapseContainer>
    <CollapseContainer class="w-full bg-white rounded-md mb-4" title="Ellipsis 定制 Tooltip 内容">
      <EllipsisText :max-width="240">
        住在我心里孤独的 孤独的海怪 痛苦之王 开始厌倦 深海的光 停滞的海浪
        <template #tooltip>
          <div style="text-align: center">
            《秦皇岛》<br />住在我心里孤独的<br />孤独的海怪 痛苦之王<br />开始厌倦 深海的光
            停滞的海浪
          </div>
        </template>
      </EllipsisText>
    </CollapseContainer>
  </PageWrapper>
</template>
<script lang="ts" setup>
  import { ref } from 'vue';
  import { CollapseContainer } from '@/components/Container';
  import { EllipsisText } from '@/components/EllipsisText';
  import { PageWrapper } from '@/components/Page';

  const text = ref(
    `
    Hello World, 你好，世界！
   `,
  );
</script>
