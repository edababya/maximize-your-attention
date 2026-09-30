PRAGMA foreign_keys = ON;

CREATE TABLE project (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    sector TEXT,
    stage TEXT,
    status TEXT NOT NULL CHECK (
        status IN ('sourcing', 'tracking', 'diligence', 'passed', 'invested')
    ),
    thesis_tags TEXT,
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE person (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT,
    org TEXT,
    x_handle TEXT,
    notes TEXT,
    last_contact TEXT
);

CREATE TABLE event (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    kind TEXT NOT NULL CHECK (
        kind IN ('meeting', 'conference', 'deadline', 'task')
    ),
    starts_at TEXT,
    location TEXT,
    notes TEXT,
    status TEXT
);

CREATE TABLE signal (
    id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    kind TEXT NOT NULL CHECK (
        kind IN ('news', 'paper', 'tweet', 'funding', 'note')
    ),
    title TEXT NOT NULL,
    url TEXT UNIQUE,
    published_at TEXT,
    summary TEXT,
    importance INTEGER NOT NULL DEFAULT 0 CHECK (
        importance BETWEEN 0 AND 5
    ),
    embedding BLOB
);

CREATE TABLE thesis (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    statement TEXT NOT NULL,
    confidence REAL NOT NULL CHECK (confidence BETWEEN 0.0 AND 1.0),
    status TEXT NOT NULL CHECK (status IN ('active', 'challenged', 'dead')),
    created_at TEXT NOT NULL
);

CREATE TABLE prediction (
    id TEXT PRIMARY KEY,
    statement TEXT NOT NULL,
    confidence REAL NOT NULL CHECK (confidence BETWEEN 0.0 AND 1.0),
    thesis_id TEXT,
    created_at TEXT NOT NULL,
    resolve_by TEXT,
    outcome TEXT NOT NULL DEFAULT 'pending' CHECK (
        outcome IN ('pending', 'true', 'false')
    ),
    FOREIGN KEY (thesis_id) REFERENCES thesis(id)
);

CREATE TABLE edge (
    id INTEGER PRIMARY KEY,
    from_type TEXT NOT NULL CHECK (
        from_type IN ('project', 'person', 'event', 'signal', 'thesis')
    ),
    from_id TEXT NOT NULL,
    to_type TEXT NOT NULL CHECK (
        to_type IN ('project', 'person', 'event', 'signal', 'thesis')
    ),
    to_id TEXT NOT NULL,
    relation TEXT NOT NULL,
    weight REAL NOT NULL DEFAULT 1.0
);

CREATE VIRTUAL TABLE signal_fts USING fts5(
    title,
    summary,
    content='signal',
    content_rowid='rowid'
);

CREATE TRIGGER signal_ai AFTER INSERT ON signal BEGIN
    INSERT INTO signal_fts(rowid, title, summary)
    VALUES (new.rowid, new.title, new.summary);
END;

CREATE TRIGGER signal_ad AFTER DELETE ON signal BEGIN
    INSERT INTO signal_fts(signal_fts, rowid, title, summary)
    VALUES ('delete', old.rowid, old.title, old.summary);
END;

CREATE TRIGGER signal_au AFTER UPDATE ON signal BEGIN
    INSERT INTO signal_fts(signal_fts, rowid, title, summary)
    VALUES ('delete', old.rowid, old.title, old.summary);
    INSERT INTO signal_fts(rowid, title, summary)
    VALUES (new.rowid, new.title, new.summary);
END;

CREATE INDEX idx_project_status ON project(status);
CREATE INDEX idx_project_sector ON project(sector);
CREATE INDEX idx_person_org ON person(org);
CREATE INDEX idx_event_starts_at ON event(starts_at);
CREATE INDEX idx_event_status ON event(status);
CREATE INDEX idx_signal_published_at ON signal(published_at);
CREATE INDEX idx_signal_importance ON signal(importance);
CREATE INDEX idx_thesis_status ON thesis(status);
CREATE INDEX idx_prediction_thesis_id ON prediction(thesis_id);
CREATE INDEX idx_prediction_resolution ON prediction(outcome, resolve_by);
CREATE INDEX idx_edge_from ON edge(from_type, from_id);
CREATE INDEX idx_edge_to ON edge(to_type, to_id);
