import { defineStore } from 'pinia';

export const useServicesStore = defineStore('servicesStore', {
    state: () => ({
        services: []  // Inicialmente vazio, será preenchido com os serviços habilitados
    }),
    actions: {
        setServices(userServices) {
            const availableServices = [];

            if (userServices.limpa_pasta === 1) {
                availableServices.push({
                    title: 'Limpa Pasta',
                    description: 'Serviço de limpeza de pastas em arquivos ZIP',
                    image: '/path/to/limpa_pasta_image.jpg'
                });
            }

            if (userServices.limpa_nome === 1) {
                availableServices.push({
                    title: 'Limpa Nome',
                    description: 'Serviço de remoção de nomes de órgãos de proteção ao crédito',
                    image: '/path/to/limpa_nome_image.jpg'
                });
            }

            this.services = availableServices;
        }
    }
});
