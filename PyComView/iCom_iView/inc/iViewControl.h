//////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
// iViewControl.h
//   (C) 2019 by Nicolas Tremblay <nmtremblay.chus@ssss.gouv.qc.ca>
//
//		
//		
//		
//
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////

#ifndef  iViewControl_h
#define  iViewControl_h 1

#include <vector>
#include <iostream>
#include <fstream>
#include <string>
#include <chrono>	//Pr�sent seulement � partir de C++11. Doit donc utiliser une version qui l'a... 
				//pour gcc, pr�sent seulement � partir de la version 4.3.
				//Chrono inclue les fonctions d'horloge au millisecondes, etc.
#include <thread>            //Pr�sent seulement � partir de C++11    
#include <time.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>	//Pour les uint64_t
#include <windows.h> //Inclus les types Windows comme DWORD, etc. qui sont utilis�s dans XISL

//#include <unistd.h>	//Normallement pas disponible sur windows. Mais vu qu'on utilise MSYS et gcc �a marche sur Windows.

#include "Acq.h"		//la librairie qui inclue les fonctions de lecture pour le iView
						//La librairie XISL peut �tre charg�e avec Visual Studio, mais pas gcc...
						//
#include "BetterTimestamp.h"


//////////////////////////////////////////////////////////////////////////////
//Variables globales n�cessaires auc fonctions d'acquisition et de fin de s�quences
//D�finies dans iViewControl.cpp
//////////////////////////////////////////////////////////////////////////////

extern bool G_save_images_acquired;
extern bool G_stop_acquisition;
extern unsigned int* G_image_index;
extern unsigned short* G_pAcqBuffer;
extern unsigned int G_nbrPixelsBuffer;     //Nombre de pixels dans le Buffer (nbrPixelsImage*nbrImageBuffer)


extern FILE* G_sequence_detail_file;
extern std::ofstream* G_iView_debug_file;

extern std::string G_image_path_name;

extern BetterTimestamp* G_horloge_iView;

//char G_image_path_name_with_index[150];
extern std::string G_sequence_detail_path_name;


////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
class iViewControl
{
	public:

		iViewControl();               
		iViewControl(short debugValue);
		iViewControl(short debugValue, short TimestampType);
		~iViewControl();            //Destructeur

		void SetDebug(short debugValue);

        void SetTimestampType(short Type); //sets the time stamp to be used. 
                                                                //0 = realtime.  Renvoie le temps en ms. Stable, mais moins grande r�solution (10 � 16ms). Utilise "GetTickCount".  Valide pour 49 jours    (horloge par d�faut)
                                                                //1 = processor. Renvoie le temps en 100ns. Grande r�solution (d�fini par la fr�quence du processeur), 
                                                                                    //mais pose des risque d'invalidit� si le procesus change de processeur ou si la fr�quence du processeur change en cours de route.

        unsigned int InitializePanel();		//Connecte au paneau et initialise certains param�tres.
		void ClosePanel();			//Fermture du paneau.
		void AcquireImage(unsigned int nbrImage);   //Avec cette fonction, l'acquisition ne se fera pas en background
		
	
		void StartAcquireContinuous();  //StartOnPause = False
		void StartAcquireContinuous(bool StartOnPause);
		void PauseImageSavingWithoutStopingAcquisition();
		void ResumeSavingImageSaving();
		void StopAcquireContinuous();
	
		void PrintHeaderInfo( std::ofstream *file );
		
		void SetSavingParameter(std::string acqName, std::string acqPath);
		
		bool DirectoryExists(const char* szPath); 		//fonction Windows seulement
	
		//Converti les fichier binaire en image txt.Utilise nBRRows et nbrColumns pour la grandeur des images
		void ConvertBinaryFiles( std::string filename );
		void ConvertBinaryFiles( char* filename );
	
	private:

		short debug;                    //0 No debug, 1 debug, 2 debug detail. Valeur dans l'initialisation de la classe.
		std::ofstream *debug_file;  //Pointeur vers le fichier de debug de la classe (debug_iViewControl.txt)
		std::vector<std::string> errornames;
		std::vector<std::string> errordescription;
		
		//
		FILE* image_file;
		std::string image_path;			//Chemin o� les fichiers doivent �tre sauvegard�.
		std::string image_name;			//Nom des images (sans l'indice (num�ro) et l'extension
		std::string image_extension;	//Extension des images (incluant le .)
		std::string image_path_name;
		char image_path_name_with_index[150];
		
		unsigned int nbrColumns;          //Normallement toujours 1024 pour iView
		unsigned int nbrRows;             //Normallement toujours 1024 pour iView
		unsigned int nbrImageBuffer;      //
		
		//Valeurs mis � jour par update_buffer_definition
		unsigned int nbrPixelsImage;      //Normallement toujours 1024x1024 pour iView
		//unsigned int nbrPixelsBuffer;     //Nombre de pixels dans le Buffer (nbrPixelsImage*nbrImageBuffer)

		HWND hWhd;
		
		unsigned int winapi;					//Statut des op�rations. Renvoie - si OK, sinon un chiffre correcpondant � un code d'Erreur.
		HACQDESC hAcqDesc;					//Valeur (typedef Handle) incluant les param�tres d'acquisition. Initialis� dans la fonction Acquisition_Init
		CHwHeaderInfo chwHeaderInfo;
		//unsigned short* pAcqBuffer;	//Buffer utilis� par XILS pour l'acquisition
		unsigned short* pwOffsetData;
		DWORD* pdwGainData;
		DWORD* pdwPixelData;
		
        void initialize_iViewControl(short debugValue, short TimestampType);
        
		void update_image_path_name();
		
		void update_buffer_parameters(); //Efface le buffer actuellement d�fini et le red�fini de nouveau avec les param�tres interne.
		
		//void save_buffer(FILE* seq_detail_file);				//Save Buffer content  in binary with "image_index" as number of image
		//void save_buffer_in_txt(char* filemane);          //Trop long pour �tre utilis� en continu, mais pratique pour le debug

		int initial_image_index_from_detail_file(std::string the_sequence_detail_path_name);      //retourne le prochain index � utiliser pour les images bas� sur l'index le plus grand pr�sent dans le fichier de r�sum� G_sequence_detail_path_name

		void initialize_error_vectors();	//Initialize values in 'errornames' and 'errordescription'
		void print_error_winapi(std::string fonction_name); //print winapi, le nom de l'erreur et la description de l'erreur. Ins�re le nom de la fonction dans le message.
		void print_acquisition_param();     //Dans le fichier debug, imprime des �ram�tres d'Acquisition en utilisant la fonction "Acquisition_GetConfiguration" du XISL
		

};


////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////

#endif // iViewControl_h
