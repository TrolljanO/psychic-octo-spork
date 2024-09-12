import axios from 'axios';

const apiClient = axios.create({
    baseURL: 'http://localhost:5000',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Interceptor para adicionar o token JWT ao cabeçalho de cada requisição
apiClient.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Interceptor para tratar respostas com erro 401 (token expirado ou inválido)
apiClient.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        if (error.response && error.response.status === 401) {
            // Se o token estiver inválido ou expirado, redirecionar para o login
            localStorage.removeItem('token');  // Remover token inválido
            window.location.href = '/login';   // Redirecionar para login
        }
        return Promise.reject(error);
    }
);

export default apiClient;
