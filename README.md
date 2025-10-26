# AI Virtual Assistant Mobile App

A complete, fully-functional AI virtual assistant mobile app built with React Native and Expo. Features an intelligent conversational interface with an animated robot avatar, conversation history tracking, and user customization options.

## Features

### Core Functionality
- **Interactive Chat Interface** - Real-time conversations with an AI assistant
- **Animated Robot Avatar** - Dynamic robot interface that pulses during conversations
- **Smart Responses** - Context-aware AI responses with personality
- **Conversation History** - Automatic saving and management of all conversations
- **User Authentication** - Secure email/password authentication with Supabase
- **Customizable Assistant** - Personalize your assistant's name and behavior

### User Experience
- **Modern UI/Design** - Clean, dark-themed interface with smooth animations
- **Message Bubbles** - Distinct styling for user and assistant messages
- **Typing Indicators** - Animated typing indicator when assistant is responding
- **Timestamp Display** - Track when each message was sent
- **Tab Navigation** - Easy navigation between Chat, History, and Settings

### Technical Features
- **Supabase Backend** - Real-time database with Row Level Security
- **Persistent Storage** - All conversations saved to database
- **User Preferences** - Customizable settings stored per user
- **Responsive Design** - Works seamlessly on all screen sizes
- **Cross-Platform** - Runs on iOS, Android, and Web

## How to Use

### Getting Started
1. Launch the app and create an account
2. Sign in with your email and password
3. Start chatting with your AI assistant

### Chat Screen
- Type your message in the input field at the bottom
- Tap the send button to send your message
- Watch the robot avatar animate as the assistant responds
- Create a new conversation by tapping the + button

### History Screen
- View all your past conversations
- See when each conversation was last updated
- Delete conversations you no longer need

### Settings Screen
- Customize your assistant's name
- View your account information
- Save your preferences
- Sign out when needed

## Technologies Used

- **React Native** - Mobile framework
- **Expo** - Development platform
- **Supabase** - Backend and authentication
- **TypeScript** - Type-safe development
- **Lucide React Native** - Icon library
- **Expo Router** - File-based routing

## Database Schema

### Conversations Table
Stores individual conversation sessions with titles and timestamps.

### Messages Table
Stores all messages with role (user/assistant) and content.

### User Preferences Table
Stores user customization settings like assistant name and theme.

## Security

- Row Level Security (RLS) enabled on all database tables
- Users can only access their own data
- Secure authentication with Supabase Auth
- Password requirements enforced

## Future Enhancements

Potential features for future versions:
- Voice input and text-to-speech
- Integration with external AI APIs (OpenAI, Claude, etc.)
- Image sharing and analysis
- Multi-language support
- Theme customization
- Export conversation transcripts
- Advanced AI memory and context awareness
