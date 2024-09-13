import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';  // Importando o Pinia
import { createVuetify } from 'vuetify';
import 'vuetify/styles'; // Certifique-se de que os estilos do Vuetify são importados

// Importa os componentes e diretivas do Vuetify
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';

// Cria a instância do Vuetify com os componentes e diretivas
const vuetify = createVuetify({
    components,
    directives,
});

// Cria a instância do Pinia
const pinia = createPinia();

// Cria a instância da aplicação Vue
const app = createApp(App);

// Usa as dependências necessárias
app.use(router);
app.use(pinia);  // Usando o Pinia na aplicação
app.use(vuetify);  // Usando o Vuetify na aplicação

// Monta a aplicação
app.mount('#app');
