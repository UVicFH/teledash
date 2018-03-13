import QtQuick 2.0
import QtGraphicalEffects 1.0

Rectangle {

	id: bodyRectangle

	// Load the LCD font
	FontLoader { id: lcdFont; source: "fonts/digital-7.ttf" }

	// 800 480 is the real car probably
	property int screenwide: 800
	property int screenhigh: 480

	// Take up the whole screen
	width: screenwide
	height: screenhigh

	// Define properties for colours and texts
	color: "#2B00AA"
	property color statuscolor: "#07DD07"
	property color linecolor: "white"
	property color rpmbg: "#7B7DFB"
	property color rpmactive: "red"
	property color rpmnumber: "white"
	property color speedcolor: "white"
	property color gearcolor: "white"
	property string statustext: "OK"
	property string speed: "-"
	property string gear: "-" 
	property int rpmAngle: -150
	property int start: 1500
	property int peak: 10000
	property int maxrpm: 14000
	property int fuelpercent: 100
	property int chargepercent: 100

	// Main actual wrapper
	Row {

		// Have 4% margin each side
		width: screenwide
		height:screenhigh*0.92
		anchors.horizontalCenter: parent.horizontalCenter
		anchors.verticalCenter: parent.verticalCenter

		// Tach
		Rectangle{

			width: parent.width*.6
			height: parent.height
			color: bodyRectangle.color

			// Tach
			Image {

				x: parent.width/2-parent.height/2
				source: "images/tach.svg"
				sourceSize.height: parent.height
				height: parent.height

			}

			// Needle
			Image {

				id: needle
				x: parent.width/2-parent.height*15/330
				y: parent.height*.5*30/330
				source: "images/needle.svg"
				sourceSize.height: parent.height*.5
				height: parent.height*.5
				transform: Rotation { origin.x: needle.height*30/330; origin.y: needle.height*300/330; angle: rpmAngle}

			}

			// 12
			Text{

				x:parent.width*.653 - this.width/2
				y:parent.height*.765 - this.height/2
				text:"12"
				height: parent.height*.1
				width:this.height
				font.pixelSize: this.height
				verticalAlignment: Text.AlignVCenter
				horizontalAlignment: Text.AlignHCenter
				color: "white"
				font.family: lcdFont.name
			
			}

			// 10
			Text{

				x:parent.width*.774 - this.width/2
				y:parent.height*.553 - this.height/2
				text:"10"
				height: parent.height*.1
				width:this.height
				font.pixelSize: this.height
				verticalAlignment: Text.AlignVCenter
				horizontalAlignment: Text.AlignHCenter
				color: "white"
				font.family: lcdFont.name
			
			}

			// 8
			Text{

				x:parent.width*.734 - this.width/2
				y:parent.height*.304 - this.height/2
				text:"8"
				height: parent.height*.1
				width:this.height
				font.pixelSize: this.height
				verticalAlignment: Text.AlignVCenter
				horizontalAlignment: Text.AlignHCenter
				color: "white"
				font.family: lcdFont.name
			
			}

			// 6
			Text{

				x:parent.width*.5 - this.width/2
				y:parent.height*.194 - this.height/2
				text:"6"
				height: parent.height*.1
				width:this.height
				font.pixelSize: this.height
				verticalAlignment: Text.AlignVCenter
				horizontalAlignment: Text.AlignHCenter
				color: "white"
				font.family: lcdFont.name
			
			}

			// 4
			Text{

				x:parent.width*.266 - this.width/2
				y:parent.height*.304 - this.height/2
				text:"4"
				height: parent.height*.1
				width:this.height
				font.pixelSize: this.height
				verticalAlignment: Text.AlignVCenter
				horizontalAlignment: Text.AlignHCenter
				color: "white"
				font.family: lcdFont.name
			
			}

			// 2
			Text{

				x:parent.width*.226 - this.width/2
				y:parent.height*.553 - this.height/2
				text:"2"
				height: parent.height*.1
				width:this.height
				font.pixelSize: this.height
				verticalAlignment: Text.AlignVCenter
				horizontalAlignment: Text.AlignHCenter
				color: "white"
				font.family: lcdFont.name
			
			}

			// 0
			Text{

				x:parent.width*.347 - this.width/2
				y:parent.height*.765 - this.height/2
				text:"0"
				height: parent.height*.1
				width:this.height
				font.pixelSize: this.height
				verticalAlignment: Text.AlignVCenter
				horizontalAlignment: Text.AlignHCenter
				color: "white"
				font.family: lcdFont.name
			
			}
			
		}

		Column{

			width: parent.width*.4
			height: parent.height
			
			Row{

				width: parent.width
				height: parent.height*.33

				Column{

					width:parent.width*.7
					height:parent.height

					Text{

						width: parent.width
						height: parent.height*.2
						color: speedcolor
						text: "Speed"
						verticalAlignment: Text.AlignVCenter
						font.pixelSize: this.height
						font.family: lcdFont.name

					}

					Text{

						width: parent.width
						height: parent.height*.8
						color: speedcolor
						text: speed
						verticalAlignment: Text.AlignVCenter
						font.pixelSize: this.height
						font.family: lcdFont.name

					}

				}

				Column{

					width:parent.width*.3
					height:parent.height

					Text{

						width: parent.width
						height: parent.height*.2
						color: speedcolor
						text: "Gear"
						verticalAlignment: Text.AlignVCenter
						font.pixelSize: this.height
						font.family: lcdFont.name

					}

					Text{

						width: parent.width
						height: parent.height*.8
						color: speedcolor
						text: gear
						verticalAlignment: Text.AlignVCenter
						font.pixelSize: this.height
						font.family: lcdFont.name

					}

				}
				
			}

			// Status
			Text{

				width: parent.width
				height: parent.height*.33
				color: statuscolor
				text: statustext
				verticalAlignment: Text.AlignVCenter
				horizontalAlignment: Text.AlignHCenter
				font.pixelSize: this.height
				font.family: lcdFont.name
				
			}

			// Fuel
			Text{

				width: parent.width
				height: parent.height*0.066
				color: speedcolor
				text: "Fuel"
				verticalAlignment: Text.AlignVCenter
				font.pixelSize: this.height
				font.family: lcdFont.name
				
			}

			// Fuelbar
			Rectangle{

				width: parent.width*.9
				height: parent.height*.1
				color: "#373AF9"

				Item{

					width:parent.width*fuelpercent/100
					height:parent.height
					
					LinearGradient {
						anchors.fill: parent
						start: Qt.point(0, 0)
						end: Qt.point(parent.parent.width*.9, 0)
						gradient: Gradient {
							GradientStop { position: 0.0; color: "red" }
							GradientStop { position: 0.25; color: "yellow" }
							GradientStop { position: 0.5; color: "green" }
							GradientStop { position: 1.0; color: "green" }
						}
					}
				}
			}

			// Charge
			Text{

				width: parent.width
				height: parent.height*0.066
				color: speedcolor
				text: "Charge"
				verticalAlignment: Text.AlignVCenter
				font.pixelSize: this.height
				font.family: lcdFont.name
				
			}

			// Chargebar
			Rectangle{

				width: parent.width*.9
				height: parent.height*.1
				color: "#373AF9"

				Item{

					width:parent.width*chargepercent/100
					height:parent.height
					
					LinearGradient {
						anchors.fill: parent
						start: Qt.point(0, 0)
						end: Qt.point(parent.parent.width*.9, 0)
						gradient: Gradient {
							GradientStop { position: 0.0; color: "red" }
							GradientStop { position: 0.25; color: "yellow" }
							GradientStop { position: 0.5; color: "green" }
							GradientStop { position: 1.0; color: "green" }
						}
					}

				}
			}
			
			
		}

	}

}
