package com.example.cwweb.activity;

import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.Map;

@Service
@RequiredArgsConstructor
public class ActivityService {
    private final ActivityRepository activityRepository;

    @Transactional
    public void createActivity(String groupId, String userId, ActivityType type,
                               Map<String, String> refIds, ActivityVisibility visibility) {
        Activity activity = Activity.builder()
                .groupId(groupId)
                .userId(userId)
                .type(type)
                .refIds(refIds)
                .visibility(visibility)
                .createdAt(LocalDateTime.now())
                .build();

        activityRepository.save(activity);
    }

    @Transactional
    public void createActivity(String userId, String goalId, ActivityType type, String description) {
        Activity activity = Activity.builder()
                .userId(userId)
                .type(type)
                .refIds(Map.of("goalId", goalId, "description", description))
                .visibility(ActivityVisibility.PRIVATE)
                .createdAt(LocalDateTime.now())
                .build();

        activityRepository.save(activity);
    }

    public Page<Activity> getGroupActivities(String groupId, Pageable pageable) {
        return activityRepository.findByGroupIdOrderByCreatedAtDesc(groupId, pageable);
    }

    public Page<Activity> getUserActivities(String userId, Pageable pageable) {
        return activityRepository.findByUserIdOrderByCreatedAtDesc(userId, pageable);
    }
}
