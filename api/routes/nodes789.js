// movies.js
const Movies1 = require('../models/nodes789')
    , _ = require('lodash')
    , writeResponse = require('../helpers/response').writeResponse
    , writeError = require('../helpers/response').writeError
    , loginRequired = require('../middlewares/loginRequired')
    , dbUtils = require('../neo4j/dbUtils');





exports.list = function (req, res, next) {
    Movies1.getAll(dbUtils.getSession(req))
        .then(response => writeResponse(res, response))
        .catch(next);
};