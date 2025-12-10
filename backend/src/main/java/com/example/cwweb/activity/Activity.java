package com.example.cwweb.activity;

import lombok.Builder;
import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.LocalDateTime;
import java.util.Map;

@Data
@Builder
@Document(collection = "activities")
public class Activity {
    @Id
    private String id;
    private String groupId;
    private String userId;
    private ActivityType type;
    private Map<String, String> refIds;
    private ActivityVisibility visibility;
    private LocalDateTime createdAt;
}

