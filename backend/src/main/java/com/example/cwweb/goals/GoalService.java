package com.example.cwweb.goals;

import com.example.cwweb.common.NotFoundException;
import com.example.cwweb.common.ForbiddenException;
import org.springframework.stereotype.Service;
import java.time.LocalDateTime;
import java.util.List;

@Service
public class GoalService {

    private final GoalRepository goalRepository;

    public GoalService(GoalRepository goalRepository) {
        this.goalRepository = goalRepository;
    }

    public Goal createGoal(String userId, CreateGoalRequest request) {
        Goal goal = Goal.builder()
                .userId(userId)
                .title(request.getTitle())
                .description(request.getDescription())
                .frequency(request.getFrequency())
                .startDate(request.getStartDate())
                .endDate(request.getEndDate())
                .isPublic(request.isPublic())
                .status(GoalStatus.ACTIVE)
                .createdAt(LocalDateTime.now())
                .updatedAt(LocalDateTime.now())
                .build();
        return goalRepository.save(goal);
    }

    public List<Goal> getUserGoals(String userId) {
        return goalRepository.findByUserId(userId);
    }

    public Goal getGoal(String goalId, String userId) {
        Goal goal = goalRepository.findById(goalId)
                .orElseThrow(() -> new NotFoundException("Goal not found"));
        if (!goal.getUserId().equals(userId) && !goal.isPublic()) {
            throw new ForbiddenException("Access denied");
        }
        return goal;
    }

    public Goal updateGoal(String goalId, String userId, UpdateGoalRequest request) {
        Goal goal = goalRepository.findById(goalId)
                .orElseThrow(() -> new NotFoundException("Goal not found"));
        if (!goal.getUserId().equals(userId)) {
            throw new ForbiddenException("Access denied");
        }

        if (request.getTitle() != null) goal.setTitle(request.getTitle());
        if (request.getDescription() != null) goal.setDescription(request.getDescription());
        if (request.getFrequency() != null) goal.setFrequency(request.getFrequency());
        if (request.getStartDate() != null) goal.setStartDate(request.getStartDate());
        if (request.getEndDate() != null) goal.setEndDate(request.getEndDate());
        if (request.getStatus() != null) goal.setStatus(request.getStatus());
        if (request.getIsPublic() != null) goal.setPublic(request.getIsPublic());
        
        goal.setUpdatedAt(LocalDateTime.now());
        return goalRepository.save(goal);
    }

    public void deleteGoal(String goalId, String userId) {
        Goal goal = goalRepository.findById(goalId)
                .orElseThrow(() -> new NotFoundException("Goal not found"));
        if (!goal.getUserId().equals(userId)) {
            throw new ForbiddenException("Access denied");
        }
        goalRepository.deleteById(goalId);
    }
}
