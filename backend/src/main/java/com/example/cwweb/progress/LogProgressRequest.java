package com.example.cwweb.progress;

import lombok.Data;
import java.time.LocalDate;

@Data
public class LogProgressRequest {
    private String goalId;
    private LocalDate date;
    private Double value;
    private String note;
}
