CREATE TABLE `daily_reports` (
	`date` text PRIMARY KEY NOT NULL,
	`payload_json` text NOT NULL,
	`updated_at` text NOT NULL
);
