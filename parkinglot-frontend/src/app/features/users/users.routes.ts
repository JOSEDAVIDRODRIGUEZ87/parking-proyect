import { Routes } from '@angular/router';

export const usersRoutes: Routes = [
    {
        path: '',
        loadComponent: () =>
            import('./user-list/user-list')
                .then(m => m.UserList)
    },
    {
        path: 'create',
        loadComponent: () =>
            import('./user-create/user-create')
                .then(m => m.UserCreate)
    },
    {
        path: 'detail/:id',
        loadComponent: () =>
            import('./user-detail/user-detail')
                .then(m => m.UserDetail)
    }
    
];