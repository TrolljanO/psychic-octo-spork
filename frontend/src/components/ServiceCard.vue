<template>
  <div :class="['card', { 'disabled-card': disabled }]">
    <img :src="image" alt="Service Image" class="card-img-top">
    <div class="card-body">
      <h5 class="card-title">{{ title }}</h5>
      <p class="card-text">{{ description }}</p>
      <a v-if="!disabled" :href="link" class="btn btn-primary">Acessar Serviço</a>
      <span v-else class="btn btn-secondary disabled">Indisponível</span>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      required: true
    },
    description: {
      type: String,
      required: true
    },
    image: {
      type: String,
      required: true
    },
    link: {
      type: String,
      required: false,
      default: '#'
    },
    disabled: {
      type: Boolean,
      required: false,
      default: false
    }
  }
};
</script>

<style scoped>
.card {
  width: 18rem;
  margin: 1rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-5px);
}

.disabled-card {
  opacity: 0.5;
}

.card-img-top {
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  height: 200px;
  object-fit: cover;
}

.btn.disabled {
  cursor: not-allowed;
}
</style>
