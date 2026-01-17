import { Component, ChangeDetectionStrategy, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { EventFacade } from '../../../application/event.facade';
import { AnalyticsData, EventStatus } from '../../../domain/models';

@Component({
  selector: 'app-analytics-dashboard',
  templateUrl: './analytics-dashboard.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [CommonModule]
})
export class AnalyticsDashboardComponent {
  private eventFacade = inject(EventFacade);
  private allEvents = this.eventFacade.events;

  // Filter signals
  statusFilter = signal<EventStatus | 'ALL'>('ALL');
  dateFromFilter = signal<string>('');
  dateToFilter = signal<string>('');
  departmentFilter = signal<string>('');

  statuses: EventStatus[] = ['TODO', 'IN_PROGRESS', 'DONE', 'CANCELLED'];

  filteredEvents = computed(() => {
    const status = this.statusFilter();
    const from = this.dateFromFilter();
    const to = this.dateToFilter();
    const organizer = this.departmentFilter().toLowerCase(); // Reusing filter for organizer

    return this.allEvents().filter(event => {
      const statusMatch = status === 'ALL' || event.status === status;
      const organizerMatch = !organizer || event.organizerTeam.toLowerCase().includes(organizer);

      const eventDate = new Date(event.eventDate);
      const fromDate = from ? new Date(from) : null;
      const toDate = to ? new Date(to) : null;

      const dateMatch = (!fromDate || eventDate >= fromDate) && (!toDate || eventDate <= toDate);

      return statusMatch && organizerMatch && dateMatch;
    });
  });

  analyticsData = computed<AnalyticsData>(() => {
    const events = this.filteredEvents();

    if (events.length === 0) {
      return {
        completedEventsCount: 0,
        totalMinutesAttended: 0,
        averageAttendancePerEvent: 0,
        attendanceByDepartment: []
      };
    }

    const completedEventsCount = events.filter(e => e.status === 'DONE').length;
    // Approximating total minutes as avg * attendees
    const totalMinutesAttended = events.reduce((sum, e) => sum + (e.averageDuration * e.totalAttendees), 0);
    const totalAttendees = events.reduce((sum, e) => sum + e.totalAttendees, 0);
    const averageAttendancePerEvent = Math.round(totalAttendees / events.length) || 0;

    const attendanceByDeptMap = new Map<string, number>();
    for (const event of events) {
      // Using organizerTeam as "Department" for analytics
      const currentAttendees = attendanceByDeptMap.get(event.organizerTeam) || 0;
      attendanceByDeptMap.set(event.organizerTeam, currentAttendees + event.totalAttendees);
    }

    const attendanceByDepartment = Array.from(attendanceByDeptMap.entries())
      .map(([department, attendees]) => ({ department, attendees }))
      .sort((a, b) => b.attendees - a.attendees);

    return {
      completedEventsCount,
      totalMinutesAttended,
      averageAttendancePerEvent,
      attendanceByDepartment
    };
  });

  maxAttendees = computed(() => {
    const data = this.analyticsData()?.attendanceByDepartment;
    if (!data || data.length === 0) {
      return 0;
    }
    return Math.max(...data.map(d => d.attendees));
  });

  getBarHeight(attendees: number): string {
    const max = this.maxAttendees();
    if (max === 0) {
      return '0%';
    }
    const percentage = (attendees / max) * 100;
    return `${percentage}%`;
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
}
