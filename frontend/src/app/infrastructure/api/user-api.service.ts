import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { ApiUser, User } from '../../domain/models';

@Injectable({ providedIn: 'root' })
export class UserApiService {
    private http = inject(HttpClient);
    private baseUrl = 'http://127.0.0.1:8000';

    getUsers(): Observable<User[]> {
        return this.http.get<ApiUser[]>(`${this.baseUrl}/users/`).pipe(
            map(apiUsers => apiUsers.map(u => this.mapToDomain(u)))
        );
    }

    createUser(payload: any): Observable<User> {
        return this.http.post<ApiUser>(`${this.baseUrl}/users/`, payload).pipe(
            map(apiUser => this.mapToDomain(apiUser))
        );
    }

    updateUser(id: string, payload: any): Observable<User> {
        return this.http.put<ApiUser>(`${this.baseUrl}/users/${id}`, payload).pipe(
            map(apiUser => this.mapToDomain(apiUser))
        );
    }

    deleteUser(id: string): Observable<void> {
        return this.http.delete<void>(`${this.baseUrl}/users/${id}`);
    }

    private mapToDomain(apiUser: ApiUser): User {
        return {
            id: apiUser.uid,
            username: apiUser.username,
            firstName: apiUser.first_name,
            lastName: apiUser.last_name,
            fullName: `${apiUser.first_name} ${apiUser.last_name}`,
            email: apiUser.email,
            countryCode: apiUser.country_code,
            roles: apiUser.roles,
            permissions: apiUser.permissions,
            isActive: apiUser.is_active,
            createdAt: apiUser.created_at,
            updatedAt: apiUser.updated_at
        };
    }
}
