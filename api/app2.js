// neo4j cypher helper module

const neo4j = require('neo4j-driver');

const driver = neo4j.driver(
    'neo4j+ssc://7dfcacd0.databases.neo4j.io'
    // 'bolt://7dfcacd0.databases.neo4j.io'
    ,
    neo4j.auth.basic(
        'neo4j',
        'B0QqyzMOAO86pdmKRCh-H6R_jzO_RWOAY2-ReiEIQgo'
    )
);
let session;

async function createAndRetrievePerson() {
    try {
        // Establish a session
        session = driver.session();

        // Create a person node
        await session.run('CREATE (a:Person {name: $name}) RETURN a', {name: 'Alice'});

        let result;

        // Retrieve the person node
        result = await session.run('MATCH (a:Person) WHERE a.name = $name RETURN a', {name: 'Alice'});

        // Process the results
        result.records.forEach(record => {
            console.log(record.get('a').properties.name);
        });

        // Delete
        // await session.run('MATCH (a:Person) WHERE a.name = $name DELETE a', {name: 'Alice'});


        // result = await session.run('' +
        //     '        MATCH (a:Person) WHERE a.name = $name \n' +
        //     '        WITH count(a) as deleted_count \n' +
        //     '        DETACH DELETE a \n' +
        //     '        RETURN deleted_count ', {name: 'Alice'});
        // console.log(result.records[0].get('deleted_count').low);


        result = await session.run(`
                    MATCH (a:Person) WHERE a.name = $name 
                    WITH a, count(a) as deleted_count 
                    DETACH DELETE a 
                    RETURN deleted_count 
                `, {name: 'Alice'}
        );
        console.log(result.records[0].get('deleted_count').low);
    } catch (error) {
        // Handle errors if any
        console.log(error);
    } finally {
        // Close the session whether there was an error or not
        await session.close();
    }
}

createAndRetrievePerson()