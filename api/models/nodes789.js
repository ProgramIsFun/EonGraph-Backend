const _ = require('lodash');

const Movie = require('../models/neo4j/movie');


// get all movies
const getAll = function (session) {
    return session.readTransaction(
        txc => (
            txc.run(

                // 'MATCH (movie:Movie) RETURN movie'
            'MATCH (n) RETURN n'

            )
        ))
        .then(r => {
            // manyMovies(r)
            //
            return r
        });
};


// export exposed functions
module.exports = {
    getAll: getAll,
    // getById: getById,
    // getByDateRange: getByDateRange,
    // getByActor: getByActor,
    // getByGenre: getByGenre,
    // getMoviesbyDirector: getByDirector,
    // getMoviesByWriter: getByWriter,
    // rate: rate,
    // deleteRating: deleteRating,
    // getRatedByUser: getRatedByUser,
    // getRecommended: getRecommended
};
