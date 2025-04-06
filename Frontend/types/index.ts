export interface Message {
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
}

export interface MediaRecorderWithStream extends MediaRecorder {
  stream: MediaStream;
}