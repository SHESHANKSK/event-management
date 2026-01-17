import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { ApiEvent, Event, AttendanceRecord } from '../../domain/models';

@Injectable({ providedIn: 'root' })
export class EventApiService {
    private http = inject(HttpClient);
    private baseUrl = 'http://127.0.0.1:8000';

    getEvents(): Observable<Event[]> {
        return this.http.get<ApiEvent[]>(`${this.baseUrl}/events/`).pipe(
            map(apiEvents => apiEvents.map(e => this.mapToDomain(e)))
        );
    }

    getEventById(id: string): Observable<Event> {
        return this.http.get<ApiEvent>(`${this.baseUrl}/events/${id}`).pipe(
            map(apiEvent => this.mapToDomain(apiEvent))
        );
    }

    createEvent(payload: Partial<ApiEvent>): Observable<Event> {
        return this.http.post<ApiEvent>(`${this.baseUrl}/events/`, payload).pipe(
            map(apiEvent => this.mapToDomain(apiEvent))
        );
    }

    updateEvent(id: string, payload: Partial<ApiEvent>): Observable<Event> {
        return this.http.put<ApiEvent>(`${this.baseUrl}/events/${id}`, payload).pipe(
            map(apiEvent => this.mapToDomain(apiEvent))
        );
    }

    deleteEvent(id: string): Observable<void> {
        return this.http.delete<void>(`${this.baseUrl}/events/${id}`);
    }

    getAttendance(eventId: string): Observable<AttendanceRecord[]> {
        return this.http.get<AttendanceRecord[]>(`${this.baseUrl}/attendance/event/${eventId}`);
    }

    uploadAttendance(eventId: string, file: File): Observable<AttendanceRecord[]> {
        const formData = new FormData();
        formData.append('file', file);
        return this.http.post<AttendanceRecord[]>(`${this.baseUrl}/attendance/upload/${eventId}`, formData);
    }

    private mapToDomain(apiEvent: ApiEvent): Event {
        return {
            eventId: apiEvent.event_id,
            title: apiEvent.event_name,
            description: apiEvent.event_description || '',
            eventDate: apiEvent.event_date,
            status: apiEvent.event_status,
            organizerTeam: apiEvent.organizing_team,
            totalAttendees: apiEvent.participants_count || 0,
            averageDuration: apiEvent.average_duration || 0,
            createdBy: apiEvent.created_by,
            createdAt: apiEvent.created_at,
            updatedBy: apiEvent.updated_by ? String(apiEvent.updated_by) : undefined,
            updatedAt: apiEvent.updated_at
        };
    }
}
