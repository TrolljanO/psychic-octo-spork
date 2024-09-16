import axios from 'axios';

// Criação do cliente da API usando axios
const apiClient = axios.create({
    baseURL: 'http://localhost:5000',  // URL base do seu backend Flask
    headers: {
        'Content-Type': 'application/json',  // Configurando o tipo de conteúdo como JSON
    },
});

// Função para realizar o cadastro (signup)
export const signup = async (email, username, password, confirmPassword) => {
    try {
        const response = await apiClient.post('/auth/signup', {
            email: email,
            username: username,
            password: password,
            confirmPassword: confirmPassword
        });
        return response.data;
    } catch (error) {
        console.error('Erro no cadastro:', error);
        throw error;
    }
};


// Função para realizar o login
export const login = async (email, password) => {
    try {
        const response = await apiClient.post('/auth/login', {
            email: email,
            password: password,
        });
        return response.data;
    } catch (error) {
        console.error('Erro no login:', error);
        throw error;
    }
};

// Interceptor para adicionar o token JWT ao cabeçalho de cada requisição, caso o token exista
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
