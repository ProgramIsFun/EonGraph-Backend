'use strict';

require('dotenv').config();

var nconf = require('nconf');

nconf.env(['PORT', 'NODE_ENV'])
  .argv({
    'e': {
      alias: 'NODE_ENV',
      describe: 'Set production or development mode.',
      demand: false,
      default: 'development'
    },
    'p': {
      alias: 'PORT',
      describe: 'Port to run on.',
      demand: false,
      default: 3062
    },
    'n': {
      alias: "neo4j",
      describe: "Use local or remote neo4j instance",
      demand: false,
      default: "local"
    }
  })
  .defaults({
    'USERNAME': 'neo4j',
    'PASSWORD' : 'B0QqyzMOAO86pdmKRCh-H6R_jzO_RWOAY2-ReiEIQgo',
    'neo4j':

        // 'local'
      // 'bolt://7dfcacd0.databases.neo4j.io'

      'neo4j+ssc://7dfcacd0.databases.neo4j.io'

      ,
    'neo4j-local':
        'neo4j+ssc://7dfcacd0.databases.neo4j.io'

        // 'bolt://7dfcacd0.databases.neo4j.io'

      //
      //   process.env.MOVIE_DATABASE_URL ||
      //   // 'bolt://localhost:7687'
      // 'neo4j+s://7dfcacd0.databases.neo4j.io'
      //
      ,
    'base_url': 'http://localhost:3091',
    'api_path': '/api/v0'
  });

module.exports = nconf;


// pw = "B0QqyzMOAO86pdmKRCh-H6R_jzO_RWOAY2-ReiEIQgo"
// us = "neo4j"
