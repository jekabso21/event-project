const mariadb = require('mariadb');

const pool = mariadb.createPool({
    host: '15.204.213.220',
    user: 'root',
    password: 'GKCi651wSa3LutHX',
    database: 'party-event',
    connectionLimit: 5
});



// Connect and check for errors
pool.getConnection((err, connection) => {
    if(err){
        if (err.code === 'PROTOCOL_CONNECTION_LOST'){
            console.error('Database connection lost');
        }
        if (err.code === 'ER_CON_COUNT_ERROR'){
            console.error('Database has too many connection');
        }
        if (err.code === 'ECONNREFUSED'){
            console.error('Database connection was refused');
        }
    }
    if(connection) connection.release();
    console.log('DB is connected');
    return;
});

module.exports = pool;