import QtQuick 2.0

Rectangle {

	id: bodyRectangle

	// 800 480 is the real car probably
	property int screenwide: 800
	property int screenhigh: 480
	
	// Take up the whole screen
    width: screenwide
    height: screenhigh

    // Define properties for colours and texts
    color: "#2B00AA"
    property color goodstatus: "#07DD07"
    property color linecolor: "white"
    property color rpmbg: "#7B7DFB"
    property color rpmactive: "red"
    property color rpmnumber: "white"
    property color speedcolor: "white"
    property color gearcolor: "white"
    property string statustext: "OK"
    property string speed: "-"
    property string gear: "-" 
    property int rpm: 0
    property int start: 500
   	property int peak: 10000
	property int maxrpm: 14000

	function rpmcolour(i){
		if(rpm > (maxrpm - start)/(60)*i+start-(maxrpm - start)/(60)){
			return rpmactive
		}
		else{
			return rpmbg
		}
	}


    // Main actual wrapper
    Column {

    	// Have 4% margin each side
        width: screenwide*0.92
        anchors.horizontalCenter: parent.horizontalCenter

        // Status text display
        Rectangle { 
            width: parent.width
            height: screenhigh*0.2
            color: parent.parent.color
            
            // Actual text item
            Text { 
            	anchors.centerIn: parent
                font.pixelSize: parent.height
                text: statustext
                color: goodstatus
            } 
      	}

      	// Line dividing status from data
      	Rectangle { 

        	color: linecolor
            width: parent.width
            height: screenhigh*0.001
      	}

      	// Spacer before Row containing tach and etc
      	Item { 

            width: parent.width
            height: screenhigh*0.05
      	}

      	// Row containing the tach etc
      	Row {

      		width: parent.width*.85

      		// Column containing tach and numbering
			Column { 

	            width: parent.width
	            height: screenhigh*0.699

	            Row{

	            	width: parent.width
	            	height:parent.height*.90
	            	property int peakheight: parent.height*.90
	            	property int startheight: parent.height*.85*.2

	            	property int linecount: 60

	            	function rpm(i){
	            		return (maxrpm - start)/(linecount)*i+start-(maxrpm - start)/(linecount)
	            	}

	            	function height(i){
	            		return (startheight - peakheight)/(start - peak)/(start - peak)*(rpm(i)-peak)*(rpm(i)-peak)+peakheight
	            	}

		            Rectangle{property int i:1; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:2; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:3; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:4; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:5; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:6; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:7; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:8; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:9; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:10; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:11; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:12; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:13; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:14; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:15; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:16; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:17; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:18; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:19; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:20; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:21; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:22; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:23; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:24; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:25; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:26; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:27; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:28; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:29; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:30; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:31; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:32; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:33; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:34; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:35; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:36; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:37; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:38; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:39; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:40; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:41; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:42; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:43; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:44; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:45; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:46; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:47; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:48; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:49; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:50; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:51; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:52; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:53; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:54; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:55; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:56; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:57; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:58; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:59; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		            Rectangle{property int i:60; height:parent.height(i); width:parent.width/parent.linecount; color:rpmcolour(i); anchors.bottom: parent.bottom}
		           	
	            }

	            Row{

	            	property int textHeight: parent.height*.05

	            	Text {width:screenwide/32*2.56; text: "500"; font.pixelSize: parent.textHeight; color: rpmnumber} 
	            	Text {width:screenwide/32*3.41; text: "2000"; font.pixelSize: parent.textHeight; color: rpmnumber} 
	            	Text {width:screenwide/32*3.41; text: "4000"; font.pixelSize: parent.textHeight; color: rpmnumber} 
	            	Text {width:screenwide/32*3.41; text: "6000"; font.pixelSize: parent.textHeight; color: rpmnumber} 
	            	Text {width:screenwide/32*3.41; text: "8000"; font.pixelSize: parent.textHeight; color: rpmnumber} 
	            	Text {width:screenwide/32*3.41; text: "10000"; font.pixelSize: parent.textHeight; color: rpmnumber} 
	            	Text {width:screenwide/32*3.41; text: "12000"; font.pixelSize: parent.textHeight; color: rpmnumber} 
	            	Text {width:screenwide/32*3.41; text: "14000"; font.pixelSize: parent.textHeight; color: rpmnumber} 

	            }

	      	}

	      	Column { 

	            width: parent.width*0.15
	            height: screenhigh*10/17

		        Text {
		        	anchors.horizontalCenter: parent.horizontalCenter
	                font.pixelSize: screenhigh*4/17
	                text: speed
	                color: "white"
	            } 

	            Text { 
	            	anchors.horizontalCenter: parent.horizontalCenter
	                font.pixelSize: screenhigh*4/17
	                text: gear
	                color: "white"
	            } 
	            
	      	}

      	}

    }
}