var express = require("express");
var app = express()
app.get('/hello', (req, res) => {
  res.send(5+5)
})




// Ruta directa para una imagen específica
app.get('/gato', (req, res) => {
  //const imagePath = path.join(__dirname, 'imagenes', 'https://purina.com.pe/sites/default/files/2022-10/Que_debes_saber_antes_de_adoptar_un_gatito.jpgfoto.png');
    res.redirect('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQgBBKSpsFEwi6RMAvfvKEh1J_lCgVTsI-7yg&s');
});



app.listen(3000,()=>{console.log("WORK")})
