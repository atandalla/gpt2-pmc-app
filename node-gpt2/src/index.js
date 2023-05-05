const path = require('path');
const express = require('express');
const morgan = require('morgan');
const app = express();
const ejs = require('ejs');
const session = require('express-session');

const HOST = '0.0.0.0';
app.set('port', process.env.PORT || 3000);
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use(session({
    secret: '34SDgsdgspxxxxxxxdfsG',
    resave: false,
    saveUninitialized: true,
}));

app.use(morgan('dev'));
app.use(express.urlencoded({ extended: false }));
app.use(express.json());

app.use(require("./routes/index.routes"));

app.use(require("./routes/books.routes"));

app.use(express.static(path.join(__dirname, 'public')));

app.listen(app.get('port'), HOST, () => {
    console.log(`server on port ${app.get('port')}`);
});