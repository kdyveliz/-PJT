import { createRouter, createWebHistory } from 'vue-router';
import ExchangeCalculator from '@/components/ExchangeCalculator.vue';
import BankLocator from '@/components/BankLocator.vue';

const routes = [
  { path: '/calculator',
    name: 'Calculator',
    component: ExchangeCalculator 
  },
  {
    path: '/bank-locator',
    name: 'BankLocator',
    component: BankLocator
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
