-- DROP TABLE IF EXISTS articles;

CREATE TABLE articles (
  article_id VARCHAR(255) PRIMARY KEY,
  article_title VARCHAR(255),
  article_content TEXT,
  publisher_name VARCHAR(255),
  author_name VARCHAR(255),
  published_time VARCHAR(255)
);

SELECT article_content FROM articles WHERE article_url LIKE 'https://www.greenmedinfo.com/blog/guts-bugs-and-babies';

SELECT article_url FROM articles WHERE article_content LIKE '%Maybe the corona epidemic %';

-- DROP TABLE IF EXISTS articleURLs;

DELETE FROM articles
WHERE publisher_name = $$The Thinking Mom's Revolution$$;

-- DELETE FROM articleurls
-- WHERE article_url LIKE '%2013%';


CREATE TABLE articleURLs (
    article_url VARCHAR(255) PRIMARY KEY,
    website_name VARCHAR(255),
    website_url varchar(255)
);

CREATE TABLE paragraphs (
    publisher_name VARCHAR(255),
    url VARCHAR(255),
    article_title VARCHAR(255),
    paragraph_id VARCHAR(255),
    paragraph_content TEXT,
    author_name VARCHAR(255),
    published_time VARCHAR(255)
);


-- DROP TABLE IF EXISTS authors;

CREATE TABLE authors (
    author_id VARCHAR(255) PRIMARY KEY,
    author_name VARCHAR(255),
    author_intro TEXT,
    author_article_list TEXT[]
);


-- DROP TABLE IF EXISTS publishers;

CREATE TABLE publishers (
    publisher_id VARCHAR(255) PRIMARY KEY,
    publisher_name VARCHAR(255),
    publisher_intro TEXT,
    publisher_reliability_score FLOAT
);

-- DROP TABLE IF EXISTS citations;

CREATE TABLE citations (
    article_id VARCHAR(255) PRIMARY KEY,
    article_paragraphs TEXT[],
    citation_links TEXT[]
);