import { Component, ChangeDetectionStrategy, input, output, viewChild, ElementRef, AfterViewInit, OnDestroy, OnChanges, SimpleChanges, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, FormArray, FormControl, ReactiveFormsModule, Validators } from '@angular/forms';
import { User } from '../../../../domain/models';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
declare const bootstrap: any;

@Component({
  selector: 'app-user-modal',
  templateUrl: './user-modal.component.html',
  imports: [CommonModule, ReactiveFormsModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class UserModalComponent implements AfterViewInit, OnDestroy, OnChanges {
  private fb = inject(FormBuilder);

  user = input<User | null>(null);
  isEditMode = input.required<boolean>();
  allRoles = input<string[]>(['admin', 'editor', 'viewer', 'support']);

  save = output<User>();

  modalEl = viewChild.required<ElementRef>('userModal');
  private modalInstance: any | null = null;

  userForm: FormGroup;

  constructor() {
    this.userForm = this.fb.group({
      id: [''],
      firstName: ['', Validators.required],
      lastName: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      department: ['', Validators.required],
      location: ['', Validators.required],
      roles: this.fb.array([])
    });
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['user'] || changes['isEditMode']) {
      this.buildForm();
    }
  }

  ngAfterViewInit() {
    this.modalInstance = new bootstrap.Modal(this.modalEl().nativeElement);
  }

  ngOnDestroy() {
    this.modalInstance?.dispose();
  }

  open() {
    this.buildForm();
    this.modalInstance?.show();
  }

  close() {
    this.modalInstance?.hide();
  }

  private buildForm() {
    this.userForm.reset();
    const rolesFormArray = this.userForm.get('roles') as FormArray;
    rolesFormArray.clear();

    const userRoles = this.user()?.roles ?? [];

    this.allRoles().forEach(role => {
      rolesFormArray.push(new FormControl(userRoles.includes(role)));
    });

    if (this.isEditMode() && this.user()) {
      this.userForm.patchValue(this.user()!);
    }
  }

  get rolesFormArray() {
    return this.userForm.get('roles') as FormArray;
  }

  onSubmit() {
    if (this.userForm.invalid) {
      this.userForm.markAllAsTouched();
      return;
    }

    const formValue = this.userForm.value;
    const selectedRoles = this.allRoles().filter((_, i) => formValue.roles[i]);

    const userToSave: User = {
      // Use existing user data as a base for edits
      ...(this.isEditMode() ? this.user() : {}),
      ...formValue,
      id: this.isEditMode() && this.user() ? this.user()!.id : `u${Date.now()}`,
      roles: selectedRoles
    };

    this.save.emit(userToSave);
    this.close();
  }
}
