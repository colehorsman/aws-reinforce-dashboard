-- Create the summaries table in Supabase
CREATE TABLE IF NOT EXISTS summaries (
    id SERIAL PRIMARY KEY,
    year INTEGER,
    domain VARCHAR(100),
    title TEXT,
    session_code VARCHAR(50),
    author TEXT,
    duration VARCHAR(50),
    word_count INTEGER,
    publish_date DATE,
    video_id VARCHAR(50),
    video_url TEXT,
    summary TEXT,
    key_points TEXT,
    technical_details TEXT,
    full_transcript TEXT,
    file_path TEXT,
    speaker_name VARCHAR(255),
    speaker_company VARCHAR(255),
    speaker_linkedin_url VARCHAR(500)
);

-- Create indexes for better performance
CREATE INDEX idx_summaries_year ON summaries(year);
CREATE INDEX idx_summaries_domain ON summaries(domain);
CREATE INDEX idx_summaries_session_code ON summaries(session_code);
CREATE INDEX idx_summaries_speaker_name ON summaries(speaker_name);