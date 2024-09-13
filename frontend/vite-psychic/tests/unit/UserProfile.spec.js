import { mount } from '@vue/test-utils';
import { describe, it, expect } from 'vitest';
import Profile from '../../src/components/Profile.vue';
import apiClient from '../../src/api/api';  // Importa o cliente de API
import MockAdapter from 'axios-mock-adapter';


function flushPromises() {
    return new Promise(setImmediate);
}

describe('Profile.vue', () => {
    it('displays user data after API call', async () => {
        // Cria o mock para interceptar requisições Axios
        const mock = new MockAdapter(apiClient);

        // Simula a resposta da API com o nome "Mocked User"
        const mockData = { name: 'Mocked User' };
        mock.onGet('http://localhost:5000/user').reply(200, mockData);

        // Monta o componente para teste
        const wrapper = mount(Profile);

        // Aguarda o componente carregar os dados da API
        await flushPromises();  // Garante que todas as promessas sejam resolvidas

        // Verifica se o nome "Mocked User" é exibido no componente
        expect(wrapper.text()).toContain('Mocked User');

    });
});
