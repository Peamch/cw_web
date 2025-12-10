package com.example.cwweb.achievements;

import com.example.cwweb.progress.ProgressLogRepository;
import org.springframework.stereotype.Service;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

@Service
public class AchievementService {

    private final AchievementRepository achievementRepository;
    private final UserAchievementRepository userAchievementRepository;
    private final ProgressLogRepository progressLogRepository;

    public AchievementService(AchievementRepository achievementRepository,
                             UserAchievementRepository userAchievementRepository,
                             ProgressLogRepository progressLogRepository) {
        this.achievementRepository = achievementRepository;
        this.userAchievementRepository = userAchievementRepository;
        this.progressLogRepository = progressLogRepository;
    }

    public List<Achievement> getAllAchievements() {
        return achievementRepository.findAll();
    }

    public List<UserAchievement> getUserAchievements(String userId) {
        return userAchievementRepository.findByUserId(userId);
    }

    public void checkAndAwardAchievements(String userId, String goalId) {
        List<Achievement> achievements = achievementRepository.findAll();
        
        for (Achievement achievement : achievements) {
            if (hasUserAchievement(userId, achievement.getId())) {
                continue;
            }

            if (isAchievementEarned(userId, goalId, achievement)) {
                awardAchievement(userId, achievement, goalId);
            }
        }
    }

    private boolean hasUserAchievement(String userId, String achievementId) {
        return userAchievementRepository.findByUserIdAndAchievementId(userId, achievementId).isPresent();
    }

    private boolean isAchievementEarned(String userId, String goalId, Achievement achievement) {
        LocalDate now = LocalDate.now();
        
        switch (achievement.getRuleType()) {
            case STREAK_DAYS:
                return checkStreak(userId, goalId, achievement.getRuleValue());
            case TOTAL_CHECKINS:
                long count = progressLogRepository.countByGoalIdAndDateBetween(
                        goalId, now.minusYears(10), now);
                return count >= achievement.getRuleValue();
            case GOAL_COMPLETED:
                return true;
            default:
                return false;
        }
    }

    private boolean checkStreak(String userId, String goalId, int requiredDays) {
        LocalDate now = LocalDate.now();
        for (int i = 0; i < requiredDays; i++) {
            LocalDate checkDate = now.minusDays(i);
            long count = progressLogRepository.countByGoalIdAndDateBetween(
                    goalId, checkDate, checkDate.plusDays(1));
            if (count == 0) {
                return false;
            }
        }
        return true;
    }

    private void awardAchievement(String userId, Achievement achievement, String goalId) {
        UserAchievement userAchievement = UserAchievement.builder()
                .userId(userId)
                .achievementId(achievement.getId())
                .goalId(goalId)
                .earnedAt(LocalDateTime.now())
                .build();
        userAchievementRepository.save(userAchievement);
    }
}
