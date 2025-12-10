package com.example.cwweb.groups;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Document(collection = "group_memberships")
public class GroupMembership {
    @Id
    private String id;
    private String groupId;
    private String userId;
    private MembershipRole role;
    private MembershipStatus status;
    private LocalDateTime createdAt;
}
