import { defineStore } from 'pinia';

export const useAuthStore = defineStore('authStore', {
    state: () => ({
        token: null,  // Armazena o token de autenticação
    }),
    getters: {
        isLoggedIn: (state) => !!state.token,  // Verifica se o usuário está logado
    },
    actions: {
        login(token) {
            this.token = token;  // Define o token ao fazer login
        },
        logout() {
            this.token = null;  // Remove o token ao fazer logout
        },
    },
});
