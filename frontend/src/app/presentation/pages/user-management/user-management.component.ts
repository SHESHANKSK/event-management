import { Component, ChangeDetectionStrategy, inject, signal, computed, viewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UserFacade } from '../../../application/user.facade';
import { User } from '../../../domain/models';
import { ConfirmationModalComponent } from '../../components/shared/confirmation-modal/confirmation-modal.component';
import { UserModalComponent } from './user-modal/user-modal.component';

@Component({
  selector: 'app-user-management',
  templateUrl: './user-management.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [CommonModule, ConfirmationModalComponent, UserModalComponent],
})
export class UserManagementComponent {
  private userFacade = inject(UserFacade);
  users = this.userFacade.users;

  confirmationModal = viewChild.required(ConfirmationModalComponent);
  userModal = viewChild.required(UserModalComponent);

  userToDelete = signal<User | null>(null);

  // State for the create/edit modal
  currentUser = signal<User | null>(null);
  isEditMode = signal(false);

  modalMessage = computed(() => {
    const user = this.userToDelete();
    if (!user) return '';
    return `Are you sure you want to delete the user '${user.firstName} ${user.lastName}'? This action cannot be undone.`;
  });

  getRoleClass(role: string): string {
    switch (role.toLowerCase()) {
      case 'admin': return 'bg-danger-subtle text-danger-emphasis';
      case 'editor': return 'bg-primary-subtle text-primary-emphasis';
      case 'viewer': return 'bg-secondary-subtle text-secondary-emphasis';
      case 'support': return 'bg-warning-subtle text-warning-emphasis';
      default: return 'bg-secondary-subtle text-secondary-emphasis';
    }
  }

  createUser() {
    this.isEditMode.set(false);
    this.currentUser.set(null);
    this.userModal().open();
  }

  editUser(user: User) {
    this.isEditMode.set(true);
    this.currentUser.set({ ...user }); // Pass a copy
    this.userModal().open();
  }

  deleteUser(user: User) {
    if (!user) {
      console.error('Attempted to initiate deletion for a null user.');
      return;
    }
    this.userToDelete.set(user);
    this.confirmationModal().open();
  }

  handleSaveUser(user: any) {
    if (this.isEditMode()) {
      // Expecting user object to have id from this.currentUser
      // We need to merge them 
      const updatedUser = { ...this.currentUser(), ...user };
      this.userFacade.updateUser(updatedUser.id, updatedUser).subscribe();
    } else {
      // user here is likely from form value, so check it matches expected format
      // calling dataService.createUser which expects backend format? 
      // UserModal likely returns { firstName, lastName... }
      // We need mapping to backend format { first_name, last_name... } for create

      const backendPayload = {
        username: user.username,
        first_name: user.firstName,
        last_name: user.lastName,
        email: user.email,
        roles: user.roles,
        country_code: 'US' // Default
      };

      this.userFacade.createUser(backendPayload).subscribe();
    }
  }

  confirmDeleteUser() {
    const user = this.userToDelete();
    if (!user) {
      console.warn('Delete confirmation was triggered, but no user was targeted.');
      return;
    }

    this.userFacade.deleteUser(user.id).subscribe();
    this.userToDelete.set(null);
  }
}
