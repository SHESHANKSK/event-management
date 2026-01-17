import { Routes } from '@angular/router';
import { EventListComponent } from './presentation/pages/event-list/event-list.component';
import { EventDetailComponent } from './presentation/pages/event-detail/event-detail.component';
import { AnalyticsDashboardComponent } from './presentation/pages/analytics-dashboard/analytics-dashboard.component';
import { UserManagementComponent } from './presentation/pages/user-management/user-management.component';

export const APP_ROUTES: Routes = [
  { path: '', redirectTo: 'events', pathMatch: 'full' },
  { path: 'events', component: EventListComponent, title: 'Event List' },
  { path: 'events/:id', component: EventDetailComponent, title: 'Event Details' },
  { path: 'analytics', component: AnalyticsDashboardComponent, title: 'Analytics Dashboard' },
  { path: 'users', component: UserManagementComponent, title: 'User Management' },
  { path: '**', redirectTo: 'events' } // Fallback route
];