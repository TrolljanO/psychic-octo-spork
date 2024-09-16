// stores/flashStore.js
import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useFlashStore = defineStore('flash', () => {
    const message = ref('');
    const type = ref('');

    function setMessage({ message: msg, type: msgType }) {
        message.value = msg;
        type.value = msgType;
    }

    function clearMessage() {
        message.value = '';
        type.value = '';
    }

    return { message, type, setMessage, clearMessage };
});
