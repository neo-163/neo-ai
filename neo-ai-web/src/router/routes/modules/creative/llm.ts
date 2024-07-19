import type { AppRouteModule } from '@/router/types';

import { LAYOUT } from '@/router/constant';
import { t } from '@/hooks/web/useI18n';

const llm: AppRouteModule = {
  path: '/llm',
  name: 'Llm',
  component: LAYOUT,
  redirect: '/llm/index',
  meta: {
    orderNo: 10000,
    hideChildrenInMenu: true,
    icon: 'whh:paintroll',
    title: t('routes.llm.llm.page'),
    hideMenu: true,
  },
  children: [
    {
      path: 'index',
      name: 'LlmPage',
      component: () => import('@/views/llm/native-llm.vue'),
      meta: {
        title: t('routes.llm.llm.page'),
        icon: 'whh:paintroll',
        hideMenu: true,
      },
    },
  ],
};

export default llm;
