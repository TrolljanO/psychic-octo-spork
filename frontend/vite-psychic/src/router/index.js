import { createRouter, createWebHistory } from 'vue-router';
import Profile from '../components/Profile.vue';
import Finance from '../components/Finance.vue';
import Login from '../components/LoginForm.vue';
import Signup from '../components/SignupForm.vue';

const routes = [
    { path: '/', component: Login },
    { path: '/profile', component: Profile },
    { path: '/finance', component: Finance },
    { path: '/login', component: Login },
    { path: '/signup', component: Signup },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
