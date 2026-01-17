import { Component, ChangeDetectionStrategy, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { EventFacade } from '../../../application/event.facade';
import { Event, EventStatus, AttendanceRecord } from '../../../domain/models';

@Component({
  selector: 'app-event-detail',
  templateUrl: './event-detail.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [CommonModule, RouterLink, ReactiveFormsModule]
})
export class EventDetailComponent {
  private route = inject(ActivatedRoute);
  private eventFacade = inject(EventFacade);
  private fb = inject(FormBuilder);

  event = signal<Event | undefined>(undefined);

  eventForm = this.fb.group({
    title: [''],
    eventDate: [''],
    organizerTeam: [''],
    department: [''],
    description: ['']
  });

  isReadOnly = computed(() => this.event()?.status === 'DONE' || this.event()?.status === 'CANCELLED');

  constructor() {
    const eventId = this.route.snapshot.paramMap.get('id');
    if (eventId) {
      this.loadEvent(eventId);
    }
  }

  loadEvent(eventId: string) {
    this.eventFacade.getEvent(eventId).subscribe({
      next: (foundEvent: Event) => {
        this.event.set(foundEvent);
        if (foundEvent) {
          this.eventForm.patchValue({
            title: foundEvent.title,
            eventDate: foundEvent.eventDate,
            organizerTeam: foundEvent.organizerTeam,
            description: foundEvent.description,
          });

          if (this.isReadOnly()) {
            this.eventForm.disable();
          }

          // Load Attendance
          this.eventFacade.getAttendance(eventId).subscribe(records => {
            const current = this.event();
            if (current) {
              // Update local event object with attendance data for view
              // We shouldn't mutate signals directly usually, but we are setting a new object
              this.event.set({ ...current, attendance: records });
            }
          });
        }
      },
      error: (e: any) => console.error(e)
    });
  }

  getBadgeClass(status: EventStatus | undefined): string {
    if (!status) return 'bg-secondary-subtle text-secondary-emphasis';
    switch (status) {
      case 'DONE': return 'bg-success-subtle text-success-emphasis';
      case 'IN_PROGRESS': return 'bg-primary-subtle text-primary-emphasis';
      case 'TODO': return 'bg-warning-subtle text-warning-emphasis';
      case 'CANCELLED': return 'bg-danger-subtle text-danger-emphasis';
      default: return 'bg-secondary-subtle text-secondary-emphasis';
    }
  }

  saveChanges() {
    if (this.eventForm.valid && this.event()) {
      const id = this.event()!.eventId;
      this.eventFacade.updateEvent(id, { ...this.eventForm.value, status: this.event()?.status }).subscribe({
        next: () => alert('Changes saved successfully.'),
        error: (err) => alert('Failed to save changes: ' + err.message)
      });
    }
  }

  onFileSelected(event: any) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file = input.files[0];
      const eventId = this.event()?.eventId;

      if (eventId) {
        this.eventFacade.uploadAttendance(eventId, file).subscribe({
          next: (records) => {
            alert(`Uploaded ${records.length} records.`);
            // Reload event to get updated stats and attendance
            this.loadEvent(eventId);
          },
          error: (err) => {
            alert('Upload failed: ' + err.error?.detail || err.message);
          }
        });
      }
      input.value = '';
    }
  }
}