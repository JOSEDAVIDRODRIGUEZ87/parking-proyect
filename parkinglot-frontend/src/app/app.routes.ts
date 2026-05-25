import { Routes } from '@angular/router';

export const routes: Routes = [
    {
        path: '',
        loadComponent: () =>
            import('./features/auth/login/login')
                .then(m => m.Login)
    },

    {
        path: 'users',
        loadChildren: () =>
            import('./features/users/users.routes')
                .then(m => m.usersRoutes)
    },

    {
        path: 'vehicles',
        loadChildren: () =>
            import('./features/vehicles/vehicles.routes')
                .then(m => m.vehiclesRoutes)
    },

    {
        path: 'parking-entry',
        loadChildren: () =>
            import('./features/parking/parking.routes')
                .then(m => m.parkingRoutes)
    },

    // 🔥 fallback opcional (recomendado)
    {
        path: '**',
        redirectTo: ''
    }
];