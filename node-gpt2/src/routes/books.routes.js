const router = require("express").Router();
const { spawn } = require('child_process');
const fs = require('fs');
const axios = require('axios');

let titlesearchindex = ""

router.post("/", async(req, res) => {

    const { nameSearch } = req.body;
    let word = nameSearch;
    titlesearchindex = word
    var enc = word.replace(/[.*+?^${}()|[\]\\:;.\-\>\<]/g, "")
    var url_abst = encodeURI(enc)
 
    const respuesta = await axios.get(`http://localhost:4000/api/search/documents/${url_abst}`);
    req.session.data = respuesta.data

    res.redirect('books/1');
});

router.get('/books/:page', (req, res, next) => {

    let data = req.session.data;
    let perPage = 5;
    let page = req.params.page || 1;
    const jsd = data.slice((perPage * page) - perPage, ((perPage * page) - perPage) + perPage) // in the first page the value of the skip is 0
    res.render('books/all-books', {
        jsd,
        current: page,
        pages: Math.ceil(data.length / perPage),
        titlesearchindex
    });
});

router.post("/ajax", async(req, res) => {
    const { id } = req.body;
    let word2 = id;
    var enc = word2.replace(/[.*+?^${}()|[\]\\:;.\-\>\<]/g, "")
    var url_abst = encodeURI(enc)
    const respuesta = await axios.get(`http://localhost:4000/api/search/Similarydocuments/${url_abst}`);
    req.session.data1 = respuesta.data
    res.redirect('/booksPro')

});

router.get('/booksPro', (req, res) => {
    let data = req.session.data1;
    res.json(data)
});

router.post('/gptView', async(req, res) => {
    const { titlegpt2, abstractgpt2 } = req.body;
    let sendtitle = titlegpt2
    let sendabstract = abstractgpt2
    var enc = sendtitle.replace(/[.*+?^${}()|[\]\\:;.\-\>\<\/]/g, "")
    var url_abst = encodeURI(enc)
    var enc2 = sendabstract.replace(/[.*+?^${}()|[\]\\:;.\-\>\<\/]/g, "")
    var url_abst2 = encodeURI(enc2)
    const respuesta = await axios.get(`http://localhost:4000/api/search/GPT2/${url_abst}/${url_abst2}`);
    req.session.data2 = respuesta.data
    let data = req.session.data2;
    res.render('books/gpt2-books', {
        data,
        sendabstract,
        sendtitle
    });

});

router.post('/contact-save', (req, res) => {
    const { name, email, subject, msg } = req.body;
    res.redirect('/');
});

module.exports = router;
