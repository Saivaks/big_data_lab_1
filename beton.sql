if schema_id('test') is null
    exec('create schema test');

IF NOT EXISTS (SELECT * FROM sys.objects
WHERE object_id = OBJECT_ID(N'test.train') AND type in (N'U'))
BEGIN
create table test.train
(
    ArticleId int,
    Text      text,
    Category  text
);
END
IF NOT EXISTS (SELECT * FROM sys.objects
WHERE object_id = OBJECT_ID(N'test.test') AND type in (N'U'))
BEGIN
create table test.test
(
    ArticleId int,
    Text text,
    Category text
);
END

IF NOT EXISTS (SELECT * FROM sys.objects
WHERE object_id = OBJECT_ID(N'test.train_split') AND type in (N'U'))
BEGIN
create table test.train_split
(
    ArticleId int,
    Text text,
    Category text
);
END

IF NOT EXISTS (SELECT * FROM sys.objects
WHERE object_id = OBJECT_ID(N'test.valid_split') AND type in (N'U'))
BEGIN
create table test.valid_split
(
    ArticleId int,
    Text text,
    Category text
);
END

IF NOT EXISTS (SELECT * FROM sys.objects
WHERE object_id = OBJECT_ID(N'test.pred_train') AND type in (N'U'))
BEGIN
create table test.pred_train
(
    Text text,
    Category text
);
END

IF NOT EXISTS (SELECT * FROM sys.objects
WHERE object_id = OBJECT_ID(N'test.pred_valid') AND type in (N'U'))
BEGIN
create table test.pred_valid
(
    Text text,
    Category text
);
END

IF NOT EXISTS (SELECT * FROM sys.objects
WHERE object_id = OBJECT_ID(N'test.pred_test') AND type in (N'U'))
BEGIN
create table test.pred_test
(
    Text text,
    Category text
);
END