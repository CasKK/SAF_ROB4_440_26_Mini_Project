
PROGRAM PLC_PRG
VAR
	state: UINT := 0;
	waitTimer: TON;
	waitTimer1: TON;
	RFID: dc_ecp.Dtm425;
	rfidData: dc_ecp.st_CPF_RfidData;
	TCPclient: dc_ecp.TcpClientByteStream;
	dateAndTime: DATE_AND_TIME;
	getDateAndTime: DTU.GetDateAndTime;
	dateAndTImeString: STRING;
	carrierIDString: STRING;
	sXmlPayload: STRING(255);
	sResponse: STRING(255);
	nStart: INT;
	nEnd: INT;
	nCarrierIDCorrected: UINT;
	stationID: UINT := 9;
	stationIDString: STRING;
	waitTime: TIME;
	processTime: INT;
	CarrierDataReceived: STRING(255);
END_VAR



#######################################################



CASE state OF
	
	0:
	IO.xQA1_RIGHT := TRUE;
	IO.xMB20 := FALSE;
	RFID.ClearError();
	TCPclient.Connect(sIP:='172.20.66.166', uiPort:=12343);
	state := 1;
	
	1:
	IF TCPclient.xConnected AND TCPclient.xReady AND RFID.xReady THEN
		// DTM425 connect = 32; CANbus networkID = 0; DTM425 SDO channel = 1
		RFID.Connect(32, 0, 1);
		waitTimer(IN:=TRUE, PT:=T#2S);
		state := 2;
	END_IF
	
	2:
	IF waitTimer.Q = TRUE THEN
		waitTimer(IN:=FALSE);
		state := 3;
	END_IF
	
	3:
	IF IO.xBG21 = TRUE THEN
		RFID.ReadTag(0, SIZEOF(rfidData), ADR(rfidData));
		getDateAndTime.xExecute := TRUE;
		state := 4;
	END_IF
	
	4:
    IF RFID.xReady AND getDateAndTime.xDone THEN
        dateAndTime := getDateAndTime.dtDateAndTime;
        dateAndTimeString := DT_TO_STRING(dateAndTime);
        stationIDString := UINT_TO_STRING(stationID);
		nCarrierIDCorrected := SHR(rfidData.uiCarrierID, 8); // Convert the RFID value the the actual cart value
        carrierIDString := UINT_TO_STRING(nCarrierIDCorrected);
        (* Build XML string *)
        sXmlPayload := CONCAT('<Data><CarrierID>', carrierIDString);
        sXmlPayload := CONCAT(sXmlPayload, '</CarrierID><DateTime>');
        sXmlPayload := CONCAT(sXmlPayload, dateAndTimeString);
        sXmlPayload := CONCAT(sXmlPayload, '</DateTime><StationID>');
        sXmlPayload := CONCAT(sXmlPayload, stationIDString);
        sXmlPayload := CONCAT(sXmlPayload, '</StationID></Data>');
        (* Send XML string over TCP *)
        TCPclient.Send(pToSend := ADR(sXmlPayload), uiSizeToSend := INT_TO_UINT(LEN(sXmlPayload)));
        state := 5;
    END_IF
	
	5:
	sResponse := '';
    TCPclient.Receive(pToReceive:=ADR(sResponse), uiSizeToReceive:=SIZEOF(sResponse));
    state := 6;

	6:
	IF TCPclient.xReady THEN
		IF LEN(sResponse) > 0 THEN
			state := 7;
		ELSE
			state := 5; // no data yet, try again
		END_IF
	END_IF
	
	7:
	IF TCPclient.xReady THEN
		nStart := FIND(sResponse, '<value>') + 7;    // 7 = ||<value>||
    	nEnd   := FIND(sResponse, '</value>');
    	CarrierDataReceived := MID(sResponse, nEnd - nStart, nStart);
		processTime := STRING_TO_INT(CarrierDataReceived);
		state := 8;
	END_IF
	
	8:
	IO.xQA1_RIGHT := FALSE;
	waitTime := INT_TO_TIME(processTime);
	waitTimer(IN:=TRUE, PT:=waitTime);
	state := 9;
	
	9:
	IF waitTimer.Q = TRUE THEN
		waitTimer(IN:=FALSE);
		IO.xMB20 := TRUE;
		IO.xQA1_RIGHT := TRUE;
		state := 10;
	END_IF
	
	10:
	waitTimer1(IN:= TRUE, PT:= T#0.5S);
	state := 11;
	
	11:
	IF waitTimer1.Q = TRUE THEN
		waitTimer1(IN:=FALSE);
		IO.xMB20 := FALSE;
		state := 1;
	END_IF
	

END_CASE
TCPclient();
RFID();
getDateAndTime();
waitTimer();
waitTimer1();
