package com.example.cwweb.goals;

import lombok.Data;
import java.time.LocalDate;

@Data
public class UpdateGoalRequest {
    private String title;
    private String description;
    private Frequency frequency;
    private LocalDate startDate;
    private LocalDate endDate;
    private GoalStatus status;
    private Boolean isPublic;
}
