package com.example.cwweb.groups;

import com.example.cwweb.common.ApiResponse;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/groups")
public class GroupController {

    private final GroupService groupService;

    public GroupController(GroupService groupService) {
        this.groupService = groupService;
    }

    @GetMapping
    public ResponseEntity<ApiResponse<Page<Group>>> getAllGroups(
            @RequestParam(required = false) Visibility visibility,
            Pageable pageable) {
        Page<Group> groups = groupService.getAllGroups(visibility, pageable);
        return ResponseEntity.ok(ApiResponse.<Page<Group>>builder()
                .success(true)
                .data(groups)
                .build());
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<Group>> getGroup(
            @PathVariable String id,
            @AuthenticationPrincipal UserDetails userDetails) {
        String userId = userDetails != null ? userDetails.getUsername() : null;
        Group group = groupService.getGroupById(id, userId);
        return ResponseEntity.ok(ApiResponse.<Group>builder()
                .success(true)
                .data(group)
                .build());
    }

    @PostMapping
    public ResponseEntity<ApiResponse<Group>> createGroup(
            @AuthenticationPrincipal UserDetails userDetails,
            @RequestBody CreateGroupRequest request) {
        String userId = userDetails.getUsername();
        Group group = groupService.createGroup(request, userId);
        return ResponseEntity.ok(ApiResponse.<Group>builder()
                .success(true)
                .message("Group created")
                .data(group)
                .build());
    }

    @PutMapping("/{id}")
    public ResponseEntity<ApiResponse<Group>> updateGroup(
            @PathVariable String id,
            @AuthenticationPrincipal UserDetails userDetails,
            @RequestBody UpdateGroupRequest request) {
        String userId = userDetails.getUsername();
        Group group = groupService.updateGroup(id, request, userId);
        return ResponseEntity.ok(ApiResponse.<Group>builder()
                .success(true)
                .message("Group updated")
                .data(group)
                .build());
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<ApiResponse<Void>> deleteGroup(
            @PathVariable String id,
            @AuthenticationPrincipal UserDetails userDetails) {
        String userId = userDetails.getUsername();
        groupService.deleteGroup(id, userId, false);
        return ResponseEntity.ok(ApiResponse.<Void>builder()
                .success(true)
                .message("Group deleted")
                .build());
    }

    @PostMapping("/{id}/join")
    public ResponseEntity<ApiResponse<GroupMembership>> joinGroup(
            @PathVariable String id,
            @AuthenticationPrincipal UserDetails userDetails) {
        String userId = userDetails.getUsername();
        GroupMembership membership = groupService.joinGroup(id, userId);
        return ResponseEntity.ok(ApiResponse.<GroupMembership>builder()
                .success(true)
                .message("Join request sent")
                .data(membership)
                .build());
    }

    @PostMapping("/{id}/leave")
    public ResponseEntity<ApiResponse<Void>> leaveGroup(
            @PathVariable String id,
            @AuthenticationPrincipal UserDetails userDetails) {
        String userId = userDetails.getUsername();
        groupService.leaveGroup(id, userId);
        return ResponseEntity.ok(ApiResponse.<Void>builder()
                .success(true)
                .message("Left group")
                .build());
    }

    @GetMapping("/{id}/members")
    public ResponseEntity<ApiResponse<List<GroupMembership>>> getMembers(
            @PathVariable String id,
            @AuthenticationPrincipal UserDetails userDetails) {
        String userId = userDetails.getUsername();
        List<GroupMembership> members = groupService.getGroupMembers(id, userId);
        return ResponseEntity.ok(ApiResponse.<List<GroupMembership>>builder()
                .success(true)
                .data(members)
                .build());
    }
}
