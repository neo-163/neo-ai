import type { AppRouteModule } from '@/router/types';

import { LAYOUT } from '@/router/constant';

const permission: AppRouteModule = {
  path: '/rag',
  name: 'Rag',
  component: LAYOUT,
  meta: {
    orderNo: 10001,
    icon: 'ion:build-outline',
    title: '知识库',
    // hideMenu: true,
  },
  children: [
    {
      path: 'index-fastgpt',
      name: 'Index-fastgpt',
      meta: {
        title: 'RAG+FastGPT',
      },
      component: () => import('@/views/llm/rag-fastgpt.vue'),
    },
    {
      path: 'index-faiss',
      name: 'Index-faiss',
      meta: {
        title: 'RAG+Faiss',
      },
      component: () => import('@/views/llm/rag-faiss.vue'),
    },
    {
      path: 'index-chroma',
      name: 'Index-chroma',
      meta: {
        title: 'RAG+Chroma',
      },
      component: () => import('@/views/llm/rag-chroma.vue'),
    },
  ],
};

export default permission;
