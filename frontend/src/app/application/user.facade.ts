import { Injectable, inject, signal } from '@angular/core';
import { UserApiService } from '../infrastructure/api/user-api.service';
import { User } from '../domain/models';
import { tap } from 'rxjs/operators';

@Injectable({ providedIn: 'root' })
export class UserFacade {
    private api = inject(UserApiService);

    private usersSignal = signal<User[]>([]);
    users = this.usersSignal.asReadonly();

    constructor() {
        this.refreshUsers();
    }

    refreshUsers() {
        this.api.getUsers().subscribe(users => this.usersSignal.set(users));
    }

    createUser(userData: any) {
        return this.api.createUser(userData).pipe(
            tap(() => this.refreshUsers())
        );
    }

    updateUser(id: string, userData: any) {
        return this.api.updateUser(id, userData).pipe(
            tap(() => this.refreshUsers())
        );
    }

    deleteUser(userId: string) {
        return this.api.deleteUser(userId).pipe(
            tap(() => this.refreshUsers())
        );
    }
}
