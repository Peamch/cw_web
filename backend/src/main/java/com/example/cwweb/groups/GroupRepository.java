package com.example.cwweb.groups;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface GroupRepository extends MongoRepository<Group, String> {
    Page<Group> findByVisibility(Visibility visibility, Pageable pageable);
}

