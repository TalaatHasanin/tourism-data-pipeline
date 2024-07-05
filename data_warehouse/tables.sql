use warehouse easy_tour_wh;
use database easy_tour_db;
use schema easy_tour_sch;

-- create tourists table
create or replace TABLE TOURISTS (
	_ID VARCHAR(50) NOT NULL,
	USER_NAME VARCHAR(50),
	EMAIL STRING,
	GENDER VARCHAR(50),
	LANGUAGE VARCHAR(50),
    "ROLE" VARCHAR(50),
    STATUS VARCHAR(50),
    UPDATED_AT DATETIME,
    CREATED_AT DATETIME,
    COUNTRY VARCHAR(50),
    PHONE_NUMBER VARCHAR(50),
	primary key (_ID)
);


-- create tourguides table
create or replace TABLE tourguides (
	_ID VARCHAR(50) NOT NULL,
	FIRST_NAME VARCHAR(50),
    LAST_NAME VARCHAR(50),
	EMAIL STRING,
    DESCRIPTION STRING,
    ADDRESS STRING,
    BIRTH_DATE VARCHAR(50),
    "ROLE" VARCHAR(50),
    STATUS VARCHAR(50),
    UPDATED_AT DATETIME,
    CREATED_AT DATETIME,
    PHONE_NUMBER VARCHAR(50),
	primary key (_ID)
);

-- create aitrips table
create or replace TABLE aitrips (
	_ID VARCHAR(50) NOT NULL,
	TOURIST_ID VARCHAR(50),
	STATUS VARCHAR(50),
	TITLE VARCHAR(50),
	"from" VARCHAR(20),
	"to" VARCHAR(20),
	primary key (_ID),
    foreign key (TOURIST_ID) references tourists (_id)
);

-- create aitrip_places table
create or replace TABLE aitrip_places (
	_id VARCHAR(50) NOT NULL unique,
	aitrip_id VARCHAR(50),
    place_name STRING,
	day_number INT,
	longitude FLOAT,
    latitude FLOAT,
	activity STRING,
	category STRING,
	primary key (_id),
    foreign key (aitrip_id) references aitrips (_id)
);


-- create customtrips table
create or replace TABLE customtrips (
	_id VARCHAR(50) NOT NULL unique,
	tourist_id VARCHAR(50) NOT NULL,
	title STRING,
	start_date VARCHAR(50),
    end_date VARCHAR(50),
	primary key (_id),
    foreign key (TOURIST_ID) references tourists (_id)
);

-- create customtrip_days table
create or replace TABLE customtrip_days (
	_id VARCHAR(50) NOT NULL unique,
	day_name VARCHAR(50),
	customtrip_id VARCHAR(50) NOT NULL,
	primary key (_id),
    foreign key (customtrip_id) references customtrips (_id)
);


-- create customtrip_places table
create or replace TABLE customtrip_places (
	_id VARCHAR(50) NOT NULL unique,
    day_id VARCHAR(50) NOT NULL,
	place_name STRING,
	government STRING,
    image STRING,
    price_range INT,
	longitude FLOAT,
    latitude FLOAT,
	activity STRING,
	category STRING,
	primary key (_id),
    foreign key (day_id) references customtrip_days (_id)
);


-- create tourguidetrips table
create or replace TABLE tourguidetrips (
	_id VARCHAR(50) NOT NULL unique,
    title STRING,
    brief STRING,
    minimum_number INT,
    created_by VARCHAR(50) NOT NULL,
    status VARCHAR(50),
    created_at DATETIME,
    updated_at DATETIME,
    maximum_number INT,
    current_travelers_no INT,
    standard FLOAT,
    luxury FLOAT,
    VIP FLOAT,
	primary key (_id),
    foreign key (created_by) references tourguides (_id)
);


-- create tourguidetrip_days table
create or replace TABLE tourguidetrip_days (
	_id VARCHAR(50) NOT NULL unique,
    tourguidetrip_id VARCHAR(50) NOT NULL,
	day_name VARCHAR(50),
	created_at DATETIME,
    updated_at DATETIME,
	primary key (_id),
    foreign key (tourguidetrip_id) references tourguidetrips (_id)
);



-- create tourguidetrip_places table
create or replace TABLE tourguidetrip_places (
	_id VARCHAR(50) NOT NULL unique,
    day_id VARCHAR(50) NOT NULL,
	place_name STRING,
    place_type STRING,
	longitude STRING,
    latitude STRING,
	activity STRING,
	primary key (_id),
    foreign key (day_id) references tourguidetrip_days (_id)
);