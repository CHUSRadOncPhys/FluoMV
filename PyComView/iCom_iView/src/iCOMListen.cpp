///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
// iCOMListen.cpp
//   (C) 2019 by Nicolas Tremblay <nmtremblay.chus@ssss.gouv.qc.ca>
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////

#include "iCOMListen.h"



//////////////////////////////////////////////////////////////////////////////
//
//////////////////////////////////////////////////////////////////////////////

extern "C"  //Tells the compile to use C-linkage for the next scope.
{
	//Note: The interface this linkage region needs to use C only.  
	iCOMListen * Create_iCOMListen( void )
	{
		// Note: Inside the function body, I can use C++. 
		return new(std::nothrow) iCOMListen(2,0);
	}

	void Delete_iCOMListen(iCOMListen * ptr)
	{
		ptr->Disconnect_iCOM();
		delete ptr; 
		ptr = NULL;
	}

	int Call_SetDebug(iCOMListen *ptr, short Debug)
	{
		try
		{
			ptr->SetDebug(Debug);
			return 1;
		}
		catch(...)
		{ return -1; }
	}

	int Call_SetTimeStampType(iCOMListen *ptr, short Type)
	{
		try
		{
			ptr->SetTimestampType(Type);
			return 1;
		}
		catch(...)
		{ return -1; }
	}
	

	
	int Call_Connect_iCOM_Vx(iCOMListen *ptr, const char *ipLinacAdress, const char *acqName, const char *acqPath)
	{

		try
		{
			int result = ptr->Connect_iCOM_Vx(std::string(ipLinacAdress));
			
			if( result > 0 )
			{
				ptr->SetSavingParameter(std::string(acqName), std::string(acqPath));
			}
			
			return result;
		}
		catch(...)
		{ return 0; }	//0 ==> Connetion pas fonctionné.
	}

	
	int Call_SetSavingParameter(iCOMListen *ptr, const char *acqName, const char *acqPath, short acqSavingPathMode)
	{
		try
		{
			ptr->SetSavingParameter(std::string(acqName), std::string(acqPath), acqSavingPathMode);
			return 1;
		}
		catch(...)
		{ return -1; }	//0 ==> Connetion pas fonctionné. 
	}
	

	int Set_useStartAcquisitionTrigger(iCOMListen *ptr, bool useStartAcquisitionTrig)
	{
		try
		{
			ptr->useStartAcquisitionTrigger = useStartAcquisitionTrig;
			return 1;
		}
		catch(...)
		{ return -1; }	//-1 erreur
	}
	
	int Set_iCOMtagListInSummary(iCOMListen *ptr, bool iCOMtagListInSum)
	{
		try
		{
			ptr->iCOMtagListInSummary = iCOMtagListInSum;
			return 1;
		}
		catch(...)
		{ return -1; }	//-1 erreur
	}

	int Set_iCOMsaveSummaryOnly(iCOMListen *ptr, bool iCOMsaveSumOnly)
	{
		try
		{
			ptr->iCOMsaveSummaryOnly = iCOMsaveSumOnly;
			return 1;
		}
		catch(...)
		{ return -1; }	//-1 erreur
	}

	int Set_acquisitionTimeoutSeconds(iCOMListen *ptr, unsigned int acqTimeoutSeconds)
	{
		try
		{
			ptr->acquisitionTimeoutSeconds = acqTimeoutSeconds;
			return 1;
		}
		catch(...)
		{ return -1; }	//-1 erreur
	}
	

	int Call_ClearTagList(iCOMListen *ptr)
	{
		try
		{
			ptr->ClearTagList();
			return 1;
		}
		catch(...)
		{ return -1; }
	}

	int Call_AddTagToList(iCOMListen *ptr, unsigned long tag, char part)
	{
		try
		{
			ptr->AddTagToList(tag, part);
			return 1;
		}
		catch(...)
		{ return -1; }
	}

	int Call_Disconnect_iCOM(iCOMListen *ptr)
	{
		try
		{
			sleep(1);
			ptr->Disconnect_iCOM();
			return 1;
		}
		catch(...)
		{
			ptr->PrintTestInDebug();
			return -1; //-1 erreur
		}
	}
	
	int Call_Save_iCOM_Messages(iCOMListen *ptr, unsigned int nbrSeconds, bool tagListInSumary, bool SumaryOnly )
	{
		try
		{
			if(nbrSeconds > 0)
			{
				ptr->Save_iCOM_Messages(nbrSeconds,tagListInSumary,SumaryOnly);
			}
			else
			{
				ptr->Save_iCOM_Messages();
			}
			return 1;
		}
		catch(...)
		{ return -1; }	//-1 erreur
		
	}
	
	int Call_Clear_iCOMstartTriggerList(iCOMListen *ptr)
	{
		try
		{
			ptr->Clear_iCOMstartTriggerList();
			return 1;
		}
		catch(...)
		{ return -1; }	//-1 erreur
	}
	
	int Call_Clear_iCOMpauseTriggerList(iCOMListen *ptr)
	{
		try
		{
			ptr->Clear_iCOMpauseTriggerList();
			return 1;
		}
		catch(...)
		{ return -1; }	//-1 erreur
	}
	
	int Call_Clear_iCOMstopTriggerList(iCOMListen *ptr)
	{
		try
		{
			ptr->Clear_iCOMstopTriggerList();
			return 1;
		}
		catch(...)
		{ return -1; }	//-1 erreur
	}
	
	int Call_Add_iCOMstartTriggerToList_tag(iCOMListen *ptr, unsigned long tag, char part, bool trigOnValueChange,  char* value)
	{
		try
		{
			ptr->Add_iCOMstartTriggerToList_tag(tag, part, trigOnValueChange, value);
			return 1;
		}
		catch(...)
		{ return -1; }	//-1 erreur
	}
	
	int Call_Add_iCOMpauseTriggerToList_tag(iCOMListen *ptr, unsigned long tag, char part, bool trigOnValueChange,  char* value)
	{
		try
		{
			ptr->Add_iCOMpauseTriggerToList_tag(tag, part, trigOnValueChange, value);
			return 1;
		}
		catch(...)
		{ return -1; }	//-1 erreur
	}
	
	int Call_Add_iCOMstopTriggerToList_tag(iCOMListen *ptr, unsigned long tag, char part, bool trigOnValueChange,  char* value)
	{
		try
		{
			ptr->Add_iCOMstopTriggerToList_tag(tag, part, trigOnValueChange, value);
			return 1;
		}
		catch(...)
		{ return -1; }	//-1 erreur
	}

	int Call_Add_iCOMstartTriggerToList_NonTag(iCOMListen *ptr, bool trigOnValueChange, short linacState, short triggerType)
	{
		try
		{
			ptr->Add_iCOMstartTriggerToList_NonTag(trigOnValueChange, linacState, triggerType);
			return 1;
		}
		catch(...)
		{ return -1; }	//-1 erreur
	}
	
	int Call_Add_iCOMpauseTriggerToList_NonTag(iCOMListen *ptr, bool trigOnValueChange, short linacState, short triggerType)
	{
		try
		{
			ptr->Add_iCOMpauseTriggerToList_NonTag(trigOnValueChange, linacState, triggerType);
			return 1;
		}
		catch(...)
		{ return -1; }	//-1 erreur
	}
	
	int Call_Add_iCOMstopTriggerToList_NonTag(iCOMListen *ptr, bool trigOnValueChange, short linacState, short triggerType)
	{
		try
		{
			ptr->Add_iCOMstopTriggerToList_NonTag(trigOnValueChange, linacState, triggerType);
			return 1;
		}
		catch(...)
		{ return -1; }	//-1 erreur
	}
	
	
	int Call_Init_iView(iCOMListen *ptr)
	{
		try
		{
			unsigned int result = 0;
			result = ptr->Init_iView();
			
			if(result < 1)
			{ return 1; }
			else
			{ return -1; }
		}
		catch(...)
		{ return -1; }	//-1 erreur
		
	}
	
	int Call_Close_iView(iCOMListen *ptr)
	{
		try
		{
			if(ptr->iview !=NULL)
			{
				ptr->Close_iView();
			}
			else
			{
				return 0;
			}
			return 1;
		}
		catch(...)
		{ return -1; }	//-1 erreur
	}
	
	int Call_iView_StartAcquireContinuous(iCOMListen *ptr, bool StartOnPause)
	{
		try
		{
			if(ptr->iview !=NULL)
			{
				ptr->iview->StartAcquireContinuous(StartOnPause);
			}
			else
			{
				return 0;
			}
			return 1;
		}
		catch(...)
		{ return -1; }	//-1 erreur
		
	}
	
	int Call_iView_PauseImageSavingWithoutStopingAcquisition(iCOMListen *ptr)
	{
		try
		{
			if(ptr->iview !=NULL)
			{
				ptr->iview->PauseImageSavingWithoutStopingAcquisition();
			}
			else
			{
				return 0;
			}
			return 1;
		}
		catch(...)
		{ return -1; }	//-1 erreur
		
	}
	
	int Call_iView_ResumeSavingImageSaving(iCOMListen *ptr)
	{
		try
		{
			if(ptr->iview !=NULL)
			{
				ptr->iview->ResumeSavingImageSaving();
			}
			else
			{
				return 0;
			}
			return 1;
		}
		catch(...)
		{ return -1; }	//-1 erreur
	}
	
	
	int Call_iView_StopAcquireContinuous(iCOMListen *ptr)
	{
		try
		{
			if(ptr->iview !=NULL)
			{
				ptr->iview->StopAcquireContinuous();
			}
			else
			{
				return 0;
			}
			return 1;
		}
		catch(...)
		{ return -1; }	//-1 erreur
	}
	
	
	int Call_iView_SetSavingParameter(iCOMListen *ptr, const char *acqName, const char *acqPath)
	{
		try
		{
			if(ptr->iview !=NULL)
			{
				ptr->iview->SetSavingParameter(std::string(acqName), std::string(acqPath));
			}
			else
			{
				return 0;
			}
			return 1;
		}
		catch(...)
		{ return -1; }	//-1 erreur
	}
		
	
} //End C linkage scope.





//////////////////////////////////////////////////////////////////////////////
//Variables globales
//////////////////////////////////////////////////////////////////////////////

BetterTimestamp* G_horloge_iCOM;

//////////////////////////////////////////////////////////////////////////////
//Variables globales nécessaires auc fonctions d'acquisition et de fin de séquences
//Définies dans iViewControl.cpp
//////////////////////////////////////////////////////////////////////////////

extern bool G_save_images_acquired;
extern bool G_stop_acquisition;
extern unsigned int* G_image_index;
extern BetterTimestamp* G_horloge_iView;

//extern unsigned short* G_pAcqBuffer;
//extern unsigned int G_nbrPixelsBuffer;     //Nombre de pixels dans le Buffer (nbrPixelsImage*nbrImageBuffer)

//extern FILE* G_sequence_detail_file;
//extern std::ofstream* G_iView_debug_file;

//extern std::string G_image_path_name;


////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
iCOMListen::iCOMListen()
{
	debug_file = new std::ofstream("debug_iCOMListen.txt");
    
    initialize_iCOMListen(2,0);
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
iCOMListen::iCOMListen(short Debug)
{
	debug_file = new std::ofstream("debug_iCOMListen.txt");

	initialize_iCOMListen(Debug,0);
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
iCOMListen::iCOMListen(short Debug, short TimestampType)
{
	debug_file = new std::ofstream("debug_iCOMListen.txt");
	
    initialize_iCOMListen(Debug,TimestampType);

}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
iCOMListen::~iCOMListen()
{
	//Fermeture du fichier de debug
	if(debug > 1)
	{
		(*debug_file) << "iCOMListen::~iCOMListen : Deleting" << std::endl;
	}
	
	//On tente de déconnecter iCOM seulement s'il est correctement connecté
	if(iCOMResult != 0)
	{
		if( iCOMGetConnectionState(hICOM) == 1 )
		{
			Disconnect_iCOM();
		}
	}
	
	//On efface l'objet iView (et on ferme la connection avec le panneau) si n'est pas déjà fait
	if(iview != NULL)
	{
		iview->ClosePanel();
		if(debug > 1)
		{
			(*debug_file) << "iCOMListen::~iCOMListen : iView closed" << std::endl;
		}
		if(G_horloge_iCOM == G_horloge_iView)
		{
			if(debug > 1)
			{
				(*debug_file) << "iCOMListen::~iCOMListen : G_horloge_iCOM == G_horloge_iView" << std::endl;
			}
			G_horloge_iView = NULL;
		}
		delete iview;
	}
	
	if(debug > 1)
	{
		(*debug_file) << "iCOMListen::~iCOMListen : iView Deleted" << std::endl;
	}
	
	//On efface l'objet de l'horloge
	if(G_horloge_iCOM != NULL)
	{
		delete G_horloge_iCOM;
	}
	
	if(debug > 1)
	{
		(*debug_file) << "iCOMListen::~iCOMListen : clock deleted." << std::endl;
	}

	
	if(iCOM_last_patient_id != NULL)
	{
		delete[] iCOM_last_patient_id;
	}
	
	//clear vectors
	errornames.clear();
	tagParts.clear();
	startTriggers.clear();
	pauseTriggers.clear();
	stopTriggers.clear();

	if(debug > 1)
	{
		(*debug_file) << "iCOMListen::~iCOMListen : All cleared, closing debug file." << std::endl;
	}
	
	debug_file->close();
	delete debug_file;


	//errordescription.clear();
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iCOMListen::SetDebug(short Debug)
{
	debug = Debug;
    (*debug_file) << "iCOMListen::SetDebug : changing debug to " << debug << std::endl;
	
	//On change la valeur dans iView aussi.
	if(iview != NULL)
	{
        iview->SetDebug(Debug);
	}
    if(G_horloge_iCOM != NULL && G_horloge_iCOM  != G_horloge_iView)
	{
        (*debug_file) << "iCOMListen::SetDebug : changing \"G_horloge_iCOM\" debug value " << std::endl;
        G_horloge_iCOM->SetDebug(Debug);
	}
    
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iCOMListen::SetTimestampType(short Type)
{
    if(debug > 0)
	{
		(*debug_file) << "iCOMListen::SetTimestampType : changing Timestamp type to : " << Type << std::endl;
	}
    
	if(iview != NULL)
	{
		iview->SetTimestampType(Type);
	}
    if(G_horloge_iCOM != NULL && G_horloge_iCOM  != G_horloge_iView)
	{
        G_horloge_iCOM->SetTimestampType(Type);
	}
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iCOMListen::PrintTestInDebug()
{
	(*debug_file) << "iCOMListen::PrintTestInDebug :: Test !!!!!" << std::endl;
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
bool iCOMListen::Connect_iCOM_Vx()
{
	return Connect_iCOM_Vx("192.168.30.2");
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
bool iCOMListen::Connect_iCOM_Vx(std::string ip_adress_linac)		//Connecte iCOM.
{
	if(debug > 0)
	{
		(*debug_file) << "iCOMListen::Connect_iCOM_Vx : Connecting iCOM.......";
	}
	
	//On se connecte à l'appareil en mode écoute seulement (Vx) avec la fonction de la librairie
	//hICOM = iComVXConnect(const char *serverIPAddress, unsigned long timeout);
	try 
	{
		hICOM = iCOMVXConnect(ip_adress_linac.c_str(), 3000);
	}
	catch (...)
	{
		if(debug > 0)
		{
			(*debug_file) << "Failed" << std::endl;
		}
		(*debug_file) << "iCOMListen::Connect_iCOM_Vx : Error catch in iCOMVXConnect" << std::endl;
	}
	
	if(  hICOM <= 0)
	{
		(*debug_file) << "Failed." << std::endl;
		//Regardons si la connection et bonne
		iCOMResult = iCOMGetConnectionState(hICOM);
		print_error_iCOMResult("iCOMGetConnectionState");
	}
	else
	{
		if(debug > 0)
		{
			(*debug_file) << "Connected !" << std::endl;
		}
	}
	
	if(iCOMResult < 0)
	{
		(*debug_file) << "iCOMListen::Connect_iCOM_Vx : Connection invalid returning false" << std::endl;
		return false;
	}
	
	return true;
	
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iCOMListen::Disconnect_iCOM()		//Déconnecte iCOM.
{
	/*if(iCOMResult == 0)
	{
		(*debug_file) << "iCOMListen::Disconnect_iCOM : Not even tried to connect before disconnecting. Not deconnecting." << std::endl;
		return;
	}*/
	
	if(debug > 0)
	{
		(*debug_file) << "iCOMListen::Disconnect_iCOM : Disconnecting iCOM" << std::endl;
	}
	
	iCOMResult = iCOMGetConnectionState(hICOM);
	print_error_iCOMResult("iCOMGetConnectionState");
	
	//On se déconnecte de l'appareil avec la fonction de la librairie
	iCOMResult = iCOMDisconnect(hICOM);
	
	if(debug > 0)
	{
		(*debug_file) << "iCOMListen::Disconnect_iCOM : Disconnected" << std::endl;
	}

	
	print_error_iCOMResult("iComDisconnect");
	iCOMResult = 0;
	
	std::cout << "iCOM s'est deconnecte correctement. \nLe logiciel peut etre ferme en toute securite" << std::endl;
	
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iCOMListen::Save_iCOM_Messages()
{
	if(debug > 0)
	{
		(*debug_file) << "iCOMListen::Save_iCOM_Messages for " << acquisitionTimeoutSeconds << " seconds." << std::endl;
	}
	
	iCOMResult = iCOMGetConnectionState(hICOM);
	
	if(iCOMResult < 0)
	{
		print_error_iCOMResult("iCOMGetConnectionState");
		(*debug_file) << "iCOMListen::Save_iCOM_Messages : Connection invalid. Returning without doing acquisition" << std::endl;
		return;
	}


	//Utilisé pour vérifier que le temps de sauvegarde n'est pas trop long. Pas nécessaire au programme
	int t0 = clock();
	//std::clock_t clocktest;
	//double clocktestresult;
	int duration = -1;
	char part;
	ICOMResult iSize;
	iCOMstopAcquisition = false;
	if(useStartAcquisitionTrigger == true)
	{
		iCOMpauseSaving = true;
		
		if(iCOMsavingPathMode >= 2 && iCOMsavingPathMode <= 5)
		{
			update_iCOMmsg_path_name();
		}            
	}
	else
	{	
		iCOMpauseSaving = false;
			
		//Met les bons nom de fichier et ouvre le fichier de résumé.	
		update_iCOMmsg_path_name();
	}
	
	
	//Défini le tems initial et quand arrêter l'acquisition.
	unsigned long long now_ms_test;
	uint64_t now_ms = G_horloge_iCOM->now();
	uint64_t endAcquisiton_ms = now_ms + (uint64_t)(acquisitionTimeoutSeconds)*10000000u;
	int nbrTag_part =  tagParts.size();

	if(debug > 0)
	{
		(*debug_file) << std::endl;
		(*debug_file) << "Debug iCOM Timestamp" << std::endl;
		(*debug_file) << G_horloge_iCOM->PrintTimestampDebugInfo();
	}
    
    
	do
	{
		
		//On attend la réception d'un message iCOM, le deuxième paramètre est le timout en ms
		if(debug < 10)
		{
			hICOMMsg = iCOMWaitForMessage( hICOM, 2000 );
		}
		else
		{
			
		}
		
		//On update le temps pour maintenant
		now_ms = G_horloge_iCOM->now();

		
		//Si ça ne fonctionne pas...
		if(hICOMMsg == INVALID_CONNECTION_HANDLE ||
				hICOMMsg == TIMEOUT_ERROR ||
				hICOMMsg == INVALID_PROTOCOL_VERSION ||
				hICOMMsg == CONNECTION_FAILED)
		{
			(*debug_file) << "iCOMWaitForMessage -> iCOMResult = " << hICOMMsg << " , " << errornames[abs(hICOMMsg)] << std::endl; //<< " : " << errordescription[abs(iCOMResult)] 
		}
		else
		{
			
			//Verification si on Resume la sauvegarde de l'acquisition
			if(iCOMpauseSaving == false)
			{
				//Trigger de pause
				if(triggerTrigerred(&pauseTriggers))
				{ 
					iCOMpauseSaving = true;
					G_save_images_acquired = false;
					std::cout << "Pause trigger" << std::endl;
				}
			}
			
			//Vérification si on arrête l'aquisiton après ça (Trigger d'arrêt
			if(triggerTrigerred(&stopTriggers))
			{
				iCOMstopAcquisition = true;
				std::cout << "Stop trigger" << std::endl;
			}
			
			//Comme autre trigger d'arrêt, on regarde si qqn appuit sur Esc
			//VK_ESCAPE = 0x1B = 27
			if(GetAsyncKeyState(VK_ESCAPE) != 0) //GetAsyncKeyState est une fonction de Windows.h
			{
				iCOMstopAcquisition = true;
				if(debug > 1)
				{
					(*debug_file) <<  "iCOMListen::Save_iCOM_Messages : Esc Button pressed ! Acquisition will stop." << std::endl;
				}
			}
			

			
			
			//Si on est en pause, on attend d'avoir un id de patient pas en pause, on enregistre !!!
			if(iCOMstopAcquisition == false)
			{
				if(iCOMpauseSaving == true)
				{
					if(iCOMsavingPathMode == 0 || iCOMsavingPathMode == 1)
					{
						//On regarde la valeur du id
						iSize = iCOMGetTagValue(hICOMMsg, 0x70010002, 'P', NULL);
												
						if(iSize > 0)
						{
							char* value = new char[iSize+1];

							iCOMResult = iCOMGetTagValue(hICOMMsg,  0x70010002, 'P', value);
							//print_error_iCOMResult("iCOMGetTagValue");
							
							if( value != NULL &&  (std::string((const char*)value)) != "" && strcmp((const char*)value,(const char*)iCOM_last_patient_id) != 0 )
							{
								
								delete[] iCOM_last_patient_id;
								iCOM_last_patient_id = value;
								iCOM_last_patient_id_str = std::string((const char*)value); 
								
								
								if(debug > 1)
								{
									(*debug_file) <<  " -> Nouveau ID de patient, on update les dossiers : " << iCOM_last_patient_id_str << std::endl;
								}
								
								//Update les paths et crée les dossiers
								update_iCOMmsg_path_name();
								
							}
							else
							{
								
								if(value != NULL)
								{
									delete[] value;
								}
							}
							
						}
						else
						{
							iCOMResult = iSize;
							//print_error_iCOMResult("iCOMGetTagValue (buffersize)");
						}
					}
					
					
					//Vérification des triggers de démarrage
					if(triggerTrigerred(&startTriggers))
					{ 
						if(debug > 1)
						{
							(*debug_file) <<  "Start Trigger !!! Pause = false." << std::endl;
						}
						
						if(iCOM_last_patient_id_str == "") //Devrait être à "" seulement s'il n'y a pas eu de update_iCOMmsg_path_name() depuis le début ou le dernier stop
						{
							update_iCOMmsg_path_name();
						}
						iCOMpauseSaving = false;
						G_save_images_acquired = true;
						std::cout << "Start trigger" << std::endl;
					}
				}

				
				if(iCOMpauseSaving == false)
				{
					//mettre l'index de l'image dans le nom du fichier de l'image
					sprintf(iCOMmsg_path_name_with_index, iCOMmsg_path_name.c_str(), iCOMmsg_index);
					
					//winapi = Acquisition_GetActFrame(hAcqDesc, &dwActAcqFrame, &dwActBuffFrame);
					//print_error_winapi("Acquisition_GetActFrame");

					//On écrit ce nom de fichier dans le résumé de la séquence
					sequence_detail_file =  fopen(sequence_detail_path_name.c_str(),"a");	//Ouverture en append
					fprintf(sequence_detail_file, "%05d,%I64u\n", iCOMmsg_index, now_ms);
					
					//On écrit la date, puis l'heure dans le résumé.
					char *pszDate = new char[30];
					char *pszTime = new char[30];
					//short linacState = 0;
					iCOMResult = iCOMGetDate(hICOMMsg,pszDate);
					iCOMResult = iCOMGetTime(hICOMMsg,pszTime);
					//linacState = iCOMGetState(hICOMMsg);
					fprintf(sequence_detail_file, "%s;Date iCOM\n", pszDate);
					fprintf(sequence_detail_file, "%s;Heure iCOM\n", pszTime);
					//fprintf(sequence_detail_file, "%i; %s\n", linacState,getLinacState(linacState).c_str());
					delete[] pszDate;
					delete[] pszTime;


					//Ici se fait la sauvegarde des tags dans le fichier de résumé.
					if(iCOMtagListInSummary == true)
					{                    
						for(int i = 0; i<nbrTag_part; i++)
						{
							iSize = iCOMGetTagValue(hICOMMsg, tagParts[i].tag, tagParts[i].part, NULL);
							
							//(*debug_file) <<" iSize " << iSize <<  std::endl;
							
							if(iSize > 0)
							{

								char* value = new char[iSize+1];

								iCOMResult = iCOMGetTagValue(hICOMMsg, tagParts[i].tag, tagParts[i].part, value);
								//print_error_iCOMResult("iCOMGetTagValue");

								if( value != NULL )
								{
									//(*debug_file) << tagParts[i].tag << " : " << value << std::endl;
									//fprintf(sequence_detail_file, ":%a,%s\n", tagParts[i].tag, value);
									fprintf(sequence_detail_file, ":0x%x,%c,%s\n", tagParts[i].tag,tagParts[i].part,value);
									//fprintf(sequence_detail_file, ":0x%x,%c,%s; %s\n", tagParts[i].tag,tagParts[i].part,value,getTag(tagParts[i].tag).c_str());	//print avec la description des tags

								}
								else
								{
									fprintf(sequence_detail_file, ":%a,NULL\n", tagParts[i].tag);
									//(*debug_file) << tagParts[i].tag << " : NULL" << std::endl;
								}
								delete[] value;
							}
							else
							{
								iCOMResult = iSize;
								//print_error_iCOMResult("iCOMGetTagValue (buffersize)");
							}
						}
					}
					
					
					fclose(sequence_detail_file);	//fermeture du fichier résumé

					//Si on veut des fichiers individuels pour chacun des message DICOM avec toutes les infos
					if(iCOMsaveSummaryOnly == false)
					{
						//Ouverture du fichier binaire
						iCOMmsg_file = fopen(iCOMmsg_path_name_with_index, "w");
						
						//Impression du time stamp
						fprintf(iCOMmsg_file, "%05d;index\n", iCOMmsg_index);//index
						fprintf(iCOMmsg_file, "%I64u;time stamp ms\n", now_ms);//timestamp en ms
						
						//On imprime tout !!!!
						printAllTags(iCOMmsg_file);
						
						//fermeture du fichier
						fclose(iCOMmsg_file);
					}
					
					//Incrément du nombre d'images
					iCOMmsg_index++;
					
					//Calcul de la duree des operations
					duration = clock() - t0;

					//(*debug_file) << "Save duration = " << ((float)duration)/CLOCKS_PER_SEC <<  " seconds" << std::endl; 
					
				}
			}
				
			iCOMResult = iCOMDeleteMessage(hICOMMsg);			
		}
		
		
	}while(endAcquisiton_ms > now_ms && iCOMstopAcquisition == false);	//Tant que l'Acquisition n'est pas terminée.

	if(debug > 0)
	{
		(*debug_file) << "iCOMListen::Save_iCOM_Messages : Acquisition finished (now_ms = " << now_ms <<  ", iCOMstopAcquisition = " << iCOMstopAcquisition << " ) " << std::endl;
	}
	
	//Dernier patient terminé, on remet le id vide au cas où on ferait une autre acquisiton
	delete[] iCOM_last_patient_id;
	iCOM_last_patient_id = NULL;
	last_timedate = "";
	std::string tmpString = "";
	iCOM_last_patient_id = new char[tmpString.length() + 1];
	iCOM_last_patient_id_str = "";
	strcpy(iCOM_last_patient_id, tmpString.c_str());
	

	//Séparateur de séquence de mesure dans le fichier de résumé, puisque le fichier est toujours en append
	sequence_detail_file =  fopen(sequence_detail_path_name.c_str(),"a");	//Ouverture en append
	fprintf(sequence_detail_file, "\n");
	fclose(sequence_detail_file);	//fermeture du fichier résumé
	
	//On arrête maintenant l'acquisition iView
	iview->StopAcquireContinuous();
	
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iCOMListen::Save_iCOM_Messages(unsigned int nbrSeconds)
{
	acquisitionTimeoutSeconds = nbrSeconds;
	Save_iCOM_Messages();
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iCOMListen::Save_iCOM_Messages(unsigned int nbrSeconds, bool tagListInSumary)
{
	acquisitionTimeoutSeconds = nbrSeconds;
	iCOMtagListInSummary = tagListInSumary;
	Save_iCOM_Messages();
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iCOMListen::Save_iCOM_Messages(unsigned int nbrSeconds, bool tagListInSumary, bool SumaryOnly)
{
	acquisitionTimeoutSeconds = nbrSeconds;
	iCOMtagListInSummary = tagListInSumary;
	iCOMsaveSummaryOnly = SumaryOnly;
	
	//Si on enregistre rien finalement
	if(tagListInSumary == false && iCOMsaveSummaryOnly == false)
	{
		tagListInSumary = true;
	}
	
	Save_iCOM_Messages();
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iCOMListen::SetSavingParameter(std::string acqName, std::string acqPath)
{
	iCOMmsg_name = acqName;
	userSelectedPath = acqPath;

	//test à voir si on doit le faire ici, puisqu'on créera les dossiers peut-être inutilement
	update_iCOMmsg_path_name();	//On s'occupe de iView dans cette fonction là !
	
	
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iCOMListen::SetSavingParameter(std::string acqName, std::string acqPath, short acqSavingPathMode)
{
	iCOMmsg_name = acqName;
	userSelectedPath = acqPath;
	iCOMsavingPathMode = acqSavingPathMode;
	

	//test à voir si on doit le faire ici, puisqu'on créera les dossiers peut-être inutilement
	update_iCOMmsg_path_name();	//On s'occupe de iView dans cette fonction là !
	
	
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iCOMListen::Clear_iCOMstartTriggerList()
{
	startTriggers.clear();
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iCOMListen::Clear_iCOMpauseTriggerList()
{
	pauseTriggers.clear();
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iCOMListen::Clear_iCOMstopTriggerList()
{
	stopTriggers.clear();
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iCOMListen::Add_iCOMstartTriggerToList_tag(unsigned long tag, char part, bool trigOnValueChange,  char* value)
{
	startTriggers.push_back({trigOnValueChange, value, 0, {ICOM_TAG(tag),part}, -1});
		
	if(debug > 1)
	{
		(*debug_file) << "iCOMListen::Add_iCOMstartTriggerToList_tag : ";
		print_trigger(startTriggers.back(), debug_file);
	}
	
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iCOMListen::Add_iCOMpauseTriggerToList_tag(unsigned long tag, char part, bool trigOnValueChange, char* value)
{
	pauseTriggers.push_back({trigOnValueChange, value, 0, {ICOM_TAG(tag),part}, -1});
	
	if(debug > 1)
	{
		(*debug_file) << "iCOMListen::Add_iCOMpauseTriggerToList_tag : ";
		print_trigger(pauseTriggers.back(), debug_file);
	}
	
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iCOMListen::Add_iCOMstopTriggerToList_tag(unsigned long tag, char part, bool trigOnValueChange, char* value)
{
	stopTriggers.push_back({trigOnValueChange, value, 0, {ICOM_TAG(tag),part}, -1});
	
	if(debug > 1)
	{
		(*debug_file) << "iCOMListen::Add_iCOMstopTriggerToList_tag : ";
		print_trigger(stopTriggers.back(), debug_file);
	}

}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iCOMListen::Add_iCOMstartTriggerToList_NonTag(bool trigOnValueChange, short linacState, short triggerType)
{
	if(triggerType < 1 || triggerType > 3)
	{
		(*debug_file) << "Error in iCOMListen::Add_iCOMstartTriggerToList_NonTag : Wrong trigger Type : " << triggerType << std::endl;
	}
	
	startTriggers.push_back({trigOnValueChange, NULL, triggerType, {ICOM_TAG(0x70010001),'P'}, linacState});

	if(debug > 1)
	{
		(*debug_file) << "iCOMListen::Add_iCOMstartTriggerToList_NonTag : ";
		print_trigger(startTriggers.back(), debug_file);
	}
	
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iCOMListen::Add_iCOMpauseTriggerToList_NonTag(bool trigOnValueChange, short linacState, short triggerType)
{
	if(triggerType < 1 || triggerType > 3)
	{
		(*debug_file) << "Error in iCOMListen::Add_iCOMpauseTriggerToList_NonTag : Wrong trigger Type : " << triggerType << std::endl;
	}
	
	pauseTriggers.push_back({trigOnValueChange, NULL, triggerType, {ICOM_TAG(0x70010001),'P'}, linacState});
	
	if(debug > 1)
	{
		(*debug_file) << "iCOMListen::Add_iCOMpauseTriggerToList_NonTag : ";
		print_trigger(pauseTriggers.back(), debug_file);
	}
	
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iCOMListen::Add_iCOMstopTriggerToList_NonTag(bool trigOnValueChange, short linacState, short triggerType)
{
	if(triggerType < 1 || triggerType > 3)
	{
		(*debug_file) << "Error in iCOMListen::Add_iCOMstopTriggerToList_NonTag : Wrong trigger Type : " << triggerType << std::endl;
	}
	
	stopTriggers.push_back({trigOnValueChange, NULL, triggerType, {ICOM_TAG(0x70010001),'P'}, linacState});
	
	if(debug > 1)
	{
		(*debug_file) << "iCOMListen::Add_iCOMstopTriggerToList_NonTag : ";
		print_trigger(stopTriggers.back(), debug_file);
	}

}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iCOMListen::ClearTagList()
{
	tagParts.clear();
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iCOMListen::AddTagToList(unsigned long tag, char part)
{
	//std::cout << tag;
	
	if(debug > 1)
	{
		(*debug_file) << "iCOMListen::AddTagToList : Adding tag : {" << tag << ", " << part << "} "
							<< getTag(tag) << std::endl;
	}
	
	if(part =='P' || part == 'S' || part=='R')
	{
		tagParts.push_back({ICOM_TAG(tag),part});
	}
	else
	{
		(*debug_file) << "iCOMListen::AddTagToList : item par not 'P', 'S' or 'R' : " << part << std::endl;
	}
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
unsigned int iCOMListen::Init_iView()  //En gros initialise le paneau en utilisant la variable debug du iCOM.
{
	unsigned int result = 0;
    //short timestamp_type = 0;   //valeur importe peu ici, puisque l'horloge utilisée sera celle de iCOM et non celle créée lors de l'initialisation de iView
	
	//Si une valeur existe pour la lecture du paneau, on ferme la lecture et delete le pointeur.
	if(iview != NULL)
	{
		iview->ClosePanel();
		if(G_horloge_iCOM == G_horloge_iView)
		{
			G_horloge_iView = NULL;
		}
		delete iview;
	}

	//Création dy pointeur de la classe
	iview = new iViewControl(debug,0);//, timestamp_type);
	
	//Connection au panneau
	result = iview->InitializePanel();
	
	if(result > 0)
	{
		if(debug > 1)
		{
			(*debug_file) << "iCOMListen::Init_iView : iView didn't connect. Deleting pointer iview." << std::endl;
		}
		if(G_horloge_iCOM == G_horloge_iView)
		{
			G_horloge_iView = NULL;
		}
		delete iview;
		iview = NULL;
	}
	else
	{
		if(debug > 1)
		{
			(*debug_file) << "iCOMListen::Init_iView : iView Connected." << std::endl;
		}
	}
	
	//On supprime l'horloge iView et on met celle de iCOM pour que les deux utilise exactement les même temps.
	delete G_horloge_iView;
	G_horloge_iView = G_horloge_iCOM;
	
	update_iCOMmsg_path_name();
	
	return result; //0 = HIS_ALL_OK, >0, implique un problème.

}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iCOMListen::Close_iView()  //En gros initialise le paneau en utilisant la variable debug du iCOM.
{
	if(debug > 0)
	{
		(*debug_file) << "iCOMListen::Close_iView : Closing iView." << std::endl;
	}

	//Si une valeur existe pour la lecture du paneau, on ferme la lecture et delete le pointeur.
	if(iview != NULL)
	{
		iview->ClosePanel();
		
		if(debug > 1)
		{
			(*debug_file) << "iCOMListen::Close_iView : iview->ClosePanel() completed." << std::endl;
		}

		if(G_horloge_iCOM == G_horloge_iView)
		{
			if(debug > 1)
			{
				(*debug_file) << "iCOMListen::Close_iView : G_horloge_iCOM == G_horloge_iView" << std::endl;
			}
			
			G_horloge_iView = NULL;
		}
		
		delete iview;
	}
	
	iview = NULL;
	
	if(debug > 1)
	{
		(*debug_file) << "iCOMListen::Close_iView : Finished." << std::endl;
	}

}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iCOMListen::initialize_iCOMListen(short Debug, short TimestampType)
{
	debug = Debug;
    
	(*debug_file) << "Debug = " << debug << std::endl;
			
	//winapi à 0 puisque pas d'erreur pour l'intant !!!
	iCOMResult = 0; //0 n'existe pas
	//Initialise des vecteurs de description d'Erreur pour aider à debugger
	initialize_error_vectors();
	
	//On initialise l'horloge
    G_horloge_iCOM = new BetterTimestamp(debug, TimestampType);
    
    (*debug_file) << "Debug iCOM Timestamp" << std::endl;
    (*debug_file) << "  " << G_horloge_iCOM->TimestampDebugInfo();

    //G_horloge_iCOM = new BetterTimestamp(debug, TimestampType,debug_file);
    	
	//Definition des paramètres d'image par defaut. On considere un buffer d'une image pour l'instant
	
	//Paramètre de sauvegarde
	userSelectedPath = "";
	iCOMmsg_path = "";	//"images\\";
	iCOMmsg_name = "iCOMmsg";
	iCOMmsg_extension = ".txt";
	
	iCOM_last_patient_id = NULL;
	last_timedate = "";
	std::string tmpString = "";
	iCOM_last_patient_id = new char[tmpString.length() + 1];
	strcpy(iCOM_last_patient_id, tmpString.c_str());
	
	
	tagParts.clear();
	startTriggers.clear();
	pauseTriggers.clear();
	stopTriggers.clear();
	//tagParts.push_back({ICOM_GANTRY_ANGLE,'R'});
	//tagParts.push_back({ICOM_DOSE_RATE_SET,'R'});

	log_name = "log_iCOM.txt";
	
	iCOMmsg_index = 0;
	
	iview = NULL;
	
	iCOMpauseSaving = false;
	iCOMstopAcquisition = false;
	useStartAcquisitionTrigger = false;
	acquisitionTimeoutSeconds = 120;
	iCOMtagListInSummary = true;
	iCOMsaveSummaryOnly = false;
	iCOMsavingPathMode = 0;

}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iCOMListen::initialize_error_vectors()
{
	//Nom et description des codes d'erreur pouvant se retrouver dans "winapi" après l'Exécution d'une fonction XISL
	
	//clear vectors au cas
	errornames.clear();
	//errordescription.clear();

	//Nom des codes d'erreur.
	errornames.push_back("N/A, pas d'erreur 0");						//0
	errornames.push_back("ICOM_RESULT_OK");		//1
	errornames.push_back("INVALID_CONNECTION_HANDLE");						//-2
	errornames.push_back("INVALID_MESSAGE_HANDLE");						//-3
	errornames.push_back("TIMEOUT_ERROR");						//-4
	errornames.push_back("CONNECTION_IN_PROGRESS");						//-5
	errornames.push_back("NOT_CONNECTED");						//-6
	errornames.push_back("INVALID_CONTROL_POINT_NUM");						//-7
	errornames.push_back("DUPLICATE_ITEM");						//-8
	errornames.push_back("MISSING_CONTROL_POINT");						//-9
	errornames.push_back("INVALID_PROTOCOL_VERSION");						//-10
	errornames.push_back("TOO_MANY_TAGS");						//-11
	errornames.push_back("CONNECTION_FAILED");						//-12
	errornames.push_back("SEND_IN_PROGRESS");						//-13
	errornames.push_back("INVALID_TAG");						//-14
	errornames.push_back("ICOM_OUT_OF_MEMORY");						//-15

	
	
	//matrice des description pour chaque erreur selon la documentation.
	//errordescription.push_back("N/A, pas d'erreur 0"); //#0+
	

}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iCOMListen::update_iCOMmsg_path_name()
{
	//Update le nom du fichier. Seule l'index reste à remplacer par la suite lors de la sauvegarde pour accélérer le code lors des acquisitions
	//À faire idéalement avant le début d'une acquisition au cas ou le path ou le nom de fichier soit changé.
	bool date_only = false; //If true, date and time
	bool date_folder = true;
	bool create_patientID_folder = true;
	bool icom_and_image_folder = true;
	std::string iviewpath = "";
	std::string filename = "";
	
	if(iCOMsavingPathMode == 0)
	{
		date_only = false;
		date_folder = true;
		create_patientID_folder = true;
		icom_and_image_folder = true;
	}
	else if(iCOMsavingPathMode == 1)
	{
		date_only = true;
		date_folder = true;
		create_patientID_folder = true;
		icom_and_image_folder = true;
	}
	else if(iCOMsavingPathMode == 2)
	{
		date_only = false;
		date_folder = true;
		create_patientID_folder = false;
		icom_and_image_folder = true;
	}
	else if(iCOMsavingPathMode == 3)
	{
		date_only = true;
		date_folder = true;
		create_patientID_folder = false;
		icom_and_image_folder = true;
	}
	else if(iCOMsavingPathMode == 4)
	{
		date_only = true;
		date_folder = false;
		create_patientID_folder = false;
		icom_and_image_folder = true;
	}
	else if(iCOMsavingPathMode == 5)
	{
		date_only = true;
		date_folder = false;
		create_patientID_folder = false;
		icom_and_image_folder = false;
	}

	
	if(iCOM_last_patient_id_str == "")
	{
		iCOM_last_patient_id_str = "unknown";
	}
	
	if(last_timedate == "")
	{
		last_timedate = getTimeDateString(date_only);
	}
	
	if(debug > 1)
	{
		(*debug_file) << "      iCOMListen::update_iCOMmsg_path_name : iCOMsavingPathMode = " << iCOMsavingPathMode << std::endl;
		(*debug_file) << "      iCOMListen::update_iCOMmsg_path_name : userSelectedPath = " << userSelectedPath << std::endl;
		(*debug_file) << "      iCOMListen::update_iCOMmsg_path_name : iCOM_last_patient_id_str = " << iCOM_last_patient_id_str << std::endl;
		(*debug_file) << "      iCOMListen::update_iCOMmsg_path_name : last_timedate = " << last_timedate << std::endl;
		(*debug_file) << "      iCOMListen::update_iCOMmsg_path_name : userSelectedPath = " << userSelectedPath << std::endl;
	}

	if(DirectoryExists(userSelectedPath.c_str()) == false)
	{
		(*debug_file) << "Error in iCOMListen::update_iCOMmsg_path_name : userSelectedPath doesnt exists : " << userSelectedPath << std::endl;
		return;
	}
	
	//Création des path de sauvegardes
	iCOMmsg_path = userSelectedPath;
	iviewpath = userSelectedPath;
	
	if(create_patientID_folder == true)
	{
		iCOMmsg_path = iCOMmsg_path + iCOM_last_patient_id_str + "\\"; 
		iviewpath = iviewpath + iCOM_last_patient_id_str + "\\";
		
		create_directory(iCOMmsg_path);
		create_directory(iviewpath);
	}
	if(date_folder == true)
	{
		iCOMmsg_path = iCOMmsg_path + last_timedate + "\\"; 
		iviewpath = iviewpath + last_timedate + "\\";
		
		create_directory(iCOMmsg_path);
		create_directory(iviewpath);
	}
	if(icom_and_image_folder == true)
	{
		iCOMmsg_path = iCOMmsg_path + "iCOM\\"; 
		iviewpath = iviewpath + "image\\";
		
		create_directory(iCOMmsg_path);
		create_directory(iviewpath);
	}
	
	if(debug > 1)
	{
		(*debug_file) << "      iCOMListen::update_iCOMmsg_path_name : iCOMmsg_path = " <<  iCOMmsg_path << std::endl;
		(*debug_file) << "      iCOMListen::update_iCOMmsg_path_name : iviewpath = " << iviewpath << std::endl;
	}
	
	/*if( DirectoryExists(iCOMmsg_path.c_str()) == false || DirectoryExists(iviewpath.c_str()) == false )
	{
		if(create_patientID_folder == true)
		{
			create_patient_datetime_directories(iCOM_last_patient_id_str, last_timedate);
		}
		else
		{
			create_datetime_directories(last_timedate);
		}
	}*/
	
	
	if(iview != NULL)
	{
		iview->SetSavingParameter(iCOMmsg_name, iviewpath);
	}
	
	filename = iCOMmsg_path; 
	filename += iCOMmsg_name;
	filename += "_detail.txt";
	
	sequence_detail_path_name = filename;
	
	//On vérifie si d'autres acquisitions au même nom ont été effectuées avant.
	iCOMmsg_index = get_iCOMmsg_index_from_sequence_detail_file(sequence_detail_path_name);
	
	
	iCOMmsg_path_name = iCOMmsg_path;
	iCOMmsg_path_name += iCOMmsg_name;
	iCOMmsg_path_name += "%05d";		//Place de 5 caractères pour le numéro de l'image
	iCOMmsg_path_name += iCOMmsg_extension;
	
	//iCOMmsg_path_name_with_index = iCOMmsg_path_name.c_str();
	
	if(debug > 1)
	{
		(*debug_file) << "iCOMListen::update_iCOMmsg_path_name :: Saving Path and name (without index replaced) : " << iCOMmsg_path_name << std::endl;
	}
	
	if(iCOMmsg_path_name.length() >257)
	{
		(*debug_file) << "Error in iViewControl::update_iCOMmsg_path_name : Path and image name to long (size " << iCOMmsg_path_name.length() 
							<< ") : " << iCOMmsg_path_name << " , endeing software with exit(1)" << std::endl;
		exit(1);
	}
		
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iCOMListen::print_error_iCOMResult(std::string fonction_name) //print winapi, le nom de l'erreur et la description de l'erreur. Insère le nom de la fonction dans le message.
{
	
	//Imprime les cdes d'erreur avec les descriptions

	if (debug > 1 || iCOMResult != ICOM_RESULT_OK) //if(winapi != 0)
	{
		(*debug_file) << fonction_name << " -> iCOMResult = " << iCOMResult << " , " << errornames[abs(iCOMResult)] << std::endl; //<< " : " << errordescription[abs(iCOMResult)] 
	}
	
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iCOMListen::printAllTags(FILE* aFile)
{
	ICOM_TAG aTag;
	char chPart = 'R';
	char *achValue = new char[255];
	char *pszDate = new char[30];
	char *pszTime = new char[30];
	short linacState = 0;
	short linacFunctionMode = 0;
	//char achValueSet[255];
	//char achValueRun[255];
	
	if(hICOMMsg > 0)
	{
		//unsigned long long now_ms = std::chrono::system_clock::now().time_since_epoch() / std::chrono::milliseconds(1);
		//fprintf(aFile, "%05d,%I64u\n", iCOMmsg_index, now_ms);
		
		//On va chercher la date et l'heure selon iCOM pour l'écrire dans le fichier
		iCOMResult = iCOMGetDate(hICOMMsg,pszDate);
		iCOMResult = iCOMGetTime(hICOMMsg,pszTime);
		linacState = iCOMGetState(hICOMMsg);
		linacFunctionMode = iCOMGetFunction(hICOMMsg);        
		fprintf(aFile, "%s;Date iCOM\n", pszDate);
		fprintf(aFile, "%s;Heure iCOM\n", pszTime);
		fprintf(aFile, "%i; %s\n", linacFunctionMode,getLinacFunctionMode(linacFunctionMode).c_str());
		fprintf(aFile, "%i; %s\n", linacState,getLinacState(linacState).c_str());

		//On prend le premier tag
		iCOMResult = iCOMGetFirstTagValue  (hICOMMsg, &aTag, &chPart, achValue);
		
		while( iCOMResult == ICOM_RESULT_OK ) //tant qu'il y a un tag
		{
			//(*debug_file) << getTag(aTag) << "," << chPart << "," <<achValue << std::endl;
			fprintf(aFile, ":0x%x,%c,%s; %s\n", aTag,chPart,achValue,getTag(aTag).c_str());	//print avec la description des tags
			//fprintf(aFile, ":0x%x,%c,%s;\n", aTag,chPart,achValue);									//print sans la description des tags, mais plus rapide un mini peu
			delete[] achValue;
			achValue = new char[255];
			iCOMResult = iCOMGetNextTagValue   (hICOMMsg, &aTag, &chPart, achValue);
		}
	}
	else
	{
		(*debug_file) << "Error in iCOMListen::printAllTags, hICOMMsg = " <<hICOMMsg << std::endl;
	}
	
	delete[] pszDate;
	delete[] pszTime;
	delete[] achValue;
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
std::string iCOMListen::getTag(ICOM_TAG tag)
{
	if(tag == ICOM_MACHINE_NAME)		//0x70010001;
	{ return "ICOM_MACHINE_NAME"; }
	else if(tag == ICOM_PATIENT_ID)				//0x70010002;
	{ return "ICOM_PATIENT_ID"; }
	else if(tag == ICOM_PATIENT_NAME)			//0x70010003;
	{ return "ICOM_PATIENT_NAME"; }
	else if(tag == ICOM_TREATMENT_ID)			//0x70010004;
	{ return "ICOM_TREATMENT_ID"; }
	else if(tag == ICOM_TREATMENT_NAME)			//0x70010005;
	{ return "ICOM_TREATMENT_NAME"; }
	else if(tag == ICOM_BEAM_ID)				//0x70010006;
	{ return "ICOM_BEAM_ID"; }
	else if(tag == ICOM_BEAM_NAME)				//0x70010007;
	{ return "ICOM_BEAM_NAME"; }
	else if(tag == ICOM_COMPLEXITY)				//0x70020005;
	{ return "ICOM_COMPLEXITY"; }
	else if(tag == ICOM_EXTERNAL_CHAN_1)		//0x50010020;
	{ return "ICOM_EXTERNAL_CHAN_1"; }
	else if(tag == ICOM_EXTERNAL_CHAN_2)		//0x50010021;
	{ return "ICOM_EXTERNAL_CHAN_2"; }
	else if(tag == ICOM_EXTERNAL_CHAN_3)		//0x50010022;
	{ return "ICOM_EXTERNAL_CHAN_3"; }
	else if(tag == ICOM_EXTERNAL_CHAN_4)		//0x50010023;
	{ return "ICOM_EXTERNAL_CHAN_4"; }
	else if(tag == ICOM_EXTERNAL_CHAN_5)		//0x50010024;
	{ return "ICOM_EXTERNAL_CHAN_5"; }
	else if(tag == ICOM_EXTERNAL_CHAN_6)		//0x50010025;
	{ return "ICOM_EXTERNAL_CHAN_6"; }
	else if(tag == ICOM_EXTERNAL_CHAN_7)		//0x50010026;
	{ return "ICOM_EXTERNAL_CHAN_7"; }
	else if(tag == ICOM_EXTERNAL_CHAN_8)		//0x50010027;
	{ return "ICOM_EXTERNAL_CHAN_8"; }
	else if(tag == ICOM_BEAM_MONITOR_UNITS)		//0x50010001;
	{ return "ICOM_BEAM_MONITOR_UNITS"; }
	else if(tag == ICOM_NR_CONTROL_POINTS)		//0x70020002;
	{ return "ICOM_NR_CONTROL_POINTS"; }
	else if(tag == ICOM_CONTROL_POINT_INDEX)	//0x70020003;
	{ return "ICOM_CONTROL_POINT_INDEX"; }
	else if(tag == ICOM_NR_DELIVERY_SEGMENTS)	//0x70020008;
	{ return "ICOM_NR_DELIVERY_SEGMENTS"; }
	else if(tag == ICOM_RADIATION_TYPE)			//0x50010002;
	{ return "ICOM_RADIATION_TYPE"; }
	else if(tag == ICOM_ENERGY)					//0x50010003;
	{ return "ICOM_ENERGY"; }
	else if(tag == ICOM_CUM_BEAM_PERCENTAGE)	//0x70020004;
	{ return "ICOM_CUM_BEAM_PERCENTAGE"; }
	else if(tag == ICOM_WEDGE_POSITION)			//0x50010004;
	{ return "ICOM_WEDGE_POSITION"; }
	else if(tag == ICOM_BEAM_TIMER)				//0x70010038;
	{ return "ICOM_BEAM_TIMER"; }
	else if(tag == ICOM_SEGMENT_TIMER)			//0x50010005;	// Retain for backwards compatibility, ignored by FX
	{ return "ICOM_SEGMENT_TIMER"; }
	else if(tag == ICOM_DOSE_RATE_SET)			//0x50010006;
	{ return "ICOM_DOSE_RATE_SET"; }
	else if(tag == ICOM_GANTRY_ANGLE)			//0x50010007;
	{ return "ICOM_GANTRY_ANGLE"; }
	else if(tag == ICOM_COLLIMATOR_ANGLE	)	//0x50010008;
	{ return "ICOM_COLLIMATOR_ANGLE"; }
	else if(tag == ICOM_COLLIMATOR_X1)			//0x50010009;
	{ return "ICOM_COLLIMATOR_X1"; }
	else if(tag == ICOM_COLLIMATOR_X2)			//0x5001000A;
	{ return "ICOM_COLLIMATOR_X2"; }
	else if(tag == ICOM_COLLIMATOR_Y1)			//0x5001000B;
	{ return "ICOM_COLLIMATOR_Y1"; }
	else if(tag == ICOM_COLLIMATOR_Y2)			//0x5001000C;
	{ return "ICOM_COLLIMATOR_Y2"; }
	else if(tag == ICOM_ELECTRON_APP_CODE)		//0x5001000D;
	{ return "ICOM_ELECTRON_APP_CODE"; }
	else if(tag == ICOM_ELECTRON_APP_FITMENT)	//0x5001000E;
	{ return "ICOM_ELECTRON_APP_FITMENT"; }
	else if(tag == ICOM_ACCESSORY_NUMBER)		//0x5001000F;
	{ return "ICOM_ACCESSORY_NUMBER"; }
	else if(tag == ICOM_TABLE_HEIGHT)			//0x50010010;
	{ return "ICOM_TABLE_HEIGHT"; }
	else if(tag == ICOM_TABLE_ROTATION)			//0x50010011;
	{ return "ICOM_TABLE_ROTATION"; }
	else if(tag == ICOM_TABLE_LATERAL)			//0x50010012;
	{ return "ICOM_TABLE_LATERAL"; }
	else if(tag == ICOM_TABLE_LONGITUDINAL)		//0x50010013;
	{ return "ICOM_TABLE_LONGITUDINAL"; }
	else if(tag == ICOM_TABLE_ISOC_ROT)			//0x50010014;
	{ return "ICOM_TABLE_ISOC_ROT"; }
	else if(tag == ICOM_FIELDSIZE_X)			//0x50010015;
	{ return "ICOM_FIELDSIZE_X"; }
	else if(tag == ICOM_FIELDSIZE_Y)			//0x50010016;
	{ return "ICOM_FIELDSIZE_Y"; }
	else if(tag == ICOM_OFFSET_X)				//0x50010017;
	{ return "ICOM_OFFSET_X"; }
	else if(tag == ICOM_OFFSET_Y)				//0x50010018;
	{ return "ICOM_OFFSET_Y"; }
	else if(tag == ICOM_GANTRY_DIRECTION)		//0x50010019;
	{ return "ICOM_GANTRY_DIRECTION"; }
	else if(tag == ICOM_BEAM_LIMITING_DEVICE)	//0x500100B8;
	{ return "ICOM_BEAM_LIMITING_DEVICE"; }
	else if(tag == ICOM_MLC_SHAPE)				//0x500100B9;	// Alt name, see Ext, I/F's Manual
	{ return "ICOM_MLC_SHAPE"; }
	else if(tag == ICOM_BEAM_LIMITING_DEVICEX)	//0x500100B9;
	{ return "ICOM_BEAM_LIMITING_DEVICEX"; }
	else if(tag == ICOM_BEAM_LIMITING_DEVICEY)	//0x500100BA;
	{ return "ICOM_BEAM_LIMITING_DEVICEY"; }
	else if(tag == ICOM_COLLIMATOR_DIRECTION)	//0x500100BB;
	{ return "ICOM_COLLIMATOR_DIRECTION"; }
	else if(tag == ICOM_TABLE_SETUP)			//0x500100BC;
	{ return "ICOM_TABLE_SETUP"; }
	else if(tag == ICOM_DELIVERED_MONITOR_UNITS)//0x70020007;
	{ return "ICOM_DELIVERED_MONITOR_UNITS"; }
	else if(tag == ICOM_FINISH_FIELD_INDICATOR)	//0x70020009;
	{ return "ICOM_FINISH_FIELD_INDICATOR"; }
	else if(tag == ICOM_DELIVER_NOW_INDICATOR)	//0x7002000A;
	{ return "ICOM_DELIVER_NOW_INDICATOR"; }
	else if(tag == ICOM_LEAF_WIDTH)				//0x70020006;
	{ return "ICOM_LEAF_WIDTH"; }
	else if(tag == ICOM_GANTRY_STOP_ANGLE)		//0x50020007;
	{ return "ICOM_GANTRY_STOP_ANGLE"; }
	else if(tag == ICOM_COLLIMATOR_STOP_ANGLE)	//0x50020008;
	{ return "ICOM_COLLIMATOR_STOP_ANGLE"; }
	else if(tag == ICOM_COLLIMATOR_X1_STOP)		//0x50020009;
	{ return "ICOM_COLLIMATOR_X1_STOP"; }
	else if(tag == ICOM_COLLIMATOR_X2_STOP)		//0x5002000A;
	{ return "ICOM_COLLIMATOR_X2_STOP"; }
	else if(tag == ICOM_COLLIMATOR_Y1_STOP)		//0x5002000B;
	{ return "ICOM_COLLIMATOR_Y1_STOP"; }
	else if(tag == ICOM_COLLIMATOR_Y2_STOP)		//0x5002000C;
	{ return "ICOM_COLLIMATOR_Y2_STOP"; }
	else if(tag == ICOM_TABLE_HEIGHT_STOP)		//0x50020010;
	{ return "ICOM_TABLE_HEIGHT_STOP"; }
	else if(tag == ICOM_TABLE_ROTATION_STOP)	//0x50020011;
	{ return "ICOM_TABLE_ROTATION_STOP"; }
	else if(tag == ICOM_TABLE_LATERAL_STOP)		//0x50020012;
	{ return "ICOM_TABLE_LATERAL_STOP"; }
	else if(tag == ICOM_TABLE_LONGITUDINAL_STOP)//0x50020013;
	{ return "ICOM_TABLE_LONGITUDINAL_STOP"; }
	else if(tag == ICOM_TABLE_ISOC_ROT_STOP)	//0x50020014;
	{ return "ICOM_TABLE_ISOC_ROT_STOP"; }
	else if(tag == ICOM_MLC_LEAF_Y1_01)			//0x50010101;
	{ return "ICOM_MLC_LEAF_Y1_01"; }
	else if(tag == ICOM_MLC_LEAF_Y1_40)			//0x50010128;
	{ return "ICOM_MLC_LEAF_Y1_40"; }
	else if(tag == ICOM_MLC_LEAF_Y1_80)			//0x50010150;
	{ return "ICOM_MLC_LEAF_Y1_80"; }
	else if(tag == ICOM_MLC_LEAF_Y2_01)			//0x50010201;
	{ return "ICOM_MLC_LEAF_Y2_01"; }
	else if(tag == ICOM_MLC_LEAF_Y2_40)			//0x50010228;
	{ return "ICOM_MLC_LEAF_Y2_40"; }
	else if(tag == ICOM_MLC_LEAF_Y2_80)			//0x50010250;
	{ return "ICOM_MLC_LEAF_Y2_80"; }
	else if(tag == ICOM_SEGMENT_ID	)			//0x70010008;
	{ return "ICOM_SEGMENT_ID"; }
	else if(tag == ICOM_LVI_STEP_MONITOR_UNIT)	//0x7002000B;
	{ return "ICOM_LVI_STEP_MONITOR_UNIT"; }
	else if(tag == ICOM_LVI_MONITOR_UNIT1)		//0x70010009;
	{ return "ICOM_LVI_MONITOR_UNIT1"; }
	else if(tag == ICOM_LVI_MONITOR_UNIT2)		//0x7001000A;
	{ return "ICOM_LVI_MONITOR_UNIT2"; }
	else if(tag == ICOM_LVI_WEDGED_MU)          //0x50010028;
	{ return "ICOM_LVI_WEDGED_MU"; }
	else if(tag == ICOM_LVI_TOLERANCE_TABLE)	//0x7001000B;
	{ return "ICOM_LVI_TOLERANCE_TABLE"; }
	else if(tag == ICOM_LVI_TECHNIQUE_ID)		//0x7001000C;
	{ return "ICOM_LVI_TECHNIQUE_ID"; }
	else if(tag == ICOM_LVI_FOR_MACHINE)		//0x7001000D;
	{ return "ICOM_LVI_FOR_MACHINE"; }
	else if(tag == ICOM_TREATMENT_REMINDER_1)	//0x7001000E;
	{ return "ICOM_TREATMENT_REMINDER_1"; }
	else if(tag == ICOM_TREATMENT_REMINDER_2)	//0x7001000F;
	{ return "ICOM_TREATMENT_REMINDER_2"; }
	else if(tag == ICOM_TREATMENT_REMINDER_3)	//0x70010010;
	{ return "ICOM_TREATMENT_REMINDER_3"; }
	else if(tag == ICOM_TREATMENT_REMINDER_4)	//0x70010011;
	{ return "ICOM_TREATMENT_REMINDER_4"; }
	else if(tag == ICOM_TREATMENT_REMINDER_5)	//0x70010012;
	{ return "ICOM_TREATMENT_REMINDER_5"; }
	else if(tag == ICOM_TREATMENT_REMINDER_6)	//0x70010013;
	{ return "ICOM_TREATMENT_REMINDER_6"; }
	else if(tag == ICOM_BEAM_REMINDER_1)		//0x70010014;
	{ return "ICOM_BEAM_REMINDER_1"; }
	else if(tag == ICOM_BEAM_REMINDER_2)		//0x70010015;
	{ return "ICOM_BEAM_REMINDER_2"; }
	else if(tag == ICOM_BEAM_REMINDER_3)		//0x70010016;
	{ return "ICOM_BEAM_REMINDER_3"; }
	else if(tag == ICOM_BEAM_REMINDER_4)		//0x70010017;
	{ return "ICOM_BEAM_REMINDER_4"; }
	else if(tag == ICOM_PRESC_TGT_DOSE)			//0x70010018;
	{ return "ICOM_PRESC_TGT_DOSE"; }
	else if(tag == ICOM_ACCUM_TGT_DOSE)			//0x70010019;
	{ return "ICOM_ACCUM_TGT_DOSE"; }
	else if(tag == ICOM_ACCUM_DOSE_B)			//0x7001001A;
	{ return " ICOM_ACCUM_DOSE_B"; }
	else if(tag == ICOM_ACCUM_DOSE_C)			//0x7001001B;
	{ return "ICOM_ACCUM_DOSE_C"; }
	else if(tag == ICOM_ACCUM_DOSE_D)			//0x7001001C;
	{ return "ICOM_ACCUM_DOSE_D"; }
	else if(tag == ICOM_ACCUM_DOSE_E)			//0x7001001D;
	{ return "ICOM_ACCUM_DOSE_E"; }
	else if(tag == ICOM_ACCUM_DOSE_F)			//0x7001001E;
	{ return "ICOM_ACCUM_DOSE_F"; }
	else if(tag == ICOM_ACCUM_DOSE_G)			//0x7001001F;
	{ return "ICOM_ACCUM_DOSE_G"; }
	else if(tag == ICOM_SESSION_TGT_DOSE)		//0x70010020;
	{ return "ICOM_SESSION_TGT_DOSE"; }
	else if(tag == ICOM_SESSION_DOSE_B)			//0x70010021;
	{ return "ICOM_SESSION_DOSE_B"; }
	else if(tag == ICOM_SESSION_DOSE_C)			//0x70010022;
	{ return "ICOM_SESSION_DOSE_C"; }
	else if(tag == ICOM_SESSION_DOSE_D)			//0x70010023;
	{ return "ICOM_SESSION_DOSE_D"; }
	else if(tag == ICOM_SESSION_DOSE_E)			//0x70010024;
	{ return "ICOM_SESSION_DOSE_E"; }
	else if(tag == ICOM_SESSION_DOSE_F)			//0x70010025;
	{ return "ICOM_SESSION_DOSE_F"; }
	else if(tag == ICOM_SESSION_DOSE_G)			//0x70010026;
	{ return "ICOM_SESSION_DOSE_G"; }
	else if(tag == ICOM_BEAM_TGT_DOSE)			//0x70010027;
	{ return "ICOM_BEAM_TGT_DOSE"; }
	else if(tag == ICOM_BEAM_DOSE_B)			//0x70010028;
	{ return "ICOM_BEAM_DOSE_B"; }
	else if(tag == ICOM_BEAM_DOSE_C)			//0x70010029;
	{ return "ICOM_BEAM_DOSE_C"; }
	else if(tag == ICOM_BEAM_DOSE_D)			//0x7001002A;
	{ return "ICOM_BEAM_DOSE_D"; }
	else if(tag == ICOM_BEAM_DOSE_E)			//0x7001002B;
	{ return "ICOM_BEAM_DOSE_E"; }
	else if(tag == ICOM_BEAM_DOSE_F)			//0x7001002C;
	{ return "ICOM_BEAM_DOSE_F"; }
	else if(tag == ICOM_BEAM_DOSE_G)			//0x7001002D;
	{ return "ICOM_BEAM_DOSE_G"; }
	else if(tag == ICOM_BEAM_ENTRY_DOSE)		//0x7001002E;
	{ return "ICOM_BEAM_ENTRY_DOSE"; }
	else if(tag == ICOM_PRESC_ENTRY_DOSE)		//0x7001002F;
	{ return "ICOM_PRESC_ENTRY_DOSE"; }
	else if(tag == ICOM_ACCUM_ENTRY_DOSE)		//0x70010030;
	{ return "ICOM_ACCUM_ENTRY_DOSE"; }
	else if(tag == ICOM_ACCUM_TGT_BEAM)			//0x70010031;
	{ return "ICOM_ACCUM_TGT_BEAM"; }
	else if(tag == ICOM_BEAM_ACCUM_B)			//0x70010032;
	{ return "ICOM_BEAM_ACCUM_B"; }
	else if(tag == ICOM_BEAM_ACCUM_C)			//0x70010033;
	{ return "ICOM_BEAM_ACCUM_C"; }
	else if(tag == ICOM_BEAM_ACCUM_D)			//0x70010034;
	{ return "ICOM_BEAM_ACCUM_D"; }
	else if(tag == ICOM_BEAM_ACCUM_E)			//0x70010035;
	{ return "ICOM_BEAM_ACCUM_E"; }
	else if(tag == ICOM_BEAM_ACCUM_F)			//0x70010036;
	{ return "ICOM_BEAM_ACCUM_F"; }
	else if(tag == ICOM_BEAM_ACCUM_G)			//0x70010037;
	{ return "ICOM_BEAM_ACCUM_G"; }
	else if(tag == ICOM_INHIBIT_REASON_1)		//0x50010050;
	{ return "ICOM_INHIBIT_REASON_1"; }
	else if(tag == ICOM_INHIBIT_REASON_2)		//0x50010051;
	{ return "ICOM_INHIBIT_REASON_2"; }
	else if(tag == ICOM_INHIBIT_REASON_3)		//0x50010054;
	{ return "ICOM_INHIBIT_REASON_3"; }
	else if(tag == ICOM_INHIBIT_REASON_4)		//0x50010055;
	{ return "ICOM_INHIBIT_REASON_4"; }
	else if(tag == ICOM_INHIBIT_REASON_5)		//0x50010056;
	{ return "ICOM_INHIBIT_REASON_5"; }
	else if(tag == ICOM_INHIBIT_REASON_6)		//0x50010057;
	{ return "ICOM_INHIBIT_REASON_6"; }
	else if(tag == ICOM_INHIBIT_REASON_7)		//0x50010058;
	{ return "ICOM_INHIBIT_REASON_7"; }
	else if(tag == ICOM_INHIBIT_REASON_8)		//0x50010059;
	{ return "ICOM_INHIBIT_REASON_8"; }
	else if(tag == ICOM_INHIBIT_REASON_9)		//0x5001005a;
	{ return "ICOM_INHIBIT_REASON_9"; }
	else if(tag == ICOM_INHIBIT_REASON_10)		//0x5001005b;
	{ return "ICOM_INHIBIT_REASON_10"; }
	else if(tag == ICOM_INHIBIT_REASON_11)		//0x5001005c;
	{ return "ICOM_INHIBIT_REASON_11"; }
	else if(tag == ICOM_INHIBIT_REASON_12)		//0x5001005d;
	{ return "ICOM_INHIBIT_REASON_12"; }
	else if(tag == ICOM_INTERRUPT_REASON)		//0x50010052;
	{ return "ICOM_INTERRUPT_REASON"; }
	else if(tag == ICOM_INTERRUPT_REASON_2)		//0x5001005E;
	{ return "ICOM_INTERRUPT_REASON_2"; }
	else if(tag == ICOM_INTERRUPT_REASON_3)		//0x50010070;
	{ return "ICOM_INTERRUPT_REASON_3"; }
	else if(tag == ICOM_INTERRUPT_REASON_4)		//0x50010071;
	{ return "ICOM_INTERRUPT_REASON_4"; }
	else if(tag == ICOM_TERMINATE_REASON)		//0x50010053;
	{ return "ICOM_TERMINATE_REASON"; }
	else if(tag == ICOM_TERMINATE_REASON_2)		//0x5001005F;
	{ return "ICOM_TERMINATE_REASON_2"; }
	else if(tag == ICOM_TERMINATE_REASON_3)		//0x50010080;
	{ return "ICOM_TERMINATE_REASON_3"; }
	else if(tag == ICOM_TERMINATE_REASON_4)		//0x50010081;
	{ return "ICOM_TERMINATE_REASON_4"; }
	else if(tag == ICOM_RV_INHIBIT)				//0x70010050;
	{ return "ICOM_RV_INHIBIT"; }
	else
	{ return ""; }

	
	
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
std::string iCOMListen::getLinacState(short linacState)
{
	//À partir du short de la fonction iCOMGetState, on peut avoir la description de l'état de la machine.
	
	if(linacState == 1)
	{ return "PREPARATORY"; }
	else if(linacState == 2)
	{ return "CONFIRM SETTINGS"; }
	else if(linacState == 3)
	{ return "READY TO START"; }
	else if(linacState == 4)
	{ return "SEGMENT START"; }
	else if(linacState == 5)
	{ return "SEGMENT IRRADIATE"; }
	else if(linacState == 6)
	{ return "SEGMENT INTERRUPT"; }
	else if(linacState == 7)
	{ return "SEGMENT INTERRUPTED"; }
	else if(linacState == 8)
	{ return "SEGMENT RESTART"; }
	else if(linacState == 9)
	{ return "SEGMENT TERMINATE"; }
	else if(linacState == 10)
	{ return "SEGMENT PAUSE"; }
	else if(linacState == 11)
	{ return "FIELD TERMINATE"; }
	else if(linacState == 12)
	{ return "TERMINATE CHECKING"; }
	else if(linacState == 13)
	{ return "FIELD TERMINATED"; }
	else if(linacState == 14)
	{ return "MOVE ONLY"; }
	else if(linacState == -3)
	{ return "ERROR: INVALID_MESSAGE_HANDLE"; }
	else
	{ return "???"; }

}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
std::string iCOMListen::getLinacFunctionMode(short linacFunctionMode)  //Retourne le mode de fonctionnement du linac correspondant au chiffre (Service mode, etc.)
{
	//À partir du short de la fonction iCOMGetFunction, on peut avoir la description de du mode du linac (mode service, etc).
	
	if(linacFunctionMode == -1)
	{ return "Unknown Mode"; }
	else if(linacFunctionMode == 1)
	{ return "Premium Therapy Treatment"; }
	else if(linacFunctionMode == 3)
	{ return "Premium Check Radiograph"; }
	else if(linacFunctionMode == 5)
	{ return "Premium Finished Field"; }
	else if(linacFunctionMode == 8)
	{ return "Standard Therapy Treatment"; }
	else if(linacFunctionMode == 9)
	{ return "Receive External Prescription"; }
	else if(linacFunctionMode == 10)
	{ return "Service Mode"; }
	else if(linacFunctionMode == 255)
	{ return "Dans aucun Mode ?"; }
	else if(linacFunctionMode == -3)
	{ return "ERROR: INVALID_MESSAGE_HANDLE"; }
	else
	{ return "???"; }
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
std::string iCOMListen::getVirtualKey(short vk_Value)  //Retourne la virtual Key (touche de clavier) correspondante au chiffre
{
	//À partir du short de la fonction iCOMGetFunction, on peut avoir la description de du mode du linac (mode service, etc).
	
	if(vk_Value == 1) { return "Left mouse button"; }        //VK_LBUTTON
	else if(vk_Value == 2) { return "Right mouse button"; }        //VK_RBUTTON
	else if(vk_Value == 3) { return "Control-break (Ctrl+Pause)"; }        //VK_CANCEL
	else if(vk_Value == 4) { return "Middle mouse button"; }        //VK_MBUTTON
	else if(vk_Value == 5) { return "X1 mouse button"; }        //VK_XBUTTON1
	else if(vk_Value == 6) { return "X2 mouse button"; }        //VK_XBUTTON2
	else if(vk_Value == 7) { return "Undefined"; }        //-
	else if(vk_Value == 8) { return "BACKSPACE key"; }        //VK_BACK
	else if(vk_Value == 9) { return "TAB key"; }        //VK_TAB
	else if(vk_Value == 10 || vk_Value == 11) { return "Reserved"; }        //-
	else if(vk_Value == 12) { return "CLEAR key (Shift+Num5)"; }        //VK_CLEAR
	else if(vk_Value == 13) { return "ENTER key"; }        //VK_RETURN
	else if(vk_Value == 14 || vk_Value == 15) { return "Undefined"; }        //-
	else if(vk_Value == 16) { return "SHIFT key"; }        //VK_SHIFT
	else if(vk_Value == 17) { return "CTRL key"; }        //VK_CONTROL
	else if(vk_Value == 18) { return "ALT key"; }        //VK_MENU
	else if(vk_Value == 19) { return "PAUSE key"; }        //VK_PAUSE
	else if(vk_Value == 20) { return "CAPS LOCK key"; }        //VK_CAPITAL
	else if(vk_Value == 21) { return "IME Kana mode"; }        //VK_KANA
	//else if(vk_Value == 21) { return "IME Hanguel mode"; }        //VK_HANGUEL
	//else if(vk_Value == 21) { return "IME Hangul mode"; }        //VK_HANGUL
	else if(vk_Value == 22) { return "Undefined"; }        //-
	else if(vk_Value == 23) { return "IME Junja mode"; }        //VK_JUNJA
	else if(vk_Value == 24) { return "IME final mode"; }        //VK_FINAL
	else if(vk_Value == 25) { return "IME Kanji mode"; }        //VK_KANJI
	//else if(vk_Value == 25) { return "IME Hanja mode"; }        //VK_HANJA
	else if(vk_Value == 26) { return "Undefined"; }        //-
	else if(vk_Value == 27) { return "ESC key"; }        //VK_ESCAPE
	else if(vk_Value == 28) { return "IME convert"; }        //VK_CONVERT
	else if(vk_Value == 29) { return "IME nonconvert"; }        //VK_NONCONVERT
	else if(vk_Value == 30) { return "IME accept"; }        //VK_ACCEPT
	else if(vk_Value == 31) { return "IME mode change request"; }        //VK_MODECHANGE
	else if(vk_Value == 32) { return "SPACEBAR"; }        //VK_SPACE
	else if(vk_Value == 33) { return "PAGE UP key"; }        //VK_PRIOR
	else if(vk_Value == 34) { return "PAGE DOWN key"; }        //VK_NEXT
	else if(vk_Value == 35) { return "END key"; }        //VK_END
	else if(vk_Value == 36) { return "HOME key"; }        //VK_HOME
	else if(vk_Value == 37) { return "LEFT ARROW key"; }        //VK_LEFT
	else if(vk_Value == 38) { return "UP ARROW key"; }        //VK_UP
	else if(vk_Value == 39) { return "RIGHT ARROW key"; }        //VK_RIGHT
	else if(vk_Value == 40) { return "DOWN ARROW key"; }        //VK_DOWN
	else if(vk_Value == 41) { return "SELECT key"; }        //VK_SELECT
	else if(vk_Value == 42) { return "PRINT key"; }        //VK_PRINT
	else if(vk_Value == 43) { return "EXECUTE key"; }        //VK_EXECUTE
	else if(vk_Value == 44) { return "PRINT SCREEN key"; }        //VK_SNAPSHOT
	else if(vk_Value == 45) { return "INS key"; }        //VK_INSERT
	else if(vk_Value == 46) { return "DEL key"; }        //VK_DELETE
	else if(vk_Value == 47) { return "HELP key"; }        //VK_HELP
	else if(vk_Value == 48) { return "0 key"; }        //
	else if(vk_Value == 49) { return "1 key"; }        //
	else if(vk_Value == 50) { return "2 key"; }        //
	else if(vk_Value == 51) { return "3 key"; }        //
	else if(vk_Value == 52) { return "4 key"; }        //
	else if(vk_Value == 53) { return "5 key"; }        //
	else if(vk_Value == 54) { return "6 key"; }        //
	else if(vk_Value == 55) { return "7 key"; }        //
	else if(vk_Value == 56) { return "8 key"; }        //
	else if(vk_Value == 57) { return "9 key"; }        //
	else if(vk_Value >= 58 && vk_Value <= 64) { return "Undefined"; }        //
	else if(vk_Value == 65) { return "A key"; }        //
	else if(vk_Value == 66) { return "B key"; }        //
	else if(vk_Value == 67) { return "C key"; }        //
	else if(vk_Value == 68) { return "D key"; }        //
	else if(vk_Value == 69) { return "E key"; }        //
	else if(vk_Value == 70) { return "F key"; }        //
	else if(vk_Value == 71) { return "G key"; }        //
	else if(vk_Value == 72) { return "H key"; }        //
	else if(vk_Value == 73) { return "I key"; }        //
	else if(vk_Value == 74) { return "J key"; }        //
	else if(vk_Value == 75) { return "K key"; }        //
	else if(vk_Value == 76) { return "L key"; }        //
	else if(vk_Value == 77) { return "M key"; }        //
	else if(vk_Value == 78) { return "N key"; }        //
	else if(vk_Value == 79) { return "O key"; }        //
	else if(vk_Value == 80) { return "P key"; }        //
	else if(vk_Value == 81) { return "Q key"; }        //
	else if(vk_Value == 82) { return "R key"; }        //
	else if(vk_Value == 83) { return "S key"; }        //
	else if(vk_Value == 84) { return "T key"; }        //
	else if(vk_Value == 85) { return "U key"; }        //
	else if(vk_Value == 86) { return "V key"; }        //
	else if(vk_Value == 87) { return "W key"; }        //
	else if(vk_Value == 88) { return "X key"; }        //
	else if(vk_Value == 89) { return "Y key"; }        //
	else if(vk_Value == 90) { return "Z key"; }        //
	else if(vk_Value == 91) { return "Left Windows key"; }        //VK_LWIN
	else if(vk_Value == 92) { return "Right Windows key"; }        //VK_RWIN
	else if(vk_Value == 93) { return "Applications key"; }        //VK_APPS
	else if(vk_Value == 94) { return "Reserved"; }        //-
	else if(vk_Value == 95) { return "Computer Sleep key"; }        //VK_SLEEP
	else if(vk_Value == 96) { return "Numeric keypad 0 key"; }        //VK_NUMPAD0
	else if(vk_Value == 97) { return "Numeric keypad 1 key"; }        //VK_NUMPAD1
	else if(vk_Value == 98) { return "Numeric keypad 2 key"; }        //VK_NUMPAD2
	else if(vk_Value == 99) { return "Numeric keypad 3 key"; }        //VK_NUMPAD3
	else if(vk_Value == 100) { return "Numeric keypad 4 key"; }        //VK_NUMPAD4
	else if(vk_Value == 101) { return "Numeric keypad 5 key"; }        //VK_NUMPAD5
	else if(vk_Value == 102) { return "Numeric keypad 6 key"; }        //VK_NUMPAD6
	else if(vk_Value == 103) { return "Numeric keypad 7 key"; }        //VK_NUMPAD7
	else if(vk_Value == 104) { return "Numeric keypad 8 key"; }        //VK_NUMPAD8
	else if(vk_Value == 105) { return "Numeric keypad 9 key"; }        //VK_NUMPAD9
	else if(vk_Value == 106) { return "Multiply key"; }        //VK_MULTIPLY
	else if(vk_Value == 107) { return "Add key"; }        //VK_ADD
	else if(vk_Value == 108) { return "Separator key"; }        //VK_SEPARATOR
	else if(vk_Value == 109) { return "Subtract key"; }        //VK_SUBTRACT
	else if(vk_Value == 110) { return "Decimal key"; }        //VK_DECIMAL
	else if(vk_Value == 111) { return "Divide key"; }        //VK_DIVIDE
	else if(vk_Value == 112) { return "F1 key"; }        //VK_F1
	else if(vk_Value == 113) { return "F2 key"; }        //VK_F2
	else if(vk_Value == 114) { return "F3 key"; }        //VK_F3
	else if(vk_Value == 115) { return "F4 key"; }        //VK_F4
	else if(vk_Value == 116) { return "F5 key"; }        //VK_F5
	else if(vk_Value == 117) { return "F6 key"; }        //VK_F6
	else if(vk_Value == 118) { return "F7 key"; }        //VK_F7
	else if(vk_Value == 119) { return "F8 key"; }        //VK_F8
	else if(vk_Value == 120) { return "F9 key"; }        //VK_F9
	else if(vk_Value == 121) { return "F10 key"; }        //VK_F10
	else if(vk_Value == 122) { return "F11 key"; }        //VK_F11
	else if(vk_Value == 123) { return "F12 key"; }        //VK_F12
	else if(vk_Value == 124) { return "F13 key"; }        //VK_F13
	else if(vk_Value == 125) { return "F14 key"; }        //VK_F14
	else if(vk_Value == 126) { return "F15 key"; }        //VK_F15
	else if(vk_Value == 127) { return "F16 key"; }        //VK_F16
	else if(vk_Value == 128) { return "F17 key"; }        //VK_F17
	else if(vk_Value == 129) { return "F18 key"; }        //VK_F18
	else if(vk_Value == 130) { return "F19 key"; }        //VK_F19
	else if(vk_Value == 131) { return "F20 key"; }        //VK_F20
	else if(vk_Value == 132) { return "F21 key"; }        //VK_F21
	else if(vk_Value == 133) { return "F22 key"; }        //VK_F22
	else if(vk_Value == 134) { return "F23 key"; }        //VK_F23
	else if(vk_Value == 135) { return "F24 key"; }        //VK_F24
	else if(vk_Value >= 136 && vk_Value <= 143) { return "Unassigned"; }        //-
	else if(vk_Value == 144) { return "NUM LOCK key"; }        //VK_NUMLOCK
	else if(vk_Value == 145) { return "SCROLL LOCK key"; }        //VK_SCROLL
	else if(vk_Value == 146) { return "OEM specific"; }        //
	else if(vk_Value == 147) { return "OEM specific"; }        //
	else if(vk_Value == 148) { return "OEM specific"; }        //
	else if(vk_Value == 149) { return "OEM specific"; }        //
	else if(vk_Value == 150) { return "OEM specific"; }        //
	else if(vk_Value >= 151 && vk_Value <= 159) { return "Unassigned"; }        //-
	else if(vk_Value == 160) { return "Left SHIFT key"; }        //VK_LSHIFT
	else if(vk_Value == 161) { return "Right SHIFT key"; }        //VK_RSHIFT
	else if(vk_Value == 162) { return "Left CONTROL key"; }        //VK_LCONTROL
	else if(vk_Value == 163) { return "Right CONTROL key"; }        //VK_RCONTROL
	else if(vk_Value == 164) { return "Left MENU key"; }        //VK_LMENU
	else if(vk_Value == 165) { return "Right MENU key"; }        //VK_RMENU
	else if(vk_Value == 166) { return "Browser Back key"; }        //VK_BROWSER_BACK
	else if(vk_Value == 167) { return "Browser Forward key"; }        //VK_BROWSER_FORWARD
	else if(vk_Value == 168) { return "Browser Refresh key"; }        //VK_BROWSER_REFRESH
	else if(vk_Value == 169) { return "Browser Stop key"; }        //VK_BROWSER_STOP
	else if(vk_Value == 170) { return "Browser Search key"; }        //VK_BROWSER_SEARCH
	else if(vk_Value == 171) { return "Browser Favorites key"; }        //VK_BROWSER_FAVORITES
	else if(vk_Value == 172) { return "Browser Start and Home key"; }        //VK_BROWSER_HOME
	else if(vk_Value == 173) { return "Volume Mute key"; }        //VK_VOLUME_MUTE
	else if(vk_Value == 174) { return "Volume Down key"; }        //VK_VOLUME_DOWN
	else if(vk_Value == 175) { return "Volume Up key"; }        //VK_VOLUME_UP
	else if(vk_Value == 176) { return "Next Track key"; }        //VK_MEDIA_NEXT_TRACK
	else if(vk_Value == 177) { return "Previous Track key"; }        //VK_MEDIA_PREV_TRACK
	else if(vk_Value == 178) { return "Stop Media key"; }        //VK_MEDIA_STOP
	else if(vk_Value == 179) { return "Play/Pause Media key"; }        //VK_MEDIA_PLAY_PAUSE
	else if(vk_Value == 180) { return "Start Mail key"; }        //VK_LAUNCH_MAIL
	else if(vk_Value == 181) { return "Select Media key"; }        //VK_LAUNCH_MEDIA_SELECT
	else if(vk_Value == 182) { return "Start Application 1 key"; }        //VK_LAUNCH_APP1
	else if(vk_Value == 183) { return "Start Application 2 key"; }        //VK_LAUNCH_APP2
	else if(vk_Value == 184) { return "Reserved"; }        //-
	else if(vk_Value == 185) { return "Reserved"; }        //-
	else if(vk_Value == 186) { return "Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the ';:' key"; }        //VK_OEM_1
	else if(vk_Value == 187) { return "For any country/region, the '+' key"; }        //VK_OEM_PLUS
	else if(vk_Value == 188) { return "For any country/region, the ',' key"; }        //VK_OEM_COMMA
	else if(vk_Value == 189) { return "For any country/region, the '-' key"; }        //VK_OEM_MINUS
	else if(vk_Value == 190) { return "For any country/region, the '.' key"; }        //VK_OEM_PERIOD
	else if(vk_Value == 191) { return "Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the '/?' key"; }        //VK_OEM_2
	else if(vk_Value == 192) { return "Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the '`~' key"; }        //VK_OEM_3
	else if(vk_Value >= 193 && vk_Value <= 215) { return "Reserved"; }        //-
	else if(vk_Value >= 216 && vk_Value <= 218) { return "Unassigned"; }        //-
	else if(vk_Value == 219) { return "Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the '[{' key"; }        //VK_OEM_4
	else if(vk_Value == 220) { return "Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the '\\|' key"; }        //VK_OEM_5
	else if(vk_Value == 221) { return "Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the ']}' key"; }        //VK_OEM_6
	else if(vk_Value == 222) { return "Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the 'single-quote/double-quote' key"; }        //VK_OEM_7
	else if(vk_Value == 223) { return "Used for miscellaneous characters; it can vary by keyboard."; }        //VK_OEM_8
	else if(vk_Value == 224) { return "Reserved"; }        //-
	else if(vk_Value == 225) { return "OEM specific"; }        //
	else if(vk_Value == 226) { return "Either the angle bracket key or the backslash key on the RT 102-key keyboard"; }        //VK_OEM_102
	else if(vk_Value == 227 || vk_Value == 228) { return "OEM specific"; }        //
	else if(vk_Value == 229) { return "IME PROCESS key"; }        //VK_PROCESSKEY
	else if(vk_Value == 230) { return "OEM specific"; }        //
	else if(vk_Value == 231) { return "Used to pass Unicode characters as if they were keystrokes."; }        //VK_PACKET
	else if(vk_Value == 232) { return "Unassigned"; }        //-
	else if(vk_Value == 233) { return "OEM specific"; }        //
	else if(vk_Value == 246) { return "Attn key"; }        //VK_ATTN
	else if(vk_Value == 247) { return "CrSel key"; }        //VK_CRSEL
	else if(vk_Value == 248) { return "ExSel key"; }        //VK_EXSEL
	else if(vk_Value == 249) { return "Erase EOF key"; }        //VK_EREOF
	else if(vk_Value == 250) { return "Play key"; }        //VK_PLAY
	else if(vk_Value == 251) { return "Zoom key"; }        //VK_ZOOM
	else if(vk_Value == 252) { return "Reserved for future use"; }        //VK_NONAME
	else if(vk_Value == 253) { return "PA1 key"; }        //VK_PA1
	else if(vk_Value == 254) { return "Clear key"; }        //VK_OEM_CLEAR
	else { return "???"; }
}

////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
bool iCOMListen::triggerTrigerred(std::vector<trigger>* triggerList)
{
	//
	bool triggerred = false;
	int size =  triggerList->size();
	char* newValue;
	short newLinacState = 0;
	short newLinacFunctionMode = 0;
	int i = 0;
	
	//Getting new linac state
	newLinacState = iCOMGetState(hICOMMsg);
	newLinacFunctionMode = iCOMGetFunction(hICOMMsg);
	
	ICOMResult iSize;


	if(size > 0)
	{
		for(i =0; i< size; i++)
		{
			
			if((*triggerList)[i].triggerType == 0)	//iCOMtag trigger
			{
				//Getting new iCOMtag Value
				iSize = iCOMGetTagValue(hICOMMsg, (*triggerList)[i].tag.tag,(*triggerList)[i].tag.part, NULL);
				newValue = new char[iSize+1];
				
				if(iSize > 0)
				{
					iCOMResult = iCOMGetTagValue(hICOMMsg,(*triggerList)[i].tag.tag, (*triggerList)[i].tag.part, newValue);
					
					//On assume que si la valeur est NULL, c'est juste que le tag n'est pas apparu cette fois-ci. Trigger pas activé.
					if( newValue == NULL)
					{
						delete[] newValue;
						continue;
					}
				}
				else	//Si la valeur est vide ou NULL, pas de trigger
				{
					iCOMResult = iSize;
					delete[] newValue;
					continue;
					//print_error_iCOMResult("iCOMGetTagValue (buffersize)");
				}

						
				//Comparing new value with stored one
				if((*triggerList)[i].trigOnValueChange == true)
				{
					
					if(strcmp(newValue, (*triggerList)[i].value) != 0)
					{
						triggerred = true;
						delete[] newValue;
						break;
					}
				}
				else //((*triggerList)[i].trigOnValueChange == false)
				{
					
					if(strcmp(newValue, (*triggerList)[i].value) == 0)
					{
						triggerred = true;
						delete[] newValue;
						break;
					}
				}
				
				delete[] newValue;

			}
			else if((*triggerList)[i].triggerType == 1)  //linac state trigger
			{
				if((*triggerList)[i].trigOnValueChange == true)
				{
					if(newLinacState != (*triggerList)[i].linacState)
					{
						triggerred = true;
						break;
					}					
				}
				else //((*triggerList)[i].trigOnValueChange == false)
				{
					if(newLinacState == (*triggerList)[i].linacState)
					{
						triggerred = true;
						break;
					}
				}
			}			
			else if((*triggerList)[i].triggerType == 2)  //linac Function Mode
			{
				if((*triggerList)[i].trigOnValueChange == true)
				{
					if(newLinacFunctionMode != (*triggerList)[i].linacState)
					{
						triggerred = true;
						break;
					}					
				}
				else //((*triggerList)[i].trigOnValueChange == false)
				{
					if(newLinacFunctionMode == (*triggerList)[i].linacState)
					{
						triggerred = true;
						break;
					}
				}
			}			
			else if((*triggerList)[i].triggerType == 3)  //Trigger avec les touches du clavier
			{
				//VK_ESCAPE = 0x1B
				if(GetAsyncKeyState((*triggerList)[i].linacState) != 0) //GetAsyncKeyState est une fonction de Windows.h égal à 0 si personne n'y touche / a touché
				{
					triggerred = true;
					if(debug > 1)
					{
						(*debug_file) <<  "iCOMListen::triggerTrigerred : \""<< getVirtualKey((*triggerList)[i].linacState) << "\" Button pressed !" << std::endl;
					}
					break;
				}
			}			
			else
			{
				(*debug_file) << "Error in iCOMListen::triggerTrigerred : unknown trigger mode = " << (*triggerList)[i].triggerType << std::endl; //test !!!!!!!!!!!!!!!!!!
			}			
		}
	}
	
	if(triggerred == true)
	{
		//Updating trigger change values
		updateTriggerListsCurrent();
		
		if(debug > 1)
		{
			(*debug_file) <<  "iCOMListen::triggerTrigerred : A trigger have been triggered :";
			print_trigger((*triggerList)[i], debug_file);
			(*debug_file) << "\t\t--> iCOMmsg_index : " <<  iCOMmsg_index << std::endl;
			(*debug_file) << "\t\t--> iView->G_image_index : " <<  G_image_index << std::endl;            
		}
		
	}
	
	
	return triggerred;
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void  iCOMListen::updateTriggerListsCurrent()	//Update les valeurs qui trig avec le changement pour les valeurs actuelles
{
		updateTriggerListCurrent(&startTriggers);
		updateTriggerListCurrent(&pauseTriggers);
		updateTriggerListCurrent(&stopTriggers);
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void  iCOMListen::updateTriggerListCurrent(std::vector<trigger>* triggerList)	//Update les valeurs qui trig avec le changement pour les valeurs actuelles
{
	//Getting new linac state
	short newLinacState = iCOMGetState(hICOMMsg);
	short newLinacFunctionMode = iCOMGetFunction(hICOMMsg);
	int i = 0;
	char* newValue;
	ICOMResult iSize;

	int size =  triggerList->size();
	
	for(i = 0; i< size; i++)
	{
		if((*triggerList)[i].trigOnValueChange == true)
		{
			if((*triggerList)[i].triggerType == 0)  //iCOMtag trigger
			{	
				//Getting new iCOMtag Value
				iSize = iCOMGetTagValue(hICOMMsg, (*triggerList)[i].tag.tag, (*triggerList)[i].tag.part, NULL);
				newValue = new char[iSize+1];
				
				if(iSize > 0)
				{
					iCOMResult = iCOMGetTagValue(hICOMMsg,(*triggerList)[i].tag.tag, (*triggerList)[i].tag.part, newValue);

					//On assume que si la valeur est NULL, c'est juste que le tag n'est pas apparu cette fois-ci. Trigger pas activé.
					if( newValue == NULL )
					{
						delete[] newValue;
						continue;
					}
					else
					{
						(*triggerList)[i].value = newValue;
					}
				}
				else
				{
					iCOMResult = iSize;
					//print_error_iCOMResult("iCOMGetTagValue (buffersize)");
				}

			}
			else if((*triggerList)[i].triggerType == 1)  //linac state trigger
			{
				(*triggerList)[i].linacState = newLinacState;
			}
			else if((*triggerList)[i].triggerType ==2)  //linac FunctionMode trigger
			{
				(*triggerList)[i].linacState = newLinacFunctionMode;
			}
		}
	}
	
	
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
bool iCOMListen::create_directory(std::string path)
{
	if (CreateDirectory(path.c_str(), NULL) || ERROR_ALREADY_EXISTS == GetLastError())
	{
		if(debug > 3)
		{
			if(ERROR_ALREADY_EXISTS == GetLastError())
			{
				(*debug_file) << path << " Already exists." << std::endl;
			}
			else
			{
				(*debug_file) << path << " was created." << std::endl;
			}
		}

		return true;
	}
	else
	{
		(*debug_file) << "Error in iCOMListen::create_directory : userSelectedPath folder could not be created." << std::endl;
		return false;
	}
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
bool iCOMListen::DirectoryExists(const char* szPath)		//fonction Windows seulement
{
	DWORD dwAttrib = GetFileAttributes((LPCTSTR)szPath);	//LPCTSTR is a const char*

	return (dwAttrib != INVALID_FILE_ATTRIBUTES && (dwAttrib & FILE_ATTRIBUTE_DIRECTORY));
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
int iCOMListen::get_iCOMmsg_index_from_sequence_detail_file(std::string the_sequence_detail_path_name) //retourne le dernuméro d'index présent dans le fichier de résumé
{
	
	//On vérifie si le fichier existe en tentant de l'ouvrir ******Tenter de faire ça plus propre plus tard*********
	sequence_detail_file =  fopen(the_sequence_detail_path_name.c_str(),"r");	//Ouverture en read
	if(sequence_detail_file == NULL) //File doesn<t exists
	{
		return 0;
	}
	fclose(sequence_detail_file);
	

	int next_image_index = 0;  //L'index de la prochaine image dont on veut faire l'acquisition
	
	std::ifstream myfile(the_sequence_detail_path_name);
	std::string line = "";
	int index_found = 0;
	
	if( myfile.is_open() )
	{
		//On loop sur toutes les lignes
		while(std::getline(myfile, line))
		{
			//Si c'est la ligne indiquant le numéro de l'image (pas de ":" au début, donc pas un tag, et une "," après 5 caractères)
			if((line.find(":") != 0) && line.find(",") == 5)
			{
				index_found = (int)( atol(line.substr(0,5).c_str()) );               

				if(index_found >= next_image_index)
				{
					next_image_index = index_found+1;
				}
				
			}

		}
		
		if(debug > 0)
		{
			(*debug_file) << "iCOMListen::get_iCOMmsg_index_from_sequence_detail_file : Sequence_detail found, starting acquisition index at : " << next_image_index << std::endl;
		}
	}
	else
	{
		if(debug > 1)
		{
			(*debug_file) << "iCOMListen::get_iCOMmsg_index_from_sequence_detail_file : Sequence_detail not found (path= " << the_sequence_detail_path_name << " ), starting index at 0" << std::endl;
		}
	}
	
	return next_image_index;
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
std::string iCOMListen::getTimeDateString()
{
	return getTimeDateString(false);
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
std::string iCOMListen::getTimeDateString(bool date_only)
{
	std::string datetimestr = "";
	
	std::time_t t = time(0);   // get time now
	struct tm * now = localtime( & t );
	
	
	datetimestr = patch::to_string(now->tm_year + 1900) + "-";
	
	if(now->tm_mon + 1 < 10)
	{
		datetimestr = datetimestr + "0";
	}
	
	datetimestr = datetimestr + patch::to_string(now->tm_mon + 1) + "-";
	
	if(now->tm_mday < 10)
	{
		datetimestr = datetimestr + "0";
	}
	
	datetimestr = datetimestr + patch::to_string(now->tm_mday);
	
	if(date_only == false)
	{
		datetimestr = datetimestr + "_";
		
		if(now->tm_hour + 1 < 10)
		{
			datetimestr = datetimestr + "0";
		}
		
		datetimestr = datetimestr + patch::to_string(1 + now->tm_hour) + "-";
		
		if(now->tm_min < 10)
		{
			datetimestr = datetimestr + "0";
		}
		
		datetimestr = datetimestr + patch::to_string(now->tm_min) + "-";
		
		if(now->tm_sec < 10)
		{
			datetimestr = datetimestr + "0";
		}
		
		datetimestr = datetimestr + patch::to_string(now->tm_sec);
	}
	
	return datetimestr;
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iCOMListen::print_trigger(trigger a_trigger, std::ofstream *file)
{
	if(a_trigger.triggerType == 0) //iCOMtag
	{
		(*file) << "trigger : Tag : {" << a_trigger.tag.tag << "," << a_trigger.tag.part << "}, value :" << a_trigger.value << " , value change : " << a_trigger.trigOnValueChange << std::endl;
	}
	else	if(a_trigger.triggerType == 1)//linac State
	{
		(*file) << "trigger : Linac State : " << a_trigger.linacState << " (" << getLinacState(a_trigger.linacState) << ") , value change : " << a_trigger.trigOnValueChange << std::endl;
	}
	else if(a_trigger.triggerType == 2)//linac Function Mode
	{
		(*file) << "trigger : Linac Function Mode : " << a_trigger.linacState << " (" << getLinacFunctionMode(a_trigger.linacState) << ") , value change : " << a_trigger.trigOnValueChange << std::endl;
	}
	else if(a_trigger.triggerType == 3)//Keyboard Key trigger
	{
		(*file) << "trigger : Keyboard Key Mode : " << a_trigger.linacState <<   ", Corresponds to virtual Key : "  << getVirtualKey(a_trigger.linacState) << std::endl;     // " , value change : " << a_trigger.trigOnValueChange << std::endl;
	}
	else
	{
		(*file) << "trigger : Trigger Type unknown : triggerType=" << a_trigger.triggerType << std::endl;     // " , value change : " << a_trigger.trigOnValueChange << std::endl;
	}

}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iCOMListen::FonctionTest() //Existe pour tester des fonction seulement dans le cadre de la programation NT
{
	int int_test = -1;
	std::string str_test = "";
	
	std::string filepath = "C:\\Sources\\iCom_iView\\acq_detail.txt";
	
	std::cout << std::endl << "iCOMListen::FonctionTest()" << std::endl << std::endl;
	
	int_test = get_iCOMmsg_index_from_sequence_detail_file(filepath);
	
	std::cout << std::endl << "iCOMListen::FonctionTest : int_test = " << int_test << std::endl << std::endl;


	
	//cin >> str_test;
	
}

