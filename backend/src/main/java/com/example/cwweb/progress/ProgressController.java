package com.example.cwweb.progress;

import com.example.cwweb.common.ApiResponse;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/progress")
public class ProgressController {

    private final ProgressService progressService;

    public ProgressController(ProgressService progressService) {
        this.progressService = progressService;
    }

    @PostMapping
    public ResponseEntity<ApiResponse<ProgressLog>> logProgress(
            @AuthenticationPrincipal UserDetails userDetails,
            @RequestBody LogProgressRequest request) {
        String userId = userDetails.getUsername();
        ProgressLog log = progressService.logProgress(userId, request);
        return ResponseEntity.ok(ApiResponse.<ProgressLog>builder()
                .success(true)
                .message("Progress logged")
                .data(log)
                .build());
    }

    @GetMapping("/goal/{goalId}")
    public ResponseEntity<ApiResponse<List<ProgressLog>>> getGoalProgress(
            @PathVariable String goalId,
            @AuthenticationPrincipal UserDetails userDetails) {
        String userId = userDetails.getUsername();
        List<ProgressLog> logs = progressService.getGoalProgress(goalId, userId);
        return ResponseEntity.ok(ApiResponse.<List<ProgressLog>>builder()
                .success(true)
                .data(logs)
                .build());
    }
}
