import React, { useEffect, useRef } from 'react';
import { View, StyleSheet, Animated } from 'react-native';
import { RobotAvatar } from './RobotAvatar';

export function TypingIndicator() {
  const dot1Anim = useRef(new Animated.Value(0)).current;
  const dot2Anim = useRef(new Animated.Value(0)).current;
  const dot3Anim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    const createAnimation = (animValue: Animated.Value, delay: number) => {
      return Animated.loop(
        Animated.sequence([
          Animated.delay(delay),
          Animated.timing(animValue, {
            toValue: -8,
            duration: 400,
            useNativeDriver: true,
          }),
          Animated.timing(animValue, {
            toValue: 0,
            duration: 400,
            useNativeDriver: true,
          }),
        ])
      );
    };

    const animations = Animated.parallel([
      createAnimation(dot1Anim, 0),
      createAnimation(dot2Anim, 150),
      createAnimation(dot3Anim, 300),
    ]);

    animations.start();

    return () => animations.stop();
  }, []);

  return (
    <View style={styles.container}>
      <View style={styles.avatarContainer}>
        <RobotAvatar size={36} isTyping />
      </View>

      <View style={styles.bubble}>
        <View style={styles.dotsContainer}>
          <Animated.View
            style={[styles.dot, { transform: [{ translateY: dot1Anim }] }]}
          />
          <Animated.View
            style={[styles.dot, { transform: [{ translateY: dot2Anim }] }]}
          />
          <Animated.View
            style={[styles.dot, { transform: [{ translateY: dot3Anim }] }]}
          />
        </View>
      </View>
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
  avatarContainer: {
    marginHorizontal: 8,
  },
  bubble: {
    backgroundColor: '#1e293b',
    paddingHorizontal: 20,
    paddingVertical: 16,
    borderRadius: 18,
    borderBottomLeftRadius: 4,
  },
  dotsContainer: {
    flexDirection: 'row',
    gap: 6,
  },
  dot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: '#6366f1',
  },
});
