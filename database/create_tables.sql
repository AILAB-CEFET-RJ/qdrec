CREATE DATABASE qdrec;

\c qdrec;

CREATE TABLE IF NOT EXISTS excerpt_metadata (
    excerpt_id TEXT,
    uf TEXT,
    cidade TEXT,
    tema TEXT,
    data TIMESTAMP,
    PRIMARY KEY(excerpt_id)
);

CREATE EXTENSION IF NOT EXISTS cube;

CREATE EXTENSION IF NOT EXISTS earthdistance;

CREATE TABLE IF NOT EXISTS vectors (
    excerpt_id TEXT NOT NULL,
    vectorized_excerpt TSVECTOR,
    CONSTRAINT fk_vectors
        FOREIGN KEY (excerpt_id)
            REFERENCES excerpt_metadata (excerpt_id)
);

CREATE TABLE IF NOT EXISTS named_entity (
    excerpt_id TEXT NOT NULL,
    content TEXT,
    entity_type VARCHAR,
    start_offset INT,
    end_offset INT,
    CONSTRAINT fk_named_entity
        FOREIGN KEY (excerpt_id)
            REFERENCES excerpt_metadata (excerpt_id)
);

--SELECT excerpt_id, texto_tsvector, earth_distance(ll_to_earth(-23.5505, -46.6333), ll_to_earth(-23.5505, -46.6333)) AS distance FROM excerpts_vectors ORDER BY distance LIMIT 5;