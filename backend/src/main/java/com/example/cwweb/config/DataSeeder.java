package com.example.cwweb.config;

import com.example.cwweb.achievements.Achievement;
import com.example.cwweb.achievements.AchievementRepository;
import com.example.cwweb.achievements.RuleType;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class DataSeeder {

    @Bean
    CommandLineRunner initDatabase(AchievementRepository achievementRepository) {
        return args -> {
            if (achievementRepository.count() == 0) {
                achievementRepository.save(Achievement.builder()
                        .name("First Steps")
                        .description("Log your first progress")
                        .ruleType(RuleType.TOTAL_CHECKINS)
                        .ruleValue(1)
                        .build());

                achievementRepository.save(Achievement.builder()
                        .name("Week Warrior")
                        .description("Maintain a 7-day streak")
                        .ruleType(RuleType.STREAK_DAYS)
                        .ruleValue(7)
                        .build());

                achievementRepository.save(Achievement.builder()
                        .name("Dedicated")
                        .description("Log 10 check-ins")
                        .ruleType(RuleType.TOTAL_CHECKINS)
                        .ruleValue(10)
                        .build());

                achievementRepository.save(Achievement.builder()
                        .name("Goal Master")
                        .description("Complete a goal")
                        .ruleType(RuleType.GOAL_COMPLETED)
                        .ruleValue(1)
                        .build());
            }
        };
    }
}
