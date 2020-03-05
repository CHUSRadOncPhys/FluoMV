///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
//BetterTimestamp.cpp
//   (C) 2019 by Nicolas Tremblay <nmtremblay.chus@ssss.gouv.qc.ca>
//
//  for the processor clock, based on : http://blog.quasardb.net/a-portable-high-resolution-timestamp-in-c/
//
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////

#include "BetterTimestamp.h"


////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
BetterTimestamp::BetterTimestamp()
{
    
    //std::cout << "BetterTimestamp : New Timestamp created" << std::endl;
	//debug = 0;
	//Timestamp_type = 0;
	initialize_Timestamp(0,0);
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
BetterTimestamp::BetterTimestamp(short Debug)
{
	if(debug > 0)
	{
		std::cout << "BetterTimestamp : New Timestamp created" << std::endl;
	}
    
    //Debug = 0;
	initialize_Timestamp(Debug,0);
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
BetterTimestamp::BetterTimestamp(short Debug, short TheTimestamp_type)
{
	if(debug > 0)
	{
		std::cout << "BetterTimestamp : New Timestamp created" << std::endl;
	}

	initialize_Timestamp(Debug,TheTimestamp_type);
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
BetterTimestamp::~BetterTimestamp()
{
    //std::cout << "BetterTimestamp::~BetterTimestamp : Deleting Timestamp." << std::endl;
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void BetterTimestamp::SetDebug(short Debug)
{
	debug = Debug;
    
	PrintTimestampDebugInfo();
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void BetterTimestamp::SetTimestampType(short type)
{
    timestamp_type = type;
		
    if(debug > 0)
	{
        std::cout << "BetterTimestamp::SetTimestampType: Type changed to : " << timestamp_type << std::endl;
    }
    
    ResetZero();
    
	if(debug > 0)
	{
		PrintTimestampDebugInfo();
	}

}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
uint64_t BetterTimestamp::now()
{
	uint64_t now = 0u;
    
    if(timestamp_type == 0)
    {
        now = realtime_now();
    }
    else if(timestamp_type == 1)
    {
        now = processor_now();
    }
    else
    {
        std::cout << "Error in BetterTimestamp::now() : timestamp_type invalide ( " << timestamp_type << " ). realtime_now() returned." << std::endl;
       now = realtime_now();
    }
	
    if(debug > 0)
    {
        if(previous_now > now)
        {
            std::cout << "Warning in BetterTimestamp::now : The time seemed to go backward from " << previous_now << " to " << now << " !!!!!" << std::endl;
        }
        previous_now = now;
    }
    
    return now;
    
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
uint64_t BetterTimestamp::realtime_now()
{
	uint64_t delta_in_ms= realtime_timestamp() - realtime_offset;
    
	return delta_in_ms + realtime_zerotime;
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
uint64_t BetterTimestamp::processor_now()
{
	uint64_t delta = processor_timestamp();
	uint64_t delta_in_us = ((delta - processor_offset) * 10000000u)/processor_frequency;

	return delta_in_us + processor_zerotime;
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void BetterTimestamp::ResetZero()
{
	previous_now = 0u;
		
	//Initialisation des valeurs du timestamp processeur
	processor_offset = processor_timestamp();
	processor_zerotime = set_zerotime();
	update_frequency();
		
	//Initialisation des valeurs realtime.
	realtime_zerotime = processor_offset/10000u; //realtime_zerotime est en ms
	realtime_offset = realtime_timestamp();
			
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
uint64_t BetterTimestamp::TimeElapsedSinceZero()
{
	uint64_t delta = 0u;
	uint64_t delta_in_us = 0u;

	if(timestamp_type == 0)
	{
		delta = realtime_timestamp() - realtime_zerotime;
		return delta;
	}
	else if(timestamp_type == 1)
	{
		delta = processor_timestamp();
		delta_in_us = ((delta - processor_offset) * 10000000u)/processor_frequency;
       
		return delta_in_us;
	}
	else
	{
		std::cout << "Error in BetterTimestamp::TimeElapsedSinceZero : timestamp_type invalide ( " << timestamp_type << " ). timestamp_type = 0 used." << std::endl;
        
		delta = realtime_timestamp() - realtime_zerotime;
		return delta;
	}
	
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
std::string BetterTimestamp::TimestampDebugInfo()
{
	std::string info = "";
    std::stringstream ss;
    
    ss << "BetterTimestamp : PrintTimestampDebugInfo\n"
        << "\tdebug: " << short_to_string(debug)  << "\n"
        << "\ttimestamp_type: " << short_to_string(timestamp_type)  << "\n"
        << "\tprocessor_offset (en processors tic): " << uint64_t_to_string(processor_offset)  << "\n"
		<< "\tprocessor_zerotime (en 100ns depuis epoch) : " << uint64_t_to_string(processor_zerotime)  << "\n"
		<< "\tprocessor_frequency (Hz) : " << uint64_t_to_string(processor_frequency)  << "\n"
		<< "\trealtime_offset en ms: "        << uint64_t_to_string(realtime_offset)  << "\n"
		<< "\trealtime_zerotime en ms : "   << uint64_t_to_string(realtime_zerotime)  << "\n";

    info = ss.str();

	return info;
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
std::string BetterTimestamp::PrintTimestampDebugInfo()
{    
	if(debug > 0)
	{
		std::cout << "BetterTimestamp : PrintTimestampDebugInfo" << std::endl;
		std::cout << "\tdebug: " << debug << std::endl;
		std::cout << "\ttimestamp_type: " << timestamp_type << std::endl;
		std::cout << "\tprocessor_offset (en processors tic): " << processor_offset << std::endl;
		std::cout << "\tprocessor_zerotime (en 100ns depuis epoch) : " << processor_zerotime << std::endl;
		std::cout << "\tprocessor_frequency (Hz) : " << processor_frequency << std::endl;
		//std::cout << "\tprocessor_tic_100ns : " << processor_tic_100ns << std::endl;
		std::cout << "\trealtime_offset en ms: " << realtime_offset << std::endl;
		std::cout << "\trealtime_zerotime en ms : " << realtime_zerotime << std::endl;
	}

	return TimestampDebugInfo();
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
void BetterTimestamp::initialize_Timestamp(short Debug, short TheTimestamp_type)
{
	debug = Debug;
	timestamp_type =  TheTimestamp_type;

	if(debug > 0)
	{
		std::cout << "BetterTimestamp::initializeTimestamp : timestamp_type: " << timestamp_type << std::endl;
		std::cout << std::endl;
	}

    //Initializing frequecy and times
    ResetZero();
    
	if(debug > 0)
	{
		PrintTimestampDebugInfo();
	}

}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
uint64_t BetterTimestamp::set_zerotime()
{
	FILETIME ft;
    uint64_t tmpres =0u; 
	
	//Contains a 64-bit value representing the number of 100-nanosecond intervals since January 1, 1601 (UTC).
	GetSystemTimeAsFileTime(&ft); 
	
	//FILETIME vient en deux DWORD qu'on fusion ici.
	tmpres |= ft.dwHighDateTime;
    tmpres <<=32;
    tmpres |= ft.dwLowDateTime;
	
	// January 1st, 1970 - January 1st, 1601 UTC ~ 369 years
    // or 11644473600000000 us
    static const uint64_t delta_epoch = 116444736000000000; //en "100 nanosecondes"
    tmpres -= delta_epoch;
    
	return tmpres;

}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
uint64_t BetterTimestamp::update_frequency()
{
	LARGE_INTEGER li;
    if(!QueryPerformanceFrequency(&li)||!li.QuadPart)
    {
        std::cout << "Error in BetterTimestamp::updatefrequency : Windows Fonction \"QueryPerformanceFrequency\" failed.";
        std::terminate();
    }
	
	uint64_t result = static_cast<uint64_t>(li.QuadPart);
	
	
	if(result <= 0u)
	{
		std::cout << "Error in BetterTimestamp::updatefrequency : result <= 0" << std::endl;
		return 1u;
	}
	
	processor_frequency = result;
	processor_tic_100ns = 1000000.0 / (double)(processor_frequency);
	
    return result;
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
 uint64_t BetterTimestamp::processor_timestamp()
{
	LARGE_INTEGER li;
    QueryPerformanceCounter(&li);
	
    return static_cast<uint64_t>(li.QuadPart);
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
 uint64_t BetterTimestamp::realtime_timestamp()
{
	//ULARGE_INTEGER TickCount64;
    DWORD TickCount;
    TickCount = GetTickCount();
	uint64_t TickCount64 = uint64_t(TickCount);
    return TickCount64;
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
std::string BetterTimestamp::short_to_string(short number)
{
    std::ostringstream o;
    o << number;
    
    return o.str();
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
std::string BetterTimestamp::double_to_string(double number)
{
    std::ostringstream o;
    o << number;
    
    return o.str();
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
std::string BetterTimestamp::uint64_t_to_string(uint64_t number)
{
    std::ostringstream o;
    o << number;
    
    return o.str();
}
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////
