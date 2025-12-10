package com.example.cwweb.activity;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import java.util.List;

public interface ActivityRepository extends MongoRepository<Activity, String> {
    Page<Activity> findByGroupIdOrderByCreatedAtDesc(String groupId, Pageable pageable);
    Page<Activity> findByUserIdOrderByCreatedAtDesc(String userId, Pageable pageable);
    List<Activity> findByUserIdOrderByCreatedAtDesc(String userId);
}
