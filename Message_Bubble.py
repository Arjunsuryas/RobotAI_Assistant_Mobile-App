import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { RobotAvatar } from './RobotAvatar';
import { User } from 'lucide-react-native';

interface MessageBubbleProps {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
}

export function MessageBubble({ role, content, timestamp }: MessageBubbleProps) {
  const isUser = role === 'user';

  return (
    <View style={[styles.container, isUser && styles.userContainer]}>
      {!isUser && (
        <View style={styles.avatarContainer}>
          <RobotAvatar size={36} />
        </View>
      )}

      <View style={[styles.bubble, isUser ? styles.userBubble : styles.assistantBubble]}>
        <Text style={[styles.text, isUser ? styles.userText : styles.assistantText]}>
          {content}
        </Text>
        {timestamp && (
          <Text style={[styles.timestamp, isUser ? styles.userTimestamp : styles.assistantTimestamp]}>
            {new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </Text>
        )}
      </View>

      {isUser && (
        <View style={styles.avatarContainer}>
          <View style={styles.userAvatar}>
            <User size={20} color="#fff" strokeWidth={2} />
          </View>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    marginVertical: 8,
    marginHorizontal: 16,
    alignItems: 'flex-end',
  },
  userContainer: {
    flexDirection: 'row-reverse',
  },
  avatarContainer: {
    marginHorizontal: 8,
  },
  userAvatar: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: '#6366f1',
    justifyContent: 'center',
    alignItems: 'center',
  },
  bubble: {
    maxWidth: '70%',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderRadius: 18,
  },
  userBubble: {
    backgroundColor: '#6366f1',
    borderBottomRightRadius: 4,
  },
  assistantBubble: {
    backgroundColor: '#1e293b',
    borderBottomLeftRadius: 4,
  },
  text: {
    fontSize: 16,
    lineHeight: 22,
  },
  userText: {
    color: '#fff',
  },
  assistantText: {
    color: '#e2e8f0',
  },
  timestamp: {
    fontSize: 11,
    marginTop: 4,
  },
  userTimestamp: {
    color: '#c7d2fe',
    textAlign: 'right',
  },
  assistantTimestamp: {
    color: '#64748b',
  },
});
