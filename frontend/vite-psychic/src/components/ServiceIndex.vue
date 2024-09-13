<template>
  <v-container>
    <v-row>
      <v-col
          v-for="(service, index) in services"
          :key="index"
          cols="12"
          md="4"
      >
        <ServiceCard :title="service.title" :image="service.image" @viewDetails="viewDetails(service)">
          <template #description>
            {{ service.description }}
          </template>
        </ServiceCard>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { useServicesStore } from '../stores/servicesStore';  // Usando a store para gerenciar serviços
import ServiceCard from './ServiceCard.vue';
import apiClient from '../api/api';  // Axios para fazer requisições à API

export default {
  name: 'ServiceIndex',
  components: {
    ServiceCard,
  },
  computed: {
    services() {
      const servicesStore = useServicesStore();
      return servicesStore.services;  // Obtém os serviços habilitados da store
    }
  },
  mounted() {
    this.fetchServices();  // Chama o método para buscar serviços do backend
  },
  methods: {
    async fetchServices() {
      try {
        const response = await apiClient.get('/user/services');  // Chama a API que retorna os serviços habilitados
        const userServices = response.data;

        // Atualiza a store com base nos serviços habilitados
        const servicesStore = useServicesStore();
        servicesStore.setServices(userServices);
      } catch (error) {
        console.error('Erro ao buscar serviços:', error);
      }
    },
    viewDetails(service) {
      if (service.title === 'Limpa Pasta') {
        this.$router.push('/limpa_pasta');
      } else if (service.title === 'Limpa Nome') {
        this.$router.push('/limpa_nome');
      }
    }
  }
};
</script>
