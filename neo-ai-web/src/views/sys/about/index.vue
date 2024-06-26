<template>
  <PageWrapper title="设置">
    <template #headerContent>
      <div class="flex justify-between items-center">
        <span class="flex-1">
          在线大模型<br/>
          <ul>
            <li class="setting-li">1. 文心一言-ernie-speed-128k</li>
            <li class="setting-li">2. 文心一言-ernie_speed</li>
            <li class="setting-li">3. 通义千问-qwen-turbo</li>
            <li class="setting-li">4. Llama-2-13B-v1</li>
          </ul>

          私有化大模型<br/>
          <ul>
            <li class="setting-li">1. 通义千问-qwen-2</li>
            <li class="setting-li">3. 通义千问-qwen-turbo</li>
            <li class="setting-li">3. Llama-3</li>
          </ul>
        </span>
      </div>
    </template>
  </PageWrapper>
</template>
<script lang="ts" setup>
  import { PageWrapper } from '@/components/Page';
  import {DescItem } from '@/components/Description';

  const { pkg } = __APP_INFO__;

  const { dependencies, devDependencies, name } = pkg;

  const schema: DescItem[] = [];
  const devSchema: DescItem[] = [];

  Object.keys(dependencies).forEach((key) => {
    schema.push({ field: key, label: key });
  });

  Object.keys(devDependencies).forEach((key) => {
    devSchema.push({ field: key, label: key });
  });

</script>

<style>
.setting-li {
  margin-left: 20px;
}
</style>