export interface Conversation {
  id: string;
  user_id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface Message {
  id: string;
  conversation_id: string;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
}

export interface UserPreferences {
  user_id: string;
  assistant_name: string;
  theme: 'light' | 'dark';
  updated_at: string;
}
