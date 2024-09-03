use alcaparros;
SET foreign_key_checks = 0;
truncate table IRA_Networks_modes_themes;
truncate table IRA_Networks_modes;
truncate table IRA_Questions_possible_answers;
truncate table IRA_Questions;
truncate table questions_vs_networks_modes;
truncate table cycles_vs_networks_modes;
SET foreign_key_checks = 1;