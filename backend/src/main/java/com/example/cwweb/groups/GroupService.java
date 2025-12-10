package com.example.cwweb.groups;

import com.example.cwweb.activity.ActivityService;
import com.example.cwweb.activity.ActivityType;
import com.example.cwweb.activity.ActivityVisibility;
import com.example.cwweb.common.ForbiddenException;
import com.example.cwweb.common.NotFoundException;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
public class GroupService {
    private final GroupRepository groupRepository;
    private final GroupMembershipRepository membershipRepository;
    private final ActivityService activityService;

    public Page<Group> getAllGroups(Visibility visibility, Pageable pageable) {
        if (visibility != null) {
            return groupRepository.findByVisibility(visibility, pageable);
        }
        return groupRepository.findAll(pageable);
    }

    public Group getGroupById(String id, String currentUserId) {
        Group group = groupRepository.findById(id)
                .orElseThrow(() -> new NotFoundException("Group not found"));

        if (group.getVisibility() == Visibility.PRIVATE && currentUserId != null) {
            if (!group.getOwnerId().equals(currentUserId) && !isMember(id, currentUserId)) {
                throw new ForbiddenException("Access denied to private group");
            }
        }

        return group;
    }

    @Transactional
    public Group createGroup(CreateGroupRequest request, String ownerId) {
        Group group = Group.builder()
                .name(request.getName())
                .description(request.getDescription())
                .visibility(request.getVisibility())
                .ownerId(ownerId)
                .createdAt(LocalDateTime.now())
                .updatedAt(LocalDateTime.now())
                .build();

        group = groupRepository.save(group);

        GroupMembership membership = GroupMembership.builder()
                .groupId(group.getId())
                .userId(ownerId)
                .role(MembershipRole.OWNER)
                .status(MembershipStatus.APPROVED)
                .createdAt(LocalDateTime.now())
                .build();
        membershipRepository.save(membership);

        Map<String, String> refIds = new HashMap<>();
        refIds.put("groupId", group.getId());
        activityService.createActivity(
                group.getId(),
                ownerId,
                ActivityType.GROUP_CREATED,
                refIds,
                group.getVisibility() == Visibility.PUBLIC ? ActivityVisibility.PUBLIC : ActivityVisibility.GROUP
        );

        return group;
    }

    @Transactional
    public Group updateGroup(String id, UpdateGroupRequest request, String userId) {
        Group group = groupRepository.findById(id)
                .orElseThrow(() -> new NotFoundException("Group not found"));

        if (!group.getOwnerId().equals(userId)) {
            throw new ForbiddenException("Only owner can update group");
        }

        if (request.getName() != null) {
            group.setName(request.getName());
        }
        if (request.getDescription() != null) {
            group.setDescription(request.getDescription());
        }
        if (request.getVisibility() != null) {
            group.setVisibility(request.getVisibility());
        }

        group.setUpdatedAt(LocalDateTime.now());
        return groupRepository.save(group);
    }

    @Transactional
    public void deleteGroup(String id, String userId, boolean isAdmin) {
        Group group = groupRepository.findById(id)
                .orElseThrow(() -> new NotFoundException("Group not found"));

        if (!isAdmin && !group.getOwnerId().equals(userId)) {
            throw new ForbiddenException("Only owner or admin can delete group");
        }

        List<GroupMembership> memberships = membershipRepository.findByGroupId(id);
        membershipRepository.deleteAll(memberships);

        groupRepository.delete(group);
    }

    public List<GroupMembership> getGroupMembers(String groupId, String userId) {
        Group group = getGroupById(groupId, userId);
        return membershipRepository.findByGroupIdAndStatus(groupId, MembershipStatus.APPROVED);
    }

    public List<GroupMembership> getPendingRequests(String groupId, String userId) {
        Group group = groupRepository.findById(groupId)
                .orElseThrow(() -> new NotFoundException("Group not found"));

        if (!group.getOwnerId().equals(userId)) {
            throw new ForbiddenException("Only owner can view pending requests");
        }

        return membershipRepository.findByGroupIdAndStatus(groupId, MembershipStatus.PENDING);
    }

    public long getMemberCount(String groupId) {
        return membershipRepository.countByGroupIdAndStatus(groupId, MembershipStatus.APPROVED);
    }

    @Transactional
    public GroupMembership joinGroup(String groupId, String userId) {
        Group group = groupRepository.findById(groupId)
                .orElseThrow(() -> new NotFoundException("Group not found"));

        if (membershipRepository.findByGroupIdAndUserId(groupId, userId).isPresent()) {
            throw new ForbiddenException("Already a member or request pending");
        }

        MembershipStatus status = group.getVisibility() == Visibility.PUBLIC 
                ? MembershipStatus.APPROVED 
                : MembershipStatus.PENDING;

        GroupMembership membership = GroupMembership.builder()
                .groupId(groupId)
                .userId(userId)
                .role(MembershipRole.MEMBER)
                .status(status)
                .createdAt(LocalDateTime.now())
                .build();

        membership = membershipRepository.save(membership);

        if (status == MembershipStatus.APPROVED) {
            Map<String, String> refIds = new HashMap<>();
            refIds.put("groupId", groupId);
            activityService.createActivity(
                    groupId,
                    userId,
                    ActivityType.MEMBER_JOINED,
                    refIds,
                    group.getVisibility() == Visibility.PUBLIC ? ActivityVisibility.PUBLIC : ActivityVisibility.GROUP
            );
        }

        return membership;
    }

    @Transactional
    public void leaveGroup(String groupId, String userId) {
        Group group = groupRepository.findById(groupId)
                .orElseThrow(() -> new NotFoundException("Group not found"));

        if (group.getOwnerId().equals(userId)) {
            throw new ForbiddenException("Owner cannot leave group");
        }

        GroupMembership membership = membershipRepository.findByGroupIdAndUserId(groupId, userId)
                .orElseThrow(() -> new NotFoundException("Not a member"));

        membershipRepository.delete(membership);

        Map<String, String> refIds = new HashMap<>();
        refIds.put("groupId", groupId);
        activityService.createActivity(
                groupId,
                userId,
                ActivityType.MEMBER_LEFT,
                refIds,
                group.getVisibility() == Visibility.PUBLIC ? ActivityVisibility.PUBLIC : ActivityVisibility.GROUP
        );
    }

    private boolean isMember(String groupId, String userId) {
        return membershipRepository.findByGroupIdAndUserId(groupId, userId)
                .map(m -> m.getStatus() == MembershipStatus.APPROVED)
                .orElse(false);
    }
}
