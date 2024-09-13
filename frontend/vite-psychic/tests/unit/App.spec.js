import { mount } from '@vue/test-utils';
import App from '../../src/App.vue';
import { createRouter, createWebHistory } from 'vue-router';
import { describe, it, expect } from 'vitest';

const router = createRouter({
    history: createWebHistory(),
    routes: [] // Simule rotas vazias ou adicione as rotas reais se necessário
});

describe('App.vue', () => {
    it('renders AppNavbar component', async () => {
        const wrapper = mount(App, {
            global: {
                plugins: [router],  // Incluir o roteador no teste
            },
        });

        await router.isReady();  // Certifique-se de que o roteador está pronto

        expect(wrapper.findComponent({ name: 'AppNavbar' }).exists()).toBe(true);
    });
});
