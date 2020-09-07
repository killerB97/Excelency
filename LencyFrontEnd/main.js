const { app, BrowserWindow, Menu, ipcMain} = require('electron')
const shell = require('electron').shell

let getStartedWindow
let ChBotWindow

function createWindow () {
 /*   const {width, height}= electron.screen.getPrimaryDisplay().bounds
    mainWindow.setBounds({
    x:width-320,
    y:height,
    width:320,
    height:height})*/
  // Create the browser window.

    getStartedWindow= new BrowserWindow({
    //titleBarStyle: "hiddenInset",
    //transparent: true,
    resizable: false,
    width: 700,
    height: 350,
    //frame:false,
    webPreferences: {
      nodeIntegration: true
      //enableRemoteModule: true
     }
     })


  // Catch item:add
    ipcMain.on('openChBotWinID', function(e, openChBotWin){
    console.log(openChBotWin);
    console.log("shi")
    ChBotWindow = new BrowserWindow({
    //titleBarStyle: "hiddenInset",
    transparent: true,
    resizable: false,
    width: 300,
    height: 450,
    //frame:false,
    webPreferences: {
      nodeIntegration: true
    }

  })
  getStartedWindow.close()
  console.log('GS')
  ChBotWindow.loadFile("./htmlFiles/chatBot.html");
  //ChBotWindow.webContents.openDevTools();
});
// and load the index.html of the app.
getStartedWindow.loadFile("./htmlFiles/getStarted.html")


  ipcMain.on('MsgFromUserID', function(e, MsgFromUser){
  console.log(MsgFromUser);
  var response= 'Ssup bruh?'
  /*
  Python functions
  get called here,
  takes input i.e. MsgFromUser,
  performs the task
  and
  stores Rasa's response in
  var response
  */
  ChBotWindow.webContents.send('response', response);
  // win.webContents.send('item:add', item);
  // addWindow.close();
  // Still have a reference to addWindow in memory. Need to reclaim memory (Grabage collection)
  //addWindow = null;
  });



 // win.webContents.send('item:add', item);
 // addWindow.close();
  // Still have a reference to addWindow in memory. Need to reclaim memory (Grabage collection)
  //addWindow = null;



  /*  win = new BrowserWindow({
    //titleBarStyle: "hiddenInset",
    transparent: true,
    resizable: false,
    //width: 300,
    height: 450,
    //frame:false,
    webPreferences: {
      nodeIntegration: true
    }
  })*/

  //win.removeMenu()

  // Open the DevTools.
   //getStartedWindow.webContents.openDevTools()

  //win.webContents.send("submitted-form", "hello")
}



// Catch item:add
//ipcMain.on('item:add', function(e, item){
//  console.log(item);
 // win.webContents.send('item:add', item);
 // addWindow.close();
  // Still have a reference to addWindow in memory. Need to reclaim memory (Grabage collection)
  //addWindow = null;


/*let display=electron.screen.getPrimaryDisplay()
const {width, height}= display.bounds
mainWindow.setBounds({
    x:width-320,
    y:height,
    width:320,
    height:height})*/

var menu= Menu.buildFromTemplate([
    {
        label: 'A',
        submenu: [
            {label: 'A1'},
            {
                label: 'A2',
                click() {
                    shell.openExternal('https://github.com/killerB97/Excelency')
                }
            },
            {type: 'separator'},
            {
                label: 'Exit',
                click() {
                    app.quit()
                }
            }
        ]
    },
    {
        label: 'B'
    }
])

Menu.setApplicationMenu(menu)

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(createWindow)



// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) 
  {
    createWindow()
  }
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.
