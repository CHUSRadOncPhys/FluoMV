///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
// iViewControl.cpp
//   (C) 2019 by Nicolas Tremblay <nmtremblay.chus@ssss.gouv.qc.ca>
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////

#include "iViewControl.h"

//////////////////////////////////////////////////////////////////////////////
//Variables globales nécessaires auc fonctions d'acquisition et de fin de séquences
//Définies dans iViewControl.cpp
//////////////////////////////////////////////////////////////////////////////

bool G_save_images_acquired;
bool G_stop_acquisition;
unsigned int* G_image_index;
unsigned short* G_pAcqBuffer;
unsigned int G_nbrPixelsBuffer;     //Nombre de pixels dans le Buffer (nbrPixelsImage*nbrImageBuffer)

FILE* G_sequence_detail_file;
std::ofstream* G_iView_debug_file;

std::string G_image_path_name;

BetterTimestamp* G_horloge_iView;

//char G_image_path_name_with_index[150];
std::string G_sequence_detail_path_name;



////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
//Fonction exécutée automatiquement lorsqu'une nouvelle image est attrappée par le frame grabber.
void CALLBACK OnEndFrameCallback(HACQDESC hAcqDesc)
{
	
	const unsigned short IRRADIATE_THRESHOLD = 15000;
	unsigned short error_pixel_value = 0;
	bool eletronic_irradiate_warning = false;
	
	//On prend le temps en premier
	uint64_t milliseconds_since_epoch;
	//milliseconds_since_epoch = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count();
	milliseconds_since_epoch = G_horloge_iView->now();
 
    //(*G_iView_debug_file) << "Debug iVew Timestamp" << std::endl;
  	
	unsigned int winapi;
	
	//
	char image_path_name_with_index[150];
	FILE* image_file;
	
	winapi = Acquisition_SetReady(hAcqDesc, false);
	
	if(G_save_images_acquired == true)
	{
		//mettre l'index de l'image dans le nom du fichier de l'image
		sprintf(image_path_name_with_index, G_image_path_name.c_str(), (*G_image_index));
		
		//winapi = Acquisition_GetActFrame(hAcqDesc, &dwActAcqFrame, &dwActBuffFrame);
		//print_error_winapi("Acquisition_GetActFrame");

		//On écrit ce nom de fichier dans le résumé de la séquence
		G_sequence_detail_file =  fopen(G_sequence_detail_path_name.c_str(),"a");
		fprintf(G_sequence_detail_file, "%05u,%I64u\n", (*G_image_index), milliseconds_since_epoch);
		fclose(G_sequence_detail_file);
		//fprintf(G_sequence_detail_file, "%05u,%s,%d, %d \n", (*G_image_index), milliseconds_since_epoch, dwActAcqFrame, dwActBuffFrame);
		//Ouverture du fichier binaire
		image_file = fopen(image_path_name_with_index, "wb");
		
		//Écriture du buffer dans le fichier
		fwrite(G_pAcqBuffer, G_nbrPixelsBuffer*sizeof(unsigned short), 1, image_file);
		  
		//fermeture du fichier
		fclose(image_file);
		
		//Vérification qu'on irradie pas dans l'électronique
		//On assume le 1024 pixels par simplicité ici
		for(unsigned int i=5138; i<6144; i+=32)  //cinquième ligne et cinquième avant dernière ligne.
		{
			if(G_pAcqBuffer[i] > IRRADIATE_THRESHOLD)
			{ 
				eletronic_irradiate_warning = true;
				error_pixel_value = G_pAcqBuffer[i];
				break;
			}
			else if(G_pAcqBuffer[i+1042432] > IRRADIATE_THRESHOLD)
			{
				eletronic_irradiate_warning = true;
				error_pixel_value = G_pAcqBuffer[i+1042432];
				break;
			}
		}
		
		for(unsigned int i = 5124; i < 1043456; i+=32768) //cinquième colone et cinquième avant dernière colone.
		{
			if(G_pAcqBuffer[i] > IRRADIATE_THRESHOLD)
			{ 
				eletronic_irradiate_warning = true;
				error_pixel_value = G_pAcqBuffer[i];
				break;
			}
			else if(G_pAcqBuffer[i+1014] > IRRADIATE_THRESHOLD)
			{
				eletronic_irradiate_warning = true;
				error_pixel_value = G_pAcqBuffer[i+1014];
				break;
			}
		}
		
		if( eletronic_irradiate_warning == true )
		{
			(*G_iView_debug_file) << "**************************************************" << std::endl;
			(*G_iView_debug_file) << "WARNING !!! Risque d'irradiation de l'electronique du panneau de l'appareil !!!" << std::endl;
			(*G_iView_debug_file) << "Frame # : " << (*G_image_index) << std::endl;            
			(*G_iView_debug_file) << "Pixel value : " << error_pixel_value << std::endl;
			(*G_iView_debug_file) << "Threshold value : " << IRRADIATE_THRESHOLD << std::endl;
			(*G_iView_debug_file) << "**************************************************" << std::endl << std::endl;
 
			std::cout << "**************************************************" << std::endl;
			std::cout << "WARNING !!! Risque d'irradiation de l'electronique du panneau de l'appareil !!!" << std::endl;
			std::cout << "Frame # : " << (*G_image_index) << std::endl;            
			std::cout << "Pixel value : " << error_pixel_value << std::endl;
			std::cout << "Threshold value : " << IRRADIATE_THRESHOLD << std::endl;
			std::cout << "**************************************************" << std::endl << std::endl;
		}
		
		
		//Incrément du nombre d'images
		(*G_image_index)++;

	}
	else
	{
		//std::cout << "On enregistre pas" << std::endl;
	}
	
	if(G_stop_acquisition == true)
	{
		(*G_iView_debug_file) << "Fin de l'acquisition." << std::endl;
		G_save_images_acquired =  false;
		
		G_sequence_detail_file =  fopen(G_sequence_detail_path_name.c_str(),"a");
		fprintf(G_sequence_detail_file, "\n");		//Ajout d'un retour de ligne à la fin du document
		fclose(G_sequence_detail_file);
		
		//********test pas sûr si nécessaire ici
		winapi = Acquisition_SetReady(hAcqDesc, true);
		
		//On arrête l'acquisition  et ferme le fichier de résumé (mais on ne ferme pas la liaison avec le paneau)
		//winapi = Acquisition_Abort(hAcqDesc);
		
		if(winapi != 0)
		{
			(*G_iView_debug_file) << "ERROR in iViewControl OnEndFrameCallback (CALLBACK): Acquisition_Abort failed -> winapi = " << winapi << std::endl;
		}
		
	}
	else
	{
		//On est prêt à attendre un nouvelle image.
		winapi = Acquisition_SetReady(hAcqDesc, true);
	}
	
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
//Fonction exécutée automatiquement à la fin d'une acquisition
void CALLBACK  OnEndAcqCallback(HACQDESC hh)
{
		(*G_iView_debug_file) << "iViewControl OnEndAcqCallback (CALLBACK) : Séquence terminée !!!!!" << std::endl;
	
	
	
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
iViewControl::iViewControl()
{
	G_iView_debug_file = new std::ofstream("debug_iViewControl.txt");
    debug_file = G_iView_debug_file;
	//Par défaut debug = 0
	initialize_iViewControl(0,0);
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
iViewControl::iViewControl(short debugValue)
{
	G_iView_debug_file = new std::ofstream("debug_iViewControl.txt");
    debug_file = G_iView_debug_file;
	//Par défaut debug = 0
	initialize_iViewControl(debugValue,0);
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
iViewControl::iViewControl(short debugValue, short TimestampType)
{
	G_iView_debug_file = new std::ofstream("debug_iViewControl.txt");
    debug_file = G_iView_debug_file;
    
    initialize_iViewControl(debugValue,TimestampType);
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
iViewControl::~iViewControl()
{
	//Fermeture du fichier de debug
	if(hAcqDesc != NULL)
	{
		winapi = Acquisition_Close(hAcqDesc);
		print_error_winapi("Acquisition_Close");
	}
	
	hAcqDesc = NULL;

	if(debug > 1)
	{
		(*debug_file) << "iViewControl::~iViewControl : Deleting" << std::endl;
	}
	
	delete G_image_index;
	if(G_horloge_iView != NULL)
	{
		delete G_horloge_iView;
	}
	
	//Suppression des autres pointeurs et allocation de mémoire.
	free(G_pAcqBuffer);  //malloc, pas d'utilisation du "new" donc pas de "delete"

	//clear vectors
	errornames.clear();
	errordescription.clear();

	if(debug > 1)
	{
		(*debug_file) << "iViewControl::~iViewControl : All deleted. Closing debug file." << std::endl;
	}
		
	debug_file->close();
	delete debug_file;
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iViewControl::SetDebug(short debugValue)
{
	debug = debugValue; //0 No debug, 1 debug, 2 debug detail.
	(*debug_file) << "iViewControl::SetDebug : changing debug to " << debugValue << std::endl;
    
    if(G_horloge_iView != NULL)
	{
		G_horloge_iView->SetDebug(debugValue);
	}
    
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iViewControl::SetTimestampType(short Type)
{
    if(debug > 0)
    {
        (*debug_file) << "iViewControl::SetTimestampType : Changing Timestamp type to : " << Type << std::endl;
    }
    
    if(G_horloge_iView != NULL)
	{
		G_horloge_iView->SetTimestampType(Type);
	}
    
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
unsigned int iViewControl::InitializePanel()		//Connecte au paneau et initialise certains paramètres. 
{
	//Définition des parmètres pour l'initialisation du panneau.
	//hAcqDesc parameter set
	DWORD dwBoardType = 1;		            //1 pour "Squirrel Frame grabber"
	int nChannelNr = 0;				            //channel ID 0 (Infinity1 en tout cas)
	bool bEnableIRQ = true;		            //Polling mode = true pour permettre les Interrupts
	unsigned int dwRows = nbrRows;
	unsigned int dwColumns = nbrColumns;
	unsigned int dwSortFlags = 0x8;		//Paneau XRD 1640
	unsigned int winapiInit = 0;
	bool bSelfInit = true;
	bool bInitAlways = false;		            //bAlwaysOpen
	DWORD dwMode;
	
	if(debug > 0)
	{
		(*debug_file) << "iViewControl::InitializePanel : Initializing panel" << std::endl;
		
		if(debug > 1)
		{
			(*debug_file) << "\tdwBoardType : " << dwBoardType << std::endl;
			(*debug_file) << "\tnChannelNr : " << nChannelNr << std::endl;
			(*debug_file) << "\tbEnableIRQ : " << bEnableIRQ << std::endl;
			(*debug_file) << "\tdwRows : " << dwRows << std::endl;
			(*debug_file) << "\tdwColumns : " << dwColumns << std::endl;
			(*debug_file) << "\tdwSortFlags : " << dwSortFlags << std::endl;
			(*debug_file) << "\tbSelfInit : " << bSelfInit << std::endl;
			(*debug_file) << "\tbInitAlways : " << bInitAlways << std::endl;
		}
	}

	//Fonction d'intialisation du paneau XISL
	winapi = Acquisition_Init( &hAcqDesc, dwBoardType, nChannelNr, bEnableIRQ, dwRows, dwColumns, dwSortFlags, bSelfInit, bInitAlways);
	print_error_winapi("Acquisition_Init");
	winapiInit = winapi;
	
	//En cas du code d'erreur typique quand on lance le logiciel d'un ordi qui n'est pas celui du iView
	if(winapi == HIS_ERROR_LOADDRIVER)
	{
		(*debug_file) << "***Pas de paneau ?? Je gage que tu n'es pas sur iView ?." << std::endl;
		return winapiInit;
		//exit(1);
	}

	if (debug > 0)
	{	
		(*debug_file) << "Is acquiring data : " << Acquisition_IsAcquiringData(hAcqDesc) << std::endl;
	}
	if (debug > 1)
	{	
		unsigned int *pdwChannelType = new unsigned int(); //0= No device (not valid), 1 = PcEye3 or Squirrel Frame Grabber, 3 = serial interfaced based RS232
		int *pnChannelNr = new int();
		
		winapi = Acquisition_GetCommChannel(hAcqDesc, pdwChannelType, pnChannelNr);
		(*debug_file) << "iViewControl::InitializePanel : Acquisition_GetCommChannel : \n\t\tpdwChannelType=" << (*pdwChannelType) << " , pnChannelNr=" << (*pnChannelNr) << std::endl;
		
		print_error_winapi("Acquisition_GetCommChannel");
		
		delete pdwChannelType;
		delete pnChannelNr;
	}


	//Pour obtenir plus d'informations du iView pour aider à comprendre XISL, on demande le header
	winapi = Acquisition_GetHwHeaderInfo(hAcqDesc, &chwHeaderInfo);
	
	if(debug > 0)
	{
		PrintHeaderInfo(debug_file);
	}

	//Assignation du nombre de lignes et colones à partir des données du paneau (ne devrait pas changer mais on le fait pareil).
	nbrRows = chwHeaderInfo.dwNrRows;
	nbrColumns = chwHeaderInfo.dwNrColumns;
	update_buffer_parameters();
	
	
	if (debug > 0)
	{
		(*debug_file) << "Setting FrameSyncMode" << std::endl;
	}

	//Choix du mode d'Acquisition
	
	//HIS_SYNCMODE_FREE_RUNNING = 4
	//HIS_SYNCMODE_INTERNAL_TIMER = 2
	//HIS_SYNCMODE_EXTERNAL_TRIGGER = 3
	//HIS_SYNCMODE_SOFT_TRIGGER = 1
	dwMode = HIS_SYNCMODE_FREE_RUNNING;

	winapi = Acquisition_SetFrameSyncMode(hAcqDesc, dwMode);
	print_error_winapi("Acquisition_SetFrameSyncMode");
	if (debug > 0)
	{
		(*debug_file) << "Acquisition_SetFrameSyncMode : " << dwMode << std::endl;
	}

	//Impression de divers paramètres d'acquisition.
	if(debug > 1)
	{
		print_acquisition_param();
	}

	//Avoir le Handle Windows
	winapi = Acquisition_GetWinHandle(hAcqDesc, &hWhd);
	print_error_winapi("Acquisition_GetWinHandle");
	
	//Messages d'erreur à poster à hWnd si une erreur survient durant l'acquisition, ou si on skip une image.
	UINT dwErrorMsg = 100;
	UINT dwLoosingFramesMsg = 1000;
	
	//Set Callbacks *************à tester**************
	winapi = Acquisition_SetCallbacksAndMessages(hAcqDesc, hWhd, dwErrorMsg, dwLoosingFramesMsg,&OnEndFrameCallback,&OnEndAcqCallback);
	print_error_winapi("Acquisition_SetCallbacksAndMessages");

	//Pour obtenir les temps d'intégration possible du panneau
	if(debug > 1)
	{
		double dblIntTmes[8];
		int nIntTimes = 8;
		
		winapi = Acquisition_GetIntTimes(hAcqDesc, dblIntTmes, &nIntTimes);
		print_error_winapi("Acquisition_GetIntTimes");
		
		(*debug_file) << "Number of available integration times : " << nIntTimes << std::endl;
		
		for(int i = 0; i<nIntTimes; i++)
		{
			(*debug_file) << i << "    : " << dblIntTmes[i]  << std::endl;
		}
	}
	
	
	//Valeur de l'initialisation pour la gestion d'erreur
	return winapiInit;
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iViewControl::ClosePanel()
{
	//Ferme l'acquisition courante
	if (debug > 0)
	{	(*debug_file) << "iViewControl::ClosePanel : Closing all Acquisitions." << std::endl;	}

	if (debug > 1)
	{	
		unsigned int *pdwChannelType = new unsigned int(); //0= No device (not valid), 1 = PcEye3 or Squirrel Frame Grabber, 3 = serial interfaced based RS232
		int *pnChannelNr = new int();
		
		winapi = Acquisition_GetCommChannel(hAcqDesc, pdwChannelType, pnChannelNr);
		(*debug_file) << "iViewControl::ClosePanel : Acquisition_GetCommChannel : \n\t\tpdwChannelType=" << (*pdwChannelType) << " , pnChannelNr=" << (*pnChannelNr) << std::endl;
		
		print_error_winapi("Acquisition_GetCommChannel");
		
		delete pdwChannelType;
		delete pnChannelNr;
		
		//(*debug_file) << "Is acquiring data : " << Acquisition_IsAcquiringData(hAcqDesc) << std::endl;
	}

	
	if(Acquisition_IsAcquiringData(hAcqDesc) == true)
	{
		if(debug > 0)
		{
			(*debug_file) << "iViewControl::ClosePanel : Data still in acquisition. Doing Acquisition_Abort" << std::endl;
		}
		try
		{
			winapi = Acquisition_Abort(hAcqDesc);
		}
		catch(...)
		{ 
			(*debug_file) << "\tiViewControl::ClosePanel : Acquisition_Abort failed (!?!)" << std::endl;
		}
		print_error_winapi("Acquisition_Abort");
	}
	
	//Fermeture du paneau XISL
	if(hAcqDesc != NULL)
	{
		try
		{
			winapi = Acquisition_Close(hAcqDesc);
			print_error_winapi("Acquisition_Close");
		}
		catch(...)
		{ 
			(*debug_file) << "iViewControl::ClosePanel : la fonction Aqcuisition_Close a fait une erreur." << std::endl;
			if (debug > 1)
			{	
				unsigned int *pdwChannelType = new unsigned int(); //0= No device (not valid), 1 = PcEye3 or Squirrel Frame Grabber, 3 = serial interfaced based RS232
				int *pnChannelNr = new int();
				
				winapi = Acquisition_GetCommChannel(hAcqDesc, pdwChannelType, pnChannelNr);
				(*debug_file) << "iViewControl::ClosePanel : Acquisition_GetCommChannel : \n\t\tpdwChannelType=" << (*pdwChannelType) << " , pnChannelNr=" << (*pnChannelNr) << std::endl;
				
				print_error_winapi("Acquisition_GetCommChannel");
				
				delete pdwChannelType;
				delete pnChannelNr;
			}
		}
	}
	else
	{
		(*debug_file) << "iViewControl::ClosePanel : Panneau semblait déjà fermé. on skip la fonction Acquisition_Close." << std::endl;
	}
	
	hAcqDesc = NULL;

	//Pour fermer toutes les acquisitions d'un coup.
	//winapi = Acquisition_CloseAll();
	//print_error_winapi("Acquisition_CloseAll");

}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iViewControl::AcquireImage(unsigned int nbrImage)
{
	unsigned int stopIndex = (*G_image_index) + nbrImage;
	
	if(Acquisition_IsAcquiringData(hAcqDesc) == true)
	{
		(*debug_file) << "Error in iViewControl::AcquireImage : Already in acquiring. Acquisition not started." << std::endl;
	}

	//On part l'acquisition
	StartAcquireContinuous();
	
	//Tnat que le nombre d'images visé n'a pas été atteint, on attend
	while((*G_image_index) <= stopIndex)
	{
		Sleep(200);
	}
	
	//Fin de l'acquisition.
	StopAcquireContinuous();
	
}

	

////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iViewControl::StartAcquireContinuous()
{
	StartAcquireContinuous(false);
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iViewControl::StartAcquireContinuous(bool StartOnPause)
{
	if(debug > 0)
	{
		(*debug_file) << "Start StartAcquireContinuous" << std::endl;
	}
	
	if(StartOnPause)
	{
		G_save_images_acquired = false;
	}
	else
	{
		G_save_images_acquired = true;
	}
	
	//On met à jour le nombre d'images **************à valider si on est en mode continu*****************
	//nbrImageBuffer = nbrImage; //*********test************
	
	//On assigne/réassigne le buffer
	update_buffer_parameters();
	
	//On update le nom de sauvegarde des images avant de commencer pour qu'il ne reste que les indices à updater pour chaque image
	update_image_path_name();
	
	if(debug > 1)
	{
		(*debug_file) << "Saving in :" << G_sequence_detail_path_name << std::endl;
	}

	//Ouverture du fichier résumé de l'acquisition //****se fait maintenant dans le callback
	//G_sequence_detail_file =  fopen(G_sequence_detail_path_name.c_str(),"a");
	//sequence_detail_file = G_sequence_detail_file;
	
	//HIS_SEQ_TWO_BUFFERS = 0x1         #Storage of the sequence into two buffers. Secure image acquisition by separated data transfer and later performed image correction.
	//HIS_SEQ_ONE_BUFFER = 0x2         #Storage of the sequence into one buffer. Direct acquisition and linked correction into one buffer.
	//HIS_SEQ_AVERAGE = 0x4            #All acquired single images are directly added into one buffer and after acquisition divided by the number of frames, including linked correction files.
	//HIS_SEQ_DEST_ONE_FRAME = 0x8      #Sequence of frames using the same image buffer
	//HIS_SEQ_COLLATE =0x10            #Skip frames after acquiring frames in a ring buffer
	//HIS_SEQ_CONTINUOUS = 0x100        #Continuous acquisitionFrames are continuously acquired into a ring buffer of dwFrames

	
	unsigned int t_dwFrames = 1;  //nbrImageBuffer si en acquisition continu**********
	unsigned int t_dwSkipFrames = 0;    //Nombre d'image à skipper avant chaque copie d'image dans le buffer. Dans notre cas, c'est 0, puisqu'on les veut toutes !
	unsigned int t_dwOpt = HIS_SEQ_CONTINUOUS;      //=0x100, acquisition continu
	//t_pwOffsetData = NULL;  //#c.POINTER(cc.c_ushort)()
	//t_pdwGainData = NULL;  //c.c_void_p(None)   #c.POINTER(ccwin.DWORD)()
	//t_pdwPixelData = NULL:  //c.c_void_p(None)   #c.POINTER(ccwin.DWORD)()
	
	
	//Début de l'Acquisition
	if(debug > 0)
	{
		(*debug_file) << "Starting Acquisition Continuous." << std::endl;
	}
	
	
	//winapi = Acquisition_ResetFrameCnt(hAcqDesc);		//Reset frame count ne marche pas avec notre version de dll
	//print_error_winapi("Acquisition_ResetFrameCnt");	

	winapi = Acquisition_Acquire_Image(hAcqDesc,t_dwFrames, t_dwSkipFrames, t_dwOpt, pwOffsetData, pdwGainData , pdwPixelData);
	print_error_winapi("Acquisition_Acquire_Image");	
	
	winapi = Acquisition_SetFrameSync(hAcqDesc);
	print_error_winapi("Acquisition_SetFrameSync");	

	//On indique qu'on est prêt pour l'acquisition
	winapi = Acquisition_SetReady(hAcqDesc, true);
	print_error_winapi("Acquisition_SetReady(true)");
	

	//On attend une seconde pour éviter que le buffer soit vide.
	//Il faut laisser un peu de temps pour que le frame grabber prenne des images.
	Sleep(410);

    
  if(debug > 1)
  {  
    (*debug_file) << std::endl;
    (*debug_file) << "Debug iView Timestamp" << std::endl;
    (*debug_file) << G_horloge_iView->TimestampDebugInfo();
  }


    
	//L'acquisition se fait via le Callback à la fin de l'acquisition des images. 
	//Le callback utilise la fonction "OnEndFrameCallback"
	
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iViewControl::PauseImageSavingWithoutStopingAcquisition()
{
	G_save_images_acquired = false;
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iViewControl::ResumeSavingImageSaving()
{
	if(Acquisition_IsAcquiringData(hAcqDesc) == true)
	{
		G_save_images_acquired = true;
	}
	else
	{
		(*debug_file) << "Error in iViewControl::ResumeSavingImageSaving : Cannot resume an acquisition that is not started." << std::endl;
	}
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iViewControl::StopAcquireContinuous()
{
	G_stop_acquisition = true;
	
	if(Acquisition_IsAcquiringData(hAcqDesc) == true)
	{
		if(debug > 0)
		{
			(*debug_file) << "iViewControl::StopAcquireContinuous : Data still in acquisition. Doing Acquisition_Abort" << std::endl;
		}
		try
		{
			winapi = Acquisition_Abort(hAcqDesc);
		}
		catch(...)
		{ 
			(*debug_file) << "\tiViewControl::StopAcquireContinuous : Acquisition_Abort failed (!?!)" << std::endl;
		}
		print_error_winapi("Acquisition_Abort");
	}

	
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iViewControl::PrintHeaderInfo( std::ofstream *file )
{
	//Getting and printing CHwHeaderInfo
	
	(*file) << "PrintHeaderInfo: chwHeaderInfo" << std::endl;

	(*file) << "\tdwPROMID = "		<< chwHeaderInfo.dwPROMID << std::endl;					//Identifies the camera's PROM set
	(*file) << "\tdwHeaderID = "	<< chwHeaderInfo.dwHeaderID << std::endl;						//identifies the used header version (version zero)
	(*file) << "\tbAddRow = "		<< chwHeaderInfo.bAddRow << std::endl;							//indicates if an additional row is transferred
	(*file) << "\tbPwrSave = "		<< chwHeaderInfo.bPwrSave << std::endl;						//indicates if the camera is in power safe mode
	(*file) << "\tdwNrRows = "		<< chwHeaderInfo.dwNrRows << std::endl;					//number of sensor rows
	(*file) << "\tdwNrColumns = "	<< chwHeaderInfo.dwNrColumns << std::endl;				//number os sensor columns
	(*file) << "\tdwZoomULRow = "	<< chwHeaderInfo.dwZoomULRow << std::endl;			//row of the upper left edge of zoom region
	(*file) << "\tdwZoomULColumn = "<< chwHeaderInfo.dwZoomULColumn << std::endl;	//column of the upper left edge of zoom region
	(*file) << "\tdwZoomBRRow = "	<< chwHeaderInfo.dwZoomBRRow << std::endl;			//row of bottom right edge of zoom region
	(*file) << "\tdwZoomBRColumn = "<< chwHeaderInfo.dwZoomBRColumn << std::endl;	//column of the bottom right edge of zoom region
	(*file) << "\tdwFrmNrRows = "	<< chwHeaderInfo.dwFrmNrRows << std::endl;				//Number of rows that are used to synthetize the frame scheme of the camera. It
																																		//results from the number of sensor rows plus the number of rows in which the sensor
																																		//only integrates charge but doesn't transfer data to the frame grabber plus the
																																		//number of filling rows
	(*file) << "\tdwFrmRowType = "	<< chwHeaderInfo.dwFrmRowType << std::endl;		//See Row Types
	(*file) << "\tdwFrmFillRowIntervalls = " << chwHeaderInfo.dwFrmFillRowIntervalls << std::endl;	//Intervals of 10 nanoseconds to synthetise a frame (see description of hardware header)
	(*file) << "\tdwNrOfFillingRows = " << chwHeaderInfo.dwNrOfFillingRows << std::endl;	//Number of rows of the above mentioned row time
	(*file) << "\tdwDataType = "	<< chwHeaderInfo.dwDataType << std::endl;						//normallt zero (unsigned 16 bit integer)
	(*file) << "\tdwDataSorting = " << chwHeaderInfo.dwDataSorting << std::endl;				//see sorting
	(*file) << "\tdwTiming = "		<< chwHeaderInfo.dwTiming << std::endl;							//selected integration time (preliminary)
	(*file) << "\tdwAcqMode = "		<< chwHeaderInfo.dwAcqMode << std::endl;					//fixed mode (0), sync mode (1) with fixed frame regime
	(*file) << "\tdwGain = "		<< chwHeaderInfo.dwGain << std::endl;							//only used for the RISL camera family otherwhise (0x7FFF)
	(*file) << "\tdwOffset = "		<< chwHeaderInfo.dwOffset << std::endl;							//only used for the RISL camera family otherwhise (0x7FFF)
	(*file) << "\tdwAccess = "		<< chwHeaderInfo.dwAccess << std::endl;							//
	(*file) << "\tbSyncMode = "		<< chwHeaderInfo.bSyncMode << std::endl;					//1 if camera operates in triggered mode else 0
	(*file) << "\tdwBias = "		<< chwHeaderInfo.dwBias << std::endl;								//10 V * SensorBias / 255
	(*file) << "\tdwLeakRows = "	<< chwHeaderInfo.dwLeakRows << std::endl;				//Number of rows without driven gates


}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iViewControl::SetSavingParameter(std::string acqName, std::string acqPath)
{
	image_name = acqName;
	image_path =acqPath;
	update_image_path_name();
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
bool iViewControl::DirectoryExists(const char* szPath)		//fonction Windows seulement
{
	DWORD dwAttrib = GetFileAttributes((LPCTSTR)szPath);	//LPCTSTR is a const char*

	return (dwAttrib != INVALID_FILE_ATTRIBUTES && (dwAttrib & FILE_ATTRIBUTE_DIRECTORY));
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iViewControl::ConvertBinaryFiles( char* filename )
{
	std::string temp= filename;
	ConvertBinaryFiles( temp );
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iViewControl::ConvertBinaryFiles( std::string filename )
{
	FILE* binary_image_file;
	FILE* txt_image_file;
	
	long fileSize =0;
	long fileNbrPixels=0;
	unsigned short* fileBuffer;
	//std::size_t filename_extension_pos = filename.find(".");	//Finding the extension position in filename
	size_t result;
	unsigned int nbrImageInBuffer = 0;
	std::string filenameTemp = "";
	char filenameTemp_with_index[155];
	int temp1 = 0;
	int temp2 = 0;

	//Nom du fichier d'écriture
	filenameTemp = image_path +  filename.substr(0,filename.find(".")) +  "_%03d.txt";	
	
	if(debug > 0)
	{
		(*debug_file) << "ConvertBinaryFiles : " << filename << " to : " << filenameTemp << std::endl;
	}
	
	binary_image_file = fopen(filename.c_str(),"rb"); //ouverture du fichier en mode lecture binaire
	if (!binary_image_file)
	{
		(*debug_file) << "Error in iViewControl::ConvertBinaryFiles : Unable to open file : " << filename << std::endl;
		exit (1);
	}

	//On regarde la taille du fichier
	fseek (binary_image_file , 0 , SEEK_END);
	fileSize = ftell (binary_image_file);
	fileNbrPixels=fileSize/2; //Divisé par deux puisqu'il y a deux bytes par valeur unsigned short
	rewind (binary_image_file);
	nbrImageInBuffer = fileNbrPixels/(nbrRows*nbrColumns);
	
	if(fileNbrPixels != nbrRows*nbrColumns*nbrImageInBuffer)
	{
		(*debug_file) << "\tError in iViewControl::ConvertBinaryFiles : nbrRows * nbrColumns*nbrImageInBuffer != fileSize : " << nbrRows*nbrColumns*nbrImageInBuffer << " != " << fileSize << std::endl;
	}
	
	if(debug > 0)
	{
		(*debug_file) << "\tfileNbrPixels : " << fileNbrPixels << " shorts" << std::endl;
		(*debug_file) << "\tnbrRows * nbrColumns : " << nbrRows << " * " << nbrColumns << " = " << nbrRows*nbrColumns << std::endl;
		(*debug_file) << "\tnbrImageInBuffer : " << nbrImageInBuffer << " images" << std::endl;
	}
	
	//on recrée un buffer pour remettre le fichier dedans
	fileBuffer = (unsigned short *) malloc(fileSize*sizeof(unsigned short));
	
	if (fileBuffer == NULL)
	{
		(*debug_file) << "Error in iViewControl::ConvertBinaryFiles : Memory error, malloc failed." << std::endl;
		exit (1);
	}
	
	result = fread (fileBuffer,1,fileSize,binary_image_file);
	if (result !=fileSize)
	{
		(*debug_file) << "Error in iViewControl::ConvertBinaryFiles : Reading error, fread failed ?" << std::endl;
		exit (1);
	}

	//Fermeture du ficheir binaire
	fclose(binary_image_file);
	
	//*******Ici je n'ai pas validé que Rows et Columns sont dans le bon ordre********test******
	for(int im=0; im < nbrImageInBuffer; im++)
	{
		sprintf(filenameTemp_with_index, filenameTemp.c_str(), im);	//insertion de l'index de l'image dans le nom du fichier txt
		
		txt_image_file = fopen(filenameTemp_with_index,"w"); //ouverture du fichier en mode lecture binaire
		temp1 = im* nbrRows *  nbrColumns;
		for(int i = 0; i < nbrRows; i++)
		{
			temp2 = temp1 + i*nbrColumns;
			fprintf(txt_image_file, "%d", fileBuffer[temp2]);
			for(int j = 1; j < nbrColumns; j++)
			{
				fprintf(txt_image_file, " %d", fileBuffer[temp2 +j]);
			}
			fprintf(txt_image_file, "\n");
		}
		//fprintf(txt_image_file, "\n");
		fclose(txt_image_file);
	}
	
	
	free(fileBuffer);
	
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iViewControl::initialize_iViewControl(short debugValue, short TimestampType)
{
    debug = debugValue; //0 No debug, 1 debug, 2 debug detail.
	//Ouverture du fichier de debug de la classe
    (*debug_file) << "iViewControl::iViewControl : debug = " << debug << std::endl;
    
    if(debug > 0)
	{
		(*debug_file) << "iViewControl::iViewControl : BetterTimestamp clock type = " << TimestampType << std::endl;
	}
    
	//On initialise l'horloge
	G_horloge_iView = new BetterTimestamp(debugValue,TimestampType);
	
	//winapi à 0 puisque pas d'erreur pour l'intant !!!
	winapi = 0; //=HIS_ALL_OK
	//Initialise des vecteurs de description d'Erreur pour aider à debugger
	initialize_error_vectors();
	
	//Definition des paramètres d'image par defaut. On considere un buffer d'une image pour l'instant
	nbrColumns = 1024;
	nbrRows = 1024;
	nbrPixelsImage = nbrColumns*nbrRows;
	nbrImageBuffer = 1;
	G_nbrPixelsBuffer = nbrImageBuffer*nbrPixelsImage;
	
	//Paramètre de sauvegarde
	G_image_index = new unsigned int(0); //Pas d'image enregistrée, l'index est à 0
	image_path = "";	//"images\\";
	image_name = "image";
	image_extension = ".bin";
	
	//Définitoin initial du buffer **********à vérifier si nécessaire ici *******test*********************
	G_pAcqBuffer = (unsigned short *) malloc(G_nbrPixelsBuffer*sizeof(unsigned short));
	
	//Paramètre de correction. mis à NULL pour l'instant puisque nous n'en tenons pas compte.
	pwOffsetData = NULL;
	pdwGainData = NULL;
	pdwPixelData = NULL;
 
	//Initialisation des variables globales.
	G_save_images_acquired = false;
	G_stop_acquisition = false;
	//pAcqBuffer = G_pAcqBuffer;
	//nbrPixelsBuffer = G_nbrPixelsBuffer;
	
	if (G_pAcqBuffer == NULL)
	{
		(*debug_file) << "iViewControl::iViewControl : Error doing malloc for G_pAcqBuffer. Exiting." << std::endl;
		exit(1);
	}

}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iViewControl::update_image_path_name()
{
	//Update le nom du fichier. Seule l'index reste à remplacer par la suite lors de la sauvegarde pour accélérer le code lors des acquisitions
	//À faire idéalement avant le début d'une acquisition au cas ou le path ou le nom de fichier soit changé.
	std::string filename = image_path;
	
	if( DirectoryExists(image_path.c_str()) == false )
	{
		if (CreateDirectory(image_path.c_str(), NULL) )
		{        
			if(debug > 0)
			{
				(*debug_file) << "iViewControl::update_image_path_name : Creation du dossier : " << image_path << std::endl;
			}
		}
		else
		{
			(*debug_file) << "Error in iViewControl::update_image_path_name  : Creation du dossier " << image_path << " a echouee." << std::endl;
		}
	}

	
	filename += image_name;
	filename += "_im_detail.txt";
	
	G_sequence_detail_path_name = filename;
	
	image_path_name = image_path;
	image_path_name += image_name;
	image_path_name += "%05u";		//Place de 5 caractères pour le numéro de l'image
	image_path_name += image_extension;
	
	G_image_path_name = image_path_name;    //On place une copie dans la variable globale aussi.
	
	//On update le numéro de l'index à utiliser avec ce nouveau nom de séquence
	(*G_image_index) = initial_image_index_from_detail_file(G_sequence_detail_path_name);
	
	if(debug > 1)
	{
		(*debug_file) << "iViewControl::update_image_path_name : G_image_path_name=" << G_image_path_name << std::endl;
		(*debug_file) << "iViewControl::update_image_path_name : G_sequence_detail_path_name=" << G_sequence_detail_path_name << std::endl;
	}
	
	if(image_path_name.length() >148)
	{
		(*debug_file) << "Error in iViewControl::update_image_path_name : Path and image name to long (size " << image_path_name.length() 
							<< ") : " << image_path_name << std::endl;
		exit(1);
	}
	
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iViewControl::update_buffer_parameters() //Efface le buffer actuellement défini et le redéfini de nouveau avec les paramètres interne.
{
	
	if(debug > 0)
	{
		(*debug_file) << "iViewControl::update_buffer_definition : Definition du buffer" << std::endl;
	}

	//Effacer le buffer actuel
	free(G_pAcqBuffer);
	
	//Update du nombre de pixels dans l'image
	nbrPixelsImage = nbrColumns*nbrRows;
	//Update du nombre total de pixels
	G_nbrPixelsBuffer = nbrImageBuffer*nbrPixelsImage;
	//nbrPixelsBuffer = G_nbrPixelsBuffer;

	
	//Création du nouveau Buffer
	G_pAcqBuffer = (unsigned short *) malloc(G_nbrPixelsBuffer*sizeof(unsigned short));
	
	if (G_pAcqBuffer == NULL)
	{
		(*debug_file) << "iViewControl::update_buffer_definition : Error doing malloc for G_pAcqBuffer. Exiting." << std::endl;
		exit(1);
	}

	//Assignation du buffer au XISL
	winapi = Acquisition_DefineDestBuffers(hAcqDesc, G_pAcqBuffer, nbrImageBuffer,nbrRows,nbrColumns);
	print_error_winapi("Acquisition_DefineDestBuffers");

}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
int iViewControl::initial_image_index_from_detail_file(std::string the_sequence_detail_path_name)      //retourne le prochain index à utiliser pour les images basé sur l'index le plus grand présent dans le fichier de résumé G_sequence_detail_path_name
{
	int next_image_index = 0;
	
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
			(*debug_file) << "iViewControl::initial_image_index_from_detail_file : Sequence_detail found, starting acquisition index at : " << next_image_index << std::endl;
		}

	}
	
	
	return next_image_index;
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iViewControl::initialize_error_vectors()
{
	//Nom et description des codes d'erreur pouvant se retrouver dans "winapi" après l'Exécution d'une fonction XISL
	
	//clear vectors au cas
	errornames.clear();
	errordescription.clear();

	//Nom des codes d'erreur.
	errornames.push_back("HIS_ALL_OK");						//0
	errornames.push_back("HIS_ERROR_MEMORY");					//1
	errornames.push_back("HIS_ERROR_BOARDINIT");					//2
	errornames.push_back("HIS_ERROR_NOCAMERA");					//3
	errornames.push_back("HIS_ERROR_CORRBUFFER_INCOMPATIBLE");	//4
	errornames.push_back("HIS_ERROR_ACQ_ALREADY_RUNNING");		//5
	errornames.push_back("HIS_ERROR_TIMEOUT");					//6
	errornames.push_back("HIS_ERROR_INVALIDACQDESC");			//7
	errornames.push_back("HIS_ERROR_VXDNOTFOUND");				//8
	errornames.push_back("HIS_ERROR_VXDNOTOPEN");				//9
	errornames.push_back("HIS_ERROR_VXDUNKNOWNERROR");			//10
	errornames.push_back("HIS_ERROR_VXDGETDMAADR");				//11
	errornames.push_back("HIS_ERROR_ACQABORT");					//12
	errornames.push_back("HIS_ERROR_ACQUISITION");				//13
	errornames.push_back("HIS_ERROR_VXD_REGISTER_IRQ");			//14
	errornames.push_back("HIS_ERROR_VXD_REGISTER_STATADR");		//15
	errornames.push_back("HIS_ERROR_GETOSVERSION");				//16
	errornames.push_back("HIS_ERROR_SETFRMSYNC");				//17
	errornames.push_back("HIS_ERROR_SETFRMSYNCMODE");			//18
	errornames.push_back("HIS_ERROR_SETTIMERSYNC");				//19
	errornames.push_back("HIS_ERROR_INVALID_FUNC_CALL");		//20
	errornames.push_back("HIS_ERROR_ABORTCURRFRAME");			//21
	errornames.push_back("HIS_ERROR_GETHWHEADERINFO");		//22
	errornames.push_back("HIS_ERROR_HWHEADER_INV");				//23
	errornames.push_back("HIS_ERROR_SETLINETRIG_MODE");			//24
	errornames.push_back("HIS_ERROR_WRITE_DATA");				//25
	errornames.push_back("HIS_ERROR_READ_DATA");					//26
	errornames.push_back("HIS_ERROR_SETBAUDRATE");				//27
	errornames.push_back("HIS_ERROR_NODESC_AVAILABLE");			//28
	errornames.push_back("HIS_ERROR_BUFFERSPACE_NOT_SUFF");		//29
	errornames.push_back("HIS_ERROR_SETCAMERAMODE");				//30
	errornames.push_back("HIS_ERROR_FRAME_INV");					//31
	errornames.push_back("HIS_ERROR_SLOW_SYSTEM");				//32
	errornames.push_back("HIS_ERROR_GET_NUM_BOARDS");			//33
	errornames.push_back("HIS_ERROR_HW_ALREADY_OPEN_BY_ANOTHER_PROCESS");	//34
	errornames.push_back("HIS_ERROR_CREATE_MEMORYMAPPING");				//35
	errornames.push_back("HIS_ERROR_VXD_REGISTER_DMA_ADDRESS");			//36
	errornames.push_back("HIS_ERROR_VXD_REGISTER_STAT_ADDR");			//37
	errornames.push_back("HIS_ERROR_VXD_UNMASK_IRQ");					//38
	errornames.push_back("HIS_ERROR_LOADDRIVER");						//39
	errornames.push_back("HIS_ERROR_FUNC_NOTIMPL");						//40
	errornames.push_back("HIS_ERROR_MEMORY_MAPPING");					//41
	errornames.push_back("HIS_ERROR_CREATE_MUTEX");						//42
	errornames.push_back("HIS_ERROR_ACQ");								//43
	errornames.push_back("HIS_ERROR_DESC_NOT_LOCAL");					//44
	errornames.push_back("HIS_ERROR_INVALID_PARAM");						//45
	errornames.push_back("HIS_ERROR_ABORT");								//46
	errornames.push_back("HIS_ERROR_WRONGBOARDSELECT");					//47
	errornames.push_back("HIS_ERROR_WRONG_CAMERA_MODE");					//48
	errornames.push_back("HIS_ERROR_AVERAGED_LOST");						//49
	errornames.push_back("HIS_ERROR_BAD_SORTING_PARAM");					//50
	errornames.push_back("HIS_ERROR_UNKNOWN_IP_MAC_NAME");				//51
	errornames.push_back("HIS_ERROR_NO_BOARD_IN_SUBNET");				//52
	errornames.push_back("HIS_ERROR_UNABLE_TO_OPEN_BOARD");				//53
	errornames.push_back("HIS_ERROR_UNABLE_TO_CLOSE_BOARD");				//54
	errornames.push_back("HIS_ERROR_UNABLE_TO_ACCESS_DETECTOR_FLASH");	//55
	errornames.push_back("HIS_ERROR_HEADER_TIMEOUT");					//56
	errornames.push_back("HIS_ERROR_NO_PING_ACK");						//57
	errornames.push_back("HIS_ERROR_NR_OF_BOARDS_CHANGED");				//58

	//matrice des description pour chaque erreur selon la documentation.
	errordescription.push_back("No error"); //#0
	errordescription.push_back("Memory couldn't allocated"); //#1
	errordescription.push_back("Unable to initialize board"); //#2
	errordescription.push_back("Got a time out for acquisition. May be no camera present"); //#3
	errordescription.push_back("Your correction files didn't have a proper size"); //#4
	errordescription.push_back("Unable to initialize board or allocate DMA buffer because a acquisition is running"); //#5
	errordescription.push_back("Got a time out from hardware"); //#6
	errordescription.push_back("Acquisition descriptor is invalid"); //#7
	errordescription.push_back("Unable to find VxD"); //#8
	errordescription.push_back("Unable to open VxD"); //#9
	errordescription.push_back("Unknown error during VxD loading"); //#10
	errordescription.push_back("VxD Error: GetDmaAddr failed"); //#11
	errordescription.push_back("An unexpected acquisition abort occured"); //#12
	errordescription.push_back("An error occured during data acquisition"); //#13
	errordescription.push_back("Unable to register interrupt"); //#14
	errordescription.push_back("Register status adress failed"); //#15
	errordescription.push_back("Gettinf version of operating system failed"); //#16
	errordescription.push_back("Can't set frame sync"); //#17
	errordescription.push_back("Can't set frame sync mode"); //#18
	errordescription.push_back("Can't set timer sync"); //#19
	errordescription.push_back("Function was called by another thread than Acquisition_Init"); //#20
	errordescription.push_back("Aborting current frame failed"); //#21
	errordescription.push_back("Getting hardware header failed"); //#22
	errordescription.push_back("Hardware header is invalid"); //#23
	errordescription.push_back("Setting line trigger mode failed"); //#24
	errordescription.push_back("Writing data failed"); //#25
	errordescription.push_back("Reading data failed"); //#26
	errordescription.push_back("Setting baud rate failed"); //#27
	errordescription.push_back("No acquisition descriptor available"); //#28
	errordescription.push_back("Buffer space not sufficient"); //#29
	errordescription.push_back("Setting camera mode failed"); //#30
	errordescription.push_back("Frame invalid"); //#31
	errordescription.push_back("System to slow"); //#32
	errordescription.push_back("Error during getting number of boards"); //#33
	errordescription.push_back("Communication channel already opened by another process"); //#34
	errordescription.push_back("Error Creating memory mapped file"); //#35
	errordescription.push_back("Error registering DMA adress"); //#36
	errordescription.push_back("Error registering static adress"); //#37
	errordescription.push_back("Unable to Unmask interrupt"); //#38
	errordescription.push_back("Unable to load driver"); //#39
	errordescription.push_back("Function is not implemented"); //#40
	errordescription.push_back("Unable to map memory"); //#41
	errordescription.push_back("Mutex couldn't created"); //#42
	errordescription.push_back("Error during acquisition"); //#43
	errordescription.push_back("Acquisition descriptor is not local"); //#44
	errordescription.push_back("Invalid parameter"); //#45
	errordescription.push_back("Error during abort aqcuisition"); //#46
	errordescription.push_back("The wrong board is selected"); //#47
	errordescription.push_back("NA");
	errordescription.push_back("NA");
	errordescription.push_back("NA");
	errordescription.push_back("NA");
	errordescription.push_back("NA");
	errordescription.push_back("NA");
	errordescription.push_back("NA");
	errordescription.push_back("NA");
	errordescription.push_back("NA");
	errordescription.push_back("NA");
	errordescription.push_back("NA");

}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void iViewControl::print_error_winapi(std::string fonction_name)
{
	//Imprime les cdes d'erreur avec les descriptions

	if (debug > 1 || winapi != HIS_ALL_OK) //if(winapi != 0)
	{
		(*debug_file) << fonction_name << " -> winapi = " << winapi << " , " << errornames[winapi] << " : " << errordescription[winapi] << std::endl;
	}

}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
 void  iViewControl::print_acquisition_param()
{
	
	unsigned int t_dwFrames = 0;
	unsigned int t_dwRows = 0;
	unsigned int t_dwColumns = 0;
	unsigned int t_dwDataType = 0;
	unsigned int  t_dwSortFlags = 0;
	BOOL t_bIRQEnabled = false;
	DWORD t_dwAcqType = 1;				//internal Data, do not have to be considered
	DWORD t_dwSystemID = 1;
	DWORD t_dwSyncMode = 1;
	DWORD t_dwHwAccess = 1;			//internal Data, do not have to be considered

	(*debug_file) << "print_acquisition_param (Acquisition_GetConfiguration) :" << std::endl;

	winapi = Acquisition_GetConfiguration( hAcqDesc, &t_dwFrames, &t_dwRows, &t_dwColumns, &t_dwDataType, &t_dwSortFlags ,&t_bIRQEnabled, &t_dwAcqType, &t_dwSystemID, &t_dwSyncMode, &t_dwHwAccess );
	
	if(debug > 0)
	{
		print_error_winapi("Acquisition_GetConfiguration");
	}

	(*debug_file) << "\tt_dwFrames : " << t_dwFrames << std::endl;
	(*debug_file) << "\tt_dwRows : " << t_dwRows << std::endl;
	(*debug_file) << "\tt_dwColumns : " << t_dwColumns << std::endl;
	(*debug_file) << "\tt_dwDataType : " << t_dwDataType << std::endl;
	(*debug_file) << "\tt_dwSortFlags : " << t_dwSortFlags << std::endl;
	(*debug_file) << "\tt_bIRQEnabled : " << t_bIRQEnabled << std::endl;
	(*debug_file) << "\tt_dwAcqType (internal Data, do not have to be considered) : " << t_dwAcqType << std::endl;
	(*debug_file) << "\tt_dwSystemID : " << t_dwSystemID << std::endl;
	(*debug_file) << "\tt_dwSyncMode : " << t_dwSyncMode << std::endl;
	(*debug_file) << "\tt_dwHwAccess (internal Data, do not have to be considered) : " << t_dwHwAccess << std::endl;
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////

