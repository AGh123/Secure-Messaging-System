export interface SendMessageRequest {
  receiver: string;
  plaintext: string;
}

export interface SendMessageResponse {
  message_id: number;
}

export interface ReadMessageResponse {
  plaintext: string;
}
