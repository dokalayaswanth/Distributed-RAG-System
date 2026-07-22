create extension if not exists "uuid-ossp";

create table if not exists documents (
    id uuid primary key default uuid_generate_v4(),
    file_name text not null,
    file_type text not null,
    file_size integer not null,
    storage_path text not null,
    status text not null default 'uploaded'
        check (status in ('uploaded', 'processing', 'indexed', 'failed')),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists ingestion_jobs (
    id uuid primary key default uuid_generate_v4(),
    document_id uuid not null references documents(id) on delete cascade,
    status text not null default 'pending'
        check (status in ('pending', 'processing', 'completed', 'failed')),
    error_message text,
    created_at timestamptz not null default now(),
    started_at timestamptz,
    completed_at timestamptz
);

create table if not exists chunks (
    id uuid primary key default uuid_generate_v4(),
    document_id uuid not null references documents(id) on delete cascade,
    chunk_index integer not null,
    content text not null,
    page_number integer,
    vector_index_position integer not null,
    created_at timestamptz not null default now()
);

create table if not exists index_versions (
    id uuid primary key default uuid_generate_v4(),
    version_number integer not null,
    index_path text not null,
    metadata_path text not null,
    status text not null default 'building'
        check (status in ('building', 'active', 'failed')),
    created_at timestamptz not null default now()
);

create table if not exists query_logs (
    id uuid primary key default uuid_generate_v4(),
    query text not null,
    answer text not null,
    top_k integer not null,
    mode text not null
        check (mode in ('retrieval', 'rag')),
    created_at timestamptz not null default now()
);