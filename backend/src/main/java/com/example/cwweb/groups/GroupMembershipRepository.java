package com.example.cwweb.groups;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

@Repository
public interface GroupMembershipRepository extends MongoRepository<GroupMembership, String> {
    Optional<GroupMembership> findByGroupIdAndUserId(String groupId, String userId);
    List<GroupMembership> findByGroupIdAndStatus(String groupId, MembershipStatus status);
    List<GroupMembership> findByGroupId(String groupId);
    List<GroupMembership> findByUserId(String userId);
    long countByGroupIdAndStatus(String groupId, MembershipStatus status);
}
