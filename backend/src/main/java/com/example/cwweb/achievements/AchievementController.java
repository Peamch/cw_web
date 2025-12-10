package com.example.cwweb.achievements;

import com.example.cwweb.common.ApiResponse;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/achievements")
public class AchievementController {

    private final AchievementService achievementService;

    public AchievementController(AchievementService achievementService) {
        this.achievementService = achievementService;
    }

    @GetMapping
    public ResponseEntity<ApiResponse<List<Achievement>>> getAllAchievements() {
        List<Achievement> achievements = achievementService.getAllAchievements();
        return ResponseEntity.ok(ApiResponse.<List<Achievement>>builder()
                .success(true)
                .data(achievements)
                .build());
    }

    @GetMapping("/me")
    public ResponseEntity<ApiResponse<List<UserAchievement>>> getMyAchievements(
            @AuthenticationPrincipal UserDetails userDetails) {
        String userId = userDetails.getUsername();
        List<UserAchievement> achievements = achievementService.getUserAchievements(userId);
        return ResponseEntity.ok(ApiResponse.<List<UserAchievement>>builder()
                .success(true)
                .data(achievements)
                .build());
    }
}
