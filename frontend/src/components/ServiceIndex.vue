<template>
  <div class="service-index">
    <h2>Selecione um Serviço</h2>
    <div class="card-container">
      <ServiceCard
          title="Limpa Pasta"
          description="Realiza o processamento dos seus arquivos compactados."
          :image="require('@/assets/4.jpg')"          link="/limpa-pasta"
          :disabled="false"
      />
      <ServiceCard
          title="Outro Serviço"
          description="Serviço ainda indisponível."
          image="https://via.placeholder.com/300x200.png?text=Outro+Serviço"
          :disabled="true"
      />
      <!-- Adicione mais ServiceCards aqui conforme necessário -->
    </div>
  </div>
</template>

<script>
import ServiceCard from './ServiceCard.vue';

export default {
  components: {
    ServiceCard
  }
};
</script>

<style scoped>
.service-index {
  text-align: center;
  padding: 2rem;
}

.card-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
</style>
