package com.example.cwweb.goals;

import lombok.Data;
import java.time.LocalDate;

@Data
public class CreateGoalRequest {
    private String title;
    private String description;
    private Frequency frequency;
    private LocalDate startDate;
    private LocalDate endDate;
    private boolean isPublic;
}
