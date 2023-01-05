DROP TABLE IF EXISTS questionsBank;

CREATE TABLE questionsBank (
    tweetId INTEGER PRIMARY KEY,
    tweet TEXT NOT NULL,
    hateExpWO TEXT NOT NULL,
    nonhateExpWO TEXT NOT NULL,
    hateExpStep TEXT NOT NULL,
    nonhateExpStep TEXT NOT NULL,
    contxtExp TEXT NOT NULL
);


DROP TABLE IF EXISTS questionsStatus;

CREATE TABLE questionsStatus (
    tweetId INTEGER,
    strategyId INTEGER,
    annotationId INTEGER,
    annotated INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (tweetId, strategyId, annotationId)
);


DROP TABLE IF EXISTS inprogress;

CREATE TABLE inprogress (
    tweetId INTEGER,
    strategyId INTEGER,
    annotationId INTEGER,
    startTime INTEGER NOT NULL,
    PRIMARY KEY (tweetId, strategyId, annotationId)

);


DROP TABLE IF EXISTS submitted;

CREATE TABLE submitted (
    user_id TEXT,
    tweetId INTEGER,
    strategyId INTEGER,
    annotationId INTEGER,

    startTime TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    surveycode INTEGER NOT NULL,

    fluency INTEGER,
    informativeness INTEGER,
    persuasiveness INTEGER,
    soundness INTEGER,
    fluency2 INTEGER,
    informativeness2 INTEGER,
    persuasiveness2 INTEGER,
    soundness2 INTEGER,
    hatefulness INTEGER NOT NULL,
    PRIMARY KEY (tweetId, strategyId, annotationId)
);

