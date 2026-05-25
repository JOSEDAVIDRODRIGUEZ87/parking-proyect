import { Routes } from '@angular/router';

export const vehiclesRoutes: Routes = [
    {
        path: '',
        loadComponent: () =>
            import('./vehicle-list/vehicle-list')
                .then(m => m.VehicleList)
    },
    {
        path: 'create-vehicle',
        loadComponent: () =>
            import('./vehicle-create/vehicle-create')
                .then(m => m.VehicleCreate)
    },
    {
        path: 'detail/:id',
        loadComponent: () =>
            import('./vehicle-detail/vehicle-detail')
                .then(m => m.VehicleDetail)
    }
];