//////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
// Test2
//   (C) 2016 by  Nicolas Tremblay <nmtremblay.chus@ssss.gouv.qc.ca>
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////

#include <iostream>
#include <fstream>
#include <string>
#include <ctime>
#include <time.h>
#include <stdio.h>      /* printf, scanf, NULL */
#include <stdlib.h>     /* malloc, free, rand */
#include <windows.h>
#include <thread>

#include "iCOMListen.h"
//#include "iCOMClient.h"
#include "iCOMAPI.h"
#include "BetterTimestamp.h"


using namespace std;

///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
int main(int argc, char ** argv)
{
    
    int debug = 2;
    int seconds = 30;
	std::string linac_ip_adress = "192.168.30.2";
	std::string filename = "iCOM"; //
	std::string path = "C:\\temp\\";
	std::string path2 = "image\\";

    std::ofstream debug_file_test("debug.txt");	//Fichier debug
	debug_file_test << "Start" << std::endl;
       

    
	if( argc == 2)
    {
        debug_file_test << "argc : " << argc << std::endl;
        linac_ip_adress = argv[1];
    }
	else if( argc == 3)
    {
        debug_file_test << "argc : " << argc << std::endl;
        linac_ip_adress = argv[1];
        seconds = atoi(argv[2]);
    }
 	else if( argc == 4)
    {
        debug_file_test << "argc : " << argc << std::endl;
        linac_ip_adress = argv[1];
        seconds = atoi(argv[2]);
        filename = argv[3];
    }
 	else if( argc >= 5)
    {
        debug_file_test << "argc : " << argc << std::endl;
        linac_ip_adress = argv[1];
        seconds = atoi(argv[2]);
        filename = argv[3];
        debug = short(atoi(argv[4]));
    }
    
    
    debug_file_test << "linac_ip_adress : " << linac_ip_adress << std::endl;
    debug_file_test << "seconds : " << seconds << std::endl;
    debug_file_test << "filename : " << filename << std::endl;
    debug_file_test << "debug : " << debug << std::endl;
   
    if(argc < 2 || argc > 5)
    {
        std::cout << "Usage: ./iCOMListen.exe [linac_ip_adress] [seconds] [filename] [debug] " << std::endl;
    }
    
    std::clock_t start;			//Clock start value
	double duration = 0;			//duration of the process to test
	//FILE *data_file;
	//data_file = fopen("image", "wb");
	    
	/// output the command line to track history
	std::ofstream cmd_history("cmd_history.txt",std::ios::app);
	for (int b=0 ; b<argc ; b++) cmd_history << argv[b] << " ";
	cmd_history << std::endl;

    

    

    //Init iCOM *******************************************
	debug_file_test << "new iCOMListen()" << std::endl;
    iCOMListen *testiCOM= new iCOMListen(debug);
	
   testiCOM->FonctionTest();
    ///*
    delete testiCOM;
    std::string temp = "";
    cin >> temp;
    exit(0);
    
    debug_file_test << "testiCOM->Connect_iCOM_Vx(" << linac_ip_adress << ");" << std::endl;
	testiCOM->Connect_iCOM_Vx(linac_ip_adress);
    
    
    
    

    
    //Init iView
	debug_file_test << "testiCOM->Init_iView();" << std::endl;
	testiCOM->Init_iView();

    //On set le nom du set d'image et le path (vide pour tout de suite).
    debug_file_test << "testiCOM->SetSavingParameter(" << filename << ", " << path << ");" << std::endl;
    testiCOM->SetSavingParameter(filename, path);
	//debug_file_test << " testiCOM->iview->SetSavingParameter(" << filename << ", " << path << ");" << std::endl;
	//testiCOM->iview->SetSavingParameter("iView", path2);

    //acquisition d'images en background
    debug_file_test << "testiCOM->iview->StartAcquireContinuous();" << std::endl;
	testiCOM->iview->StartAcquireContinuous();
    //*//*
    testiCOM->useStartAcquisitionTrigger =false;
    
    //std::string tempStr = "Infinity3";
    //char* testValue = new char[tempStr.length() + 1];
    //strcpy(testValue, tempStr.c_str());
    
    testiCOM->AddTagToList(0x50010007,'R');
    testiCOM->AddTagToList(0x50010006,'R');
    testiCOM->AddTagToList(0x70010007,'P');
    testiCOM->AddTagToList(0x70010008,'R');
    testiCOM->AddTagToList(0x70010001,'P');
    testiCOM->AddTagToList(0x50010003,'R');
    
    testiCOM->Add_iCOMstartTriggerToList_NonTag(false, 10,1);
    testiCOM->Add_iCOMstopTriggerToList_NonTag(false, 13,1);
   
    debug_file_test << "testiCOM-> Save_iCOM_Messages("<< seconds <<")" << std::endl;
    
	testiCOM->Save_iCOM_Messages(seconds, true, false);
    
    //delete[] testValue;
    
    ///*
    //On arrête l'acquisition iView ici.
	debug_file_test << "testiCOM->iview->StopAcquireContinuous();" << std::endl;
	testiCOM->iview->StopAcquireContinuous();

    //Close iView
	debug_file_test << "testiCOM->Close_iView();" << std::endl;
	testiCOM->Close_iView();
//*//*
	//Fermeture de l'acquisition avec la paneau
    debug_file_test << "testiCOM->Disconnect_iCOM();" << std::endl;
    testiCOM->Disconnect_iCOM();
    
    
	debug_file_test << "On vide les valeurs." << std::endl;
	/**/
	//Fermeture des ficheiers d'output
	cmd_history.close();
	//fclose(data_file);
	delete testiCOM;/**/

    debug_file_test << "End of Main" << std::endl;
   	debug_file_test.close();
    std::string teststop;
    std::cin >> teststop;
    //
	return 0;
}
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
