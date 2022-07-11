

-- Replace values for hobby_type & update family member id
-- Execute when ready
-- Easier to populate than doing a procedure with calls 
INSERT INTO family_hobbies(hobby_type, created_ts, family_id)
VALUES('Going to music', CURRENT_TIMESTAMP, (SELECT id FROM family WHERE id = 14));

