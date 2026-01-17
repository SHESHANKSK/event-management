export type EventStatus = 'TODO' | 'IN_PROGRESS' | 'DONE' | 'CANCELLED';

export interface AttendanceRecord {
  attendance_id?: string;
  email: string;
  duration: number; // minutes
  role: string;
  full_name?: string;
  join_time?: string;
  leave_time?: string;
}

// Backend Model
export interface ApiEvent {
  event_id: string;
  event_name: string;
  event_description: string;
  event_date: string;
  event_status: EventStatus;
  organizing_team: string;
  participants_count: number;
  average_duration: number;
  created_by: string;
  created_at: string;
  updated_by?: string;
  updated_at: string;
}

// Frontend Model (mapped)
export interface Event {
  eventId: string;
  title: string;
  description: string;
  eventDate: string;
  status: EventStatus;
  organizerTeam: string;
  totalAttendees: number;
  averageDuration: number;
  attendance?: AttendanceRecord[];
  createdBy: string;
  createdAt: string; // ISO String
  updatedBy?: string;
  updatedAt: string; // ISO String
}

export interface ApiUser {
  uid: string;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  country_code: string;
  roles: string[];
  permissions: string[];
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface User {
  id: string;
  username: string;
  firstName: string;
  lastName: string;
  fullName: string;
  email: string;
  countryCode: string;
  roles: string[];
  permissions: string[];
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface AnalyticsData {
  completedEventsCount: number;
  totalMinutesAttended: number;
  averageAttendancePerEvent: number;
  attendanceByDepartment: { department: string; attendees: number }[];
}