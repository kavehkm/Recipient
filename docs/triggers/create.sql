-----------------------
-- GroupKala Trigger --
-----------------------
CREATE TRIGGER RecipientTrgGroupKala
ON GroupKala
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE CategoryMap
    SET update_required = 1
    FROM CategoryMap AS cm
    INNER JOIN inserted AS i ON i.ID = cm.id
END


----------------------
-- KalaList Trigger --
----------------------
CREATE TRIGGER RecipientTrgKalaList
ON KalaList
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE ProductMap
    SET update_required = 1
    FROM ProductMap AS pm
    INNER JOIN inserted AS i ON i.ID = pm.id
END


-----------------------
-- KalaPrice Trigger --
-----------------------
CREATE TRIGGER RecipientTrgKalaPrice
ON KalaPrice
AFTER UPDATE, INSERT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE ProductMap
    SET update_required = 1
    FROM ProductMap AS pm
    INNER JOIN inserted AS i ON i.KalaID = pm.id
END


---------------------
-- Faktor2 Trigger --
---------------------
CREATE TRIGGER RecipientTrgFaktor2
ON Faktor2
AFTER UPDATE, INSERT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE ProductMap
    SET update_required = 1
    FROM ProductMap AS pm
    INNER JOIN inserted AS i ON i.IDKala = pm.id
END


----------------------
-- Tamirat3 Trigger --
----------------------
CREATE TRIGGER RecipientTrgTamirat3
ON Tamirat3
AFTER UPDATE, INSERT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE ProductMap
    SET update_required = 1
    FROM ProductMap AS pm
    INNER JOIN inserted AS i ON i.IDKala = pm.id
END


------------------------
-- MojodiList Trigger --
------------------------
CREATE TRIGGER RecipientTrgMojodiList
ON MojodiList
AFTER UPDATE, INSERT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE ProductMap
    SET update_required = 1
    FROM ProductMap AS pm
    INNER JOIN inserted AS i ON i.IdKala = pm.id
END


--------------------
-- Resid2 Trigger --
--------------------
CREATE TRIGGER RecipientTrgResid2
ON Resid2
AFTER UPDATE, INSERT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE ProductMap
    SET update_required = 1
    FROM ProductMap AS pm
    INNER JOIN inserted AS i ON i.IDKala = pm.id
END


-----------------------
-- TolidKala Trigger --
-----------------------
CREATE TRIGGER RecipientTrgTolidKala
ON TolidKala
AFTER UPDATE, INSERT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE ProductMap
    SET update_required = 1
    FROM ProductMap AS pm
    INNER JOIN inserted AS i ON i.IDKala = pm.id
END


---------------------
-- Havale2 Trigger --
---------------------
CREATE TRIGGER RecipientTrgHavale2
ON Havale2
AFTER UPDATE, INSERT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE ProductMap
    SET update_required = 1
    FROM ProductMap AS pm
    INNER JOIN inserted AS i ON i.IDKala = pm.id
END


---------------------------
-- AnbarGardani2 Trigger --
---------------------------
CREATE TRIGGER RecipientTrgAnbarGardani2
ON AnbarGardani2
AFTER UPDATE, INSERT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE ProductMap
    SET update_required = 1
    FROM ProductMap AS pm
    INNER JOIN inserted AS i ON i.KalaID = pm.id
END


-------------------------
-- AnbarResid2 Trigger --
-------------------------
CREATE TRIGGER RecipientTrgAnbarResid2
ON AnbarResid2
AFTER UPDATE, INSERT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE ProductMap
    SET update_required = 1
    FROM ProductMap AS pm
    INNER JOIN inserted AS i ON i.IDKala = pm.id
END