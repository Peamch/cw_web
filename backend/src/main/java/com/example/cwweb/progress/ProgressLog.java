package com.example.cwweb.progress;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Document(collection = "progress_logs")
public class ProgressLog {
    @Id
    private String id;
    private String goalId;
    private String userId;
    private LocalDate date;
    private Double value;
    private String note;
    private LocalDateTime createdAt;
}
