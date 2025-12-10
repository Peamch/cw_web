package com.example.cwweb.goals;

import com.example.cwweb.common.ApiResponse;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/goals")
public class GoalController {

    private final GoalService goalService;

    public GoalController(GoalService goalService) {
        this.goalService = goalService;
    }

    @PostMapping
    public ResponseEntity<ApiResponse<Goal>> createGoal(
            @AuthenticationPrincipal UserDetails userDetails,
            @RequestBody CreateGoalRequest request) {
        String userId = userDetails.getUsername();
        Goal goal = goalService.createGoal(userId, request);
        return ResponseEntity.ok(ApiResponse.<Goal>builder()
                .success(true)
                .message("Goal created")
                .data(goal)
                .build());
    }

    @GetMapping
    public ResponseEntity<ApiResponse<List<Goal>>> getUserGoals(
            @AuthenticationPrincipal UserDetails userDetails) {
        String userId = userDetails.getUsername();
        List<Goal> goals = goalService.getUserGoals(userId);
        return ResponseEntity.ok(ApiResponse.<List<Goal>>builder()
                .success(true)
                .data(goals)
                .build());
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<Goal>> getGoal(
            @PathVariable String id,
            @AuthenticationPrincipal UserDetails userDetails) {
        String userId = userDetails.getUsername();
        Goal goal = goalService.getGoal(id, userId);
        return ResponseEntity.ok(ApiResponse.<Goal>builder()
                .success(true)
                .data(goal)
                .build());
    }

    @PutMapping("/{id}")
    public ResponseEntity<ApiResponse<Goal>> updateGoal(
            @PathVariable String id,
            @AuthenticationPrincipal UserDetails userDetails,
            @RequestBody UpdateGoalRequest request) {
        String userId = userDetails.getUsername();
        Goal goal = goalService.updateGoal(id, userId, request);
        return ResponseEntity.ok(ApiResponse.<Goal>builder()
                .success(true)
                .message("Goal updated")
                .data(goal)
                .build());
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<ApiResponse<Void>> deleteGoal(
            @PathVariable String id,
            @AuthenticationPrincipal UserDetails userDetails) {
        String userId = userDetails.getUsername();
        goalService.deleteGoal(id, userId);
        return ResponseEntity.ok(ApiResponse.<Void>builder()
                .success(true)
                .message("Goal deleted")
                .build());
    }
}
