import QtQuick 2.0
import QtGraphicalEffects 1.0

Rectangle {

    id: backcolor

    // Load the LCD font
    FontLoader { id: lcdFont; source: "fonts/arial.ttf" }

    Image {
        id: gaugecluster
        z: 0
        scale: 1.4
        anchors.fill: parent
        fillMode: Image.Stretch
        source: "images/background.svg"

        Text {
            id: engtemp
            x: 614
            y: 435
            width: 75
            height: 30
            color: "#ffffff"
            text: statustext
            scale: 1.4
            font.italic: true
            font.bold: true
            font.family: lcdFont.name
            font.pixelSize: 29
        }

        Image {
            id: chargedial
            x: 466
            y: 244
            width: 349
            height: 423
            fillMode: Image.Stretch
            source: "images/chargedial.svg"
        }

        Image {
            id: tachdial
            x: 905
            y: 226
            width: 22
            height: 178
            transformOrigin: Item.Top
            antialiasing: true
            fillMode: Image.PreserveAspectFit
            source: "images/tachdial.svg"
            transform: Rotation { origin.x: tachdial.width/2; origin.y: tachdial.height; angle: rpmAngle}
        }

        Image {
            id: speeddial
            x: 353
            y: 226
            width: 22
            height: 178
            source: "images/speeddial.svg"
            transformOrigin: Item.Bottom
            antialiasing: true
            fillMode: Image.PreserveAspectFit
            transform: Rotation { origin.x: speeddial.width/2; origin.y: speeddial.height; angle: speedAngle}

        }

        Text {
            id: speedtxt
            x: 322
            y: 383
            width: 86
            height: 41
            color: "#ffffff"
            text: speednum
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
            x: 873
            y: 383
            width: 86
            height: 41
            color: "#ffffff"
            text: rpmnum
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            font.italic: true
            font.bold: true
            smooth: true
            font.pixelSize: 34
            font.family: lcdFont.name
            antialiasing: true
        }
    }

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
