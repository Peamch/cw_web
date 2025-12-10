package com.example.cwweb.activity;

import com.example.cwweb.common.ApiResponse;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/activities")
public class ActivityController {

    private final ActivityService activityService;

    public ActivityController(ActivityService activityService) {
        this.activityService = activityService;
    }

    @GetMapping("/group/{groupId}")
    public ResponseEntity<ApiResponse<Page<Activity>>> getGroupActivities(
            @PathVariable String groupId,
            Pageable pageable) {
        Page<Activity> activities = activityService.getGroupActivities(groupId, pageable);
        return ResponseEntity.ok(ApiResponse.<Page<Activity>>builder()
                .success(true)
                .data(activities)
                .build());
    }

    @GetMapping("/me")
    public ResponseEntity<ApiResponse<Page<Activity>>> getMyActivities(
            @AuthenticationPrincipal UserDetails userDetails,
            Pageable pageable) {
        String userId = userDetails.getUsername();
        Page<Activity> activities = activityService.getUserActivities(userId, pageable);
        return ResponseEntity.ok(ApiResponse.<Page<Activity>>builder()
                .success(true)
                .data(activities)
                .build());
    }
}
