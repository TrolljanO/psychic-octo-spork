import { defineStore } from 'pinia';

export const useFlashStore = defineStore('flash', {
    state: () => ({
        message: null,  // Certifique-se de que 'message' está definido no estado inicial
        type: null,     // Tipo de mensagem: 'success', 'error', etc.
    }),
    actions: {
        setFlash(message, type = 'info') {
            this.message = message;
            this.type = type;
        },
        clearFlash() {
            this.message = null;
            this.type = null;
        }
    }
});
