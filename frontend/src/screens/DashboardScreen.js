import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { objectivesAPI, checkInAPI, tipsAPI } from '../api/client';
import useStore from '../store/useStore';

export default function DashboardScreen() {
  const { objectives, setObjectives, updateObjective, user } = useStore();
  const [loading, setLoading] = useState(true);
  const [dailyTip, setDailyTip] = useState(null);
  const [showCheckIn, setShowCheckIn] = useState(false);

  useEffect(() => {
    loadDashboard();
    loadDailyTip();
  }, []);

  const loadDashboard = async () => {
    try {
      const response = await objectivesAPI.getDailyPlan();
      setObjectives(response.data.objectives || []);
    } catch (error) {
      Alert.alert('Error', 'Failed to load daily plan');
    } finally {
      setLoading(false);
    }
  };

  const loadDailyTip = async () => {
    try {
      const response = await tipsAPI.getRandom();
      setDailyTip(response.data);
    } catch (error) {
      console.log('Failed to load tip');
    }
  };

  const toggleObjective = async (objective) => {
    try {
      const newStatus = !objective.is_completed;
      await objectivesAPI.update(objective.id, { is_completed: newStatus });
      updateObjective(objective.id, { is_completed: newStatus });
    } catch (error) {
      Alert.alert('Error', 'Failed to update objective');
    }
  };

  const handleEndOfDay = () => {
    setShowCheckIn(true);
  };

  const submitCheckIn = async (mood) => {
    try {
      await checkInAPI.submit({
        mood,
        notes: '',
        date: new Date().toISOString().split('T')[0],
      });
      setShowCheckIn(false);
      Alert.alert('Success', 'Check-in submitted! See you tomorrow.');
    } catch (error) {
      Alert.alert('Error', 'Failed to submit check-in');
    }
  };

  if (loading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color="#4F46E5" />
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.greeting}>Hello{user?.username ? `, ${user.username}` : ''}!</Text>
        <Text style={styles.date}>{new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })}</Text>
      </View>

      {dailyTip && (
        <View style={styles.tipCard}>
          <Text style={styles.tipCategory}>{dailyTip.category}</Text>
          <Text style={styles.tipContent}>{dailyTip.content}</Text>
          <Text style={styles.tipSource}>— {dailyTip.source}</Text>
        </View>
      )}

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Today's Objectives</Text>
        {objectives.length === 0 ? (
          <Text style={styles.emptyText}>No objectives for today</Text>
        ) : (
          objectives.map((objective) => (
            <TouchableOpacity
              key={objective.id}
              style={styles.objectiveCard}
              onPress={() => toggleObjective(objective)}
            >
              <View style={styles.checkbox}>
                {objective.is_completed && <Text style={styles.checkmark}>✓</Text>}
              </View>
              <Text
                style={[
                  styles.objectiveText,
                  objective.is_completed && styles.completedText,
                ]}
              >
                {objective.description}
              </Text>
            </TouchableOpacity>
          ))
        )}
      </View>

      <TouchableOpacity style={styles.checkInButton} onPress={handleEndOfDay}>
        <Text style={styles.checkInButtonText}>End of Day Check-In</Text>
      </TouchableOpacity>

      {showCheckIn && (
        <View style={styles.modal}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>How was your day?</Text>
            {['Productive', 'Tired', 'Stressful', 'Energetic', 'Focused'].map((mood) => (
              <TouchableOpacity
                key={mood}
                style={styles.moodButton}
                onPress={() => submitCheckIn(mood)}
              >
                <Text style={styles.moodButtonText}>{mood}</Text>
              </TouchableOpacity>
            ))}
            <TouchableOpacity onPress={() => setShowCheckIn(false)}>
              <Text style={styles.cancelText}>Cancel</Text>
            </TouchableOpacity>
          </View>
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F9FAFB',
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  header: {
    padding: 20,
    paddingTop: 60,
    backgroundColor: '#4F46E5',
  },
  greeting: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
  },
  date: {
    fontSize: 16,
    color: '#E0E7FF',
    marginTop: 5,
  },
  tipCard: {
    margin: 20,
    padding: 20,
    backgroundColor: '#FEF3C7',
    borderRadius: 12,
  },
  tipCategory: {
    fontSize: 12,
    fontWeight: 'bold',
    color: '#92400E',
    marginBottom: 8,
  },
  tipContent: {
    fontSize: 16,
    color: '#78350F',
    marginBottom: 8,
    lineHeight: 24,
  },
  tipSource: {
    fontSize: 14,
    color: '#92400E',
    fontStyle: 'italic',
  },
  section: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#111827',
  },
  emptyText: {
    fontSize: 16,
    color: '#6B7280',
    textAlign: 'center',
    padding: 20,
  },
  objectiveCard: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    backgroundColor: '#fff',
    borderRadius: 8,
    marginBottom: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  checkbox: {
    width: 24,
    height: 24,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#4F46E5',
    marginRight: 12,
    justifyContent: 'center',
    alignItems: 'center',
  },
  checkmark: {
    color: '#4F46E5',
    fontSize: 16,
    fontWeight: 'bold',
  },
  objectiveText: {
    flex: 1,
    fontSize: 16,
    color: '#111827',
  },
  completedText: {
    textDecorationLine: 'line-through',
    color: '#9CA3AF',
  },
  checkInButton: {
    margin: 20,
    padding: 16,
    backgroundColor: '#4F46E5',
    borderRadius: 8,
  },
  checkInButtonText: {
    color: '#fff',
    textAlign: 'center',
    fontSize: 16,
    fontWeight: 'bold',
  },
  modal: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    backgroundColor: '#fff',
    padding: 30,
    borderRadius: 12,
    width: '80%',
  },
  modalTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
  },
  moodButton: {
    padding: 15,
    backgroundColor: '#F3F4F6',
    borderRadius: 8,
    marginBottom: 10,
  },
  moodButtonText: {
    fontSize: 16,
    textAlign: 'center',
    color: '#111827',
  },
  cancelText: {
    marginTop: 10,
    textAlign: 'center',
    color: '#6B7280',
    fontSize: 16,
  },
});
