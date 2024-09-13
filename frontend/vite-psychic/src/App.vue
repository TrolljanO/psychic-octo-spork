<template>
  <div id="app">
    <router-view></router-view>  <!-- Aqui os componentes serão renderizados -->
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

#app {
  margin-top: 70px; /* Para que o conteúdo não fique escondido atrás da navbar fixa */
}
</style>