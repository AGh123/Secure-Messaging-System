import {
  ChangeDetectionStrategy,
  Component,
  computed,
  inject,
  signal,
  OnInit,
} from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';

import { AuthService } from './services/auth.service';
import { MessageService } from './services/message.service';
import { SessionService } from './services/session.service';

import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { TextareaModule } from 'primeng/textarea';
import { CardModule } from 'primeng/card';
import { ToastModule } from 'primeng/toast';
import { MessageService as ToastService } from 'primeng/api';

@Component({
  selector: 'app-root',
  imports: [
    ReactiveFormsModule,
    InputTextModule,
    ButtonModule,
    TextareaModule,
    CardModule,
    ToastModule,
  ],
  providers: [ToastService],
  templateUrl: './app.html',
  styleUrl: './app.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class App implements OnInit {
  private fb = inject(FormBuilder);
  private authService = inject(AuthService);
  private messageService = inject(MessageService);
  private session = inject(SessionService);
  private toast = inject(ToastService);

  /* ================= FORMS ================= */

  authForm = this.fb.nonNullable.group({
    username: ['', [Validators.required, Validators.minLength(3)]],
    password: ['', [Validators.required, Validators.minLength(6)]],
  });

  sendForm = this.fb.nonNullable.group({
    message: ['', Validators.required],
  });

  /* ================= STATE ================= */

  users = signal<string[]>([]);
  inbox = signal<{ from_user: string; count: number }[]>([]);
  selectedUser = signal<string | null>(null);
  receivedMessage = signal<string | null>(null);

  currentUser = computed(() => this.session.user()?.username ?? '');
  loggedIn = computed(() => this.session.isLoggedIn());

  /* ================= INIT ================= */

  ngOnInit() {
    this.authService.me()?.subscribe({
      next: (res) => {
        this.session.setUser(res.username);
        this.loadUsers();
        this.loadInbox();
      },
      error: () => this.session.clear(),
    });
  }

  /* ================= AUTH ================= */

  register() {
    if (this.authForm.invalid) return;

    this.authService.register(this.authForm.getRawValue()).subscribe({
      next: () =>
        this.toast.add({
          severity: 'success',
          summary: 'Registered',
        }),
      error: (err) =>
        this.toast.add({
          severity: 'error',
          summary: 'Error',
          detail: err.error?.detail,
        }),
    });
  }

  login() {
    if (this.authForm.invalid) return;

    this.authService.login(this.authForm.getRawValue()).subscribe({
      next: (res) => {
        this.session.setToken(res.token);
        this.authService.me()?.subscribe((me) => {
          this.session.setUser(me.username);
          this.loadUsers();
          this.loadInbox();
        });
        this.toast.add({ severity: 'success', summary: 'Logged in' });
      },
      error: (err) =>
        this.toast.add({
          severity: 'error',
          summary: 'Login failed',
          detail: err.error?.detail,
        }),
    });
  }

  logout() {
    this.authService.logout()?.subscribe(() => {
      this.session.clear();
      this.users.set([]);
      this.inbox.set([]);
      this.selectedUser.set(null);
      this.receivedMessage.set(null);
      this.sendForm.reset();
      this.toast.add({ severity: 'info', summary: 'Logged out' });
    });
  }

  /* ================= USERS ================= */

  loadUsers() {
    this.authService.getUsers().subscribe((users) => this.users.set(users));
  }

  selectUser(user: string) {
    this.selectedUser.set(user);
    this.sendForm.reset();
  }

  /* ================= MESSAGES ================= */

  loadInbox() {
    this.messageService.getInbox().subscribe((data) => this.inbox.set(data));
  }

  sendMessage() {
    if (this.sendForm.invalid || !this.selectedUser()) return;

    this.messageService
      .sendMessage({
        receiver: this.selectedUser()!,
        plaintext: this.sendForm.controls.message.value,
      })
      .subscribe(() => {
        this.sendForm.reset();
        this.toast.add({ severity: 'success', summary: 'Message sent' });
      });
  }

  openMessage(fromUser: string) {
    this.messageService.openMessage(fromUser).subscribe((res) => {
      this.receivedMessage.set(res.plaintext);
      this.loadInbox();
      this.toast.add({
        severity: 'info',
        summary: 'Message opened',
        detail: 'Message has been deleted',
      });
    });
  }
}
