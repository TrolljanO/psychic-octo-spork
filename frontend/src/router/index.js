import { createRouter, createWebHistory } from 'vue-router';
import LimpaPasta from '../components/LimpaPasta.vue'; // Página do Limpa Pasta
import Profile from '../components/Profile.vue'; // Página de perfil
import Finance from '../components/Finance.vue';
import ServiceIndex from "@/components/ServiceIndex.vue";
import NotFound from "@/components/NotFound.vue"; // Página de financeiro

const routes = [
    {
        path: '/',
        name: 'Home',
        component: ServiceIndex,
    },
    {
        path: '/limpa-pasta',
        name: 'LimpaPasta',
        component: LimpaPasta,
    },
    {
        path: '/profile',
        name: 'Profile',
        component: Profile,
    },
    {
        path: '/finance',
        name: 'Finance',
        component: Finance,
    },
    {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: NotFound
    },
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

export default router;
