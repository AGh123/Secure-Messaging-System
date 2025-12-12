import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { SessionService } from './session.service';

export interface SendMessageRequest {
  receiver: string;
  plaintext: string;
}

export interface InboxItem {
  from_user: string;
  count: number;
}

export interface ReadMessageResponse {
  plaintext: string;
}

@Injectable({ providedIn: 'root' })
export class MessageService {
  private http = inject(HttpClient);
  private session = inject(SessionService);

  private readonly baseUrl = 'http://127.0.0.1:8000/messages';

  private authHeaders() {
    return {
      headers: new HttpHeaders({
        Authorization: this.session.token() ?? '',
      }),
    };
  }

  sendMessage(payload: SendMessageRequest) {
    return this.http.post(`${this.baseUrl}/send`, payload, this.authHeaders());
  }

  getInbox() {
    return this.http.get<InboxItem[]>(
      `${this.baseUrl}/inbox`,
      this.authHeaders()
    );
  }

  openMessage(fromUser: string) {
    return this.http.post<ReadMessageResponse>(
      `${this.baseUrl}/open`,
      { from_user: fromUser },
      this.authHeaders()
    );
  }
}
