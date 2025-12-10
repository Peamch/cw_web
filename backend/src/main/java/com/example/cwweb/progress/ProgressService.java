package com.example.cwweb.progress;

import com.example.cwweb.achievements.AchievementService;
import com.example.cwweb.activity.ActivityService;
import com.example.cwweb.activity.ActivityType;
import com.example.cwweb.common.ForbiddenException;
import com.example.cwweb.common.NotFoundException;
import com.example.cwweb.goals.Goal;
import com.example.cwweb.goals.GoalRepository;
import org.springframework.stereotype.Service;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

@Service
public class ProgressService {

    private final ProgressLogRepository progressRepository;
    private final GoalRepository goalRepository;
    private final ActivityService activityService;
    private final AchievementService achievementService;

    public ProgressService(ProgressLogRepository progressRepository, 
                          GoalRepository goalRepository,
                          ActivityService activityService,
                          AchievementService achievementService) {
        this.progressRepository = progressRepository;
        this.goalRepository = goalRepository;
        this.activityService = activityService;
        this.achievementService = achievementService;
    }

    public ProgressLog logProgress(String userId, LogProgressRequest request) {
        Goal goal = goalRepository.findById(request.getGoalId())
                .orElseThrow(() -> new NotFoundException("Goal not found"));
        
        if (!goal.getUserId().equals(userId)) {
            throw new ForbiddenException("Access denied");
        }

        ProgressLog log = ProgressLog.builder()
                .goalId(request.getGoalId())
                .userId(userId)
                .date(request.getDate() != null ? request.getDate() : LocalDate.now())
                .value(request.getValue())
                .note(request.getNote())
                .createdAt(LocalDateTime.now())
                .build();
        
        log = progressRepository.save(log);
        
        activityService.createActivity(userId, goal.getId(), ActivityType.PROGRESS_LOGGED, 
                "logged progress for goal: " + goal.getTitle());
        
        achievementService.checkAndAwardAchievements(userId, goal.getId());
        
        return log;
    }

    public List<ProgressLog> getGoalProgress(String goalId, String userId) {
        Goal goal = goalRepository.findById(goalId)
                .orElseThrow(() -> new NotFoundException("Goal not found"));
        
        if (!goal.getUserId().equals(userId) && !goal.isPublic()) {
            throw new ForbiddenException("Access denied");
        }
        
        return progressRepository.findByGoalIdOrderByDateDesc(goalId);
    }
}
