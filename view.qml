import QtQuick 2.0
import QtGraphicalEffects 1.0

Rectangle {

    id: backcolor

    // Load the LCD font

    Image {
        id: backgroubd
        x: 0
        y: 0
        width: 1280
        height: 800
        z: 1
        fillMode: Image.PreserveAspectCrop
        source: "images/background.svg"
    }

    Image {
        id: fuelcover
        x: 470
        y: 128
        width: 337
        height: 188
        fillMode: Image.PreserveAspectFit
        z: 3
        source: "images/fuel outline.svg"
    }

    Rectangle {
        id: fuelbar
        x: 484
        y: 175
        width: 311*fuelpercent/100
        height: 88
        color: "#efe619"
        z: 2
    }

    Image {
        id: chargecover
        x: 473
        y: 505
        width: 337
        height: 167
        z: 3
        fillMode: Image.PreserveAspectFit
        source: "images/charge outline.svg"
    }

    Rectangle {
        id: chargebar
        x: 484
        y: 534
        width: 314*chargepercent/100
        height: 88
        color: "#09fb09"
        z: 2
    }

    Image {
        id: tachdial
        x: 1015
        y: 130
        width: 27
        height: 270
        z: 2
        transformOrigin: Item.Top
        antialiasing: true
        fillMode: Image.PreserveAspectFit
        source: "images/tachdial.svg"
        transform: Rotation { origin.x: tachdial.width/2; origin.y: tachdial.height; angle: rpmAngle}
    }

    Image {
        id: speeddial
        x: 238
        y: 130
        width: 27
        height: 270
        z: 2
        source: "images/speeddial.svg"
        transformOrigin: Item.Bottom
        antialiasing: true
        fillMode: Image.PreserveAspectFit
        transform: Rotation { origin.x: speeddial.width/2; origin.y: speeddial.height; angle: speedAngle}

    }

    Text {
        id: engtemp
        x: 612
        y: 463
        width: 75
        height: 30
        color: "#ffffff"
        text: statustext
        z: 2
        scale: 1.4
        font.italic: true
        font.bold: true
        font.family: lcdFont.name
        font.pixelSize: 29
    }

    Text {
        id: speedtxt
        x: 192
        y: 578
        width: 86
        height: 41
        color: "#ffffff"
        text: speednum
        z: 2
        font.pixelSize: 34
        smooth: true
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
        antialiasing: true
        font.italic: true
        font.bold: true
        font.family: lcdFont.name
    }

    Text {
        id: tachtxt
        x: 988
        y: 592
        width: 86
        height: 41
        color: "#ffffff"
        text: rpmnum
        z: 2
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
        font.italic: true
        font.bold: true
        smooth: true
        font.pixelSize: 34
        font.family: lcdFont.name
        antialiasing: true
    }



    FontLoader { id: lcdFont; source: "fonts/arial.ttf" }








    // 800 480 is the real car probably
    property int screenwide: 1280
    property int screenhigh: 800

    // Take up the whole screen
    width: screenwide
    height: screenhigh
    color: "#36363b"
    transformOrigin: Item.Bottom

    // Define properties for colours and texts
    property color statuscolor: "#07DD07"
    property color linecolor: "white"
    property color rpmbg: "#7B7DFB"
    property color rpmactive: "red"
    property color rpmnumber: "white"
    property color speedcolor: "white"
    property color gearcolor: "white"
    property string statustext: "OK"
    property string speednum: "-"
    property string rpmnum: "-"
    property string gear: "-"
    property int rpmAngle: -115
    property int speedAngle: -115
    property int start: 1500
    property int peak: 10000
    property int maxrpm: 14000
    property int fuelpercent: 100
    property int chargepercent: 100

    // Main actual wrapper







}
