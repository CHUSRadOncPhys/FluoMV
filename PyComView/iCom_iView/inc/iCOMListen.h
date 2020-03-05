//////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
// iCOMListen.h
//   (C) 2019 by Nicolas Tremblay <nmtremblay.chus@ssss.gouv.qc.ca>
//
//		 
//		
//		
//
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////

#ifndef  iCOMListen_h
#define  iCOMListen_h 1

#include <vector>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <chrono>	//Présent seulement à partir de C++11. Doit donc utiliser une version qui l'a... 
				//pour gcc, présent seulement à partir de la version 4.3.
				//Chrono inclue les fonctions d'horloge au millisecondes, etc.
#include <thread>            //Présent seulement à partir de C++11  
#include <new> //For std::nothrow
#include <ctime>	//for time_t
#include <time.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>	//Pour les uint64_t
#include <windows.h> //Inclus les types Windows comme DWORD, etc. qui sont utilisés dans XISL

//#include <unistd.h>	//Normallement pas disponible sur windows. Mais vu qu'on utilise MSYS et gcc ça marche sur Windows.

//#include "iCOMClient.h"
#include "iCOMAPI.h"
#include "iViewControl.h"
#include "BetterTimestamp.h"

#include <unistd.h> //fonction sleep


namespace patch
{
	template < typename T > std::string to_string( const T& n )
	{
		std::ostringstream stm ;
		stm << n ;
		return stm.str() ;
	}
}


typedef struct {
	ICOM_TAG    tag;
	char    part;	//'P' Prescribed, 'S' Set, 'R' Run
} tag_part;

typedef struct {
	bool trigOnValueChange; //If false, waiting for value, waiting for value to change
	char* value;
	short triggerType;  //0 = tag, 1 = linacState, 2 =FunctionMode, 3=Keyboard key //ancienne version : bool trueiCOMtag_falselinacState;
	tag_part tag;
	short linacState;   //Linac State OR Function Mode OR  or Virtual Key Code (voir liste au bas du document)
} trigger;


//////////////////////////////////////////////////////////////////////////////
//Variables globales
//////////////////////////////////////////////////////////////////////////////

extern BetterTimestamp* G_horloge_iCOM;

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
class iCOMListen
{
	public:

		iCOMListen();               
		iCOMListen(short Debug);
		iCOMListen(short Debug, short TimestampType);
		~iCOMListen();            //Destructeur
	
		void SetDebug(short Debug);
    
        void SetTimestampType(short type); //sets the time stamp to be used. 
                                                                //0 = realtime.  Renvoie le temps en ms. Stable, mais moins grande résolution (10 à 16ms). Utilise "GetTickCount".  Valide pour 49 jours    (horloge par défaut)
                                                                //1 = processor. Renvoie le temps en 100ns. Grande résolution (défini par la fréquence du processeur), 
                                                                                    //mais pose des risque d'invalidité si le procesus change de processeur ou si la fréquence du processeur change en cours de route.

		void PrintTestInDebug();

		bool Connect_iCOM_Vx();		//Connecte iCOM en mode écoute seulement (Vx) (retourne vrai si la connection a fonctionné.)
		bool Connect_iCOM_Vx(std::string ip_adress_linac);		//Connecte iCOM en mode écoute seulement (Vx) (retourne vrai si la connection a fonctionné.)
		void Disconnect_iCOM();		//Déconnecte iCOM.
	
		//Fonctions qui sauvegardent les images. On reste dans la fonction tant que l'acquisition n'est pas terminée.
		void Save_iCOM_Messages();	//
		void Save_iCOM_Messages(unsigned int nbrSeconds);	//Sauvegarde les messages iCOM au complet
		void Save_iCOM_Messages(unsigned int nbrSeconds, bool tagListInSumary);	//Sauvegarde les messages iCOM au complet, mais met aussi la list de tag
																															//dans "tagParts" dans le fichier de résumé si tagListInSumary=true
		void Save_iCOM_Messages(unsigned int nbrSeconds, bool tagListInSumary, bool SumaryOnly);	//Sauvegarde les messages iCOM au complet, mais met aussi la list de tag
																															//dans "tagParts" dans le fichier de résumé si tagListInSumary=true+
	
		//void Save_iCOM_Continuous();  //Tentative de sauvegarde en continu
		//void iCOMmessageCallback(unsigned long long (*endOfMessageEvent)(void));
	
		//Pour gérer les acquisitions de façon manuelle (attention de ne pas perdre des fichiers iCOM en cours de route !
		
		

		//void Save_iCOM_tagList(unsigned int nbrSeconds);	//Sauvegarde seulement les tags iCOM présent dans "tagParts" dans le fichier de résumé seulement
	
		void SetSavingParameter(std::string acqName, std::string acqPath);
		void SetSavingParameter(std::string acqName, std::string acqPath, short acqSavingPathMode);
		
		//Différents paramètres accessibles de l'Extérieur
		bool useStartAcquisitionTrigger;
		bool iCOMtagListInSummary;
		bool iCOMsaveSummaryOnly;
		short iCOMsavingPathMode;       //Default = 0 :  \ID\date_time\iCOM
														//1 : \ID\date\iCOM
														//2 : \date_time\iCOM
														//3 : \date\iCOM
														//4: \iCOM
														//5: enregistre tout au "user path"
		unsigned int acquisitionTimeoutSeconds;
		
		bool iCOMpauseSaving;		//à mettre global ???
		bool iCOMstopAcquisition;	//à mettre global ????
		
		
		//Fonctions pour gérer l'jout et la suppression de conditions pour le départ et l'arrêt des acquisitions iCOM.
		void Clear_iCOMstartTriggerList();
		void Clear_iCOMpauseTriggerList();
		void Clear_iCOMstopTriggerList();
		
		void Add_iCOMstartTriggerToList_tag(unsigned long tag, char part, bool trigOnValueChange,  char* value);
		void Add_iCOMpauseTriggerToList_tag(unsigned long tag, char part, bool trigOnValueChange, char* value);
		void Add_iCOMstopTriggerToList_tag(unsigned long tag, char part, bool trigOnValueChange, char* value);

		void Add_iCOMstartTriggerToList_NonTag(bool trigOnValueChange, short linacState, short triggerType);
		void Add_iCOMpauseTriggerToList_NonTag(bool trigOnValueChange, short linacState, short triggerType);
		void Add_iCOMstopTriggerToList_NonTag(bool trigOnValueChange, short linacState, short triggerType);
				
		void ClearTagList();
		void AddTagToList(unsigned long tag, char part); //Ajout un tag à la liste à sauver dans le résumé
				
		//Variable pour contrôler le iView d'ici aussi. Pas initialisé d'emblée.
		iViewControl *iview;
		unsigned int Init_iView();  //En gros initialise le paneau en utilisant la variable debug du iCOM.
		void Close_iView(); //ferme l'acquisition et delete le pointeur iView corectement. 
		
		
		
	void FonctionTest();    //Existe pour tester des fonction seulement dans le cadre de la programation NT

		
	private:

		short debug;                    //0 No debug, 1 debug, 2 debug detail. Valeur dans l'initialisation de la classe.
		std::ofstream *debug_file;  //Pointeur vers le fichier de debug de la classe (debug_iComListen.txt)
		std::vector<std::string> errornames;			//Nom des erreurs pour iCOMResult (classée en valeur absolue, erreur -14, se retrouve à l'index 14)
		//std::vector<std::string> errordescription;	//Description des erreurs pour iCOMResult (classée en valeur absolue, erreur -14, se retrouve à l'index 14)

        void initialize_iCOMListen(short Debug, short TimestampType);

        void initialize_error_vectors();	//Initialize values in 'errornames' and 'errordescription'
		//void print_error_winapi(std::string fonction_name); //print winapi, le nom de l'erreur et la description de l'erreur. Insère le nom de la fonction dans le message.

		FILE* iCOMmsg_file;
		FILE* sequence_detail_file;  //Pointeur vers le fichier derésumé des acquisitions
		int iCOMmsg_index;					//Nombre d'image (buffer) sauvegardé
		std::string userSelectedPath;			//Chemin où dossiers de sauvegarde seront créés.
		std::string iCOMmsg_name;			//Nom des fichiers (sans l'indice (numéro) et l'extension
		std::string iCOMmsg_extension;	//Extension des images (incluant le .txt)
		std::string iCOMmsg_path_name;
	
		char* iCOM_last_patient_id;   //dernier id prescrit reçu durant l'acquisition [0x70010002,P]
		std::string iCOM_last_patient_id_str;
		std::string last_timedate;
	
		std::string iCOMmsg_path;			//Chemin où les fichiers doivent être sauvegardé.

	
		char iCOMmsg_path_name_with_index[260];
		std::string sequence_detail_path_name;
		
		ICOMResult iCOMResult; 		//Valeur qui indique si les fonctions de la librairie iCOM fonctionne (1 si OK, chiffre négatif si erreur)

		//std::string log_path;	//
		std::string log_name;	//Nom du fichier du log
	
		ICOMHandle hICOM;	//Handle iCOM de la connection

		ICOMMsgHandle hICOMMsg;		//Handle qui contient toute l'information
		std::vector<tag_part> tagParts;	
		
		std::vector<trigger> startTriggers;
		std::vector<trigger> pauseTriggers;
		std::vector<trigger> stopTriggers;
		
		void update_iCOMmsg_path_name();
	
		void print_error_iCOMResult(std::string fonction_name); //print winapi, le nom de l'erreur et la description de l'erreur. Insère le nom de la fonction dans le message.

		void printAllTags(FILE* aFile);
		
		//std::thread 


		std::string getTag(ICOM_TAG tag);
		std::string getLinacState(short linacState);
		std::string getLinacFunctionMode(short linacFunctionMode);  //Rteourne le mode de fonctionnement du linac correspondant au chiffre (Service mode, etc.)
		std::string getVirtualKey(short vk_Value);
		
		bool triggerTrigerred(std::vector<trigger>* triggerList);
		void updateTriggerListsCurrent();	//Update les valeurs qui trig avec le changement pour les valeurs actuelles
		void updateTriggerListCurrent(std::vector<trigger>* triggerList);	//Update les valeurs qui trig avec le changement pour les valeurs actuelles
		bool create_directory(std::string path);

		bool DirectoryExists(const char* szPath);	//Fonction Windows seulement
		
		int get_iCOMmsg_index_from_sequence_detail_file(std::string the_sequence_detail_path_name); //retourne le dernuméro d'index présent dans le fichier de résumé
		
		std::string getTimeDateString();	//Retourne un string avec la date et l'heure où cette fonction est appelée (pour générer ultérieurement un folder)
		std::string getTimeDateString(bool date_only);	//Retourne un string avec la date et l'heure (si bool == false) où cette fonction est appelée (pour générer ultérieurement un folder)

		void print_trigger(trigger a_trigger, std::ofstream *file);
						
};


////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////

#endif // iCOMListen_h

/*
Virtual Key codes:

vk_BackSpace = 8;
vk_Tab = 9;
vk_Return = 13;
vk_Shift = 16;
vk_Control = 17;
vk_Alt = 18;
vk_Pause = 19;
vk_CapsLock = 20;
vk_Escape = 27;
vk_Space = 32;
vk_PageUp = 33;
vk_PageDown = 34;
vk_End = 35;
vk_Home = 36;
vk_Left = 37;
vk_Up = 38;
vk_Right = 39;
vk_Down = 40;
vk_PrintScreen = 44;
vk_Insert = 45;
vk_Delete = 46;

// NOTE: vk_0..vk_9 vk_A.. vk_Z match regular ASCII codes for digits and A-Z letters

vk_0 = 48;
vk_1 = 49;
vk_2 = 50;
vk_3 = 51;
vk_4 = 52;
vk_5 = 53;
vk_6 = 54;
vk_7 = 55;
vk_8 = 56;
vk_9 = 57;
vk_A = 65;
vk_B = 66;
vk_C = 67;
vk_D = 68;
vk_E = 69;
vk_F = 70;
vk_G = 71;
vk_H = 72;
vk_I = 73;
vk_J = 74;
vk_K = 75;
vk_L = 76;
vk_M = 77;
vk_N = 78;
vk_O = 79;
vk_P = 80;
vk_Q = 81;
vk_R = 82;
vk_S = 83;
vk_T = 84;
vk_U = 85;
vk_V = 86;
vk_W = 87;
vk_X = 88;
vk_Y = 89;
vk_Z = 90;

vk_LWin = 91;
vk_RWin = 92;
vk_Apps = 93;
//numerical key pad
vk_NumPad0 = 96;
vk_NumPad1 = 97;
vk_NumPad2 = 98;
vk_NumPad3 = 99;
vk_NumPad4 = 100;
vk_NumPad5 = 101;
vk_NumPad6 = 102;
vk_NumPad7 = 103;
vk_NumPad8 = 104;
vk_NumPad9 = 105;
vk_Multiply = 106;
vk_Add = 107;
vk_Subtract = 109;
vk_Decimal = 110;
vk_Divide = 111;
// function keys 
vk_F1 = 112;
vk_F2 = 113;
vk_F3 = 114;
vk_F4 = 115;
vk_F5 = 116;
vk_F6 = 117;
vk_F7 = 118;
vk_F8 = 119;
vk_F9 = 120;
vk_F10 = 121;
vk_F11 = 122;
vk_F12 = 123;
vk_F13 = 124;
vk_F14 = 125;
vk_F15 = 126;
vk_F16 = 127;

vk_NumLock = 144;
vk_ScrollLock = 145;
vk_LShift = 160;
vk_RShift = 161;
vk_LControl = 162;
vk_RControl = 163;
vk_LAlt = 164;
vk_RAlt = 165;
vk_SemiColon = 186;
vk_Equals = 187;
vk_Comma = 188;
vk_UnderScore = 189;
vk_Period = 190;
vk_Slash = 191;
vk_BackSlash = 220;
vk_RightBrace = 221;
vk_LeftBrace = 219;
vk_Apostrophe = 222;
*/