/*const { app } = require("electron")

const printIt = document.getElementById('send')

printIt.addEventListener('click', function (event)
{
  //app.quit()
  document.write(document.getElementById("message").value + "</br>");
})
*/

const electron = require('electron')
//const path = require('path')
const { app, BrowserWindow } = require('electron')
//const BrowserWindow = electron.remote.BrowserWindow

const notifyBtn = document.getElementById('send')

notifyBtn.addEventListener('click', function (event) {
  //document.write(document.getElementById("message").value + "</br>");
    //app.quit()
    //const modalPath = path.join('file://', __dirname, 'add.html')
    //const modalPath= "C:\Users\DELL\ElectronFolder\electron-api-demos\LencyBot\src\add.html"
    //console.log(modalPath)
    let win = new BrowserWindow({     
    transparent: true,
    resizable: false,  
    width: 300,
    height: 450, })
    win.on('close', function () { win = null })
    win.loadFile('src/add.html')
    win.show()
})
