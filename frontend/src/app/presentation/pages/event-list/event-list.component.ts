import { Component, ChangeDetectionStrategy, inject, signal, computed, viewChild } from '@angular/core';
import { CommonModule, formatDate } from '@angular/common';
import { Router } from '@angular/router';
import { EventFacade } from '../../../application/event.facade';
import { Event, EventStatus } from '../../../domain/models';
import { ConfirmationModalComponent } from '../../components/shared/confirmation-modal/confirmation-modal.component';

@Component({
  selector: 'app-event-list',
  templateUrl: './event-list.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [CommonModule, ConfirmationModalComponent]
})
export class EventListComponent {
  private eventFacade = inject(EventFacade);
  private router = inject(Router);

  events = this.eventFacade.events;

  statusFilter = signal<EventStatus | 'ALL'>('ALL');
  dateFromFilter = signal<string>('');
  dateToFilter = signal<string>('');
  departmentFilter = signal<string>('');

  statuses: EventStatus[] = ['TODO', 'IN_PROGRESS', 'DONE', 'CANCELLED'];

  modal = viewChild.required(ConfirmationModalComponent);
  eventToDelete = signal<Event | null>(null);

  modalMessage = computed(() => {
    const event = this.eventToDelete();
    if (!event) return '';
    return `Are you sure you want to delete the event '${event.title}'? This action cannot be undone.`;
  });

  filteredEvents = computed(() => {
    const status = this.statusFilter();
    const from = this.dateFromFilter();
    const to = this.dateToFilter();
    const organizer = this.departmentFilter().toLowerCase();

    return this.events().filter(event => {
      const statusMatch = status === 'ALL' || event.status === status;
      const organizerMatch = !organizer || event.organizerTeam.toLowerCase().includes(organizer);

      const eventDate = new Date(event.eventDate);
      const fromDate = from ? new Date(from) : null;
      const toDate = to ? new Date(to) : null;

      const dateMatch = (!fromDate || eventDate >= fromDate) && (!toDate || eventDate <= toDate);

      return statusMatch && organizerMatch && dateMatch;
    });
  });

  getBadgeClass(status: EventStatus): string {
    switch (status) {
      case 'DONE': return 'bg-success-subtle text-success-emphasis';
      case 'IN_PROGRESS': return 'bg-primary-subtle text-primary-emphasis';
      case 'TODO': return 'bg-warning-subtle text-warning-emphasis';
      case 'CANCELLED': return 'bg-danger-subtle text-danger-emphasis';
      default: return 'bg-secondary-subtle text-secondary-emphasis';
    }
  }

  onStatusChange(event: any) {
    const target = event.target as HTMLSelectElement;
    this.statusFilter.set(target.value as EventStatus | 'ALL');
  }

  onDateFromChange(event: any) {
    const target = event.target as HTMLInputElement;
    this.dateFromFilter.set(target.value);
  }

  onDateToChange(event: any) {
    const target = event.target as HTMLInputElement;
    this.dateToFilter.set(target.value);
  }

  onDepartmentChange(event: any) {
    const target = event.target as HTMLInputElement;
    this.departmentFilter.set(target.value);
  }

  viewEvent(eventId: string) {
    this.router.navigate(['/events', eventId]);
  }

  editEvent(eventId: string) {
    // Navigate to edit view, for now same as detail view
    this.router.navigate(['/events', eventId]);
  }

  deleteEvent(event: Event) {
    this.eventToDelete.set(event);
    this.modal().open();
  }

  confirmDeleteEvent() {
    const event = this.eventToDelete();
    if (event) {
      // In a real app, this would call a service and handle confirmation
      console.log('Soft deleting event:', event.eventId);
      alert(`Event "${event.title}" would be soft-deleted.`);
      this.eventToDelete.set(null);
    }
  }

  formatDate(dateString: string): string {
    return formatDate(dateString, 'MMM d, y, h:mm a', 'en-US');
  }
}
