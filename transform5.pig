DEFINE SequenceFileLoader org.apache.pig.piggybank.storage.SequenceFileLoader();
DEFINE CSVLoader org.apache.pig.piggybank.storage.CSVExcelStorage;

accidents = LOAD 'output_mr3/*' USING SequenceFileLoader AS (key:chararray, amount:int);
accidents = FILTER accidents BY amount > 0;
accidents = FOREACH accidents GENERATE FLATTEN(STRSPLIT(key,',', 4)) as (street: chararray, zip_code: chararray, person_type: chararray, character: chararray), amount as amount;
accidents = GROUP accidents BY (street, zip_code, person_type);
accidents = FOREACH accidents {
	killed = FILTER accidents BY character == 'killed';
	sum_killed = SUM(killed.amount);
	injured = FILTER accidents BY character == 'injured';
	sum_injured = SUM(injured.amount);
	GENERATE group.street as street,
		group.zip_code as zip_code,
		group.person_type as person_type,
		(sum_killed IS NOT NULL ? sum_killed : 0) as killed,
		(sum_injured IS NOT NULL ? sum_injured : 0) as injured;
};

boroughs = LOAD 'input/datasource4/zips-boroughs.csv' USING CSVLoader(',', 'NO_MULTILINE','UNIX','SKIP_INPUT_HEADER') as (zip_code: chararray, boroughs: chararray);
boroughs = FILTER boroughs BY boroughs == 'MANHATTAN';

result = JOIN accidents BY zip_code, boroughs BY zip_code;
result = GROUP result BY (street, person_type);
result = FOREACH result {
    killed = SUM(result.killed);
    injured = SUM(result.injured);
    GENERATE
        group.street as street,
        group.person_type as person_type,
        killed as killed,
        injured as injured,
        killed + injured as casualties;
};

result = GROUP result BY person_type;
result = FOREACH result {
    ordered_streets = ORDER result BY casualties DESC;
    top_streets = LIMIT ordered_streets 3;
    GENERATE
        group as person_type,
        top_streets as result;
};

result = FOREACH result GENERATE person_type, FLATTEN(result);
result = FOREACH result GENERATE person_type, street as street, killed as killed, injured as injured;

STORE result INTO 'output6/' USING JsonStorage();