import { createRouter, createWebHistory } from 'vue-router';
import Profile from '../components/Profile.vue';
import Finance from '../components/Finance.vue';
import Login from '../components/LoginForm.vue';
import Signup from '../components/SignupForm.vue';
import ServiceIndex from '../components/ServiceIndex.vue';
import { useAuthStore } from '@/stores/authStore'; // Store de autenticação

const routes = [
    { path: '/', component: Login },
    { path: '/login', component: Login },
    { path: '/signup', component: Signup },
    {
        path: '/index',
        component: ServiceIndex,
        meta: { requiresAuth: true },  // Protege a rota
    },
    {
        path: '/profile',
        component: Profile,
        meta: { requiresAuth: true },  // Protege a rota
    },
    {
        path: '/finance',
        component: Finance,
        meta: { requiresAuth: true },  // Protege a rota
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

// Guard global para verificar autenticação
router.beforeEach((to, from, next) => {
    const authStore = useAuthStore();

    if (to.meta.requiresAuth && !authStore.isLoggedIn) {
        // Se a rota requer autenticação e o usuário não está logado, redireciona para login
        next({ path: '/login' });
    } else {
        next();
    }
});

export default router;
