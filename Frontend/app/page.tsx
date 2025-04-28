"use client";

import { useState, useRef, useEffect, FormEvent, ChangeEvent } from 'react';
import { Mic, MicOff, Send, Bot, User, Loader2, AlertCircle } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Message, MediaRecorderWithStream } from '@/types';
import { Alert, AlertDescription } from "@/components/ui/alert";

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>('');
  const [isRecording, setIsRecording] = useState<boolean>(false);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [microphoneError, setMicrophoneError] = useState<string>('');
  const chatContainerRef = useRef<HTMLDivElement | null>(null);
  const mediaRecorderRef = useRef<MediaRecorderWithStream | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  const checkMicrophonePermission = async (): Promise<boolean> => {
    try {
      const permissionStatus = await navigator.permissions.query({ name: 'microphone' as PermissionName });
      
      if (permissionStatus.state === 'denied') {
        setMicrophoneError('Microphone access was denied. Please enable it in your browser settings to use voice recording.');
        return false;
      }
      
      return true;
    } catch (err) {
      console.error('Error checking microphone permission:', err);
      return false;
    }
  };

  const startRecording = async (): Promise<void> => {
    setMicrophoneError(''); // Clear any previous errors
    
    const hasPermission = await checkMicrophonePermission();
    if (!hasPermission) return;

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream) as MediaRecorderWithStream;
      
      mediaRecorderRef.current.ondataavailable = (event: BlobEvent) => {
        chunksRef.current.push(event.data);
      };

      mediaRecorderRef.current.onstop = () => {
        // Here you would typically send the audio data to your backend
        // For demo purposes, we'll just add a message
        const message = "Voice message processed...";
        handleNewMessage(message, 'user');
        handleNewMessage("I understood your voice message!", 'assistant');
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (err) {
      console.error('Error accessing microphone:', err);
      if (err instanceof Error) {
        if (err.name === 'NotAllowedError') {
          setMicrophoneError('Microphone access was denied. Please enable it in your browser settings to use voice recording.');
        } else {
          setMicrophoneError('Failed to access microphone. Please ensure your device has a working microphone.');
        }
      }
    }
  };

  const stopRecording = (): void => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
      setIsRecording(false);
    }
  };

  const handleNewMessage = (content: string, role: Message['role']): void => {
    setMessages(prev => [...prev, { content, role, timestamp: new Date() }]);
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>): Promise<void> => {
    e.preventDefault();
    if (!input.trim() || isProcessing) return;

    setIsProcessing(true);
    handleNewMessage(input, 'user');
    setInput('');

    //fetch response from the server
    try {
      const textInput = encodeURIComponent(input);
      const response = await fetch(`http://127.0.0.1:8000/ask-question?question=${textInput}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });

      if (!response.ok) throw new Error('Network response was not ok');

      const data = await response.json();
      handleNewMessage(data.result, 'assistant');
    } catch (error) {
      console.error('Error fetching response:', error);
      handleNewMessage('An error occurred while processing your request.', 'assistant');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-background">
      <header className="border-b">
        <div className="container mx-auto px-4 py-4 flex items-center gap-2">
          <Bot className="h-6 w-6 text-primary" />
          <h1 className="text-xl font-semibold">AI Assistant</h1>
        </div>
      </header>

      <main className="flex-1 overflow-hidden container mx-auto px-4 py-4 flex flex-col">
        {microphoneError && (
          <Alert variant="destructive" className="mb-4">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{microphoneError}</AlertDescription>
          </Alert>
        )}
        
        <div 
          ref={chatContainerRef}
          className="flex-1 overflow-y-auto space-y-4 pb-4"
        >
          {messages.map((message, index) => (
            <div
              key={index}
              className={cn(
                "flex items-start gap-3 max-w-3xl mx-auto",
                message.role === 'assistant' ? "flex-row" : "flex-row-reverse"
              )}
            >
              <div className={cn(
                "p-2 rounded-full",
                message.role === 'assistant' ? "bg-primary" : "bg-secondary"
              )}>
                {message.role === 'assistant' ? (
                  <Bot className="h-5 w-5 text-primary-foreground" />
                ) : (
                  <User className="h-5 w-5 text-secondary-foreground" />
                )}
              </div>
              <div className={cn(
                "rounded-lg p-4 flex-1",
                message.role === 'assistant' ? "bg-muted" : "bg-primary text-primary-foreground"
              )}>
                {message.content}
              </div>
            </div>
          ))}
          {isProcessing && (
            <div className="flex items-center justify-center">
              <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
            </div>
          )}
        </div>

        <form onSubmit={handleSubmit} className="mt-4 flex gap-2 items-end max-w-3xl mx-auto w-full">
          <div className="flex-1 relative">
            <textarea
              value={input}
              onChange={(e: ChangeEvent<HTMLTextAreaElement>) => setInput(e.target.value)}
              placeholder="Type your message..."
              className="w-full rounded-lg border bg-background px-4 py-3 pr-12 text-sm focus:outline-none focus:ring-2 focus:ring-primary min-h-[52px] max-h-32 resize-none"
              rows={1}
              disabled={isProcessing}
            />
          </div>
          
          <button
            type="button"
            onClick={isRecording ? stopRecording : startRecording}
            className={cn(
              "rounded-full p-3 transition-colors",
              isRecording 
                ? "bg-destructive text-destructive-foreground hover:bg-destructive/90"
                : "bg-secondary text-secondary-foreground hover:bg-secondary/80"
            )}
          >
            {isRecording ? (
              <MicOff className="h-5 w-5" />
            ) : (
              <Mic className="h-5 w-5" />
            )}
          </button>

          <button
            type="submit"
            disabled={!input.trim() || isProcessing}
            className="bg-primary text-primary-foreground rounded-full p-3 transition-colors hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="h-5 w-5" />
          </button>
        </form>
      </main>
    </div>
  );
}