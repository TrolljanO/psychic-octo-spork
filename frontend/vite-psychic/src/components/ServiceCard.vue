<template>
  <v-card class="mx-auto" max-width="400">
    <v-img
        :src="image"
        height="200px"
    ></v-img>
    <v-card-title>{{ title }}</v-card-title>
    <v-card-text>
      <slot name="description">Descrição padrão do serviço.</slot>
    </v-card-text>
    <v-card-actions>
      <v-btn text @click="viewDetails">Ver Detalhes</v-btn>
      <slot name="actions"></slot> <!-- Slot adicional para ações dinâmicas -->
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'ServiceCard',
  props: {
    title: {
      type: String,
      required: true,
    },
    image: {
      type: String,
      default: '', // Adiciona uma imagem padrão, se necessário
    }
  },
  methods: {
    viewDetails() {
      this.$emit('viewDetails'); // Emite um evento para o componente pai
    }
  }
};
</script>
