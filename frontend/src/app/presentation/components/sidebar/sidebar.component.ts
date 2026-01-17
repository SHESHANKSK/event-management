import { Component, ChangeDetectionStrategy, signal } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

interface NavLink {
  path: string;
  label: string;
  icon: string;
}

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [RouterLink, RouterLinkActive]
})
export class SidebarComponent {
  navLinks = signal<NavLink[]>([
    { path: '/events', label: 'Events', icon: 'M13 10V3L4 14h7v7l9-11h-7z' },
    { path: '/analytics', label: 'Analytics', icon: 'M3 13.125C3 12.504 3.504 12 4.125 12H8.25c.621 0 1.125.504 1.125 1.125v6.75C9.375 20.496 8.871 21 8.25 21H4.125C3.504 21 3 20.496 3 19.875v-6.75zM14.625 6C15.246 6 15.75 6.504 15.75 7.125v12.75c0 .621-.504 1.125-1.125 1.125H11.25c-.621 0-1.125-.504-1.125-1.125V7.125C10.125 6.504 10.629 6 11.25 6h3.375zM20.25 10.125v9.75c0 .621.504 1.125 1.125 1.125h.375c.621 0 1.125-.504 1.125-1.125v-9.75c0-.621-.504-1.125-1.125-1.125h-.375c-.621 0-1.125.504-1.125 1.125z' },
    { path: '/users', label: 'User Management', icon: 'M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2' }
  ]);
}