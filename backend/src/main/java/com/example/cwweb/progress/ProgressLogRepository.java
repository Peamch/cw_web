package com.example.cwweb.progress;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;
import java.time.LocalDate;
import java.util.List;

@Repository
public interface ProgressLogRepository extends MongoRepository<ProgressLog, String> {
    Page<ProgressLog> findByGoalId(String goalId, Pageable pageable);
    List<ProgressLog> findByGoalIdOrderByDateDesc(String goalId);
    List<ProgressLog> findByUserIdAndDateBetween(String userId, LocalDate startDate, LocalDate endDate);
    long countByGoalIdAndDateBetween(String goalId, LocalDate startDate, LocalDate endDate);
}
