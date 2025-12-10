package com.example.cwweb.groups;

import lombok.Data;

@Data
public class UpdateGroupRequest {
    private String name;
    private String description;
    private Visibility visibility;
}
