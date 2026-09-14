CREATE TABLE `review_schedule` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`source_date` text NOT NULL,
	`review_date` text NOT NULL,
	`interval` text NOT NULL,
	`category` text NOT NULL,
	`completed` integer DEFAULT false NOT NULL,
	FOREIGN KEY (`source_date`) REFERENCES `study_days`(`date`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE TABLE `skill_snapshots` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`date` text NOT NULL,
	`skill` text NOT NULL,
	`stability_low` integer NOT NULL,
	`stability_high` integer NOT NULL,
	`grade` text NOT NULL,
	FOREIGN KEY (`date`) REFERENCES `study_days`(`date`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE TABLE `study_days` (
	`date` text PRIMARY KEY NOT NULL,
	`study_minutes` integer NOT NULL,
	`study_time_is_minimum` integer DEFAULT false NOT NULL,
	`test_correct` integer NOT NULL,
	`test_total` integer NOT NULL,
	`test_minutes` integer NOT NULL,
	`allowed_minutes` integer NOT NULL,
	`wrong_count` integer NOT NULL,
	`n3_current_low` integer NOT NULL,
	`n3_current_high` integer NOT NULL,
	`n3_projected` integer NOT NULL,
	`n2_current_low` integer NOT NULL,
	`n2_current_high` integer NOT NULL,
	`n2_projected` integer NOT NULL,
	`source_label` text NOT NULL
);
--> statement-breakpoint
CREATE TABLE `type_metrics` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`date` text NOT NULL,
	`category` text NOT NULL,
	`correct` integer NOT NULL,
	`total` integer NOT NULL,
	`average_seconds` real NOT NULL,
	`status` text NOT NULL,
	`includes_audio` integer DEFAULT false NOT NULL,
	FOREIGN KEY (`date`) REFERENCES `study_days`(`date`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
INSERT INTO `study_days` (`date`,`study_minutes`,`study_time_is_minimum`,`test_correct`,`test_total`,`test_minutes`,`allowed_minutes`,`wrong_count`,`n3_current_low`,`n3_current_high`,`n3_projected`,`n2_current_low`,`n2_current_high`,`n2_projected`,`source_label`) VALUES ('2026-08-26',247,1,4,10,7,18,6,23,39,82,6,16,48,'공식 형식 기반 자체 제작 N3 기반 + N2 입문');
--> statement-breakpoint
INSERT INTO `skill_snapshots` (`date`,`skill`,`stability_low`,`stability_high`,`grade`) VALUES ('2026-08-26','한자·어휘',35,45,'D'),('2026-08-26','문법·활용',45,55,'C-'),('2026-08-26','독해',45,60,'C-'),('2026-08-26','청해',25,40,'D-');
--> statement-breakpoint
INSERT INTO `type_metrics` (`date`,`category`,`correct`,`total`,`average_seconds`,`status`,`includes_audio`) VALUES ('2026-08-26','한자 읽기',1,1,16,'안정',0),('2026-08-26','유의표현',0,1,33,'복습',0),('2026-08-26','형용사 활용',0,1,63,'복습',0),('2026-08-26','동사 활용',1,1,12,'강점',0),('2026-08-26','문법형식 판단',1,2,28,'유지',0),('2026-08-26','단문 내용이해',1,1,54,'강점',0),('2026-08-26','단문 주장 이해',0,1,102,'복습',0),('2026-08-26','포인트이해',0,1,38,'복습',1),('2026-08-26','과제이해',0,1,48,'복습',1);
--> statement-breakpoint
INSERT INTO `review_schedule` (`source_date`,`review_date`,`interval`,`category`,`completed`) VALUES ('2026-08-26','2026-08-27','D+1','유의표현',0),('2026-08-26','2026-08-27','D+1','형용사 활용',0),('2026-08-26','2026-08-27','D+1','문법형식 판단',0),('2026-08-26','2026-08-27','D+1','단문 주장 이해',0),('2026-08-26','2026-08-27','D+1','포인트이해',0),('2026-08-26','2026-08-27','D+1','과제이해',0),('2026-08-26','2026-08-29','D+3','유의표현',0),('2026-08-26','2026-08-29','D+3','형용사 활용',0),('2026-08-26','2026-08-29','D+3','문법형식 판단',0),('2026-08-26','2026-08-29','D+3','단문 주장 이해',0),('2026-08-26','2026-08-29','D+3','포인트이해',0),('2026-08-26','2026-08-29','D+3','과제이해',0),('2026-08-26','2026-09-02','D+7','유의표현',0),('2026-08-26','2026-09-02','D+7','형용사 활용',0),('2026-08-26','2026-09-02','D+7','문법형식 판단',0),('2026-08-26','2026-09-02','D+7','단문 주장 이해',0),('2026-08-26','2026-09-02','D+7','포인트이해',0),('2026-08-26','2026-09-02','D+7','과제이해',0);
