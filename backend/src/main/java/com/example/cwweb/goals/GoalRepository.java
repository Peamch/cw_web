package com.example.cwweb.goals;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

@Repository
public interface GoalRepository extends MongoRepository<Goal, String> {
    Page<Goal> findByUserId(String userId, Pageable pageable);
    List<Goal> findByUserId(String userId);
    Page<Goal> findByUserIdAndStatus(String userId, GoalStatus status, Pageable pageable);
    List<Goal> findByIsPublicTrue();
    Optional<Goal> findByIdAndUserId(String goalId, String userId);
}
