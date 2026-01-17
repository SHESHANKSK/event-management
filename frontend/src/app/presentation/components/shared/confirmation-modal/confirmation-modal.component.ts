// FIX: Corrected casing for AfterViewInit lifecycle hook from 'afterViewInit' to 'AfterViewInit'.
import { Component, ChangeDetectionStrategy, input, output, ElementRef, viewChild, AfterViewInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
declare const bootstrap: any;

@Component({
  selector: 'app-confirmation-modal',
  templateUrl: './confirmation-modal.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [CommonModule],
})
export class ConfirmationModalComponent implements AfterViewInit, OnDestroy {
  title = input.required<string>();
  message = input.required<string>();
  confirmButtonText = input<string>('Delete');

  confirm = output<void>();

  modalEl = viewChild.required<ElementRef>('modal');
  confirmButtonEl = viewChild.required<ElementRef>('confirmButton');
  private modalInstance: any | null = null;
  
  ngAfterViewInit() {
    this.modalInstance = new bootstrap.Modal(this.modalEl().nativeElement);
    this.modalEl().nativeElement.addEventListener('shown.bs.modal', () => {
      this.confirmButtonEl().nativeElement.focus();
    });
  }

  ngOnDestroy() {
    this.modalInstance?.dispose();
  }

  open() {
    this.modalInstance?.show();
  }
  
  close() {
    this.modalInstance?.hide();
  }

  onConfirm() {
    this.confirm.emit();
    this.close();
  }
}
