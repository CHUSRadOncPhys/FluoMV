//////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
// BetterTimestamp.h
//   (C) 2019 by Nicolas Tremblay <nmtremblay.chus@ssss.gouv.qc.ca>
//
//		Fonction de timestamp faite pour donner l'heure réelle (et non du processus)
//
//		*****Valid for Windows only****
//		
//		for the processor clock, based on : http://blog.quasardb.net/a-portable-high-resolution-timestamp-in-c/
//
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////

#ifndef  BetterTimestamp_h
#define  BetterTimestamp_h 1
#include <stdint.h>	//Pour les uint64_t
#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <iostream>
#include <fstream>
#include <sstream> //pour ostringstream
#include <string>
#include <time.h>
#include <sys/time.h>


////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
class BetterTimestamp
{
	public:
		BetterTimestamp();
		BetterTimestamp(short Debug);
		BetterTimestamp(short Debug, short  TheTimestamp_type);
		~BetterTimestamp();		//Destructeur

		void SetDebug(short Debug);
       
		void SetTimestampType(short type); //sets the time stamp to be used. 
                                                                //0 = realtime.  Renvoie le temps en ms. Stable, mais moins grande résolution (10 à 16ms). Utilise "GetTickCount".  Valide pour 49 jours    (horloge par défaut)
                                                                //1 = processor. Renvoie le temps en 100ns. Grande résolution (défini par la fréquence du processeur), 
                                                                                    //mais pose des risque d'invalidité si le procesus change de processeur ou si la fréquence du processeur change en cours de route.
    
		uint64_t now();
		uint64_t realtime_now();	//en ms, mais résolution entre 10ms et 16 ms
		uint64_t processor_now();	//en 100 ns
		
		
		void ResetZero();
		uint64_t TimeElapsedSinceZero(); //en 100 ns
    
		std::string PrintTimestampDebugInfo(); //cout and return string
		std::string TimestampDebugInfo();       //reutn string only
	
	private:

		short debug;
    
		short timestamp_type; //sets the time stamp to be used. 
                                        //0 = realtime.  Renvoie le temps en ms. Stable, mais moins grande résolution (10 à 16ms). Utilise "GetTickCount".  Valide pour 49 jours    (horloge par défaut)
                                        //1 = processor. Renvoie le temps en 100ns. Grande résolution (défini par la fréquence du processeur), 
                                                                //mais pose des risque d'invalidité si le procesus change de processeur ou si la fréquence du processeur change en cours de route.

		uint64_t previous_now;              //Valeur du "now" précédent utilisé en debug pour valider que le temps ne recule pas.
		
		uint64_t processor_zerotime;		//Time at initialisation. (défini dans cette classe comme étant le temps depuis epoch)
		uint64_t processor_offset;			//Time between FIXME
		uint64_t processor_frequency;
		double processor_tic_100ns;	//durée des tics en 100ns (10 000 000 / frequency)
    
		uint64_t realtime_zerotime;   //Temps à l'inititalisation. (défini dans cette classe comme étant le temps depuis epoch)
		uint64_t realtime_offset;		  //Time between FIXME
        
		
        void initialize_Timestamp(short Debug, short  TheTimestamp_type);
        
		uint64_t set_zerotime();

		uint64_t processor_timestamp();
		uint64_t update_frequency();
		//uint64_t initial_timeoffset();
    
		uint64_t realtime_timestamp();
        
        std::string short_to_string(short number);
        std::string double_to_string(double number);
        std::string uint64_t_to_string(uint64_t number);
	
};

////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
///**/
#endif // BetterTimestamp_h
