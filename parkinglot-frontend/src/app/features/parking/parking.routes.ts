import { Routes } from '@angular/router';

export const parkingRoutes: Routes = [
    {
        path: '',
        loadComponent: () =>
            import('../parking/tickets/parking-tickets/parking-tickets')
                .then(m => m.ParkingTickets)
    },
    {
        path: 'entry',
        loadComponent: () =>
            import('../parking/entry/parking-entry/parking-entry')
                .then(m => m.ParkingEntry)
    },
    {
        path: 'exit',
        loadComponent: () =>
            import('../parking/exit/parking-exit/parking-exit')
                .then(m => m.ParkingExit)
    },
    {
        path: 'tickets',
        loadComponent: () =>
            import('../parking/tickets/parking-tickets/parking-tickets')
                .then(m => m.ParkingTickets)
    }
];