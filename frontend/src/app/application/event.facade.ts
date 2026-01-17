import { Injectable, inject, signal } from '@angular/core';
import { EventApiService } from '../infrastructure/api/event-api.service';
import { Event } from '../domain/models';
import { tap } from 'rxjs/operators';

@Injectable({ providedIn: 'root' })
export class EventFacade {
    private api = inject(EventApiService);

    private eventsSignal = signal<Event[]>([]);
    events = this.eventsSignal.asReadonly();

    constructor() {
        this.loadEvents();
    }

    loadEvents() {
        this.api.getEvents().subscribe(events => this.eventsSignal.set(events));
    }

    getEvent(id: string) {
        return this.api.getEventById(id);
    }

    createEvent(eventData: any) {
        const payload = {
            event_name: eventData.title,
            event_description: eventData.description,
            event_date: eventData.eventDate,
            organizing_team: eventData.organizerTeam
        };
        return this.api.createEvent(payload).pipe(
            tap(() => this.loadEvents())
        );
    }

    updateEvent(id: string, eventData: any) {
        const payload = {
            event_name: eventData.title,
            event_description: eventData.description,
            organizing_team: eventData.organizerTeam,
            event_date: eventData.eventDate,
            event_status: eventData.status
        };
        return this.api.updateEvent(id, payload).pipe(
            tap(() => this.loadEvents())
        );
    }

    deleteEvent(id: string) {
        return this.api.deleteEvent(id).pipe(
            tap(() => this.loadEvents())
        );
    }

    getAttendance(eventId: string) {
        return this.api.getAttendance(eventId);
    }

    uploadAttendance(eventId: string, file: File) {
        return this.api.uploadAttendance(eventId, file).pipe(
            tap(() => this.loadEvents())
        );
    }
}
